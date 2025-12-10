# DynamicPopulationModel_LeoNico
By Leo Pan 030025552 and Nicolas Piker 029966545

## Dependencies
We installed and utilized the python `networkx` and `matplotlib.pyplot` packages.

All other packages are standard numpy installation.

## Implementations
`Argparse` used to read command line arguments, and `networkx` for reading the input graph .gml.

- `--action` is just a string of either cascade or covid with validation. required to run the program. Covid will end once lifespan is reached or no more nodes are infected. Cascade ends when all nodes are converted, or there is no change 2 rounds in a row.
- `--initiator --threshold --probability_of_infection --probability_of_death --lifespan` are all just constants with input validation. Every round during a covid simulation will randomly infect neighboring nodes at the rate of infection, each infected node will then either become recovered or dead. After one round of being recovered the node will once again become susceptible. Dead nodes, recovered nodes, and infected nodes cannot become infected.
- `--shelter` will dynamically know if it is given 1 or more list of nodes, or a float to randomly shelter a portion of the uninfected nodes. Sheltered nodes do not become infected.
- `--vaccination` will take a float only between 0 and 1, to vaccinate a portion of the nodes. Vaccinated nodes do not become infected.
- `--interactive` and `--plot` are both just flags to trigger their visualizations. for `--interactive` closing the window will advance to the next round. `--plot` will pull up a line graph once the simulation ends. Here is the interactive color coding for the states of the nodes in covid(if nodes are multi-state, prioritizes displaying the top state):<br>
Legend:<br>
Red      :   Infected<br>
Green    :   Recovered<br>
Black    :   Dead<br>
Yellow   :   Sheltered<br>
Blue     :   Vaccinated<br>
Lightgray:   Susceptible<br>

***Note: shelter and vaccination notes when given a portions (value between 0-1), will not choose nodes to become multiple states (any combination of sheltered, vaccinated, or infected). Nodes can be multiple states only if you set the starting infected nodes and a list of sheltered to nodes overlap.

## Running the program
When creating the `gml` file, please use the format given in our example file.

Example Command:
`python ./dynamic_population.py example.gml --action covid --initiator 3,4 --probability_of_infection 0.75 --lifespan 100 --shelter 0.1 --vaccination 0.1 --interactive --probability_of_death 0.1 --plot`

`python ./dynamic_population.py example.gml --action cascade --initiator 3,4 --lifespan 100 --interactive --plot --threshold 0.4`
