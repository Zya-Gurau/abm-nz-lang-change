import math
import random
from network_setup import *
from Agent import *
import matplotlib.pyplot as plt
import numpy as np
from data_processing import *
import csv

def format_agents_csv(agents):
    format_agents = []
    for agent in agents:
        c_a = ''
        if agent.isAdult == True:
            c_a = 'Adult'
        else:
            c_a = 'Child'
        format_agents.append((agent.id, agent.ideolect, c_a))
    return format_agents

def new_generation(agents, lam, h, set_speaking, prop_speaking, num_child):
    MAX_ID = len(agents)
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
                new_child = Agent(lam, h, agent.ideolect, MAX_ID, False)
                new_agents.append(new_child)
                MAX_ID+=1
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

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS, NUM_SIMULATIONS, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT, THRESHHOLD, THREE_GEN_EXACT):
    starttime = time.time()
    set_x = []
    set_y = []
    max_x = set()
    gens = []
    years =[]
    csv_data = []
    for i in range(0, NUM_SIMULATIONS):
        year = 0
        num_interactions = 0
        gens_complete = 0
        finish = 0
        x = []
        y = []
        speaker_data = []
        cur_x = 0
        
        if USE_GEN_REPLACE == True:
            prop_speaking = (NUM_CHILD_PER_ADULT + 1) *math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
            finish = (NUM_CHILD_PER_ADULT + 1) * NUM_AGENTS
        else:
            prop_speaking = math.floor(NUM_AGENTS * INITIAL_VARIANT_OCCURENCE)
            finish = NUM_AGENTS

        agents, set_speaking = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT)
        
        #while len(set_speaking) < len(agents):
        while gens_complete < 2:

            if USE_GEN_REPLACE:
                num_interactions += 1
                if num_interactions % ((((1.3 * (10 ** 5)) / 50) * 25) * len(agents) ) == 0:
                    gens_complete+=1
                    speaker_data.append(format_agents_csv(agents))
                    gens.append(num_interactions)
                    agents, prop_speaking = new_generation(agents, LAMBDA, H, set_speaking, prop_speaking, NUM_CHILD_PER_ADULT)
                    print("NEW GENERATION!!!")
                    print("Number of interactions: " + str(num_interactions))
                    num_interactions = 0

            agent_one, agent_two = choose_agents(agents)
            prop_speaking = agent_interaction(agent_one, agent_two, prop_speaking, set_speaking, WEIGHTS, THRESHHOLD)
            if num_interactions % (((1.3 * (10 ** 5)) / 50) * len(agents) ) == 0: #get data every 6 months
                year += 1
                print("data added! for year: " + str(year))
                years.append(cur_x)
                x.append(cur_x)
                y.append(len(set_speaking))
                max_x.add(cur_x)
            
            cur_x+=1

        print("SIM COMPLETE")

        speaker_data.append(format_agents_csv(agents))
        csv_data.append(speaker_data)
        set_x.append(x)
        set_y.append(y)
        print(speaker_data)
    if USE_GEN_REPLACE == True: 
        av_gen1, av_gen2 = get_average_props(csv_data, NUM_AGENTS, NUM_CHILD_PER_ADULT, NUM_SIMULATIONS)
        print("GEN 1 AVERAGE:")
        print(av_gen1)
        print("GEN 2 AVERAGE:")
        print(av_gen2)
    
    #mean_x_axis = [i for i in range(max(max_x))]
    mean_x_axis = [i for i in range(50)]
    #ys_interp = [np.interp(mean_x_axis, set_x[i], set_y[i]) for i in range(len(set_x))]
    mean_y_axis = np.mean(set_y, axis=0)

    for gen in gens:
        plt.axvline(x = gen, color = 'b', label = 'new generation', alpha=0.3)
    for year in years:
        plt.axvline(x = year, color = 'g', label = 'new generation', alpha=0.3)

    #for i in range(0, len(set_x)):
        #plt.plot(set_x[i], set_y[i])

    plt.plot(mean_x_axis, mean_y_axis, color = 'b')
    print(mean_y_axis)

    plt.savefig('graph.png')
    
    endtime = time.time()
    print("Model took " + str(endtime - starttime) + " seconds to run")

    with open('gen_one.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["agent_id", "variant_prob", "age"])
        for agent in av_gen1:
            csvwriter.writerow([agent[0], agent[1], agent[2]])
    print("Wrote first")

    with open('gen_two.csv', 'w', newline='') as csvfile:
        csvwritertwo = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwritertwo.writerow(["agent_id", "variant_prob", "age"])
        for agent in av_gen2:
            csvwritertwo.writerow([agent[0], agent[1], str(agent[2])])
    print("Wrote second")

    with open('prop_speaking.csv', 'w', newline='') as csvfile:
        csvwriterthree = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csvwriterthree.writerow(["prop_speaking"])
        for item in mean_y_axis:
            csvwriterthree.writerow([item])
    print("Wrote third")
    
  
