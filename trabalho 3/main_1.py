#Leonardo Vaz Ferreira n# 13862330
#Rodrigo Alexandre Gilgen n# 13686921

import argparse, sys

class Image:
    def __init__(self, type, width, height, maxval, matz):
        self._type = type
        self._width, self._height = int(width), int(height)
        self._maxval = maxval
        self._matz = matz
        self._hist = [0]*256

        for y in self._matz:
            for x in y:
                self._hist[x] += 1 

    def thresholding(self, t=127):
        self._t = t
        self._new_matz = [[] for x in range (self._height)]
        self._mean = 0
        self._median = []
        self._g1 = 0
        self._g2 = 0
        self._m1 = 0
        self._m2 = 0

        #faz o thresholding e faz as médias
        for y in range(self._height):
            for x in range(self._width):
                if self._matz[y][x] > self._t:
                    self._g1 += 1
                    self._m1 += self._matz[y][x]
                    self._mean += self._matz[y][x]
                    self._median.append(self._matz[y][x])
                    self._new_matz[y].append(255)

                else:
                    self._g2 += 1
                    self._m2 += self._matz[y][x]
                    self._mean += self._matz[y][x]
                    self._median.append(self._matz[y][x])
                    self._new_matz[y].append(0)
                    
        if self._g1 != 0:
            self._m1 = int(self._m1/self._g1)

        if self._g2 != 0:
            self._m2 = int(self._m2/self._g2)

        self._median.sort()
        self._median = self._median[int((self._width*self._height)/2)]
        self._mean = int(self._mean/(self._width*self._height))

        new_maxval = 0

        #encontra o maxval
        for i in self._new_matz:
            for h in i:
                if h > new_maxval:
                    new_maxval = h

        return Image(self._type, self._width, self._height, new_maxval, self._new_matz)

    def sgt(self, dt=1, t=127):
        self._dt = dt
        self._new_t = t
        self._t = 0
        self._new_maxval = 0

        #calcula dt e faz do thresholding
        while abs(self._new_t - self._t) >= self._dt:
            self._t = self._new_t 
            self.thresholding(self._new_t)
            self._new_t = int((self._m1 + self._m2)/2)

        for i in self._matz:
            for h in i:
                if h > self._new_maxval:
                    self._new_maxval = h

        return Image(self._type, self._width, self._height, self._new_maxval, self._new_matz)


    def mean(self, k=3):
        self._k = k
        self._new_matz = [[0]*self._width for x in range (self._height)]
        self._viz = int((self._k-1)/2)

        #percorre a matz
        for y in range (self._height):
            for x in range (self._width):
                #percorre a vizinhança de matz[y][x]
                for i in range (-self._viz, self._viz + 1):
                    for h in range (-self._viz, self._viz + 1):
                        #tratamento das bordas
                        if y+i >= 0 and x+h >= 0:
                            try:
                                self._new_matz[y][x] += self._matz[y+i][x+h]
                            except:
                                self._new_matz[y][x] += 0
                        else:
                            self._new_matz[y][x] += 0
                                
                #faz a média
                self._new_matz[y][x] = int(self._new_matz[y][x]/((self._k**2)))

        new_maxval = 0

        #encontra o maxval
        for i in self._new_matz:
            for h in i:
                if h > new_maxval:
                    new_maxval = h

        return Image(self._type, self._width, self._height, new_maxval, self._new_matz)

    def median(self, k=3):
        self._k = k
        self._new_matz = [[0]*self._width for x in range (self._height)]
        self._viz = int((self._k-1)/2)

        #percorre matz
        for y in range (self._height):
            for x in range (self._width):
                self._aux = []
                #percorre a vizinhança de matz[y][x]
                for i in range (-self._viz, self._viz+1):
                    for h in range (-self._viz, self._viz+1):
                        #tratamento das bordas
                        if y+i >= 0 and x+h >= 0:
                            try:
                                self._aux.append(self._matz[y+i][x+h])
                            except:
                                self._aux.append(0)
                        else:
                            self._aux.append(0)

                #faz a mediana
                self._aux.sort()

                self._new_matz[y][x] = self._aux[int(((self._k**2)-1)/2)]

        new_maxval = 0

        #encontra o maxval
        for i in self._new_matz:
            for h in i:
                if h > new_maxval:
                    new_maxval = h

        return (save_image('_median_k', self._type, self._width, self._height, new_maxval, self._new_matz))


    def sobel(self):
        Gx = [
            [1, 0, -1],
            [2, 0, -2],
            [1, 0, -1]
        ]

        Gy = [
            [1, 2, 1],
            [0, 0, 0],
            [-1, -2, -1]
        ]

        self._Ex = [[0]*self._width for x in range (self._height)]
        self._Ey = [[0]*self._width for x in range (self._height)]
        self._new_matz = [[0]*self._width for x in range (self._height)]

        #percorre matz
        for y in range (self._height):
            for x in range (self._width):
                #percorre a vizinhança (3x3) de Gx e da matz
                for i in range (-1, 2):
                    for h in range (-1, 2):
                        if y+i >= 0 and x+h >= 0:
                            try:
                                self._Ex[y][x] += self._matz[y+i][x+h] * Gx[i+1][h+1]
                                self._Ey[y][x] += self._matz[y+i][x+h] * Gy[i+1][h+1]
                            except:
                                self._Ex[y][x] += 0
                                self._Ey[y][x] += 0
                        else:
                            self._Ex[y][x] += 0
                            self._Ey[y][x] += 0

        for y in range (self._height):
            for x in range (self._width):
                self._new_matz[y][x] = (self._Ex[y][x]**2 + self._Ey[y][x]**2)**(1/2)
        
        #calcula o fator de conversão 
        self._max = 0

        for i in self._new_matz:
            for j in i:
                if j > self._max:
                    self._max = j

        conv = 255/self._max
        
        for y in range (self._height):
            for x in range (self._width):
                self._new_matz[y][x] = round(self._new_matz[y][x]*conv)

        new_maxval = 0

        #encontra o maxval
        for i in self._new_matz:
            for h in i:
                if h > new_maxval:
                    new_maxval = h

        return Image(self._type, self._width, self._height, new_maxval, self._new_matz)


