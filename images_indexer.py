import os
import sqlite3
from typing import List

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

    def isExistImagesByChannel(self, channel: int) -> bool:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        files = self.cursor.execute(command).fetchall()
        self.connection.close()
        return len(files) > 0

    def getFilesByChannel(self, channel: int) -> List[str]:
        self.connection = sqlite3.connect('my_database.db')
        self.cursor = self.connection.cursor()
        command = "SELECT Path FROM Images WHERE Channel = {0}".format(channel)
        files = self.cursor.execute(command).fetchall()
        self.connection.close()
        return files