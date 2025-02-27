import pygame
import random
import math
from math import e
from collections import deque

# Initialize Pygame
pygame.init()

REC_LIMIT = 500

# Screen dimensions
WIDTH, HEIGHT = 600, 400
TILE_SIZE = 40
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rescue the Hostage - Local Search")

# Colors
WHITE = (240, 248, 255)
RED = (255, 69, 0)      # Hostage color
BLUE = (30, 144, 255)   # Player color
LIGHT_GREY = (211, 211, 211) # Background grid color
FLASH_COLOR = (50, 205, 50) # Victory flash color
BUTTON_COLOR = (50, 205, 50) # Button color
BUTTON_TEXT_COLOR = (255, 255, 255) # Button text color

# Load images for player, hostage, and walls
player_image = pygame.image.load("AI1.png")  
hostage_image = pygame.image.load("AI2.png")  
wall_images = [
    pygame.image.load("AI3.png"),
    pygame.image.load("AI4.png"),
    pygame.image.load("AI5.png")
]

# Resize images to fit the grid
wall_images = [pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) for img in wall_images]
player_image = pygame.transform.scale(player_image, (TILE_SIZE, TILE_SIZE))
hostage_image = pygame.transform.scale(hostage_image, (TILE_SIZE, TILE_SIZE))

# Constants for recent positions
MAX_RECENT_POSITIONS = 10
GENERATION_LIMIT = 50
MUTATION_RATE = 0.1
temperature = 100  # Initial temperature
cooling_rate = 0.99

# Function to generate obstacles
def generate_obstacles(num_obstacles):
    obstacles = []
    while len(obstacles) < num_obstacles:
        new_obstacle = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        if new_obstacle not in obstacles:  # Make sure obstacles are not overlapping
            obstacles.append(new_obstacle)
    obstacle_images = [random.choice(wall_images) for _ in obstacles]
    return obstacles, obstacle_images

# Function to start a new game
def start_new_game():
    global temperature
    temperature = 100
    global player_pos, hostage_pos, recent_positions, obstacles, obstacle_images
    obstacles, obstacle_images = generate_obstacles(20)
    recent_positions = []

    # Generate player and hostage positions with a larger distance
    while True:
        player_pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        hostage_pos = (random.randint(0, COLS-1), random.randint(0, ROWS-1))
        distance = math.dist(player_pos, hostage_pos)
        if distance > 8 and player_pos not in obstacles and hostage_pos not in obstacles:
            break
def calculate_distance(player , hostage):
    return (hostage[0] - player[0]) ** 2 +  (hostage[1] - player[1]) **2
# Function to move the player closer to the hostage using Hill Climbing algorithm
def hill_climbing(player, hostage, obstacles):
    #todo 
    allowed_moves = [(player[0] ,player[1] + 1 ) ,(player[0]+1 ,player[1] ) ,(player[0] ,player[1] - 1 ) ,(player[0] - 1 ,player[1] )]
    max = player
    for i in range (len(allowed_moves)):
        if (allowed_moves[i] in obstacles) or (allowed_moves[i][0] < 0 or allowed_moves[i][0]>= COLS or allowed_moves[i][1] < 0 or allowed_moves[i][1]>= ROWS) :
            continue
        if calculate_distance (max , hostage) > calculate_distance(allowed_moves[i] , hostage):
            max = allowed_moves[i]
    
    return max

    

# Function for Simulated Annealing

