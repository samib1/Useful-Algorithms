import numpy as np
import sys
import math
from timeit import default_timer as timer
from datetime import timedelta

def recursiverodcut(p,n):
    """Recursively optimize the revenue on selling a rod of length n with length prices p.
    
    """
    if n == 0:
        return 0
    
    r = float('-Inf')
    for i in range(1,n+1): #cut at location 1 up to location n (note location n = no cut)
        r = max(r, p[i-1] + recursiverodcut(p, n-i)) #zero based access for price p
    return r

def memoizedrodcut(p,n):
    """Wrapper function for memoized recursive rod cut (dymanic programming approach)
        
        """
    rvec = np.zeros(n+1)            #memos (list of values to be kept)
    rvec[0:n+1] = -float('Inf')     #initialize to "not calculated"
    r = memoizedrecursiverodcut(p,n,rvec)
    return r


def memoizedrecursiverodcut(p,n,rvec):
    """Recursively optimize the revenue on selling a rod of length n with length prices p.
        
        """
    if rvec[n] >= 0.0:              #if the memo exists, just return it
        return rvec[n]
    
    if n == 0:                      #the rest is like our recursive function in Lecture 13
        r = 0
    else:
        r = float('-Inf')
        for i in range(1,n+1): #cut at location 1 up to location n (note location n = no cut)
            r = max(r, p[i-1] + memoizedrecursiverodcut(p, n-i, rvec)) #zero based access for price p
        rvec[n] = r; #keep the record (write the memo)
    return r

def bottomuprodcut(p,n):
    """Solve the rod cutting problem bottom up to optimize revenue on selling a rod of length n with length prices p
        
        """    
    rvec = np.zeros(n+1)    #record of values
    svec = np.zeros(n+1)    #best cuts for each length
    rvec[0] = 0 #a zero-size piece gets 0 revenue
    
    
    neg_inf = float('-Inf')
    for j in range(1,n+1): #determine max revenue for size j = 1 up to and including n
        r = neg_inf
        for i in range(1, j+1):     #for solving problem j, find which cut length i maximizes profit
            if (r < p[i-1] + rvec[j-i]):
                r = p[i-1] + rvec[j-i]
                svec[j] = i         #store the cut length that maximizes profit
        rvec[j] = r #keep the record (write the memo)
    return rvec[n], svec

def printrodcutsolution(p,n,r,svec):
    """Display the solution to the rod cutting problem
                    
    """
    print("Rod cutting solution for problem size n = ", n, " with prices p = ", p)
    print("Max revenue r = ", r, " using cut lengths: ")
    n_remaining = n
    r_from_cuts = 0
    cutcount = 0
    while n_remaining > 0: #while we still have length left
        cutcount += 1
        cutsize = int(np.floor(svec[n_remaining]))  #the best length to cut off is stored in svec
        cutvalue = p[cutsize - 1]                   #p excludes 0
        print("\tCut # ", cutcount, ": length = ", cutsize, " value = ", cutvalue)  #display the cut
        n_remaining = n_remaining - cutsize         #we've cut off cutsize so we are left with this
        r_from_cuts += cutvalue                     #add up the revenue to check answer
    print("Sum of cut values = ", r_from_cuts)

#main entry point
n = 15
p = np.random.randint(1,n,n)

print("\n\nRod-cutting problem with n = ", n)
print("Price list = ", p, "\n")

#recursive version
start_time = timer()
rrecursive = recursiverodcut(p, n)
end_time = timer();
time_recursive = timedelta(seconds=end_time-start_time)
print("Divide-and-conquer time = ", time_recursive)
print("Divide-and-conquer max revenue = ", rrecursive, "\n")

#memoized version
start_time = timer()
rmemoized = memoizedrodcut(p,n)
end_time = timer()
time_memoized = timedelta(seconds=end_time-start_time)
print("Memoized time = ", time_memoized)
print("Memoized max revenue = ", rmemoized)
print("Memoization Speedup = ", time_recursive/time_memoized, "\n")

#bottom-up version
start_time = timer()
rbottomup, svec = bottomuprodcut(p,n)
end_time = timer()
time_bottomup = timedelta(seconds=end_time-start_time)
print("Bottom-up time = ", time_bottomup)
print("Bottom-up max revenue = ", rbottomup)
print("Bottom-up vs Memoization Speedup = ", time_memoized/time_bottomup, "\n")

#display the solution
printrodcutsolution(p, n, rbottomup, svec)
                




