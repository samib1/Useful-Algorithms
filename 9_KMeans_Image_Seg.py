import numpy as np
import sys
import math
import copy
from matplotlib import image as mpimg
from matplotlib import pyplot as plt
from timeit import default_timer as timer
from datetime import timedelta

fig, ((ax1, ax2, ax3)) = plt.subplots(1, 3) #make global for convenience - not recommended in general

def kmeanssegment(imgdata, k, max_its):

    """ Simple k-means image segmentation.
        Ian Jeffrey - April 2020. """

    #get image size
    m = len(imgdata)
    n = len(imgdata[0])

    imgdata_copy = copy.copy(imgdata)

    #initialize k means
    mean_vector = np.ndarray(shape=(k,3), dtype=float)
    new_mean_vector = np.ndarray(shape=(k,3), dtype=float)
    mean_pixel_counts = np.ndarray(shape=(k), dtype=int)
    mean_index_for_pixel = np.ndarray(shape=(m,n), dtype=int)
    
    #convert image data to numpy for easy math
    npimgdata = np.ndarray(shape=(m,n,3), dtype=int)
    npmeanmap = np.ndarray(shape=(m,n), dtype=int)
    for row in range(0,m):
        for col in range(0, n):
            npimgdata[row,col,0:3] = imgdata[row,col,0:3]
            npmeanmap[row,col] = -1

    #initalize means randomly
    for i in range(0, k):
        row = np.random.randint(0,m,1)[0]
        col = np.random.randint(0,n,1)[0]
        mean_vector[i,:] = npimgdata[row,col,:]
        
    iteration = 0

    #stat iterations
    while iteration <= max_its:
        print("k means iteration ", iteration, " of ", max_its)
        
        #calculate distances to each mean (matrix operations would be far better here!)
        for row in range(0,m):
            for col in range(0,n):
                min_distance = sys.maxsize
                for j in range(0, k):
                    distance_to_mean = np.dot(npimgdata[row,col] - mean_vector[j], npimgdata[row,col] - mean_vector[j])
                    distance_to_mean = distance_to_mean**0.5
                    
                    if distance_to_mean < min_distance:
                        min_distance = distance_to_mean
                        mean_index_for_pixel[row,col] = j
        
        #reset means and counts
        for j in range(0, k):
            new_mean_vector[j] = [0, 0, 0]
            mean_pixel_counts[j] = 0
        
        #calculate updated (new) means
        for row in range(0,m):
            for col in range(0,n):
                mean_index = mean_index_for_pixel[row][col]
                new_mean_vector[mean_index] += npimgdata[row,col,:]
                mean_pixel_counts[mean_index] += 1
            
        #finish updating means by scaling according to count
        for j in range(0,k):
            new_mean_vector[j,:] /= mean_pixel_counts[j]
            new_mean_vector[j,0] = int(new_mean_vector[j,0])
            new_mean_vector[j,1] = int(new_mean_vector[j,1])
            new_mean_vector[j,2] = int(new_mean_vector[j,2])
            
        #update the mean vector (could have just overwritten mean to begin with but... debugging.)
        mean_vector = new_mean_vector
    
        print("After iteration ", iteration, " the means are: \n", mean_vector)
    
        #produce an image that shows the means for each pixel (just for visualization)
        for row in range(0,m):
            for col in range(0,n):
                mean_index = mean_index_for_pixel[row][col]
                imgdata_copy[row,col,0:3] = mean_vector[mean_index,:]
                
        #plot some results
        if iteration%1 == 0:
            ax1.set_title('Original Image',fontsize=11)
            ax2.set_title(['K-Means at Iteration ',iteration],fontsize=11)
            ax3.set_title(['Groups at Iteration ', iteration],fontsize=11)
            ax1.matshow(imgdata)
            ax2.matshow(imgdata_copy)
            ax3.matshow(mean_index_for_pixel)
            ax1.xaxis.set_ticks_position('bottom')
            ax2.xaxis.set_ticks_position('bottom')
            ax3.xaxis.set_ticks_position('bottom')
            plt.pause(0.005)
            
        iteration += 1
            
    plt.show()

    return mean_vector, mean_index_for_pixel

#main
filename="./zoo-4821484_640.png" #grab your favourite image to try

imgdata = mpimg.imread(filename, 1) #read as unit format

k = 4
maxits = 10
mean_vector, mean_for_pixel = kmeanssegment(imgdata,k, maxits)






