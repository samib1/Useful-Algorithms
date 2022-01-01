import numpy as np
import sys
import math
from timeit import default_timer as timer
from datetime import timedelta

def findmaximumcrossingsubarray(A, low, mid, high):
    """Find the maximum subarray of A[low] to A[high] crossing index mid.

    """

    #error checks should be here (omitted)
    #e.g. low <= mid <= high
    #what happens if low == mid or high == mid?

    leftsum = float('-Inf')
    sum = 0
    for i in range(mid, low-1, -1):
        sum += A[i]
        if (sum > leftsum):
            leftsum = sum
            left = i
            
    rightsum = float('-Inf')
    sum = 0
    for j in range(mid+1, high+1):
        sum += A[j]
        if (sum > rightsum):
            rightsum = sum
            right = j
    
    return left, right, leftsum + rightsum

def findmaximumsubarray(A, low, high):
    """Find the maximum subarray of A[low] to A[high].

    Recursive implementation using divide-and-conquer.
    """

    #error checks should be here (omitted)

    if (high > low):
        mid = int(math.floor(high+low)/2)
        leftlow, lefthigh, leftsum = findmaximumsubarray(A,low,mid)
        rightlow, righthigh, rightsum = findmaximumsubarray(A, mid+1, high)
        crosslow, crosshigh, crosssum = findmaximumcrossingsubarray(A, low, mid, high)
        if (leftsum >= rightsum and leftsum >= crosssum):
            return leftlow, lefthigh, leftsum
        elif (rightsum >= crosssum):
            return rightlow, righthigh, rightsum
        else:
            return crosslow, crosshigh, crosssum
    else:
        return low, high, A[low]

def bruteforcemaximumsubarray(A):
    """Find the maximum subarray of A.

    Brute force implementation checking all possibilities
    """

    maxsum = float('-Inf')
    
    for i in range(0, len(A)):
        for j in range(0, len(A)): #could be improved
            sum = 0
            for k in range(i, j+1): #but this omits cases j < i
                sum += A[k]
    
            if sum > maxsum:
                maxsum = sum
                left = i
                right = j
                
    return left, right, maxsum
    
def kadanemaximumsubarray(A):
    """Find the maximum subarray of A.

    Kadane's algorithm
    """
    maxsum = float('-Inf')
    bestleft = bestright = 0
    sum = 0
    for right in range(0, len(A)):
        if sum <= 0:
            # Start a new sequence at the current element
            left = right
            sum = A[left]
        else:
            # Extend the existing sequence with the current element
            sum += A[right]

        if sum > maxsum:
            maxsum = sum
            bestleft = left
            bestright = right

    return bestleft, bestright, maxsum
    
#main point of entry
n = 300
A = np.random.randint(-10,10,n)

start_time = timer()
[left, right, sum] = findmaximumsubarray(A, 0, n-1)
end_time = timer();
print("Divide-and-conquer time = ", timedelta(seconds=end_time-start_time))

bf_start_time = timer()
[bf_left, bf_right, bf_sum] = bruteforcemaximumsubarray(A);
bf_end_time = timer()
print("Brute-force time = ", timedelta(seconds=bf_end_time-bf_start_time))

kadane_start_time = timer()
[kadane_left, kadane_right, kadane_sum] = kadanemaximumsubarray(A);
kadane_end_time = timer()
print("Kadane time = ", timedelta(seconds=kadane_end_time-kadane_start_time))

print("Maximum subarray sum = ", sum, " from " , left, " to ", right)
print("Maximum brute force subarray sum = ", bf_sum, " from " , bf_left, " to ", bf_right)
print("Maximum kadane subarray sum = ", kadane_sum, " from " , kadane_left, " to ", kadane_right)







