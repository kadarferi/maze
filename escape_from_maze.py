
from AStarGraphMod import *
import sys
from Plot import *

# default files
file_path   = 'Input1.txt'
output_file = 'Output1.txt'

if len(sys.argv) > 1:
    file_path   = sys.argv[1]     # maze input file
if len(sys.argv) > 2:
    output_file = sys.argv[2]     # maze output file with the optimal escape route

# labirintus beolvasása fájlból
graph = AStarGraphMod(file_path)

# ------------------------------------------------------------------------------------
min_step = np.inf
min_cost = np.inf
# ------------------------------------------------------------------------------------
shortest_route = []
shortest_result = {}

# kezdetben nincs plusz költsége az aknáknak, de folyamatosan növelem
# addig megyünk, míg találunk max. 2 aknás megoldást - ha több van, abból a legrövidebb kell
for i in range(1, graph.nrow*graph.ncol//2):
    print("Step", i)
    graph.mine_cost = i
    results = []

    barrier_counter = []    # ha csak falon át lehet kijutni, az derüljön ki az 1. lépésben!
    # több kilépési pont lehet
    for ep in graph.end_points:
        route, cost = AStarSearch(graph.start_point, ep, graph)
        steps = len(route)
        mine_count    = sum([1 for step in route if step in graph.mines])
        barrier_count = sum([1 for step in route if step in graph.barriers[0]])
        barrier_counter.append(barrier_count)
        actual_result = {'End Point': ep, 'Route': route, 'Cost': cost,
                         'Steps': steps, 'Mines': mine_count,'Barriers': barrier_count}
        #print("\n",i, ". Actual result: ", actual_result)
        #plot_maze(graph, route, 'Pic/' + output_file[:-3]+str(i)+str(ep)+ '.png')
        results.append(actual_result)

    if min(barrier_counter) > 0: break    # ha nincs kiút egyáltalán, akkor álljunk le

    # a különböző kilépési pontokhoz tartozó utakból kiválasztjuk a legrövidebbet
    # de csak akkor jó, ha max 2 aknára futott
    for r in results:
        route = r['Route']
        #print(i,". Steps:", r['Steps'], " Mines: ", r['Mines'], ' Min. Steps: ', min_step)
        if r['Mines'] > 2: r['Steps'] = np.inf  # ha 2-nél több akna, akkor nem jó
        if r['Steps'] < min_step and r['Mines'] < 3:
            shortest_result = r
            shortest_route = r['Route']
            min_step = r['Steps']
            min_cost = r['Cost']
    #print('Min cost: ', min_cost)

    # ha max. 2 akna volt, és nem mentünk át a falon, akkor kész vagyunk
    if min_step < np.inf and min_cost < np.inf and shortest_result['Mines'] < 3:
        break

# -----------------------------------------------------------------------------------------
# Save maze with escape route if exists
if min_step < np.inf and min_cost < np.inf:
    print('\nOptimal escape route:', shortest_result)
    graph.update_matrix_with_route(shortest_route)
    graph.matrix_to_file(output_file)
    plot_maze(graph, shortest_route, output_file[:-3] + 'png')
else:
    print("\nNo escape route.", shortest_result)

    with open(output_file, "wt") as outfile:
         outfile.write('\nNo escape route')
    plot_maze(graph, [], output_file[:-3] + 'png')
