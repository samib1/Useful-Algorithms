import numpy as np
import sys
import math
import copy
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from datetime import timedelta

def gcd(a,b):
    d = euclid(abs(a), abs(b))
    return d
    
def euclid(a,b):
    if b == 0:
        return a
    else:
        return euclid(b, a%b)

def extendedgcd(a,b):
    temp = extendedeuclid(abs(a), abs(b))
    d = temp[0]
    x = temp[1]
    y = temp[2]
    return d, x, y

def extendedeuclid(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        temp = extendedeuclid(b, a%b) #returns tuple (d, x, y)
        d = temp[0]
        x = temp[2]
        y = temp[1] - (a//b)*temp[2] #floor division
        return (d,x,y)

def modlineqsol(a,b,n):
    temp = extendedgcd(a,n)
    d = temp[0]
    x = temp[1]
    y = temp[2]
    if b%d == 0:
        solutions = [None]*d
        x0 = (x*(b//d)%n) #because d is gcd, floor division equiv to division (but forces integer)
        for i in range(0, d):
            solutions[i] = (x0 + i*(n//d))%n
        return solutions
    else:
        return None
        
def modexp(a,b,n):
    c = 0
    d = 1
    k = 64 #assume 64 bit integers
    for i in range(k,-1,-1): #k bits
        c = 2*c
        d = (d*d)%n
        bit = (b >> i) & 1
        if bit == 1:
            c = c + 1
            d = (d*a)%n
    return d

def nomodexp(a,b):
    c = 0
    d = 1
    k = 64 #assume 64 bit integers
    for i in range(k,-1,-1): #k bits
        c = 2*c
        d = (d*d)
        bit = (b >> i) & 1
        if bit == 1:
            c = c + 1
            d = (d*a)
    return d

def pseudoprime(n):
    d = modexp(2,n-1,n)
    if d%n == 1:
        return True
    else:
        return False
        
def generateprime(a,b, maxtries):
    for trials in range(0, maxtries):
        r = np.random.randint(a,b)
        if pseudoprime(r) == True:
            return r, trials
    
    return [], maxtries
    
#main point of entry

#test gcd functions
a = 30
b = 100

d = gcd(a,b)
print("gcd of ",a, " and ",b," is ", d)
d, x, y = extendedgcd(a,b)
print("gcd of ",a, " and ",b," is ", d, " with d = ", x, "a + ", y, "b")

#test modular linear equation solver
a = 14
b = 30
n = 100
solutions = modlineqsol(a,b,n)
print(solutions)

#test modular exponentiation
d1 = modexp(9, 560, 561)
d2 = (9**560)%561
print("modexp(9, 560, 561) = ", d1)
print("(9**560)%561 = ", d2)

#test pseudoprime
p = 319919
print(pseudoprime(p))
p = 319917
print(pseudoprime(p))

#test primality verification
p, tries = generateprime(int(1e6), int(100e6), 3000)
print("prime p = ", p)
q, tries = generateprime(int(1e6), int(100e6), 3000)
print("prime q = ", q)

dpq = gcd(p,q)
print("GCD of p and q = ", dpq) #if actually prime this will be 1

#test RSA

p = 11
q = 13
n = p*q

phin = (p-1)*(q-1) #Euler's phi function for n, a product of primes

#find e, odd and relatively prime to phin
for e in range(3,min(p, q),2): #consider only odd values
    print(e)
    d = gcd(e, phin)
    if d == 1:
        break
    
print("e = ", e)

#solve ed = 1 (mod n)
d = modlineqsol(e,1,phin)
d = d[0] #missing error check that a solution exits
print("d = ", d)

#next... encode and decode message 



