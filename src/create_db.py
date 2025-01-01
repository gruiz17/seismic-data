from obspy.clients.filesystem.tsindex import Indexer
import os
from obspy import read
from obspy.core import UTCDateTime
import sqlite3
import os
from pathlib import Path


def create_database():
    """Create the SQLite database and necessary tables
    
    Returns: None
    """
    conn = sqlite3.connect('seismic_data.sqlite')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS traces (
            id INTEGER PRIMARY KEY,
            network TEXT,
            station TEXT,
            location TEXT,
            channel TEXT,
            starttime TEXT,
            endtime TEXT,
            sampling_rate REAL,
            npts INTEGER,
            filename TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS waveforms (
            trace_id INTEGER,
            data BLOB,
            FOREIGN KEY(trace_id) REFERENCES traces(id)
        )
    ''')

    conn.commit()
    return conn


def process_mseed_files():
    """Process all .mseed files in the SEP directory

    Returns: None
    """
    conn = create_database()
    c = conn.cursor()
    directory = "SEP"
    mseed_files = list(Path(directory).glob('**/*.mseed'))

    for file_path in mseed_files:
        try:
            st = read(str(file_path))
            for tr in st:
                c.execute('''
                    INSERT INTO traces (
                        network, station, location, channel,
                        starttime, endtime, sampling_rate, npts, filename
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    tr.stats.network,
                    tr.stats.station,
                    tr.stats.location,
                    tr.stats.channel,
                    str(tr.stats.starttime),
                    str(tr.stats.endtime),
                    tr.stats.sampling_rate,
                    tr.stats.npts,
                    str(file_path)
                ))

                trace_id = c.lastrowid

                c.execute('''
                    INSERT INTO waveforms (trace_id, data)
                    VALUES (?, ?)
                ''', (trace_id, tr.data.tobytes()))

            conn.commit()
            print(f"Processed {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            continue

    conn.close()


def create_indexer_db():
    """Creates indexer database, based on the mseedindex schema

    Returns: None
    """
    if not os.path.exists('timeseries.sqlite'):
        indexer = Indexer('SEP')
        indexer.run()
    else:
        print('Database already exists')

