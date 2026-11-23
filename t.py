import os
import sys

def load(FileName : str) -> bytes:
    f = open(FileName, 'rb')
    fd = f.read()
    f.close()
    return fd

fasla = str('tintin7').encode('utf-8')
d = load('p.jpg')
nd = d + fasla + b'kokmi'
Ineed = nd.split(fasla)
print(str(Ineed[0]))
#print(str(len(d)))
#for x in range(10):
#    print(str(d[x]))