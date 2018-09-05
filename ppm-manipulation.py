import sys
import fileinput
import numpy as np

def main():
    file_data = PPM()
    with fileinput.input(files=sys.argv[1], mode="r") as _filePGM:
        file_data.data = fileInputToList(_filePGM)
        fileinput.close()
    file_data.manhattanDistance()
    #file_data.euclideanDistance()
    #file_data.KNN()
    #file_data.mahalanobisDistance()
    file_data.SavePPM()

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

class PPM:
    def __init__(self):
        self.type = None
        self.H = None
        self.W = None
        self._data = None
    
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

    def SavePPM(self):
        fileOut = open('imgOutPGM.ppm', 'w')
        fileOut.write(self.type)
        fileOut.write(str(self.W) + " " + str(self.H) + "\n")
        fileOut.write("255 \n")
        for line in self._data:   
            fileOut.write(str(line) + "\n")
        fileOut.close()
    
    def manhattanDistance(self):
        (r, g, b) = (0, 0, 0)
        
        """# values : apple
        rr = 210
        rg = 50
        rb = 15
        threshold = 110"""

        # values : star
        rr = 255
        rg = 200
        rb = 40
        threshold = 110

        """# values : flower
        rr = 210
        rg = 128
        rb = 128
        threshold = 110"""

        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]
                
                if(r > rr-threshold and r < rr+threshold):
                    if(g > rg-threshold and g < rg+threshold):
                        if(b > rb-threshold and b < rb+threshold):
                            self._data[i*self.W*3 + j*3] = 0
                            self._data[i*self.W*3 + j*3 + 1] = 0
                            self._data[i*self.W*3 + j*3 + 2] = 0

    def euclideanDistance(self):
        (r, g, b) = (0, 0, 0)
        
        # values : apple
        rr = 210
        rg = 150
        rb = 20
        threshold = 210

        """# values : star
        rr = 255
        rg = 70
        rb = 20
        threshold = 160"""

        """# values : flower
        rr = 200
        rg = 70
        rb = 40
        threshold = 115"""
        
        euclDistance = 0

        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]
                
                euclDistance = (r-rr)**2 + (g-rg)**2 + (b-rb)**2
                if(euclDistance**(1/2) < threshold):
                    self._data[i*self.W*3 + j*3] = 0
                    self._data[i*self.W*3 + j*3 + 1] = 0
                    self._data[i*self.W*3 + j*3 + 2] = 0

    def KNN(self):
        # values : apple
        r1, g1, b1 = (75, 10, 0)
        r2, g2, b2 = (215, 60, 55)
        r3, g3, b3 = (255, 220, 219)
        r4, g4, b4 = (230, 150, 80)
        threshold = 105

        """# values : star
        r1, g1, b1 = (115, 15, 25)
        r2, g2, b2 = (255, 215, 160)
        r3, g3, b3 = (180, 90, 50)
        r4, g4, b4 = (230, 150, 80)
        threshold = 65"""

        """# values : flower
        r1, g1, b1 = (90, 10, 10)
        r2, g2, b2 = (170, 40, 10)
        r3, g3, b3 = (240, 90, 70)
        r4, g4, b4 = (200, 170, 15)
        threshold = 57"""
        
        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]

                d1 = ((r-r1)**2 + (g-g1)**2 + (b-b1)**2)**(1/2)
                d2 = ((r-r2)**2 + (g-g2)**2 + (b-b2)**2)**(1/2)
                d3 = ((r-r3)**2 + (g-g3)**2 + (b-b3)**2)**(1/2)
                d4 = ((r-r4)**2 + (g-g4)**2 + (b-b4)**2)**(1/2)

                if(d1 < threshold or d2 < threshold or d3 < threshold or d4 <threshold):
                    self._data[i*self.W*3 + j*3] = 0
                    self._data[i*self.W*3 + j*3 + 1] = 0
                    self._data[i*self.W*3 + j*3 + 2] = 0

    def mahalanobisDistance(self):
        var_rr = 0
        var_gg = 0
        var_bb = 0
        cov_rg = 0
        cov_rb = 0
        cov_gb = 0

        n_inst = 0

        #threshold = 1.6     # star flower
        threshold = 2       # apple

        mean_v = self.getMeanValues()
        avr_r, avr_g, avr_b = self.average(mean_v)

        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]

                var_rr = var_rr + (r - avr_r)**2
                var_gg = var_gg + (g - avr_g)**2
                var_bb = var_bb + (b - avr_b)**2
                cov_rg = cov_rg + (r - avr_r)*(g - avr_g)
                cov_rb = cov_rb + (r - avr_r)*(b - avr_b)
                cov_gb = cov_gb + (g - avr_g)*(b - avr_b)
                
                n_inst += 1
        
        var_rr = var_rr / n_inst
        var_gg = var_gg / n_inst
        var_bb = var_bb / n_inst
        cov_rg = cov_rg / n_inst
        cov_rb = cov_rb / n_inst
        cov_gb = cov_gb / n_inst

        cov_matrix = [[var_rr, cov_rg, cov_rb],
                      [cov_rg, var_gg, cov_gb],
                      [cov_rb, cov_gb, var_bb]]

        cov_matrix_inv = np.linalg.inv(cov_matrix)

        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]

                dif_transp = [[r - avr_r, g - avr_g, b - avr_b]]
                dif = [[r - avr_r], [g - avr_g], [b - avr_b]]
                
                mahal_dist = np.matmul(dif_transp, cov_matrix_inv)
                mahal_dist = np.matmul(mahal_dist, dif)
                mahal_dist = mahal_dist**(1/2)

                if(mahal_dist > threshold):
                    self._data[i*self.W*3 + j*3] = 0
                    self._data[i*self.W*3 + j*3 + 1] = 0
                    self._data[i*self.W*3 + j*3 + 2] = 0

    def average(self, V):
        avr_r = 0
        avr_g = 0
        avr_b = 0
        n_inst = 0

        for i in range(0, len(V) - 2):
            r = V[i]
            g = V[i+1]
            b = V[i+2]
                
            avr_r = avr_r + r
            avr_g = avr_g + g
            avr_b = avr_b + b

            n_inst += 1
            
        avr_r = avr_r / n_inst
        avr_g = avr_g / n_inst
        avr_b = avr_b / n_inst

        return avr_r, avr_g, avr_b

    def getMeanValues(self):
        # values : apple
        r1, g1, b1 = (75, 10, 0)
        r2, g2, b2 = (215, 60, 55)
        r3, g3, b3 = (255, 220, 219)
        r4, g4, b4 = (230, 150, 80)
        threshold = 105

        """# values : star
        r1, g1, b1 = (115, 15, 25)
        r2, g2, b2 = (255, 215, 160)
        r3, g3, b3 = (180, 90, 50)
        r4, g4, b4 = (230, 150, 80)
        threshold = 65"""

        """# values : flower
        r1, g1, b1 = (90, 10, 10)
        r2, g2, b2 = (170, 40, 10)
        r3, g3, b3 = (240, 90, 70)
        r4, g4, b4 = (200, 170, 15)
        threshold = 57"""
        
        mean_v = []

        for i in range(0, self.H - 1):
            for j in range(0, self.W -1):
                r = self._data[i*self.W*3 + j*3]
                g = self._data[i*self.W*3 + j*3 + 1]
                b = self._data[i*self.W*3 + j*3 + 2]

                d1 = ((r-r1)**2 + (g-g1)**2 + (b-b1)**2)**(1/2)
                d2 = ((r-r2)**2 + (g-g2)**2 + (b-b2)**2)**(1/2)
                d3 = ((r-r3)**2 + (g-g3)**2 + (b-b3)**2)**(1/2)
                d4 = ((r-r4)**2 + (g-g4)**2 + (b-b4)**2)**(1/2)

                if(d1 < threshold or d2 < threshold or d3 < threshold or d4 <threshold):
                    mean_v.append(self._data[i*self.W*3 + j*3])
                    mean_v.append(self._data[i*self.W*3 + j*3 + 1])
                    mean_v.append(self._data[i*self.W*3 + j*3 + 2])

        return mean_v


if __name__ == "__main__":
    main()