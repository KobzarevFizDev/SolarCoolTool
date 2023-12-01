import os
import sqlite3
from astropy.io import fits

class ImagesIndexer:
    def __init__(self, path):
        self.path = path

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
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS Images")
        cursor.execute("""
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
            cursor.execute(insertCommand, insertData)
        connection.commit()
        connection.close()