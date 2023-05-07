from collections import deque
import copy
import math

# map=[
# [0, 5, 3, 1, 1, 1, 1, 1, 1, 1],
# [0, 1, 0, 0, 1, 0, 0, 0, 1, 1],
# [0, 1, 1, 0, 3, 5, 1, 0, 2, 0],
# [0, 1, 1, 1, 3, 1, 1, 1, 1, 0],
# [6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [1, 1, 4, 1, 1, 1, 1, 1, 1, 0],
# [1, 1, 0, 4, 4, 0, 0, 1, 1, 5],
# [1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
# [0, 0, 0, 0, 1, 1, 5, 0, 0, 0],
# [1, 1, 1, 0, 1, 1, 6, 1, 1, 1]]

class Node():

    def __init__(self, parent, position, map, seeds, spheres, cost, heuristic):
        self.parent = parent
        self.position = position
        self.map = map
        self.seeds = seeds
        self.spheres = spheres
        self.cost = cost
        self.heuristic = heuristic
    
class Greedy_Search():
    def __init__(self, map):
        self.map = map

    def expand_node(self, node, mapa):
        n_mapa=copy.deepcopy(mapa)
        child_nodes = self.node_neighbors(node, n_mapa)
        return child_nodes

    def node_neighbors(self,node,n_mapa):

        #print ("hola neig")
        x = node.position[0]
        y = node.position[1]

        #print(parent_x, parent_y)
        # print(n_mapa)
        neighbors=[] 

        if(((x)-1>=0 and n_mapa[(x)-1][y]!=1) and self.check_parent_state(node, 'up') ):
            child = self.state(node, x-1, y)
            neighbors.append(child)

        if(((x)+1<10 and n_mapa[(x)+1][y]!=1) and self.check_parent_state(node, 'down')):
            child = self.state(node, x+1, y)
            neighbors.append(child)

        if(((y)+1<10 and n_mapa[(x)][(y)+1]!=1) and self.check_parent_state(node, 'right')):
            child = self.state(node, x, y+1)
            neighbors.append(child)

        if(((y)-1>=0 and n_mapa[(x)][(y)-1]!=1) and self.check_parent_state(node, 'left')):
            child = self.state(node, x, y-1)
            neighbors.append(child)
            
        #print(neighbors)
        return neighbors


    def check_parent_state(self, node, direction):
        if node.parent == None:
            return True
        
        parent_x = node.parent.position[0]
        parent_y = node.parent.position[1]
        parent_seeds=node.parent.seeds
        parent_spheres=node.parent.spheres

        x = node.position[0]
        y = node.position[1]

        if direction=='up':
            if parent_seeds != node.seeds or parent_spheres != node.spheres:
                return True

            return self.avoid_cicle(node, ((x-1),y))
        
        if direction=='down':
            if parent_seeds != node.seeds or parent_spheres != node.spheres:
                return True

            return self.avoid_cicle(node, ((x+1),y))
        
        if direction=='left':
            if parent_seeds != node.seeds or parent_spheres != node.spheres:
                return True

            return self.avoid_cicle(node, (x,(y-1)))

        if direction=='right':
            if parent_seeds != node.seeds or parent_spheres != node.spheres:
                return True

            return self.avoid_cicle(node, (x,(y+1)))
                
        return True


    def avoid_cicle(self,node, new_position):
        #print(new_position, node.position)
        current = node
        while current is not None:
            if current.position == new_position:
                return False
            current = current.parent
        else:
            return True


        
    def state(self, node, position_x, position_y):

        map = copy.deepcopy(node.map)
        child = None

        
        if map[position_x][position_y] == 3: #freezer
            if(node.seeds>0):
                map[position_x][position_y] = 0
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+1, heuristic((position_x,position_y), map))
                
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+4, heuristic((position_x,position_y), map))

        elif map[position_x][position_y] == 4: #cell
            if(node.seeds>0):
                map[position_x][position_y] = 0
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+1, heuristic((position_x,position_y), map))
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+7, heuristic((position_x,position_y), map))

        elif map[position_x][position_y] == 5: # seed
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds+1, node.spheres, node.cost+1, heuristic((position_x,position_y), map))

        elif map[position_x][position_y] == 6: # sphere
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres+1, node.cost+1, heuristic((position_x,position_y), map))

        else:
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+1, heuristic((position_x,position_y), map))

        #print(child.position)
        return child
        
    def solve(self):
        
        starting_position = None
        expanded_nodes = 0

        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == 2:
                    starting_position = (i, j)

        print('starting position', starting_position)
        initial_node = Node(None, starting_position, self.map, 0, 0, 0, heuristic(starting_position, self.map))
        
        queue = [initial_node]
        finished = False

        while not finished:
            
            #current_node_position = queue[0].position
            if queue[0].spheres == 2:
                finished = True
            else:
                expanded_nodes += 1
                #print("Nodo expandido:", queue[0].position)
                #queue = priority_queue(queue[1:], self.expand_node(queue[0],self.map))
                queue = queue[1:] + self.expand_node(queue[0],self.map)
                queue.sort(key=lambda x: x.heuristic)
                #print("Queue: ", queue)

        solution = queue[0]
        print("Semillas:", queue[0].seeds)
        path = []
        maps = []
        while solution.parent is not None:
            path.append(solution.position)
            maps.append(solution.map)
            solution = solution.parent

        path.append(solution.position)
        path.reverse()

        maps.append(solution.map)
        maps.reverse()

        for i in range(len(queue[0].map)):
            row = ''
            for j in range(len(queue[0].map)):
                row += str(queue[0].map[i][j]) + ' '
            # print(row)

        return path, expanded_nodes, maps, queue[0].cost
    




def heuristic(position, map):
    spheres = []
    for i in range(len(map)):
        for j in range(len(map)):
            if map[i][j] == 6:
                spheres.append((i,j))

    if len(spheres) == 0:
        return 0


    distances = []
    for sphere in spheres:
        distances.append(euclidian_distance(position[0], position[1], sphere[0],sphere[1]))

    if len(spheres) == 2:
        sphere_distance = euclidian_distance(spheres[0][0], spheres[0][1], spheres[1][0], spheres[1][1])
    else:
        sphere_distance = 0

    if len(distances) == 1:
        total = sphere_distance + distances[0]
    else:
        total = sphere_distance + min(distances[0], distances[1])
    # print(total)
    return total

def euclidian_distance(x1,y1,x2,y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)



# path, nodes, maps, cost = Uniform_Cost_Search(map).solve()
# print("Path: ", path)
# print("Nodos expandidos: ", nodes)
# print("Costo: ", cost)