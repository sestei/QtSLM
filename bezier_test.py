#!/usr/bin/python

from pylab import *

def f(t):
	return a*t**3 + b*t**2 + c*t + d

P0 = 0
P3 = 1.0
P1 = 1.00
P2 = 0.0

a = P3 - 3*P2 + 3*P1 - P0
b = 3*P2 - 6*P1 + 3*P0
c = 3*P1 - 3*P0
d = P0

t = linspace(0,1.0,100)
plot(t, f(t), [0, 1/3., 2/3., 1.0], [P0,P1,P2,P3])
show()
