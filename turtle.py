from scipy import stats
import random

def generate_grid(length):
    # Probability of finding diamonds at any location
    p_diamond = 0.3
    # Length of sides of grid
    # length = 3
    
    # Generate blocks for 16x16x16 grid
    samples = []
    for i in range(0, length**3):
        samples.append(stats.bernoulli.rvs(p_diamond, 0))
    
    # Dimensions: 16 x 16 x 16
    grid = [[[0 for x in range(length)] for x in range(length)] for x in range(length)]
    # Insert samples into 3D grid array
    index = 0
    for i in range(0, length):
        for j in range(0, length):
            for k in range(0, length):
                grid[i][j][k] = samples[index]
                index += 1
    return grid
    
# Let state = 
# 0 --> X-pos
# 1 --> Z-pos
# 2 --> Y-pos
# 3 --> Energy left

# state[0] += 1

# Movement functions
def move_north(state, m):
    state[3] -= 1
    if state[0] < m - 1:
        state[0] += 1

def move_south(state, m):
    state[3] -= 1
    if state[0] > 0:
        state[0] -= 1

def move_east(state, m):
    state[3] -= 1
    if state[2] < m - 1:
        state[2] += 1

def move_west(state, m):
    state[3] -= 1
    if state[2] > 0:
        state[2] -= 1

def move_down(state, m):
    state[3] -= 1
    if state[1] < m - 1:
        state[1] += 1

def move_up(state, m):
    state[3] -= 1
    if state[1] > 0:
        state[1] -= 1

# Gene Generation Function (Old)
#def create_genes():
#    genes = []
#    for i in range(64):
#        # Create single gene array within genes matrix
#        genes.append([])
#        # Get binary representation
#        index = bin(i)[2:]
#        # Increase to six characters if necessary
#        while length(index) < 6:
#            index.insert(0,0)
#        # Insert first six bits of gene:
#        for j in range(6):
#            genes[i].append(index[j])
#        # Generate random number, 1-6, dictating action
#        random.seed()
#        action = random.randrange(1,6,1)
#        genes[i].append(action)
#    return genes

# Gene Generation Function
def create_genes():
    genes = []
    genes_dir_pairs = []
    genes_act_pairs = []
    gene_num = 64
    pairs_dir_num = 6
    pairs_act_num = 1
    
    # Set seed
    random.seed()
    
    # Generate gene pairs for sensor direction sequence
    # 0 = Nothing, 1 = Diamonds, 2 = Wall
    for i in range(0, gene_num):
        genes_dir_pairs.append([])
        for j in range(0, pairs_dir_num):
            genes_dir_pairs[i].append(random.randrange(0,2,1))     # Basic random numbers
    
    # Generate gene pairs for actions
    # 0 = North, 1 = South, 2 = East, 3 = West, 4 = Down, 5 = Up, 6 = Random
    for i in range(0, gene_num * pairs_act_num):
        genes_act_pairs.append([])
        for j in range(0, pairs_act_num):
            genes_act_pairs[i].append(random.randrange(0,6,1))
    
    # Combine sensor direction sequence with action sequence for all genes
    for i in range(0, gene_num):
        # Create single gene array within genes matrix
        genes.append([])
        # Append the first sensor direction bits of the genes
        for j in range(0, pairs_dir_num):
            genes[i].append(genes_dir_pairs[i][j])
        # Append the action pair(s)
        for k in range(0, pairs_act_num):
            genes[i].append(genes_act_pairs[i][k])
    
    # Create 65th gene for random action
    random_gene = [0,0,0,0,0,0,random.randrange(0,6,1)]
    genes.append(random_gene)
    
    return genes

# Sensor read function
def sensor_read(state, grid, grid_length):
    sensors = [0,0,0,0,0,0]

    # For each direction
    for i in range(0, len(sensors)):
        # North
        if i == 0:
            # Check if north is wall
            if state[0] == grid_length - 1:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]+1][state[1]][state[2]] # 1 North
        
        # South
        if i == 1:
            # Check if north is wall
            if state[0] == 0:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]-1][state[1]][state[2]] # 1 South
        
        # East
        if i == 2:
            # Check if east is wall
            if state[2] == grid_length - 1:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]][state[1]][state[2]+1] # 1 East
        
        # West
        if i == 3:
            # Check if west is wall
            if state[2] == 0:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]][state[1]][state[2]-1] # 1 West
        
        # Down
        if i == 4:
            # Check if down is wall
            if state[1] == grid_length - 1:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]][state[1]+1][state[2]] # 1 Down
        
        # Up
        if i == 5:
            # Check if up is wall
            if state[1] == 0:
                sensors[i] = 2
            # Else, get sensor reading
            else:
                sensors[i] = grid[state[0]][state[1]-1][state[2]] # 1 Up
    
    return sensors
    
# Gene match with action function
def gene_match(sensors, genes):
    # Default to random action (last item in 2D gene matrix)
    action = genes[-1][-1]
    
    # Attempt to match with first 64 (non-random) genes:
    for i in range(0, len(genes)-1):
        if genes[i][0:6] == sensors:
            action = genes[i][-1]
    
    return action

# Simulation Function - Simulates 1 liftime of 1 turtle
def simulate_turtle(genes):
    print("Simulate")
    score = 0
    # Set battery life
    life = 20
    # Generate grid
    grid_length = 16
    grid = generate_grid(grid_length)
    
    # Drop turtle in random place
    random.seed()
    start_x = random.randrange(0,grid_length - 1,1) # North-South
    start_z = random.randrange(0,grid_length - 1,1) # Down-Up
    start_y = random.randrange(0,grid_length - 1,1) # East-West
    state = [start_x, start_z, start_y, life]
    
    # Array of move functions
    movements = [move_north, move_south, move_east, move_west, move_down, move_up]
    
    while state[3] > 0:
        print("State: ",state[0],state[1],state[2])
        # If current position is on diamond, add score
        if grid[state[0]][state[1]][state[2]] == 1:
            score += 1
        
        # Get sensor data
        # [NORTH, SOUTH, EAST, WEST, DOWN, UP]
        sensors = sensor_read(state, grid, grid_length)
        
        # Attempt to match sensors with genes 1-64:
        action = gene_match(sensors, genes)
        
        # Perform movement
        if action < 6:
            movements[action](state, grid_length)
        else:
            random.seed()
            move = random.randrange(0,5,1)
            movements[move](state, grid_length)
    
    return score
    

# Mining Turtle Class
class Turtle:
    species = "Turtle"
    
    def __init__(self, name):
        self.name = name
        self.dna = create_genes()
        self.score = 0
    
    def simulate(self):
        self.score = simulate_turtle(self.dna)

turtle1 = Turtle("Tortoise")
turtle1.simulate()
print(turtle1.score)

#grid = generate_grid(16)
#print(grid)

# Assuming m x m x m grid:

# In range:
#print(grid[0][0][m-1])

# Not in range:
#print(grid[0][0][m])