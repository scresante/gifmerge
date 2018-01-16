# the GifCombiner class is a utility library for combining gif files in order

It will naively take a list of files, and extract multiimage frames from them
Then it will check there are no duplicates going backwards and if so discard

The use case is for combining multiple data pulls over time from NOAA's ice coverage data into one single animated gif

# the NOAADownloader class is a utility for doing the scraping and defaults to thickness / erie

This is a WIP and these details will change

**Example usage as a script**

gifmerge.py [--lake lake] [--datatype dtype]
where lake is one of erie, superior, huron, michigan or ontario
and datatype is thickness, or concentration

Run that every 40 hours or so for a while, and you'll have a bunch of gifs.
Run GifCombiner on them like so to get one nice big gif

*GifCombiner(*mylistofgifs)*


[required reading](https://en.wikisource.org/wiki/The_Rime_of_the_Ancyent_Marinere_(1798))
