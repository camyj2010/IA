
from collections import deque
import copy

# map=[
# [0, 5, 3, 1, 1, 1, 1, 1, 1, 1],
# [0, 1, 0, 0, 1, 0, 0, 1, 1, 1],
# [0, 1, 1, 0, 3, 5, 1, 0, 2, 0],
# [1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
# [6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
# [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 4, 4, 1, 0, 1, 1, 5],
# [1, 1, 0, 0, 1, 1, 0, 1, 1, 0],
# [0, 1, 0, 0, 1, 1, 5, 0, 0, 0],
# [1, 1, 1, 6, 1, 1, 0, 1, 1, 1]]

class Node():

    def __init__(self, parent, position, map, seeds, spheres, cost=0):
        self.parent = parent
        self.position = position
        self.map = map
        self.seeds = seeds
        self.spheres = spheres
        self.cost = cost
    

class Depth_Search():

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

        neighbors=[] 

        if(((x)-1>=0 and n_mapa[(x)-1][y]!=1) and self.check_parent_state(node, 'up')):
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
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+1)
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+4)

        elif map[position_x][position_y] == 4: #cell
            if(node.seeds>0):
                map[position_x][position_y] = 0
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+1)
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+7)

        elif map[position_x][position_y] == 5: # seed
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds+1, node.spheres, node.cost+1)

        elif map[position_x][position_y] == 6: # sphere
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres+1, node.cost+1)

        else:
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+1)

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
        initial_node = Node(None, starting_position, self.map, 0, 0)
        
        queue = [initial_node]
        finished = False

        while not finished:
            
            #current_node_position = queue[0].position
            if queue[0].spheres == 2:
                finished = True
            else:
                expanded_nodes += 1
                #print("Nodo expandido:", queue[0].position)
                queue = self.expand_node(queue[0],self.map) + queue[1:]
                #print("Queue: ", queue)

        solution = queue[0]
        #print("Semillas:", queue[0].seeds)
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
            #print(row)

        return path, expanded_nodes, maps, queue[0].cost

# path, nodes = Depth_Search(map).solve()
# print("Path: ", path)
# print("Nodos expandidos: ", nodes)
