import networkx as nx 
import argparse
import os
import random
import matplotlib.pyplot as plt

# command to check to see if the threshold is reached
def infection_threshold_reached(G, node, threshold):
    neighbors = list(G.neighbors(node))
    if not neighbors:  # avoid divide-by-zero
        return False

    # this gets the amount of nodes that have the infected flag set to true
    infected_count = sum(
        1 for nbr in neighbors 
        if G.nodes[nbr].get("infected", False)
    )
    # this is the check to see if it is enough
    return infected_count >= threshold * len(neighbors)

def main(argv=None):
    parser = argparse.ArgumentParser(description='Reading command lines')
    parser.add_argument('graph', help='graph file')
    parser.add_argument('--action', choices=['covid','cascade'], help='Either simulates a cascading effect through the network (e.g., information spread) or simulates the spread of a pandemic like COVID-19 across the network')
    parser.add_argument('--initiator', type=str, help='Choose the initial node(s) from which the action will start. Replace m with the specific node identifier(s) separated by commas')
    parser.add_argument('--threshold', type=str, help='Set the threshold value q (e.g., between 0 and 1) of the cascade effect.')
    parser.add_argument('--probability_of_infection',type=str,help='Set the probability of infection p of the infections')
    parser.add_argument('--probability_of_death',type=str, help='Set the probability q of death while infected')
    parser.add_argument('--lifespan',type=int,help='Define the lifespan l (e.g., a number of time steps or days) of the rounds')
    parser.add_argument('--shelter',type=str, help='Set the sheltering parameter s (e.g., a proportion or list of nodes that will be sheltered or protected from the infection).')
    parser.add_argument('--vaccination',type=str,help='Set the vaccination rate or proportion r (e.g., a number between 0 and 1) representing the proportion of the network that is vaccinated.')
    parser.add_argument('--interactive',action='store_true',help='Plot the graph and the state of the nodes for every round')
    parser.add_argument('--plot',action='store_true',help='Plot the number of new infections per day when the simulation completes')
    args = parser.parse_args(argv)

    if not args.graph.lower().endswith(".gml"):
        print(f"Error: Input file '{args.graph}' is not a .gml file.")
        exit()

    if not os.path.isfile(args.graph):
        print(f"Error: Input file '{args.graph}' does not exist.")
        exit()
    # load the graph from input .gml
    # graph will be an undirected graph object
    G = nx.read_gml(args.graph)
    
    if not args.action:
        print("No action given, please choose covid or cascade. Exiting program...")
        exit()

    if args.initiator:
        # The initiators of the cascade or infection
        begin = [int(x) for x in args.initiator.split(",")]
    
    #splitting up the 2 types of action
    if args.action == 'covid':
        #prob of infection
        if args.probability_of_infection:
            infect = float(args.probability_of_infection)
        else:
            print("Please provide a probability of infection with the --probability_of_infection argument. Exiting program...")
            exit()
        
        #prob of death 
        death = 0
        if args.probability_of_death:
            death = float(args.probability_of_death)
        
        #lifespan 
        if args.lifespan:
            lifespan = int(args.lifespan)
        else:
            print("Please provide a probability of lifespan with the --lifespan. Exiting program...")
            exit()
        
        #shelter: dynamically decides if a portion are sheltered if given a number between 0 and 1, if a list, then shelters the listed nodes.
        if args.shelter:
            #treat as a portion sheltered
            if not ',' in args.shelter and float(args.shelter) > 0 and float(args.shelter) < 1:
                shelter_ratio = float(args.shelter)
                number_sheltered = int(G.number_of_nodes() * shelter_ratio)
                uninfected = list(set(G.nodes) - set(begin))
                try: #if there's not enough people left, shelter the rest
                    sheltered = random.sample(uninfected, k=number_sheltered) #infected nodes can also be sheltered, so picks randomly from the whole pool
                except:
                    sheltered = list(uninfected)
            else: #treat as list of sheltered nodes
                sheltered = [int(num) for num in args.shelter.split(',')]

        #vaccination
        if args.vaccination:
            vacc = float(args.vaccination)
            if vacc < 0 or vacc > 1:
                print("Please provide a vaccination ratio between 0 and 1. Exiting program...")
                exit()

            number_vacc = int(G.number_of_nodes() * vacc)
            uninfected = list(set(G.nodes) - set(begin) - set(sheltered))
            try: #if there's not enough people left, just make all of the rest vaccinated
                vaccinated = random.sample(uninfected, k=number_vacc) #assuming infected nodes cannot be vaccinated already, so picks randomly from uninfected nodes
            except:
                vaccinated = list(uninfected)

        #begin running the rounds of the simulation
        infected = list(begin)
        new_infected = []
        recovered = []
        dead = []
        pos = nx.spring_layout(G)

        if args.plot:
            new_infections_count = [len(begin)]

        #labels for the color states
        print("Legend:\n"
              "Red      :   Infected\n"
              "Green    :   Recovered\n"
              "Black    :   Dead\n"
              "Yellow   :   Sheltered\n"
              "Blue     :   Vaccinated\n"
              "Lightgray:   Susceptible")
        for round in range(lifespan):
            # showing the updated graph with newly infected nodes
            if args.interactive:
                colors = [    "red" if n in infected
                    else "green" if n in recovered
                    else "black" if n in dead
                    else "yellow" if n in sheltered
                    else "blue"  if n in vaccinated
                    else "lightgray"
                    for n in G.nodes()
                ]
                nx.draw(G, pos, node_color=colors, with_labels=True)
                plt.show()
            
            # check to see if there are no more infected nodes
            if infected == []:
                print("Covid has died out, no more infected individuals.")
                break
            
            #This will go through each infected node and see if it infects each of its susceptible neighbors
            for sick_node in infected:
                neighbors = list(G[sick_node])
                for node in neighbors:
                    if (node in infected or 
                        node in recovered or 
                        node in dead or 
                        node in new_infected or
                        node in vaccinated or
                        node in sheltered):
                        continue
                    will_infect = random.random() < infect
                    if will_infect:
                        new_infected.append(node)

            #infection phase over, all recovered go back to being susceptible
            recovered = []
                
            #Now see which infected die to the illness, if not, they recover
            for sick_node in infected:
                die = random.random() < death
                if die:
                    dead.append(sick_node)
                else:
                    recovered.append(sick_node)
            
            # adding the amount of changed nodes on that step
            if args.plot:
                new_infections_count.append(len(new_infected))
            
            #add the newly infected as infected
            infected = list(new_infected)
            new_infected = []

        # plotting
        if args.plot:
            plt.figure()
            plt.plot(new_infections_count, marker='o')
            plt.xlabel("Round")
            plt.ylabel("New infections")
            plt.title("New infections per round")
            plt.grid(True)
            plt.xticks(range(len(new_infections_count)))
            plt.show()
            
    else:
        # Threshold is unique to cascade
        try:
            threshold = float(args.threshold)
        except:
            print("You need a threshold for a cascade")
            exit()
        # Setting the position of the nodes in the graph for -interactive
        pos = nx.spring_layout(G)
        # list to check to see if it changes 
        unInfected = list(G.nodes())
        # setting up intial nodes
        for i in begin:
            G.nodes[i]["infected"] = True
            unInfected.remove(i)
        # Our while loop is gonna run until nothing changes 
        changed = True

        # interactive graph with the intial infected as red
        if args.interactive:
            colors = ["red" if G.nodes[n].get("infected", False) else "lightgray" for n in G.nodes()]
            nx.draw(G, pos, node_color=colors, with_labels=True)
            plt.show()
        
        # inital value for the changed nodes
        if args.plot:
            new_infections = [len(begin)]

        while changed:
            changeNode = []
            changed = False
            # checks every item in the unInfected to see if the newly infected nodes change it 
            for i in unInfected:
                if infection_threshold_reached(G, i, threshold):
                    changed = True
                    changeNode.append(i)
            
            # every node that should change on the step changes now so that it does cascade prematurely
            for node in changeNode:
                G.nodes[node]["infected"] = True
                unInfected.remove(node)
            
            # showing the updated graph with newly infected nodes
            if args.interactive:
                colors = ["red" if G.nodes[n].get("infected", False) else "lightgray" for n in G.nodes()]
                nx.draw(G, pos, node_color=colors, with_labels=True)
                plt.show()

            # adding the amount of changed nodes on that step
            if args.plot:
                new_infections.append(len(changeNode))
        
        # plotting
        if args.plot:
            plt.figure()
            plt.plot(new_infections, marker='o')
            plt.xlabel("Round")
            plt.ylabel("New infections")
            plt.title("New infections per round")
            plt.grid(True)
            plt.show()

main()