def simulated_annealing(player, hostage, obstacles):
    def acceptance_probability(old_cost, new_cost, temp):
        haha = e** ((old_cost - new_cost)/ temp)
        
        haha *=10000
        hehe = random.randint(0 , 10000)

        print (f"chosen number : {hehe} , prob : {haha}")
        return  hehe<= haha
    global temperature , cooling_rate 
    temperature *= cooling_rate
    allowed_moves = [(player[0] ,player[1] + 1 ) ,(player[0]+1 ,player[1] ) ,(player[0] ,player[1] - 1 ) ,(player[0] - 1 ,player[1] )]
    a = []
    for i in range (len(allowed_moves)):
        if (allowed_moves[i] in obstacles) or (allowed_moves[i][0] < 0 or allowed_moves[i][0]>= COLS or allowed_moves[i][1] < 0 or allowed_moves[i][1]>= ROWS) :
            continue
        a.append(allowed_moves[i])
    random_choice = a[random.randint(0 , len(a) - 1)]
    if calculate_distance(player , hostage) > calculate_distance(random_choice , hostage):
        return random_choice
    else:
        if acceptance_probability( calculate_distance(player , hostage) , calculate_distance(random_choice , hostage) , temperature):
            return random_choice
        else:
            return player

    
    # Acceptance probability function

        
#def random_dfs():

class genome:
    def __init__(self , player_pos):
        self.visited = set()
        self.corrupts = set()
        self.path = []
        self.value = 0
        self.path.append(player_pos)


