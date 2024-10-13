import math
import random
from network_setup import *
from Agent import *
import numpy as np
from data_processing import *
import csv

def write_data(av_gen1, av_gen2, mean_y_axis):
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

def format_agents_csv(agents):
    format_agents = []
    for agent in agents:
        c_a = ''
        if agent.isAdult == True:
            c_a = 'Adult'
        else:
            c_a = 'Child'

        id = agent.id
        idie = agent.ideolect
        format_agents.append((int(id), list(idie), c_a))
    return format_agents

def new_generation(agents, lam, h, num_child):
    MAX_ID = len(agents)
    new_agents = []

    #remove current adults
    for agent in agents:
        if agent.isAdult == False:
            new_agents.append(agent)
            
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

    return new_agents

def agent_interaction(agent_one, agent_two, weights):
    one_utterance = agent_one.reproduction()
    two_utterance = agent_two.reproduction()

    agent_one.retention(one_utterance, two_utterance, agent_two, weights)
    agent_two.retention(two_utterance, one_utterance, agent_one, weights)

def choose_agents(agents):
    agent_list = random.sample(agents, 2)
    first_agent = agent_list[0]
    second_agent = agent_list[1]
    return first_agent, second_agent

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS, NUM_SIMULATIONS, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT):
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
        x = []
        y = []
        speaker_data = []
        cur_x = 0

        agents = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, USE_GEN_REPLACE, NUM_CHILD_PER_ADULT)
        
        while gens_complete < 2:

            if USE_GEN_REPLACE:
                num_interactions += 1
                if num_interactions % ((((1.3 * (10 ** 5)) / 50) * 25) * len(agents) ) == 0:
                    gens_complete+=1

                    speaker_data.append(format_agents_csv(agents))
                    
                    gens.append(num_interactions)
                    agents = new_generation(agents, LAMBDA, H, NUM_CHILD_PER_ADULT)
                    print("NEW GENERATION")
                    num_interactions = 0

            agent_one, agent_two = choose_agents(agents)
            agent_interaction(agent_one, agent_two, WEIGHTS)
            if num_interactions % (((1.3 * (10 ** 5)) / 50) * len(agents) ) == 0: #get data every 6 months
                year += 1
                print("data added! for year: " + str(year))
                years.append(cur_x)
                x.append(year)

                y.append(get_average_a(agents, NUM_AGENTS, NUM_CHILD_PER_ADULT))

                max_x.add(cur_x)
            
            cur_x+=1

        print("SIM COMPLETE")

        csv_data.append(speaker_data)
        set_x.append(x)
        set_y.append(y)

    if USE_GEN_REPLACE == True: 
        av_gen1, av_gen2 = get_average_props(csv_data)

    mean_y_axis = np.mean(set_y, axis=0)
    
    endtime = time.time()

    print("Model took " + str(endtime - starttime) + " seconds to run")

    write_data(av_gen1, av_gen2, mean_y_axis)
    
  
