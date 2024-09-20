import math
from Agent import *
import numpy as np

MAX_ID = 0

def get_model_agents(h, lam, num, init, use_gen, num_child):
    global MAX_ID
    agents = []
    set_speaking = set()
    
    if use_gen == True:
        #Adults
        for i in range(0, math.floor(num*init)):
            agent = Agent(lam * (1/200), h, [1, 0], MAX_ID, True)
            agents.append(agent)
            set_speaking.add(agent)
            MAX_ID+=1

        for i in range(math.floor(num*init), num):
            agent = Agent(lam * (1/200), h, [0, 1], MAX_ID, True)
            agents.append(agent)
            MAX_ID+=1

        #children
        for i in range(0, math.floor(num*init)*num_child):
            agent = Agent(lam, h, [1, 0], MAX_ID, False)
            agents.append(agent)
            set_speaking.add(agent)
            MAX_ID+=1

        for i in range(math.floor(num*init)*num_child, num*num_child):
            agent = Agent(lam, h, [0, 1], MAX_ID, False)
            agents.append(agent)
            MAX_ID+=1
    else:
        #children
        for i in range(0, math.floor(num*init)):
            agent = Agent(lam, h, [1, 0], MAX_ID, False)
            agents.append(agent)
            set_speaking.add(agent)
            MAX_ID+=1

        for i in range(math.floor(num*init), num):
            agent = Agent(lam, h, [0, 1], MAX_ID, False)
            agents.append(agent)
            MAX_ID+=1
    print('completed set up')    
    print(MAX_ID)
    return agents, set_speaking

