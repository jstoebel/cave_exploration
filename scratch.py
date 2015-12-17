__author__ = 'stoebelj'
from collections import deque

d = deque()

for i in range(10):
    d.push(i)

for j in reversed(d):
    print j

print d