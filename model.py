import math
import random
from network_setup import *
import Agent
from datetime import datetime
import matplotlib.pyplot as plt
from numba import jit, cuda

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

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS):
    data = []
    prop_speaking = math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
    agents, set_speaking = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE)

    print(prop_speaking)
    while prop_speaking < NUM_AGENTS:
        
        agent_one, agent_two = choose_agents(agents)
        prop_speaking = agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, WEIGHTS)
        data.append(prop_speaking)

    plt.plot(data)
    plt.show() 
    
  
