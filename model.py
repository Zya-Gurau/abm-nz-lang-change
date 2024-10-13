import random
from network_setup import *
from Agent import *
import numpy as np
from data_processing import *
import csv

#"Magic numbers" for specifc year values in the simulation
TWENTY_FIVE_YEARS = (((1.3 * (10 ** 5)) / 50) * 25)
ONE_YEAR = ((1.3 * (10 ** 5)) / 50)

def write_data(av_gen1, av_gen2, mean_y_axis):
    """
        takes the average reproduction probabilities for each speaker in generation one and two 
        over all simulations as well as the average reproduction probability for the population
        over time.

        Writes the given data to three ".csv" files
    """

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
    """
        Takes a list of agents and formats them for data processing.
    """

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
    """
        Carries out generational replacment ona population of agents.
        First removes all current adult speakers, Next age up current child speakers
        by changing their lambda value. Finally create new child speakers for each adult 
        speaker. Child ideolect is based of parent ideolect.

        Returns a new list of agents.

    """

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
    """
        Caries out an interaction between two agents.
    """

    #Create utterances
    one_utterance = agent_one.reproduction()
    two_utterance = agent_two.reproduction()

    #Modify reproduction probabilities based on created utterences
    agent_one.retention(one_utterance, two_utterance, weights)
    agent_two.retention(two_utterance, one_utterance, weights)

def choose_agents(agents):
    """
        Choose two agents at random for the population.
        Assumes flat network structure.
    """

    agent_list = random.sample(agents, 2)
    first_agent = agent_list[0]
    second_agent = agent_list[1]
    return first_agent, second_agent

def setup_model(NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, H, LAMBDA, WEIGHTS, NUM_SIMULATIONS, NUM_CHILD_PER_ADULT):
    """
        Sets up and runs a number of simulations and writes data to files. 
        Parameters given are a number of config data points. 
        
        Each simulation runs for two generations (50 years)
    """

    starttime = time.time()
    set_y = []
    csv_data = []
    for i in range(0, NUM_SIMULATIONS):
        year = 0
        num_interactions = 0
        gens_complete = 0
        y = []
        speaker_data = []

        #Agents are created with a given h and lambd.
        #Child to Adult ratio is also provided to the function
        agents = get_model_agents(H, LAMBDA, NUM_AGENTS, INITIAL_VARIANT_OCCURENCE, NUM_CHILD_PER_ADULT)
        
        #If simulation is still running
        while gens_complete < 2:
            #Carry out one round of the simulation 
            num_interactions += 1

            #Check if generational replacement should occur (every twenty five years)
            if num_interactions % (TWENTY_FIVE_YEARS * len(agents)) == 0:
                gens_complete+=1
                #collect data at the end of a generation
                speaker_data.append(format_agents_csv(agents))
                #get new population after replacement 
                agents = new_generation(agents, LAMBDA, H, NUM_CHILD_PER_ADULT)
                print("NEW GENERATION")
                num_interactions = 0

            #choose agents 
            agent_one, agent_two = choose_agents(agents)
            #interaction between the two agents
            agent_interaction(agent_one, agent_two, WEIGHTS)

            #get data every year
            if num_interactions % (ONE_YEAR * len(agents)) == 0: 
                year += 1
                print("data added! for year: " + str(year))

                y.append(get_average_a(agents))

        print("SIM COMPLETE")
        #collect data for this simualtion
        csv_data.append(speaker_data)
        set_y.append(y)

    #get average data over every simulation
    av_gen1, av_gen2 = get_average_props(csv_data)
    mean_y_axis = np.mean(set_y, axis=0)
    
    endtime = time.time()
    print("Model took " + str(endtime - starttime) + " seconds to run")
    #write data 
    write_data(av_gen1, av_gen2, mean_y_axis)
    
  
