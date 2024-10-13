import math
from Agent import *

MAX_ID = 0

def get_model_agents(h, lam, num, init, num_child):
    """
        Create initial population of agents.
        A number of adult speakers and child speakers based on a 
        provided ratio.

        init: (float) The initial occurence probabilty of variant A,
                        determines the proportion of speakers that use 
                        exclusively variant A.
    """

    global MAX_ID
    agents = []
    set_speaking = set()
    
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
        MAX_ID+=1

    for i in range(math.floor(num*init)*num_child, num*num_child):
        agent = Agent(lam, h, [0, 1], MAX_ID, False)
        agents.append(agent)
        MAX_ID+=1

    print('completed set up')    
    return agents

