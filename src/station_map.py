from obspy.core.inventory import read_inventory
import folium


def create_map():
    inv = read_inventory('stationxml.xml')

    stations = inv[0].stations
    center_lat = sum(sta.latitude for sta in stations) / len(stations)
    center_lon = sum(sta.longitude for sta in stations) / len(stations)

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=13
    )

    for sta in stations:
        folium.Marker(
            location=[sta.latitude, sta.longitude],
            popup=f"""
            <b>{sta.code}</b><br><br>
            Name: {sta.site.name}<br><br>
            Latitude: {sta.latitude}°<br>
            Longitude: {sta.longitude}°<br><br>
            Elevation: {sta.elevation}m<br><br>
            Description: {sta.site.description}
            """,
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

    return m
