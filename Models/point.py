from PyQt5.QtCore import Qt

class Point:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r
        self.w = 1
        self.color = Qt.red


    def highlightThisPointAsSelected(self):
        self.color = Qt.blue


    def unhightlightThisPointAsSelected(self):
        self.color = Qt.red