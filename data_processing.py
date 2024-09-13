import time
import pandas as pd

def get_average_props(data, num_agents, child_per_adult, num_sims):
    start_time = time.time()
    gen1 = []
    gen2 = []
    for sim in data:
        gen1.append(sim[0])
        gen2.append(sim[1])
    # gen 1 average
    av_gen1 = []
    for i in range(len(gen1[0])):
        av_agent = []
        for gen in gen1:
            av_agent.append(gen[i])
        av_gen1.append(get_agents_average(av_agent))
    # gen 2 average
    av_gen2 = []
    for i in range(len(gen2[0])):
        av_agent = []
        for gen in gen2:
            av_agent.append(gen[i])
        av_gen2.append(get_agents_average(av_agent))
    endtime = time.time()
    print("Data Processing took: " + str(endtime - start_time) + " seconds")
    return av_gen1, av_gen2
        

    
def get_agents_average(data):
    idiolect1 = 0
    idiolect2 = 0
    for agent in data:
        idiolect1 += agent[0][0]
        idiolect2 += agent[0][1]
    av_1 = round(idiolect1 / len(data), 2)
    av_2 = round(idiolect2 / len(data), 2)
    new_agent = (av_1, data[0][1])
    return new_agent

    