#salvar as imagens
def save_image(name, image):
    type, width, height, maxval, matz = image._type, image._width, image._height, image._maxval, image._matz
    with open(name, 'w') as img:
        img.write('{}\n'.format(type))
        img.write('{} {}\n'.format(width, height))
        img.write('{}\n'.format(maxval))

        for i in matz:
            #img.write(' '.join(i))
            for x in i:
                img.write('{} '.format(x))
            img.write('\n')

def config_argparse():
    operations = []
    for argument in sys.argv:
        if argument == '--op':
            index = sys.argv.index(argument) + 1
            first = index - 1
            while (index < len(sys.argv) and sys.argv[index] != '--output'):
                operations.append(sys.argv[index])
                index += 1
            del sys.argv[first:index]
            break

    parser = argparse.ArgumentParser(prog = 'filter')
    parser.add_argument('--imgpath', action = 'store', dest = 'img_name', required = True)
    parser.add_argument('--outputpath', action = 'store', dest = 'output', default= '')
    args = parser.parse_args(sys.argv[1:])
    return args, operations

def read_arq(args):
    with open(args.img_name) as img:
        type = img.readline().replace('\n','')
        width, height = img.readline().split()
        width, height = int(width), int(height)
        maxval = int(img.readline())
        matz = []
        for i in range(height):
            matz.append(list(map(int, img.readline().replace('\n', '').split())))

    return(type, width, height, maxval, matz)

def verify_args(args, operations):
    img_name = args.img_name
    output_path = args.output
    # verificando múltiplas operações (sem repetições)
    outops = {}
    ops = {'sobel': None, 'sgt': '--dt', 'thresholding': '--t', 'median': '--k', 'mean': '--k'}
    operorder = [op for op in operations if op in ops.keys()]
    for index in range(0, len(operations)):
        operation = operations[index]
        if operation in ops.keys():
            if operation != 'sobel':
                index += 1
                if operations[index] == ops[operation]: 
                    index += 1
                    outops[operation] = int(operations[index])
    return img_name, outops, operorder, output_path

def new_name(old_name, operations, operorder, output):
    old_name = old_name.replace('.pgm', '')
    name = [old_name]
    for operation in operorder:
        name.append(operation)
        if operation != 'sobel':
            name.append(str(operations[operation]))
    new_name = output + '-'.join(name) + '.pgm'
    return new_name
        

def exec_ops(operations, order, image):
    for operation in order:
        if operation == 'thresholding':
           image = image.thresholding(operations[operation])
        elif operation == 'sgt':
           image = image.sgt(operations[operation])
        elif operation == 'mean':
           image = image.mean(operations[operation])
        elif operation == 'median':
           image = image.median(operations[operation])
        elif operation == 'sobel':
           image = image.sobel()
    return image

def print_info(name, operations, order):
    ops = {'sgt': '--dt', 'thresholding': '--t', 'median': '--k', 'mean': '--k'}
    print(f'image_name: {name}')
    for operation in order:
        print(f'op: {operation}')
        if operation != 'sobel':
            print((f'    {ops[operation]}: {operations[operation]}').replace('--', ''))

def main():
    # verificar input
    args, ops = config_argparse()
    img_name, operations, order, output = verify_args(args, ops)
    #objeto img
    type, width, height, maxval, matz = read_arq(args)
    obj = Image(type, width, height, maxval, matz)
    outname = new_name(img_name, operations, order, output)
    # realizar as operações pedidas e salvar a imagem
    new_image = exec_ops(operations, order, obj)
    save_image(outname, new_image)
    # enviar as informações pedidas
    print_info(img_name, operations, order)

if __name__ == '__main__':
    main()
