import numpy as np
import sys
import math
import operator #for sorting lists of classes by attribute
from timeit import default_timer as timer
from datetime import timedelta

class SimpleActivity:
    """A simple activity class"""
    start_time = -1
    finish_time = -1

    def __init__(self, start, finish):
        self.start_time = start;
        self.finish_time = finish;

    def __repr__(self):
        return str("Activity instance") + str(self.__dict__)
    def __str__(self):
        return str("Activity instance") + str(self.__dict__)


def RecursiveGreedySchedule(activities, k, n, schedule):
    """Greedy Schedule using Recursion"""

    m = k + 1 #we start looking at activities after k, n is the total number of activities
    
    #move through activities until we find the first one that starts after activity
    #k finishes. this activity has the earliest end time as the list is pre-sorted
    while (m < n and activities[m].start_time < activities[k].finish_time):
        m += 1
    
    #as long as we haven't gone off the end of the list, schedule activity m
    #and make a recursive call starting after activity m
    if m < n:
        schedule.append(activities[m])
        RecursiveGreedySchedule(activities, m, n, schedule)

def IterativeGreedySchedule(activities):
    """Greedy Schedule Iteratively"""

    n = len(activities)
    schedule = [];
    schedule.append(activities[0])
    k = 0
    for m in range(1,n):
        #keep moving through activities to find the next one that can start
        #this activity also has the earliest end time as the list is pre-sorted
        if (activities[m].start_time >= activities[k].finish_time):
            schedule.append(activities[m])  #once found add the activity to the list
            k = m   #we now need to look after this activity in the sorted list

    return schedule


#main point of entry
num_activities = 150
activity_set = [];
activity_set.append(SimpleActivity(0,0)) #ficticious activity so we can start looking after a0

#create a liist of random activities
for i in range(0,num_activities):

    activity_start_time = np.random.randint(0,60,1)
    activity_stop_time = np.random.randint(activity_start_time + 1, 61, 1) #stop time must happen after start time
    activity_set.append(SimpleActivity(activity_start_time[0], activity_stop_time[0]))

#sort the list by finish time
activity_set.sort(key=operator.attrgetter('finish_time'))

#display the list of activities
for i in activity_set:
    print(i)

#run and time the recursive schedule
start_time = timer()
recursive_schedule = [];    #start with a blank schedule
RecursiveGreedySchedule(activity_set, 0, num_activities, recursive_schedule)
end_time = timer();
time_recursive = timedelta(seconds=end_time-start_time)
print("Recursive Schedule time = ", time_recursive)
del activity_set[0] #delete that ficticious activity (it isn't needed in the recursive case)

#run and time the iterative schedule
start_time = timer()
iterative_schedule = IterativeGreedySchedule(activity_set)
end_time = timer();
time_iterative = timedelta(seconds=end_time-start_time)
print("Iterative Schedule time = ", time_iterative)

#display the solutions (recursive left, iterative right)
#some weird indexing here
for i in range(0, len(iterative_schedule)):
    print("Recursive Event Scheduled: \t", recursive_schedule[i], " --- Iterative Event Scheduled: ", iterative_schedule[i])

