import networkx as nx 
import argparse
import os

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
    parser.add_argument('--interactive',help='Plot the graph and the state of the nodes for every round')
    parser.add_argument('--plot',help='Plot the number of new infections per day when the simulation completes')
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
        begin = [int(x) for x in args.initiator.split(",")]
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
        #threshold
        threshold = float(args.threshold)
        unInfected = list(G.nodes())
        for i in begin:
            G.nodes[i]["infected"] = True
            unInfected.remove(i)
