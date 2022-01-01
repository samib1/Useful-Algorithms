import numpy as np
import math
import matplotlib as mpl
from matplotlib import pyplot as plt

fig, ((ax1, ax2, ax3)) = plt.subplots(1, 3) #make global for convenience - not recommended in general

def robotsearch(grid, moves):
    """Given an m x n grid of items evaluate a score based on items picked up by a robot searching the space.
       
       It is assumed the robot starts at location (0,0), and the moves is a sequence of binary
       digits twice the length as the number of actual moves. Moves are: 00 left, 01 right, 10 down, 11 up.
       
       A move that hits the edge of the board leaves the robot unmoved.
       
       """
    
    gridcopy = np.copy(grid)    #a copy of the grid to keep track of what items are collected
    robot_path = np.copy(grid)  #a copy of the grid to keep track of the robot's path
    
    #initialize
    m, n = grid.shape
    robot_row = 0
    robot_col = 0
    assert(len(moves)%2 == 0)
    num_moves = int(len(moves)/2)  #the number of moves is half the size of "moves" as that is a binary representation
    
    #for each move (+1 for the initial location) we store the row, col and score of the robot
    robot_row_history = np.zeros(num_moves + 1)
    robot_col_history = np.zeros(num_moves + 1)
    robot_score_history = np.zeros(num_moves + 1)
    
    #initialize the row, col and score
    robot_row_history[0] = robot_row
    robot_col_history[0] = robot_col
    robot_score = grid[robot_row, robot_col]
    
    #for each move, decode the move
    for i in range(0, num_moves):
        if moves[2*i] == 0 and moves[2*i+1] == 0:
            robot_col = max(robot_col - 1, 0) # move left, stop by boundary
        elif moves[2*i] == 0 and moves[2*i+1] == 1:
            robot_col = min(robot_col + 1, n-1) # move right, stop by boundary
        elif moves[2*i] == 1 and moves[2*i+1] == 0:
            robot_row = max(robot_row - 1, 0) # move down, stop by boundary
        elif moves[2*i] == 1 and moves[2*i+1] == 1:
            robot_row = min(robot_row + 1, m-1) # move up, stop by boundary
        else:
            print("Unsupported Move Detected")
            assert(0==1)
            
        robot_row_history[i+1] = robot_row #store the move
        robot_col_history[i+1] = robot_col
        
        robot_score += gridcopy[robot_row, robot_col] #increase the score
        robot_score_history[i+1] = robot_score
        gridcopy[robot_row, robot_col] = 0 #already visited this
        robot_path[robot_row, robot_col] = 0.5

    return robot_score_history[len(robot_score_history)-1], robot_path #just return the final score and path


