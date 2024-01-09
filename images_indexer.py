import os
import sqlite3
from typing import List

import numpy as np
import sunpy.visualization.colormaps.cm
from PyQt5.QtGui import QImage
from astropy.io import fits

class SolarImage:
    def __init__(self, id: int, path: str, channel: int, date: str):
        self.__id = id
        self.__path = path
        self.__channel = channel
        self.__date = date

        hdul = fits.open(self.__path)
        data = hdul[1].data
        hdul.close()
        img_w = data.shape[0]
        img_h = data.shape[1]
        cm = {94: sunpy.visualization.colormaps.cm.sdoaia94,
              131: sunpy.visualization.colormaps.cm.sdoaia131,
              171: sunpy.visualization.colormaps.cm.sdoaia171,
              193: sunpy.visualization.colormaps.cm.sdoaia193,
              211: sunpy.visualization.colormaps.cm.sdoaia211,
              304: sunpy.visualization.colormaps.cm.sdoaia304,
              355: sunpy.visualization.colormaps.cm.sdoaia335}[channel]

        a = np.array(255 * cm(data), dtype=np.uint8)
        self.__image = QImage(a, img_h, img_w, 4 * img_w, QImage.Format_RGBA8888)
        hdul.close()

    @property
    def id(self):
        return self.__id

    @property
    def path(self):
        return self.__path

    @property
    def channel(self):
        return self.__channel

    @property
    def date(self):
        return self.__date

    @property
    def image(self):
        return self.__image

class ImagesIndexer:
    def __init__(self, path):
        self.__pathToCatalog = path
        self.__connection = None
        self.__cursor = None
        self.__images: List[SolarImage] = list()

    def indexContents(self):
        files = self.__getAllFilesInTargetDir()
        channels = self.__getChannels(files)
        dates = self.__getDates(files)
        self.__createDatabase(files, channels, dates)

    # TODO: Плохое название. Эта функция помещает все данные из базы данных в массив
    def cacheChannel(self, channel: int):
        paths = self.getPathsToImagesInChannel(channel)
        ids = self.getIdOfImagesInChannel(channel)
        dates = self.getDatesOfImagesInChannel(channel)

        self.__images.clear()
        for i, path in enumerate(paths):
            id = ids[i]
            date = dates[i]
            solarImage = SolarImage(id, path, channel, date)
            self.__images.append(solarImage)
            print("Cache channel {0}. Progress = {1}/{2}".format(channel, i, len(paths)))

    def __getChannelsStorredInDatabase(self) -> List[int]:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT DISTINCT Channel FROM Images"
        channels = self.__cursor.execute(command).fetchall()
        self.__connection.close()
        return channels

    # TODO: Устаревшее

    def __getAllFilesInTargetDir(self):
        relativeFilePaths = list(filter((lambda f: "image" in f), os.listdir(self.__pathToCatalog)))
        absoluteFilePaths = [self.__pathToCatalog + "\\" + rf for rf in relativeFilePaths]
        return absoluteFilePaths

    def __getChannels(self, files):
        return [f.split('.')[3] for f in files]

    def __getDates(self, files):
        return [f.split('.')[2][0:10] for f in files]

    #TODO: Название нехорошее. Эта функция индексирует каталог и вносит все в БД
    def __createDatabase(self, files, channels, dates):
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute("DROP TABLE IF EXISTS Images")
        self.__cursor.execute("""
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
            self.__cursor.execute(insertCommand, insertData)
        self.__connection.commit()
        self.__connection.close()

    def isExistImagesInChannel(self, channel: int) -> bool:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        images = self.__cursor.execute(command).fetchall()
        self.__connection.close()
        return len(images) > 0

    def getPathsToImagesInChannel(self, channel: int) -> List[str]:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        pathsToImages = self.__cursor.execute(command).fetchall()
        pathsToImages = [pathsToImages[i][0] for i in range(len(pathsToImages))]
        self.__connection.close()
        return pathsToImages

    def getIdOfImagesInChannel(self, channel: int) -> List[int]:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT Id FROM Images WHERE Channel = {0}".format(channel)
        ids = self.__cursor.execute(command).fetchall()
        ids = [ids[i][0] for i in range(len(ids))]
        self.__connection.close()
        return ids

    def getDatesOfImagesInChannel(self, channel: int) -> List[str]:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT Date FROM Images WHERE Channel = {0}".format(channel)
        dates = self.__cursor.execute(command).fetchall()
        dates = [dates[i][0] for i in range(len(dates))]
        self.__connection.close()
        return dates

    def getCountImagesInChannel(self, channel: int) -> int:
        self.__connection = sqlite3.connect('my_database.db')
        self.__cursor = self.__connection.cursor()
        command = "SELECT COUNT(*) FROM Images WHERE Channel = {0}".format(channel)
        countImages = int(self.__cursor.execute(command).fetchall()[0][0])
        self.__connection.close()
        return countImages

    def getImageInChannelByIndex(self, indexInChannel: int) -> QImage:
        return self.__images[indexInChannel].image
