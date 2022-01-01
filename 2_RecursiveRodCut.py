import numpy as np
import sys
import math
from timeit import default_timer as timer
from datetime import timedelta

#def recursiverodcut(p,n, tabstr):
def recursiverodcut(p,n):
    """Recursively optimize the revenue on selling a rod of length n with length prices p.
    
    """
    if n == 0:
        return 0
    
    r = float('-Inf')

    for i in range(1,n+1): #cut at location 1 up to location n (note location n = no cut)
        r = max(r, p[i-1] + recursiverodcut(p, n-i)) #zero based access for price p
    return r

def directrodcut(p,n):
    """Directly optimize the revenue on selling a rod of length n with length prices p.

    """
    
    r = float('-Inf');  #maximum revenue

    for i in range(0, 2**(n-1)): #for every possible set of cuts
        
        bitstring = bin(i)[2:].zfill(n-1) #determine cut bitstring

        value = 0.0         #value of current set of cuts
        piece_size = 1      #current piece size
        
        for j in range(0,n-1): #loop over the cut bitstring
            if int(bitstring[j]) == 1: #if we encounter a cut
                value += p[piece_size-1] #add value of current piece (note price list doesn't include size 0)
                piece_size = 1 #reset piece size for next piece
            else:
                piece_size += 1 #extend piece size
        value += p[piece_size - 1] #add value of last piece
        r = max(r,value)


#main entry point
n = 18 #this starts to take a lot of time quickly - go from here and increase cautiously.
p = np.random.randint(1,n,n)

print("Rod-cutting problem with n = ", n)
print("Price list = ", p)

start_time = timer()
rrecursive = recursiverodcut(p, n)
end_time = timer();
print("Divide-and-conquer time = ", timedelta(seconds=end_time-start_time))
print("Divide-and-conquer max revenue = ", rrecursive)

start_time = timer()
rdirect = directrodcut(p,n)
end_time = timer()
print("Direct time = ", timedelta(seconds=end_time-start_time))
print("Direct max revenue = ", rrecursive)