# Function for Genetic Algorithm
def genetic_algorithm(player, hostage, obstacles):
    population_size = 20
    generations = 50
    
    # Fitness function
    def fitness(individual):
        value = 10 * len(individual.corrupts)
        value += len(individual.path)
        individual.value = 10000 / value 

    def return_choice_genetic(choice , array):
        for i in range(len(array)):
            if choice <= array[i].value:
                return i
            choice -= array[i].value
        return len(array) - 1

    def return_choice(choice , array):
        for i in range(len(array)):
            if choice <= array[i]:
                return i
            choice -= array[i]
        return len(array) - 1


    # Generate random population
    def generate_population( gene ):
        if gene.path[len(gene.path) - 1] == hostage:
            return True
        gene.visited.add (gene.path[len(gene.path) - 1])
        allowed_moves = [ (gene.path[len(gene.path) - 1][0] ,gene.path[len(gene.path) - 1][1] + 1 ) 
        ,(gene.path[len(gene.path) - 1][0] + 1 ,gene.path[len(gene.path) - 1][1] ) 
        ,(gene.path[len(gene.path) - 1][0] ,gene.path[len(gene.path) - 1][1] - 1 ) 
        ,(gene.path[len(gene.path) - 1][0] - 1 ,gene.path[len(gene.path) - 1][1] )]
        a = []
        prob = []
        sum_prob = 0.0
        for i in range (len(allowed_moves)):
            if allowed_moves[i][0] < 0 or allowed_moves[i][0]>= COLS or allowed_moves[i][1] < 0 or allowed_moves[i][1]>= ROWS or allowed_moves[i] in gene.visited :
                continue
            delta = calculate_distance(player , hostage) - calculate_distance(allowed_moves[i] , hostage)
            
            prob.append(delta if delta > 0 else abs(delta)/2)
            sum_prob += delta if delta > 0 else abs(delta)/2
            a.append(allowed_moves[i])
        if len(a) == 0:
            return False
        sum_prob = math.floor (sum_prob)
        choice =return_choice( random.randint(0 , math.floor(sum_prob)) , prob )
        #print(a)
        #print(choice)
        #print (len(prob))
        gene.path.append (a[choice])
        if a[choice] in obstacles:
            gene.corrupts.add (a[choice])    
        return generate_population(gene)

    # Crossover function
    def crossover(parent1, parent2):
        if parent1 == parent2:
            return None , None
        inter = parent1.visited.intersection( parent2.visited)
        if len(inter) == 0:
            return None , None
        choice = random.choice(tuple(inter))
        if choice == player:
            return None , None
        new_gene = genome(player)
        new_gene2 = genome(player)
        flag = False
        print (parent1.path)
        print (parent2.path)
        print (choice)
        second_check_point= 0
        for i in range(1 , len(parent1.path)):
            if parent1.path[i] == choice:
                second_check_point = i
                break
            new_gene.path.append(parent1.path[i])
            new_gene.visited.add(parent1.path[i])
        new_gene.corrupts = new_gene.visited.intersection(parent1.corrupts)

        flag = False
        for i in range(1 , len(parent2.path)):
            if parent2.path[i] == choice and not flag:
                print(parent2.path[i])
                flag = True
            if not flag:
                new_gene2.path.append(parent2.path[i])
                new_gene2.visited.add(parent2.path[i])
                continue
            new_gene.path.append(parent2.path[i])
            new_gene.visited.add(parent2.path[i])

        new_gene2.corrupts = new_gene2.visited.intersection(parent2.corrupts)
        new_gene.corrupts = new_gene.corrupts.union( new_gene.visited.intersection(parent2.corrupts))

        while second_check_point < len(parent1.path):
            new_gene2.path.append(parent1.path[second_check_point])
            new_gene2.visited.add(parent1.path[second_check_point])
            second_check_point+=1
        new_gene2.corrupts = new_gene2.corrupts.union( new_gene2.visited.intersection(parent1.corrupts))

        return new_gene , new_gene2

    # Mutation function
    def mutate(individual):
        rec_counter = 0
        def find_new_path(gene , end_lies_here):
            nonlocal rec_counter
            rec_counter += 1
            if rec_counter > REC_LIMIT :
                return False
            if gene.path[len(gene.path) - 1] == hostage or (gene.path[len(gene.path) - 1] in end_lies_here and gene.path[len(gene.path) - 1] not in gene.visited):
                return True
            gene.visited.add (gene.path[len(gene.path) - 1])
            allowed_moves = [ (gene.path[len(gene.path) - 1][0] ,gene.path[len(gene.path) - 1][1] + 1 ) 
            ,(gene.path[len(gene.path) - 1][0]+1 ,gene.path[len(gene.path) - 1][1] ) 
            ,(gene.path[len(gene.path) - 1][0] ,gene.path[len(gene.path) - 1][1] - 1 ) 
            ,(gene.path[len(gene.path) - 1][0] - 1 ,gene.path[len(gene.path) - 1][1] )]
            a = []
            prob = []
            sum_prob = 0.0
            for i in range (len(allowed_moves)):
                if allowed_moves[i][0] < 0 or allowed_moves[i][0]>= COLS or allowed_moves[i][1] < 0 or allowed_moves[i][1]>= ROWS or allowed_moves[i] in gene.visited :
                    continue
                delta = calculate_distance(player , hostage) - calculate_distance(allowed_moves[i] , hostage)

                prob.append(delta if delta > 0 else abs(delta)/2)
                sum_prob += delta if delta > 0 else abs(delta)/2
                a.append(allowed_moves[i])
            if len(a)== 0:
                temp = gene.path.pop()
                gene.visited.remove(temp)
                gene.corrupts.discard(temp)
                return find_new_path(gene , end_lies_here)
                #return False
            sum_prob = math.floor (sum_prob)
            choice =return_choice( random.randint(0 , int(sum_prob)) , prob )
            gene.path.append (a[choice])
            if a[choice] in obstacles:
                gene.corrupts.add(a[choice]) 
            if not find_new_path(gene , end_lies_here):
                flag = True
                while flag:
                    #print (gene.path)
                    if len(gene.path) == 0:
                        return False
                    temp = gene.path.pop()
                    #temp = gene.path.pop()
                    #print (temp)
                    gene.visited.discard(temp)
                    gene.corrupts.discard(temp)
                    if find_new_path(gene , end_lies_here):
                        return True
            else:
                return True

        if len(individual.corrupts) == 0:
            return None
        gene = genome(player)
        choice = random.choice(tuple(individual.corrupts))
        print(choice)
        i = 1
        while i < len(individual.path):
            if choice == individual.path[i]:
                if individual.path[i][1] - individual.path[i - 1][1] == 0:
                    haha = random.randint(0 , 1)
                    if haha == 1:
                        if individual.path[i - 1][1] < COLS - 1:
                            gene.path.append((individual.path[i - 1][0] , individual.path[i - 1][1] + 1))
                            gene.visited.add((individual.path[i - 1][0] , individual.path[i - 1][1] + 1))
                        else:
                            gene.path.append((individual.path[i - 1][0] , individual.path[i - 1][1] - 1))
                            gene.visited.add((individual.path[i - 1][0] , individual.path[i - 1][1] - 1))
                    else:
                        if individual.path[i - 1][1] > 0: 
                            gene.path.append((individual.path[i - 1][0] , individual.path[i - 1][1] - 1))
                            gene.visited.add((individual.path[i - 1][0] , individual.path[i - 1][1] - 1))
                        else:
                            gene.path.append((individual.path[i - 1][0] , individual.path[i - 1][1] + 1))
                            gene.visited.add((individual.path[i - 1][0] , individual.path[i - 1][1] + 1))
                else:
                    haha = random.randint(0 , 1)
                    if haha == 1:
                        if individual.path[i - 1][0] < ROWS - 1:
                            gene.path.append((individual.path[i - 1][0] + 1 , individual.path[i - 1][1] ))
                            gene.visited.add((individual.path[i - 1][0] + 1 , individual.path[i - 1][1] ))
                        else:
                            gene.path.append((individual.path[i - 1][0] - 1 , individual.path[i - 1][1]))
                            gene.visited.add((individual.path[i - 1][0] - 1 , individual.path[i - 1][1]))
                    else:
                        if individual.path[i - 1][0] > 0:
                            gene.path.append((individual.path[i - 1][0] - 1 , individual.path[i - 1][1]))
                            gene.visited.add((individual.path[i - 1][0] - 1 , individual.path[i - 1][1]))
                        else:
                            gene.path.append((individual.path[i - 1][0] + 1 , individual.path[i - 1][1] ))
                            gene.visited.add((individual.path[i - 1][0] + 1 , individual.path[i - 1][1] ))
                print("path so far : ")
                print (gene.path)
                if not find_new_path(gene , individual.visited):
                    return None
                print("path after finding new path : ")
                print (gene.path)
                while gene.path[len(gene.path) - 1] != individual.path[i]:
                    i+=1
                    if len(individual.path ) == i:
                        break
            else:
                gene.path.append(individual.path[i])
                gene.visited.add(individual.path[i])
            i+=1
            
        gene.corrupts = gene.corrupts.union(gene.visited.intersection(individual.corrupts))
        
        return gene

    def jump_check(gene):
        if gene == None:
            return False
        for i in range (1 , len(gene.path)):
            if calculate_distance(gene.path[i] , gene.path[i - 1]) != 1:
                return True
        return False

    all_genes = []
    sum_fitness = 0.0
    for i in range(20):
        new_gene = genome(player)
        if not generate_population(new_gene):
            i-=1
            continue
        fitness(new_gene)
        sum_fitness += new_gene.value
        all_genes.append(new_gene)

    sum_fitness = math.floor(sum_fitness)

    counter = 0
    while len (all_genes[0].corrupts) != 0 or counter < 100: #and counter > 50: 
        #print("highest:")
        #print(all_genes[0].path)
        #print(all_genes[0].corrupts)
        if (counter > 1000) :
            break
        #print (counter)
        for i in range(generations):
            choice1 = return_choice_genetic(random.randint(0 , sum_fitness) , all_genes)
            choice2 = return_choice_genetic(random.randint(0 , sum_fitness) , all_genes)
            new_gene1 , new_gene2 = crossover(all_genes[choice1] , all_genes[choice2])
            if jump_check(new_gene1):
                print ("fucked up in crossover")
                print(new_gene1.path)
                exit()
            if jump_check(new_gene2):
                print ("fucked up in crossover 2")
                print(new_gene2.path)
                exit()
            if new_gene1 == None or new_gene2 == None:
                i-=1
                continue
            fitness(new_gene1)
            fitness(new_gene2)
            all_genes.append(new_gene1)
            all_genes.append(new_gene2)

        #for g in  all_genes:
        #    if jump_check(g):
        #        print ("fucked up")
            
        for i in range(math.floor(population_size * MUTATION_RATE)):
            choice1 = return_choice_genetic(random.randint(0 , sum_fitness) , all_genes)
            #print(f"{i} ,{choice1} ")
            #print (f"before mutate :")
            #print(all_genes[choice1].path)
            #print(all_genes[choice1].corrupts)
            new_gene = mutate(all_genes[choice1])
            if new_gene == None:
                i-=1
                continue
            #print (f"after mutate :")
            #print(new_gene.path)
            #print(new_gene.corrupts)
            if jump_check(new_gene):
                print ("fucked up in mutate")
                exit()
            #print ("mutation tick!")
            for i in range (len (new_gene.path) - 1):
                if new_gene.path[i] in obstacles and new_gene.path[i] not in new_gene.corrupts:
                    print("corrupt error")
                    new_gene.corrupts.add(new_gene.path[i])
                if new_gene.path[i] not in new_gene.visited:
                    new_gene.visited.add(new_gene.path[i] )
                    print("error in visited")
                    
            fitness(new_gene)
            all_genes.append(new_gene)
        all_genes = sorted (all_genes , key=lambda x: x.value , reverse=True)[:population_size]
        counter +=1
    print(counter)

    print (all_genes[0].path)
    print (all_genes[0].corrupts)
    print (obstacles)
    return all_genes[0]
    

