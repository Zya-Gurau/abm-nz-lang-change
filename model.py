import math
import random
from network_setup import *
import Agent
from datetime import datetime
import matplotlib.pyplot as plt
from numba import jit, cuda
import numpy as np

#ADD CHILDREN
def new_generation(agents, lam, h):
    for agent in agents:
        if agent.isAdult == True:
            #remove current adult
            agents.remove(agent)
        else:
            #make adult
            agent.isAdult = True
            agent.lamb = agent.lamb * (1/200)
    #create new children
    for agent in agents:
        if agent.isAdult == True:
            new_child = Agent(lam, h, agent.ideolect, 0, False)
            agents.append(new_child)
    pass

def agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, weights):
    global PROPORTION_SPEAKING_A_FIFTY
    one_utterance = agent_one.reproduction()
    two_utterance = agent_two.reproduction()

    agent_one.retention(one_utterance, two_utterance, agent_two, weights)

    if agent_one.id not in set_speaking and agent_one.ideolect[0] >= 1:
        set_speaking.add(agent_one.id)
        prop_speaking += 1

    agent_two.retention(two_utterance, one_utterance, agent_one, weights)

    if agent_two.id not in set_speaking and agent_two.ideolect[0] >= 1:
        set_speaking.add(agent_two.id)
        prop_speaking += 1
    return prop_speaking


def choose_agents(agents):
    agent_list = random.sample(agents, 2)
    first_agent = agent_list[0]
    second_agent = agent_list[1]
    return first_agent, second_agent

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS, NUM_SIMULATIONS):
    set_x = []
    set_y = []
    max_x = set()
    for i in range(0, NUM_SIMULATIONS):
        x = []
        y = []
        cur_x = 0
        prop_speaking = math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
        agents, set_speaking = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE)
        while prop_speaking < NUM_AGENTS:
            
            agent_one, agent_two = choose_agents(agents)
            prop_speaking = agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, WEIGHTS)
            x.append(cur_x)
            y.append(prop_speaking)
            max_x.add(cur_x)
            cur_x+=1
        set_x.append(x)
        set_y.append(y)
    mean_x_axis = [i for i in range(max(max_x))]
    ys_interp = [np.interp(mean_x_axis, set_x[i], set_y[i]) for i in range(len(set_x))]
    mean_y_axis = np.mean(ys_interp, axis=0)
    for i in range(0, len(set_x)):
        plt.plot(set_x[i], set_y[i])
    plt.plot(mean_x_axis, mean_y_axis)
    #plt.plot(data)
    plt.show() 
    
  
