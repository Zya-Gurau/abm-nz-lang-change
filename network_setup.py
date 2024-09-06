import math
from Agent import *
import numpy as np

def get_model_agents(h, lam, num, init):
    agents = []
    set_speaking = set()

    #children
    for i in range(0, math.floor(num*init)):
        agent = Agent(lam, h, [1, 0], i)
        agents.append(agent)
        set_speaking.add(agent.id)

    for i in range(math.floor(num*init), num):
        agent = Agent(lam, h, [0, 1], i)
        agents.append(agent)
        
    
    return agents, set_speaking

