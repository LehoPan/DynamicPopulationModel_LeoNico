import networkx as nx 
import argparse
import os
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
    parser.add_argument('--shelter',type=int, help='Set the sheltering parameter s (e.g., a proportion or list of nodes that will be sheltered or protected from the infection).')
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

    if args.initiator:
        # The initiators of the cascade or infection
        begin = [int(x) for x in args.initiator.split(",")]
    
    #splitting up the 2 types of action
    if args.action == 'covid':
        #prob of infection
        if args.probability_of_infection:
            infect = float(args.probability_of_infection)
        
        #prob of death 
        if args.probability_of_death:
            death = float(args.probability_of_death)
        
        #lifespan 
        if args.lifespan:
            lifespan = int(args.lifespan)
        
        #TODO shelter - has to take both a probablity or list of protected ones 
        if args.shelter:
            pass
        #vaccination
        if args.vaccination:
            vacc = args.vaccination
        pass
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