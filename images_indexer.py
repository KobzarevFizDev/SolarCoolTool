import os
import sqlite3
from typing import List

import numpy as np
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage
from astropy.io import fits

class ImagesIndexer:
    def __init__(self, path):
        self.path = path
        self.connection = None
        self.cursor = None

    def indexContents(self):
        files = self.__getAllFilesInTargetDir()
        channels = self.__getChannels(files)
        dates = self.__getDates(files)
        self.__createDatabase(files, channels, dates)

    def __getAllFilesInTargetDir(self):
        relativeFilePaths = list(filter((lambda f: "image" in f), os.listdir(self.path)))
        absoluteFilePaths = [self.path + "\\" + rf for rf in relativeFilePaths]
        return absoluteFilePaths

    def __getChannels(self, files):
        return [f.split('.')[3] for f in files]

    def __getDates(self, files):
        return [f.split('.')[2][0:10] for f in files]

    def __createDatabase(self, files, channels, dates):
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("DROP TABLE IF EXISTS Images")
        self.cursor.execute("""
        CREATE TABLE Images(
        Id INTEGER PRIMARY KEY,
        Path TEXT NOT NULL,
        Channel INTEGER NOT NULL,
        Date TEXT NOT NULL
        )
        """)
        for i, file in enumerate(files):
            insertCommand = "INSERT INTO Images (Id, Path, Channel, Date) VALUES (?,?,?,?)"
            insertData = (i, file, channels[i], dates[i])
            self.cursor.execute(insertCommand, insertData)
        self.connection.commit()
        self.connection.close()

    def isExistImagesInChannel(self, channel: int) -> bool:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        images = self.cursor.execute(command).fetchall()
        self.connection.close()
        return len(images) > 0

    def getPathsToImagesInChannel(self, channel: int) -> List[str]:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        pathsToImages = self.cursor.execute(command).fetchall()
        self.connection.close()
        return pathsToImages

    def getCountImagesInChannel(self, channel: int) -> int:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        command = "SELECT COUNT(*) FROM Images WHERE Channel = {0}".format(channel)
        countImages = int(self.cursor.execute(command).fetchall()[0][0])
        print(countImages)
        self.connection.close()
        return countImages

    def getImage(self, channel: int, indexOfImage: int) -> QImage:
        pathsToImagesInChannel = self.getPathsToImagesInChannel(channel)
        pathToImage = pathsToImagesInChannel[indexOfImage][0]
        hdul = fits.open(pathToImage)
        data = hdul[1].data
        hdul.close()
        img_w = data.shape[0]
        img_h = data.shape[1]
        cm = {94:  sunpy.visualization.colormaps.cm.sdoaia94,
              131: sunpy.visualization.colormaps.cm.sdoaia131,
              171: sunpy.visualization.colormaps.cm.sdoaia171,
              193: sunpy.visualization.colormaps.cm.sdoaia193,
              211: sunpy.visualization.colormaps.cm.sdoaia211,
              304: sunpy.visualization.colormaps.cm.sdoaia304,
              355: sunpy.visualization.colormaps.cm.sdoaia335}[channel]

        a = np.array(255 * cm(data), dtype=np.uint8)
        return QImage(a, img_h, img_w, 4 * img_w, QImage.Format_RGBA8888)

