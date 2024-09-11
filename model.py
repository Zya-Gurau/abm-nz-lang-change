import math
import random
from network_setup import *
from Agent import *
from datetime import datetime
import matplotlib.pyplot as plt
from numba import jit, cuda
import numpy as np

def new_generation(agents, lam, h, set_speaking, prop_speaking, num_child):
    new_agents = []

    #remove current adults
    for agent in agents:
        if agent.isAdult == False:
            new_agents.append(agent)
        #else:
            #if agent in set_speaking:
                #set_speaking.remove(agent)
            

    #make new adults
    for agent in new_agents:
        if agent.isAdult == False:
            agent.isAdult = True
            agent.lamb = agent.lamb * (1/200)

    #create new children
    for agent in new_agents:
        if agent.isAdult == True:
            for i in range(num_child):
                new_child = Agent(lam, h, agent.ideolect, 0, False)
                new_agents.append(new_child)
            #if agent in set_speaking:
                #set_speaking.add(new_child)

    return new_agents, prop_speaking

def agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, weights, THRESHHOLD):
    one_utterance = agent_one.reproduction()
    two_utterance = agent_two.reproduction()

    agent_one.retention(one_utterance, two_utterance, agent_two, weights)

    if agent_one not in set_speaking and agent_one.ideolect[0] >= THRESHHOLD:
        set_speaking.add(agent_one)
        prop_speaking += 1

    agent_two.retention(two_utterance, one_utterance, agent_one, weights)

    if agent_two not in set_speaking and agent_two.ideolect[0] >= THRESHHOLD:
        set_speaking.add(agent_two)
        prop_speaking += 1
    return prop_speaking


def choose_agents(agents):
    agent_list = random.sample(agents, 2)
    first_agent = agent_list[0]
    second_agent = agent_list[1]
    return first_agent, second_agent

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS, NUM_SIMULATIONS, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT, THRESHHOLD):
    set_x = []
    set_y = []
    max_x = set()
    for i in range(0, NUM_SIMULATIONS):
        num_interactions = 0
        finish = 0
        x = []
        y = []
        cur_x = 0
        
        if USE_GEN_REPLACE == True:
            prop_speaking = (NUM_CHILD_PER_ADULT + 1) *math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
            finish = (NUM_CHILD_PER_ADULT + 1) * NUM_AGENTS
        else:
            prop_speaking = math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
            finish = NUM_AGENTS

        agents, set_speaking = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT)
        
        while len(set_speaking) < len(agents):

            if USE_GEN_REPLACE:
                num_interactions += 1
                if num_interactions % ((1.3 * (10 ** 5)) * ((NUM_CHILD_PER_ADULT + 1) * NUM_AGENTS) /25 ) == 0:
                    
                    agents, prop_speaking = new_generation(agents, LAMBDA, H, set_speaking, prop_speaking, NUM_CHILD_PER_ADULT)
                    print("NEW GENERATION!!!")
                    print("Number of interactions: " + str(num_interactions))

            agent_one, agent_two = choose_agents(agents)
            prop_speaking = agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, WEIGHTS, THRESHHOLD)
            x.append(cur_x)
            y.append(len(set_speaking))
            max_x.add(cur_x)
            cur_x+=1

        print("SIM COMPLETE")
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
    
  