#Objective: Check if the player is stuck in a repeating loop.
def in_loop(recent_positions, player):
    return False
    return player in recent_positions

#Objective: Make a random safe move to escape loops or being stuck.
def random_move(player, obstacles):
    allowed_moves = [(player[0] ,player[1] + 1 ) ,(player[0]+1 ,player[1] ) ,(player[0] ,player[1] - 1 ) ,(player[0] - 1 ,player[1] )]
    a = []
    for i in range (len(allowed_moves)):
        if (allowed_moves[i] in obstacles) or (allowed_moves[i][0] < 0 or allowed_moves[i][0]>= COLS or allowed_moves[i][1] < 0 or allowed_moves[i][1]>= ROWS) :
            continue
        a.append(allowed_moves[i])
    return a[random.randint(0 , len(a) - 1)]

#Objective: Update the list of recent positions. 
def store_recent_position(recent_positions, new_player_pos, max_positions=MAX_RECENT_POSITIONS):
    
    recent_positions.append(new_player_pos)
#    if new_player_pos not in recent_positions:
#        recent_positions.append(new_player_pos)

# Function to show victory flash
def victory_flash():
    for _ in range(5):
        screen.fill(FLASH_COLOR)
        pygame.display.flip()
        pygame.time.delay(100)
        screen.fill(WHITE)
        pygame.display.flip()
        pygame.time.delay(100)

