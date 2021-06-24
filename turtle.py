from scipy import stats
import random

def generate_grid():
    # Probability of finding diamonds at any location
    p_diamond = 0.3
    # Length of sides of grid
    m = 3
    
    # Generate blocks for 16x16x16 grid
    samples = []
    for i in range(0, m**3):
        samples.append(stats.bernoulli.rvs(p_diamond, 0))
    
    # Dimensions: 16 x 16 x 16
    grid = [[[0 for x in range(m)] for x in range(m)] for x in range(m)]
    # Insert samples into 3D grid array
    index = 0
    for i in range(0, m):
        for j in range(0, m):
            for k in range(0, m):
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
    if state[0] < m:
        state[0] += 1

def move_south(state, m):
    state[3] -= 1
    if state[0] > 0:
        state[0] -= 1

def move_east(state, m):
    state[3] -= 1
    if state[2] < m:
        state[2] += 1

def move_west(state, m):
    state[3] -= 1
    if state[2] > 0:
        state[2] -= 1

def move_down(state, m):
    state[3] -= 1
    if state[1] < m:
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
    gene_dir_pairs = []
    gene_act_pairs = []
    gene_num = 64
    pairs_dir_num = 6
    pairs_act_num = 1
    
    # Set seed
    random.seed()
    
    # Generate gene pairs for sensor direction sequence
    # 0 = Nothing, 1 = Diamonds, 2 = Wall
    for i in range(0, gene_num * pairs_dir_num):
        #genes_dir_pairs.append(stats.binom.rvs(2, 2/3, 0)) # Binomial dist for random nums
        genes_dir_pairs.append(random.randrange(0,2,1))     # Basic random numbers
    
    # Generate gene pairs for actions
    # 0 = North, 1 = South, 2 = East, 3 = West, 4 = Down, 5 = Up, 6 = Random
    for i in range(0, gene_num * pairs_act_num):
        genes_act_pairs.append(random.randrange(0,6,1))
    
    # Combine sensor direction sequence with action sequence for all genes
    for i in range(0, gene_num * (pairs_dir_num + pairs_act_num)):
        # Create single gene array within genes matrix
        genes.append([])
        # Append the first sensor direction bits of the genes
        for j in range(pairs_dir_num):
            genes[i].append(genes_dir_pairs[j + (i * pairs_dir_num)])   # Index + offset (ex. if i = 3 and j = 0, append 0 + (3 * 6) = 18th direction pair
        # Append the action pair(s)
        for k in range(pairs_act_num):
            genes[i].append(genes_act_pairs[k + (i * pairs_act_num)])   # Same concept
    return genes

# Simulation Function
def simulate_turtle(grid, grid_length, genes):
    score = 0
    # Set battery life
    life = 205
    # Drop turtle in random place
    random.seed()
    start_x = random.randrange(0,15,1)
    start_z = random.randrange(0,15,1)
    start_y = random.randrange(0,15,1)
    state = [start_x, start_z, start_y, life]
    
    while state[3] > 0:
        # If current position is on diamond, add score
        if grid[state[0], state[1], state[2]] == 1:
            score += 1
        # Initialize sensor data
        # [NORTH, SOUTH, EAST, WEST, DOWN, UP]
        sensors = [0,0,0,0,0,0]
        # Get senses, take appropriate course of action (TODO)
    

# Mining Turtle Class
class Turtle:
    species = "Turtle"
    
    def __init__(self, name):
        self.name = name
        self.dna = create_genes()
        self.score = 0
    
    def simulate(self):
        self.score = simulate_turtle(self.dna)

grid = generate_grid()
print(grid)

# Assuming m x m x m grid:

# In range:
#print(grid[0][0][m-1])

# Not in range:
#print(grid[0][0][m])