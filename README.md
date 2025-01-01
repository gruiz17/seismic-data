# Seismic Data Coding Prompt

All of the requirements have been executed step-by-step. All of the instructions are in the included `main.ipynb` folder, so I'll just list out some details about the structure + technologies:

```
Directory structure:
└── seismic-data/
    ├── requirements_pip.txt
    ├── requirements.txt
    ├── main.ipynb
    ├── SEP/
    │   ├── SEP02.mseed
    │   ├── SEP01.mseed
    │   └── SEP03.mseed
    └── src/
        ├── viz.py
        ├── station_map.py
        ├── util.py
        └── create_db.py
```

## Top-level: Installation and running

* `requirements_pip.txt` is for the sake of being able to run this in Colab. Colab uses pip.
* `requirements.txt` contains the original conda environment I used to develop this on my machine.
* `main.ipynb` is, of course, the entry point + the notebook containins all of the execution.

## Technologies used

The high-level overview is that I'm very heavily relying on [ObsPy](https://docs.obspy.org/) to process all the `.mseed` files. ObsPy has been around for a decade, and it's a pretty well-established framework for seismology. I've used its built-in charts for the helicorder-style plots as well.

Of note, I am also using [Folium](https://python-visualization.github.io/folium/latest/) for interactive mapping. I found it to be the easiest mapping framework to work with.

Other than that, I'm using a pretty standard Python toolkit: `sqlite3` for DB operations, `requests` for the one network request to IRIS for station data, etc.

### Side Note: mseedindex approach

I do have some alternate code in here, following [this guidance](https://ds.iris.edu/ds/newsletter/vol24/no1/547/efficiently-reading-large-miniseed-data-sets-using-obspy/), depicting an approach that utilizes `mseedindex` and `obspy`'s built-in `TSIndex`. This would be helpful for a much larger and harder-to-organize dataset. I'm not sure if this can be run on Colab, but I wanted to demonstrate that this was possible.

## Inside `src/`

Exploring each of these:

* `util.py` -- Just one function for extracting metadata from a stream, and another for extracting waveform data if one is using the `mseedindex` approach.
* `create_db.py` -- functions to create the relevant DB + tables, as well as the indexer DB if one were to take the `mseedindex` approach
* `viz.py` -- functions to create the helicorder plots + the metadata boxes.
* `station_map.py` -- gets the relevant XML for the stations of interest from [this endpoint](https://service.iris.edu/fdsnws/station/1/query?net=CC&sta=SEP,HOA,SUG&level=station&format=xml&includecomments=true&nodata=404), and draws a map accordingly.