# Function to show a button and wait for player's input
def show_button_and_wait(message, button_rect):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, BUTTON_TEXT_COLOR)
    button_rect.width = text.get_width() + 20
    button_rect.height = text.get_height() + 10
    button_rect.center = (WIDTH // 2, HEIGHT // 2)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    screen.blit(text, (button_rect.x + (button_rect.width - text.get_width()) // 2,
                       button_rect.y + (button_rect.height - text.get_height()) // 2))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# Function to get the algorithm choice from the player
def get_algorithm_choice():
    print("Choose an algorithm:")
    print("1: Hill Climbing")
    print("2: Simulated Annealing")
    print("3: Genetic Algorithm")

    while True:
        choice = input("Enter the number of the algorithm you want to use (1/2/3): ")
        if choice == "1":
            return hill_climbing
        elif choice == "2":
            return simulated_annealing
        elif choice == "3":
            return genetic_algorithm
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
#function to show the path
def show_path(recent_positions):
    recorder = {}
    for i in  range (len(recent_positions)):
        if recent_positions[i] not in recorder:
            recorder[recent_positions[i]] = i
    i = len(recent_positions) - 1
    print(i)
    path = deque()
    while i >= 0:
        if recorder[recent_positions[i]] < i :
            i = recorder[recent_positions[i]]
        else:
            path.append(recent_positions[i])
            i-=1
    while len(path) != 0:
        screen.fill(WHITE)
        playyer_pos = path.pop()
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

        # Draw obstacles
        for idx, obs in enumerate(obstacles):
            obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(obstacle_images[idx], obs_rect)

        # Draw player
        player_rect = pygame.Rect(playyer_pos[0] * TILE_SIZE, playyer_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(player_image, player_rect)

        # Draw hostage
        hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(hostage_image, hostage_rect)
        pygame.display.flip()
        clock.tick(5)  # Lower frame rate for smoother performance

        # Check if player reached the hostage
    print("Hostage Rescued!")
    victory_flash()  # Show the victory flash
        

# Main game loop
running = True
clock = pygame.time.Clock()
start_new_game()
button_rect = pygame.Rect(0, 0, 0, 0)

# Get the algorithm choice from the player
chosen_algorithm = get_algorithm_choice()

if chosen_algorithm == genetic_algorithm:
    while running:
        gene = chosen_algorithm(player_pos, hostage_pos, obstacles)
        for player_pos in gene.path:
            screen.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the grid background
            for row in range(ROWS):
                for col in range(COLS):
                    rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

            # Draw obstacles
            for idx, obs in enumerate(obstacles):
                obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                screen.blit(obstacle_images[idx], obs_rect)

            # Draw player
            player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(player_image, player_rect)

            # Draw hostage
            hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(hostage_image, hostage_rect)

            # Check if player reached the hostage
            if player_pos == hostage_pos:
                print("Hostage Rescued!")
                victory_flash()  # Show the victory flash
                show_button_and_wait("New Game", button_rect)
                start_new_game()

            # Update the display
            pygame.display.flip()
            clock.tick(5)  # Lower frame rate for smoother performance
else:

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Perform the chosen algorithm step
        new_player_pos = chosen_algorithm(player_pos, hostage_pos, obstacles)

        # Check for stuck situations
        if chosen_algorithm != simulated_annealing or False:
            if new_player_pos == player_pos or in_loop(recent_positions, new_player_pos):
                # Perform a random move when stuck
                new_player_pos = random_move(player_pos, obstacles)

        # Update recent positions
        store_recent_position(recent_positions, new_player_pos)
        # Update player's position
        player_pos = new_player_pos

        # Draw the grid background
        for row in range(ROWS):
            for col in range(COLS):
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, LIGHT_GREY, rect, 1)

        # Draw obstacles
        for idx, obs in enumerate(obstacles):
            obs_rect = pygame.Rect(obs[0] * TILE_SIZE, obs[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            screen.blit(obstacle_images[idx], obs_rect)

        # Draw player
        player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(player_image, player_rect)

        # Draw hostage
        hostage_rect = pygame.Rect(hostage_pos[0] * TILE_SIZE, hostage_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(hostage_image, hostage_rect)

        # Check if player reached the hostage
        if player_pos == hostage_pos:
            print("Hostage Rescued!")
            victory_flash()  # Show the victory flash
            show_button_and_wait("See the final path", button_rect)
            recent_positions_copy = recent_positions.copy()
            #start_new_game()
            show_path(recent_positions_copy)
            show_button_and_wait("New Game", button_rect)
            start_new_game()

        # Update the display
        pygame.display.flip()
        clock.tick(5)  # Lower frame rate for smoother performance
pygame.quit()
