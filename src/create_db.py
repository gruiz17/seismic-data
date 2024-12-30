from obspy.clients.filesystem.tsindex import Indexer
import os


def create_indexer_db():
    """Creates indexer database, based on the mseedindex schema

    Returns: None
    """
    if not os.path.exists('timeseries.sqlite'):
        indexer = Indexer('SEP')
        indexer.run()
    else:
        print('Database already exists')
