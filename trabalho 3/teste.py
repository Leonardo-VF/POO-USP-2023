import argparse


parser = argparse.ArgumentParser(prog = 'filter')
parser.add_argument('--imgpath', action = 'store', dest = 'img_name', required = True)
parser.add_argument('--op',action = 'store', dest = 'operation', required = True)
parser.add_argument('--t', action = 'store', dest = 't', default = 127, type = int)
parser.add_argument('--dt', action = 'store', dest = 'dt', default = 1, type = int)
parser.add_argument('--k', action = 'store', dest = 'k', default = 3, type = int)
parser.add_argument('--outputpath', action = 'store', dest = 'output', default= '')
args = parser.parse_args()

print(args)