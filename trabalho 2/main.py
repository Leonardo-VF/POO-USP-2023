import argparse


parser = argparse.ArgumentParser(prog='filter')
parser.add_argument('--imgpath', action = 'store', dest = 'img_name', required = True)
parser.add_argument('--op',action = 'store', dest = 'operation', choises = ['thresholding', 'sgt', 'mean', 'median'], required= True)
parser.add_argument('--t', action = 'store', dest = 't', default = 127, type = 'int')
parser.add_argument('--dt', action = 'store', dest = 'dt', default = 1, type = 'int')
parser.add_argument('--k', action = 'store', dest = 'k', default = 3, type = 'int')
parser.add_argument('--outputpath', action = 'store', dest = 'output', default = 'img_name')

img = open('img_name')
project_type = img.readline()
width, height = img.readline().split()
pixels = int(width)*int(height)
maxval = int(img.readline())

class Image:
    def init(self):
        self._matz = img.read().replace('\n', '').split()
        self._type = project_type
        self._maxval = maxval
        self._height = height
        self._width = width
        self._pixels = pixels
        self._hist = [0 for x in range (self._pixels)]

        for y in range (self._height):
            for x in range (self._width):
                self._hist[self._matz[y][x]] += 1


    def thresholding(self, t):
        self._t = t
        new_matz = []
        self._g1 = 0
        self._g2 = 0
        self._m1 = 0
        self._m2 = 0

        for i in range(self._height):
            new_matz.append([])

        self._new_matz = new_matz
        
        for y in range(self._height):
            for x in range(self._width):
                if self._matz[y][x] < t:
                    self._new_matz[y].append(self._maxval)
                    self._g1 += 1
                    self._m1 += self._matz[y][x]
                    self._m1 = self._m1/self._g1

                else:
                    self._new_matz[y].append(0)
                    self._g2 += 1
                    self._m2 += self._matz[y][x]
                    self._m2 = self._m2/self._g2


    def sgt(self, dt, t):
        self._dt = dt

        while self._t > self._dt:
            self.thresholding(t)
            self._t = (self._m1 + self._m2)/2


    def mean(self, k):
        self._k = k

        for y in range (self._height):
            for x in range (self._width):
                for i in range (-self._k, self._k):
                    self._new_matz[y][x] = self._matz[y+i][x+i]
                self._new_matz[y][x] = self._new_matz[y][x]/(self._k**2)


    def median(self, k):
        self._k
        self._aux = []

        for y in range (self._height):
            for x in range (self._width):
                for i in range (-self._k, self._k):
                    self._aux.append(self._matz[y+i][x+i])
    
                self._aux.sort()
                self._new_matz[y][x] = self._aux[(self._k**2)/2]