def garobotsearch(m, n, itemfraction, nummoves, population_size, maxits):

    """Setup and run a Genetic Algorithm to optimize the number of items a robot picks up
        as evaluated by the robotsearch() function.
    """

    #setup the initial grid an populate it
    grid = np.zeros([m,n])
    numitems = int(itemfraction*m*n)
    item_rows = np.random.randint(m, size=numitems)
    item_cols = np.random.randint(n, size=numitems)

    best_possible_score = 0 #this assumes a set of moves that can cover the whole board - may not be the case
    for i in range(0, numitems):
        grid[item_rows[i], item_cols[i]] = 1.0
        best_possible_score += grid[item_rows[i], item_cols[i]]

    #display initial setup
    print("Running GA on ", m, " x ", n, " grid with ", itemfraction*100, "% item density. Best possible score = ", best_possible_score)

    #set population, genes are twice as long as moves to encode 00, 01, 10, 11 as a move
    gene_size = int(nummoves*2)
    population = np.random.randint(2, size=[population_size, nummoves*2])
    new_population = 0*population

    #initial fitness evaluation
    fitness = np.zeros(population_size)
    population_best_fitness = 0
    for i in range(0, population_size):
        score, robot_path = robotsearch(grid, population[i,:])
        fitness[i] = score
        if fitness[i] > population_best_fitness:
            population_best_robot_path = np.copy(robot_path)
            population_best_fitness = fitness[i]
            population_best_gene = np.copy(population[i,:])

    #best over all populations
    best_robot_path = np.copy(population_best_robot_path)
    best_fitness = population_best_fitness
    best_gene = np.copy(population_best_gene)

    #normalize fitness
    normalized_fitness = fitness/max(fitness)

    #set ga random parameters
    crossover_percent = 0.7
    mutation_percent = 0.1

    #start looping
    iteration = 0
    while iteration < maxits:
    
        iteration = iteration + 1

        #The following code block allocates an array of population indexes where the number of times
        #a given population index appears in the list is proportional to its fitness. For example:
        #if gene 1, gene 2, and gene 3 have respective fitness 10, 5, and 20, then gene 3 would appear
        #twice as many times in the list as gene 1, and 4 times as may times as gene 2.

        gene_count_by_fitness = np.zeros(population_size+1) #the number of counts assigned based on fitness
        for i in range(0, population_size):
            gene_count_by_fitness[i+1] = gene_count_by_fitness[i] + int(normalized_fitness[i]*100) #the count is proportional to the normalized fitness
            
        gene_selection_lottery_array = np.zeros(int(gene_count_by_fitness[population_size])) #this will store the gene labels for selection
            
        for i in range(0, population_size):
            gene_selection_lottery_array[int(gene_count_by_fitness[i]):int(gene_count_by_fitness[i+1])] = i #and here we put gene i in the selection array a number of times proportional to fitness

        
        #now we are ready to produce a new generation / population
        for i in range(1, int(population_size/2)): #we mate pairs, so take half the population size
            
            #step 1 is selection: select two genes (biased towards better fitness)
            lottery_tickets = np.random.randint(max(gene_count_by_fitness), size=2)
            
            parent1_index = int(gene_selection_lottery_array[lottery_tickets[0]])
            parent2_index = int(gene_selection_lottery_array[lottery_tickets[1]])
            
            parent1 = population[parent1_index,:]
            parent2 = population[parent2_index,:]
            
            #step 2 is crossover/mating - we may crossover or not in this implementation
            dice_role = np.random.rand(1)
            if dice_role[0] <= crossover_percent:
                crossover_index = np.random.randint(gene_size, size=1)
                child1 = parent1 #start the child as parent 1
                child1[int(crossover_index):int(gene_size)] = parent2[int(crossover_index):int(gene_size)] #add parent 2's part to the end
                child2 = parent2
                child2[int(crossover_index):int(gene_size)] = parent1[int(crossover_index):int(gene_size)] #add parent 1's part to the end
                new_population[2*i,:] = child1
                new_population[2*i+1] = child2
            else:
                new_population[2*i,:] = parent1 #if no cross over keep both parents
                new_population[2*i+1,:] = parent2
        
            #step 3: mutation - we may mutate each bit of the gene or not in this implementation
            dice_role = np.random.rand(gene_size)
            for mutation_index in range(0, gene_size):
                if dice_role[mutation_index] <= mutation_percent:
                    new_population[i,mutation_index] = (new_population[i,mutation_index]+1)%2 #just a toggle because it is binary

        #population has been updated
        population = np.copy(new_population)
    
        #fitness evaluation
        population_best_fitness = 0
        for i in range(0, population_size):
            score, robot_path = robotsearch(grid, population[i,:])
            fitness[i] = score
            if fitness[i] > population_best_fitness:
                population_best_robot_path = np.copy(robot_path)
                population_best_fitness = fitness[i]
                population_best_gene = np.copy(population[i,:])

        #best over all populations
        if population_best_fitness > best_fitness:
            best_robot_path = np.copy(population_best_robot_path)
            best_fitness = population_best_fitness
            best_gene = np.copy(population_best_gene)
    
        #normalize fitness
        normalized_fitness = fitness/max(fitness)
        
        print("iteration ", iteration, " max pop fitness = ", population_best_fitness, " max overall = ", best_fitness)

        if iteration%100 == 0:
            ax1.matshow(grid)
            ax2.matshow(population_best_robot_path)
            ax3.matshow(best_robot_path)
            plt.pause(0.005)
            ax1.set_title('Original Items',fontsize=11)
            ax2.set_title('Best Path - Current Population',fontsize=11)
            ax3.set_title('Best Path - Overall',fontsize=11)
            fig.suptitle(['GA Robot Search at Iteration ',iteration])

    plt.show()

#main point of entry

maxits = 1000
population_size = 20
nummoves = 300
m = 30
n = 30
itemfraction = 0.1 #multiply by 100 for percentage of grid points that are items

garobotsearch(m, n, itemfraction, nummoves, population_size, maxits)
