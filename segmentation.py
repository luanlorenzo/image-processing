 # Image segmentation algorithm: Watershed
 #  python3 segmentation.py image.ppm

import sys
import fileinput
import numpy as np
from random import randrange

#----------------------------------------------------
def main():
    segmentator = Flood()
    threshold = 5
    with fileinput.input(files=sys.argv[1], mode="r") as _filePGM:
        segmentator.data = fileInputToList(_filePGM)
        fileinput.close()
    
    k = 0
    for i in range(0, segmentator.H):
        for j in range(0, segmentator.W):
            if(segmentator.isAvailable(i, j)):
                k += 1
                area = segmentator.ExtractPartition(j, i, threshold, k)
                #print("Regions: " + str(segmentator.numberOfRegions) + "has area " + str(area))    

    result = segmentator.GetSegmentedImage()
    segmentator.SaveCustomPPM("Segmented", result)
#----------------------------------------------------
def fileInputToList(_fileInput):
    fileList = []
    count = 0
    for line in _fileInput:
        if(count < 2):
            fileList.append(line.replace('\n', ''))
            count = count + 1
        else: 
            fileList.append(int(line.replace('\n', '')))
    return fileList

#----------------------------------------------------
class Stack:
    def __init__(self):
        self.items = []
    
    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def at(self, index):
        return self.items[index]

    def size(self):
        return len(self.items)
        

#----------------------------------------------------
class Color:
    def __init__(self, red, green, blue):
        self.r = red
        self.g = green
        self.b = blue

#----------------------------------------------------
class Point:
    def __init__(self, m_x, m_y):
        self.x = m_x
        self.y = m_y

#----------------------------------------------------
class Flood:
    def __init__(self):
        self.type = None
        self.H = None
        self.W = None
        self._data = None
        self.indexMap = None
        self.numberOfRegions = 0
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self.type = data[0]
        self.W, self.H = data[1].split(" ")
        self.W = int(self.W)
        self.H = int(self.H)
        self.indexMap = [0]*(self.H * self.W)
        del data[0:3]
        self._data = data

    def SavePPM(self):
        fileOut = open('imgOutPGM.ppm', 'w')
        fileOut.write(self.type)
        fileOut.write(str(self.W) + " " + str(self.H) + "\n")
        fileOut.write("255 \n")
        for line in self._data:   
            fileOut.write(str(line) + "\n")
        fileOut.close()
    
    def SaveCustomPPM(self, fileName, imgData):
        fileOut = open(str(fileName) + '.ppm', 'w')
        fileOut.write(self.type + "\n")
        fileOut.write(str(self.W) + " " + str(self.H) + "\n")
        fileOut.write("255 \n")
        for line in imgData:   
            fileOut.write(str(line) + "\n")
        fileOut.close()
    
    def isAvailable(self, i, j):
        if(self.indexMap[i*self.W + j] > 0):
            return False
        return True
    
    def ExtractPartition(self, x, y, threshold, index):
        stack = Stack()
        stack.push(Point(x, y))
        
        area = 1
        indexToMark = index
        self.indexMap[y*self.W + x] = indexToMark
        self.numberOfRegions = self.numberOfRegions + 1

        while(stack.size() > 0):
            pos = self.validatePosition(x, y, threshold)
            
            if (pos == 1):
                self.indexMap[(y-1)*self.W + x] = indexToMark
                area += 1
                y -= 1
                stack.push(Point(x, y))
            
            if (pos == 2):
                self.indexMap[y*self.W + x-1] = indexToMark
                area += 1
                x -= 1
                stack.push(Point(x, y))

            if (pos == 3):
                self.indexMap[(y+1)*self.W + x] = indexToMark
                area += 1
                y += 1
                stack.push(Point(x, y))

            if (pos == 4):
                self.indexMap[y*self.W + x+1] = indexToMark
                area += 1
                x += 1
                stack.push(Point(x, y))
            
            if (pos == 0):
                x = stack.peek().x
                y = stack.peek().y 
                stack.pop()
        return area

    def validatePosition(self, x, y, threshold):
        # up up up up
        if(y > 0):
            if(self.indexMap[(y-1)*self.W + x] == 0):
                current = y*self.W*3 + x*3
                query = (y-1)*self.W*3 + x*3
                
                r1 = self._data[current]
                r2 = self._data[query]
                g1 = self._data[current+1]
                g2 = self._data[query+1]
                b1 = self._data[current+2]
                b2 = self._data[query+2]
                DE = (r1-r2)*(r1-r2)+(b1-b2)*(b1-b2)+(g1-g2)*(g1-g2)
                DE = np.sqrt(DE)
                if(DE < threshold):
                    return 1
        
        # left left left
        if(x > 0):
            if(self.indexMap[y*self.W+(x-1)] == 0):
                current = y*self.W*3+x*3
                query   = y*self.W*3+(x-1)*3
                
                r1 = self._data[current]
                r2 = self._data[query]
                g1 = self._data[current+1]
                g2 = self._data[query+1]
                b1 = self._data[current+2]
                b2 = self._data[query+2]
                DE = (r1-r2)*(r1-r2)+(b1-b2)*(b1-b2)+(g1-g2)*(g1-g2)
                DE = np.sqrt(DE)
                if(DE < threshold):
                    return 2

        # down down down
        if(y < self.H-1):
            if(self.indexMap[(y+1)*self.W+x] == 0):
                current = y*self.W*3 + x*3
                query   = (y+1)*self.W*3 + x*3
                
                r1 = self._data[current]
                r2 = self._data[query]
                g1 = self._data[current+1]
                g2 = self._data[query+1]
                b1 = self._data[current+2]
                b2 = self._data[query+2]
                DE = (r1-r2)*(r1-r2)+(b1-b2)*(b1-b2)+(g1-g2)*(g1-g2)
                DE = np.sqrt(DE)
                if(DE < threshold):
                    return 3
        
        # right right right
        if(x < self.W-1):
            if(self.indexMap[y*self.W+x+1] == 0):
                current = y*self.W*3 + x*3
                query   = y*self.W*3 + (x+1)*3
                
                r1 = self._data[current]
                r2 = self._data[query]
                g1 = self._data[current+1]
                g2 = self._data[query+1]
                b1 = self._data[current+2]
                b2 = self._data[query+2]
                DE = (r1-r2)*(r1-r2)+(b1-b2)*(b1-b2)+(g1-g2)*(g1-g2)
                DE = np.sqrt(DE)
                if(DE < threshold):
                    return 4
        return 0 

    def GetSegmentedImage(self):
        resultData = [0]*(self.H*self.W*3)
        rndColors = Stack()
        
        for i in range(0, self.numberOfRegions):
            rndColors.push(Color(randrange(0, 255), randrange(0, 255), randrange(0, 255)))
        
        for i in range(0, self.H):
            for j in range(0, self.W):
                if(self.indexMap[i*self.W + j] > 0):
                    resultData[i*self.W*3+j*3]   = rndColors.at(self.indexMap[i*self.W+j]-1).r
                    resultData[i*self.W*3+j*3+1] = rndColors.at(self.indexMap[i*self.W+j]-1).g
                    resultData[i*self.W*3+j*3+2] = rndColors.at(self.indexMap[i*self.W+j]-1).b
                else:
                    resultData[i*self.W*3+j*3]   = 255
                    resultData[i*self.W*3+j*3+1] = 0
                    resultData[i*self.W*3+j*3+2] = 0
        return resultData

#================================================
if __name__ == "__main__":
    main()