from obspy import read
from obspy.clients.filesystem.tsindex import Client


def get_all_metadata(mseed_file):
    """gets the metadata from an mseed file

    Args:
        mseed_file (string): path to the mseed file, either of "SEP01.mseed", "SEP02.mseed", "SEP03.mseed"

    Returns:
        tuple: network, station, location, channel, starttime, endtime
    """
    st = read(mseed_file)
    network = st[0].stats.network
    station = st[0].stats.station
    location = st[0].stats.location
    channel = st[0].stats.channel
    starttime = st[0].stats.starttime
    endtime = st[len(st) - 1].stats.endtime
    return network, station, location, channel, starttime, endtime


def get_waveforms_for_event(network, station, location, channel, starttime, endtime):
    """gets the waveforms for a given event, based on a metadata tuple
    Note: This actually requires the database to have been created, based on the
    mseedindex schema.

    Args:
        network (string): network code
        station (string): station code
        location (string): location code
        channel (string): channel code
        starttime (UTCDateTime): start time of the event
        endtime (UTCDateTime): end time of the event

    Returns:
        Stream: waveforms for the event, based on a TSIndex query
    """
    client = Client('timeseries.sqlite')
    waveforms = client.get_waveforms(
        network, station, location, channel, starttime, endtime)
    return waveforms
