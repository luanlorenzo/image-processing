import sys
import fileinput
import math

def main():
    file_data = PGM()
    #with fileinput.input(files=sys.argv[1], mode="r") as _filePGM:
    #    file_data.data = fileInputToList(_filePGM)
    #    fileinput.close()
    
    file_in = open('lena.pgm', 'r')
    data_pgm = fileInputToList(file_in)
    file_data.data = data_pgm
    file_in.close()

    file_data.Sobel()
    file_data.Roberts()
    file_data.Robinson()
    #file_data.SavePGM()

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

class PGM:
    def __init__(self):
        self.type = ''
        self.H = 0
        self.W = 0
        self._data = []
    
    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, data):
        self.type = data[0]
        self.W, self.H = data[1].split(" ")
        self.W = int(self.W)
        self.H = int(self.H)
        del data[0:3]
        self._data = data    

    def SavePGM(self):
        fileOut = open('output.pgm', 'w')
        fileOut.write(self.type + "\n")
        fileOut.write(str(self.W) + " " + str(self.H) + "\n")
        fileOut.write("255 \n")
        for line in self._data:   
            fileOut.write(str(line) + "\n")
        fileOut.close()

    def SaveCustomPGM(self, fileName, imgData):
        fileOut = open(str(fileName) + '.pgm', 'w')
        fileOut.write(self.type + "\n")
        fileOut.write(str(self.W) + " " + str(self.H) + "\n")
        fileOut.write("255 \n")
        for line in imgData:   
            fileOut.write(str(line) + "\n")
        fileOut.close()

    def Sobel(self):
        kernelDx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        kernelDy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

        p = [0]*9
        
        dx = [0]*(self.H * self.W)
        dy = [0]*(self.H * self.W)

        borderG = [0]*(self.H * self.W)
        borderGG = [0]*(self.H * self.W)

        gradientX = [0]*(self.H * self.W)
        gradientY = [0]*(self.H * self.W)
        
        min = float('inf')
        max = 0
        
        for i in range(1, int(self.H)-1):
            for j in range(1, int(self.W)-1):
                p[0] = self._data[(i-1)*self.W + (j-1)] * kernelDx[0][0]
                p[1] = self._data[(i-1)*self.W + j] * kernelDx[0][1]
                p[2] = self._data[(i-1)*self.W + (j+1)] * kernelDx[0][2]

                p[3] = self._data[(i)*self.W + (j-1)] * kernelDx[1][0]
                p[4] = self._data[((i)*self.W + j)] * kernelDx[1][1]
                p[5] = self._data[(i)*self.W + (j+1)] * kernelDx[1][2]

                p[6] = self._data[(i+1)*self.W + (j-1)] * kernelDx[2][0]
                p[7] = self._data[(i+1)*self.W + j] * kernelDx[2][1]
                p[8] = self._data[(i+1)*self.W + (j+1)] * kernelDx[2][2]
                
                dx[(i)*self.W + j] = sum(p)

                p[0] = self._data[(i-1)*self.W + (j-1)] * kernelDy[0][0]
                p[1] = self._data[(i-1)*self.W + j] * kernelDy[0][1]
                p[2] = self._data[(i-1)*self.W + (j+1)] * kernelDy[0][2]

                p[3] = self._data[(i)*self.W + (j-1)] * kernelDy[1][0]
                p[4] = self._data[(i)*self.W + j] * kernelDy[1][1]
                p[5] = self._data[(i)*self.W + (j+1)] * kernelDy[1][2]

                p[6] = self._data[(i+1)*self.W + (j-1)] * kernelDy[2][0]
                p[7] = self._data[(i+1)*self.W + j] * kernelDy[2][1]
                p[8] = self._data[(i+1)*self.W + (j+1)] * kernelDy[2][2]
                
                dy[(i)*self.W + j] = sum(p)                 

                min = dx[i*self.W + j] if (dx[i*self.W + j] < min) else min
                min = dy[i*self.W + j] if (dy[i*self.W + j] < min) else min
                max = dx[i*self.W + j] if (dx[i*self.W + j] > max) else max
                max = dy[i*self.W + j] if (dy[i*self.W + j] > max) else max

                border_01 = (abs(dx[(i)*self.W + j])+abs(dy[(i)*self.W + j]))//2
                border_02 = math.sqrt(dx[(i)*self.W + j]*dx[(i)*self.W + j] + dy[(i)*self.W + j]*dy[(i)*self.W + j])

                # Resulting images
                borderG[(i)*self.W + j] = int(border_01)
                borderGG[(i)*self.W + j] = int(border_02)

        self.SaveCustomPGM('borderG', borderG)   
        self.SaveCustomPGM('sobel', borderGG)   

        for i in range(1, int(self.H)-1):
            for j in range(1, int(self.W)-1):
                gradientX[i*self.W + j] = int((dx[i*self.W + j]-min) / (max-min) * 255)
                gradientY[i*self.W + j] = int((dy[i*self.W + j]-min) / (max-min) * 255)
        
        self.SaveCustomPGM('gradientX', gradientX)   
        self.SaveCustomPGM('gradientY', gradientY)

    def Roberts(self):
        kernelDx = [[0, 1], [-1, 0]]
        kernelDy = [[1, 0], [0, -1]]

        p = [0]*4
        
        dx = 0
        dy = 0
    
        borderG = [0]*(self.H * self.W)
        
        for i in range(1, int(self.H)-1):
            for j in range(1, int(self.W)-1):
                p[0] = self._data[(i-1)*self.W + (j-1)] * kernelDx[0][0]
                p[1] = self._data[(i-1)*self.W + j] * kernelDx[0][1]
                p[2] = self._data[(i)*self.W + (j-1)] * kernelDx[1][0]
                p[3] = self._data[(i)*self.W + (j)] * kernelDx[1][1]
                
                dx = sum(p)

                p[0] = self._data[(i-1)*self.W + (j-1)] * kernelDy[0][0]
                p[1] = self._data[(i-1)*self.W + j] * kernelDy[0][1]
                p[2] = self._data[(i)*self.W + (j-1)] * kernelDy[1][0]
                p[3] = self._data[(i)*self.W + (j)] * kernelDy[1][1]
                
                dy = sum(p)                 

                border = math.sqrt(dx*dx + dy*dy)

                # Resulting image
                borderG[(i)*self.W + j] = int(border)

        self.SaveCustomPGM('roberts', borderG)   

    def Robinson(self):
        kernelD1 = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        kernelD2 = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
        kernelD3 = [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]
        kernelD4 = [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]]
        kernelD5 = [[1, 0, -1], [2, 0, -2], [1, 0, -1]]
        kernelD6 = [[1, 2, 1], [0, 0, 0], [-1, -2, -1]]
        kernelD7 = [[2, 1, 0], [1, 0, -1], [0, -1, -2]]
        kernelD8 = [[0, -1, -2], [1, 0, -1], [2, 1, 0]]

        d = [0]*8

        p = [0]*9

        borderG = [0]*(self.H * self.W)

        def convolution(data, kernel, i, j, W):
            p[0] = data[(i-1)*W + (j-1)] * kernel[0][0]
            p[1] = data[(i-1)*W + j] * kernel[0][1]
            p[2] = data[(i-1)*W + (j+1)] * kernel[0][2]
            p[3] = data[(i)*W + (j-1)] * kernel[1][0]
            p[4] = data[(i)*W + j] * kernel[1][1]
            p[5] = data[(i)*W + (j+1)] * kernel[1][2]
            p[6] = data[(i+1)*W + (j-1)] * kernel[2][0]
            p[7] = data[(i+1)*W + j] * kernel[2][1]
            p[8] = data[(i+1)*W + (j+1)] * kernel[2][2]

            return sum(p)

        for i in range(1, int(self.H)-1):
            for j in range(1, int(self.W)-1):
                d[0] = convolution(self._data, kernelD1, i, j, self.W)
                d[1] = convolution(self._data, kernelD2, i, j, self.W)
                d[2] = convolution(self._data, kernelD3, i, j, self.W)
                d[3] = convolution(self._data, kernelD4, i, j, self.W)
                d[4] = convolution(self._data, kernelD5, i, j, self.W)
                d[5] = convolution(self._data, kernelD6, i, j, self.W)
                d[6] = convolution(self._data, kernelD7, i, j, self.W)
                d[7] = convolution(self._data, kernelD8, i, j, self.W)

                border = d[0]*d[0] + d[1]*d[1] + d[2]*d[2] + d[3]*d[3]
                border = border + d[4]*d[4] + d[5]*d[5] + d[6]*d[6] + d[7]*d[7]
                border = math.sqrt(border)
                
                # Resulting image
                borderG[(i)*self.W + j] = int(border)

        self.SaveCustomPGM('robinson', borderG)

if __name__ == "__main__":
    main()
