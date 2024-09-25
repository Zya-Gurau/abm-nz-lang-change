import time

def get_average_a(agents, num_child, num_agents):
    cur = 0
    for agent in agents:
        cur += agent.ideolect[0]
    return round(cur / len(agents), 3)

def get_average_props(data):
    start_time = time.time()
    gen1 = []
    gen2 = []

    for sim in data:
        gen1.append(sim[0])
        print("sim one!!")
        print(sim[0])

        gen2.append(sim[1])
        print("sim Two!!")
        print(sim[1])

    # gen 1 average
    av_gen1 = []
    
    for i in range(0,len(gen1[0])):
        av_agent = []
        for gen in gen1:
            av_agent.append(gen[i])
        print("Gen One Agents " + str(i) + ":")
        for agent in av_agent:
            print(agent)
        av_gen1.append(get_agents_average(av_agent))
        
    # gen 2 average
    av_gen2 = []
    for i in range(0, len(gen2[0])):
        av_agent = []
        for gen in gen2:
            av_agent.append(gen[i])
        print("Gen Two Agents " + str(i) + ":")
        for agent in av_agent:
            print(agent)
        av_gen2.append(get_agents_average(av_agent))
    endtime = time.time()
    print("Data Processing took: " + str(endtime - start_time) + " seconds")
    return av_gen1, av_gen2
        

    
def get_agents_average(data):
    idiolect1 = 0
    idiolect2 = 0
    for agent in data:
        idiolect1 += agent[1][0]
        idiolect2 += agent[1][1]
    av_1 = round(idiolect1 / len(data), 3)
    av_2 = round(idiolect2 / len(data), 3)
    new_agent = (data[0][0], av_1, data[0][2])
    return new_agent

    
