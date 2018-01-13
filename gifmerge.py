#!/usr/bin/python3

from hashlib import md5
import requests
from time import gmtime, strftime
from collections import OrderedDict
from os.path import getmtime,isdir
from os import mkdir

import imageio

import logging

IMAGEDATA = './gifdata/'
if not isdir(IMAGEDATA): mkdir(IMAGEDATA)

class ImageDownloader:
    """ This downloads and stores a set of images from NOAA as gifs
    Basically a front-end for imageio arrays """
    dtype = ''
    images = []

    def __init__(self, lake='erie', datatype='thickness'):
        """ datatype is either thickness concentration or both """
        self.lake = lake
        allowed_types = {'thickness':'thk', 'concentration': 'con'}
        self.dtype = allowed_types[datatype]

    def downloadImages(self, num_to_fetch:'0<int<50'=49):
        def makeUrl(lake, dtype, num):
            base_url = 'https://www.glerl.noaa.gov/res/glcfs/ncast' \
                f'/{lake[0]}ice{dtype}-{num:02}.gif'
            return base_url

        # return as many images as user asks for
        for n in range(0,num_to_fetch):
            print('.', end='', flush=True)
            URL = makeUrl(self.lake, self.dtype, n)
            cur_image = requests.get(URL)
            self.images.append(imageio.imread(cur_image.content))
            # print(f'got {len(cur_image.content)} bytes from {URL}')

        self.images.reverse() #put images in chronological order

    def writeImages(self):
        fname = f"ice-{self.lake}-{self.dtype}-{strftime('%Y-%m-%d %H:%M:%S', gmtime())}.gif"
        fname = IMAGEDATA + fname
        imageio.mimwrite(fname, self.images)
        print(f'{fname} written ({len(self.images)} images)')

    def exec(self):
        self.downloadImages()
        self.writeImages()


class GifCombiner:
    """ This gizmo takes a list of gifs, and then deduplicates them,
    in order, effectively concatenating them"""
    frames = OrderedDict()
    def __init__(self, *files, grep:'optional filter'=''):
        self.pcount = 0
        if len(files) == 0:
            raise ValueError('no files given')
        grepF = lambda x: grep in x
        self.wtf = files
        self.files = sorted(list(filter(grepF,*files)), key=getmtime)
        # print(f'self.files is now: {self.files}')
        for f in self.files:
            self.collectImageData(f)

    def writeFrames(self):
        fname = f"combineout-{strftime('%Y-%m-%d %H:%M:%S', gmtime())}.gif"
        fname = IMAGEDATA + fname
        imageio.mimwrite(fname, self.frames.values())
        print(f"{fname} written")

    def collectImageData(self, file):
        " collect a set of images from a file, adding them to frames only if new"
        image_set = []
        with imageio.get_reader(file) as reader:
            for image in reader:
                self.pcount += 1
                # this is important - add image's md5sum to object
                image.md5sum = md5(image.tostring()).hexdigest()
                self.updateFrames(image)
            print('.', end='', flush=True)
        logging.info(f'collectImageData has read {len(image_set)} images from {len(self.files)} files')
        return len(self.frames)

    def updateFrames(self, image):
        " updates self.frames with new image checking if existing "
        # self.frames.update( { k:v for k,v in image.items() if k not in self.frames })
        if image.md5sum not in self.frames:
            self.frames.update( {image.md5sum:image})

    def __repr__(self):
        return f'I have these files: {self.files}'
