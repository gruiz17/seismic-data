import matplotlib.pyplot as plt


def create_metadata_text(network, station, location, channel, starttime, endtime):
    """Generates metadata text for the plot

    Args:
        network (string): network code
        station (string): station code
        location (string): location code
        channel (string): channel code
        starttime (UTCDateTime): start time of the event
        endtime (UTCDateTime): end time of the event

    Returns:
        string: metadata text
    """
    metadata_text = f'Network: {network}\nStation: {station}\nLocation: {location}\nChannel: {channel}\nStarttime: {starttime.strftime('%Y-%m-%d %H:%M:%S')}\nEndtime: {endtime.strftime('%Y-%m-%d %H:%M:%S')}'
    return metadata_text


def plot_waveforms(waveform, metadata):
    """gets the waveforms for a given event, based on a metadata tuple
    Note: This actually requires the database to have been created, based on the
    mseedindex schema.

    Args:
        waveform (Stream): waveforms for the event
        metadata (tuple): network, station, location, channel, starttime, endtime

    Returns:
        plot: 24-hour seismic recording plot
    """
    fig = plt.figure(figsize=(12, 10))
    metadata_text = create_metadata_text(*metadata)

    fig.suptitle(f"24-Hour Seismic Recording - Station CC.SEP.EHZ\n{metadata[4].date}",
                 fontsize=14,
                 y=0.98)

    plt.figtext(0.1, 0.92, metadata_text,
                fontsize=10,
                family='monospace',
                bbox=dict(facecolor='white',
                          edgecolor='black',
                          boxstyle='round,pad=1'))

    return waveform.plot(
        type='dayplot',
        interval=60,  # One line per hour
        size=(1200, 800),
        dpi=150,
        bgcolor='white',
        grid_color='#e5e7eb',
        grid_linewidth=0.3,
        vertical_scaling_range=None,
        x_labels_size=10,
        y_labels_size=10,
        title_size=12,
        title=f"24-Hour Seismic Recording - Station CC.SEP.EHZ\n{
            metadata[4].date}",
        subplots_adjust_left=0.12,
        subplots_adjust_right=0.95,
        subplots_adjust_top=.9,  # Adjusted to make room for metadata
        subplots_adjust_bottom=0.1,
        show_y_UTC_label=True,
        one_tick_per_line=True,
        fig=fig
    )
