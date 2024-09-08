import math
from Agent import *
import numpy as np

def get_model_agents(h, lam, num, init):
    agents = []
    set_speaking = set()

    #adults
    for i in range(0, math.floor(num*init)):
        agent = Agent(lam * (1/200), h, [1, 0], i, True)
        agents.append(agent)
        set_speaking.add(agent.id)

    for i in range(math.floor(num*init), num):
        agent = Agent(lam * (1/200), h, [0, 1], i, True)
        agents.append(agent)

    #children
    for i in range(0, math.floor(num*init)):
        agent = Agent(lam, h, [1, 0], i, False)
        agents.append(agent)
        set_speaking.add(agent.id)

    for i in range(math.floor(num*init), num):
        agent = Agent(lam, h, [0, 1], i, False)
        agents.append(agent)
        
    
    return agents, set_speaking

