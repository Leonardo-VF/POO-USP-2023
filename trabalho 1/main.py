import sys


img_name = sys.argv[1]
num = int(sys.argv[2])
img = open(img_name)

project_type = img.readline()
width, height = img.readline().split()
pixels = int(width)*int(height)
maxval = int(img.readline())+1

def main():

    matz = img.read().replace('\n', '').split()
    matz = [int(x) for x in matz]
    matz.sort()

    prob = (maxval)/num
    intval = []

    for i in range (num):
        intval.append([])

    for x in matz:
        for n in range (num):
            if x < prob*(n+1) and x >= prob*n:
                intval[n].append(x)
    
    for i in range (num):
        print ('[{:.2f}, {:.2f}) {} {:.5f}'.format(prob*i, prob*(i+1), len(intval[i]), len(intval[i])/pixels))

if num <= 0:
    print('Erro: não é possível gerar {} bins.'.format(num))

elif num > maxval:
    print('Erro: número de bins pedido {}, mas {} é o valor máximo de intensidade na imagem.'.format(num, maxval-1))

else:
    main()