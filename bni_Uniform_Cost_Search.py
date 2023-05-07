import copy

# Costos de las acciones
COST = 1
FR_COST = 3 + COST
CL_COST = 6 + COST


class Node():
    '''
    Clase que define un nodo teniendo en cuenta un padre, la posicion de goku, un mapa, 
    las semillas y las esferas que tiene goku hasta el momento, adicional se tiene un atributo costo. 
    '''
    def __init__(self, parent, position, map, seeds, spheres, cost=0):
        self.parent = parent
        self.position = position
        self.map = map
        self.seeds = seeds
        self.spheres = spheres
        self.cost = cost
    
class Uniform_Cost_Search():
    '''
    Clase que define el algoritmo de busqueda por costo uniforme.
    '''
    def __init__(self, map):
        self.map = map

    def expand_node(self, node, mapa):
        '''
        Funcion que expande un nodo, es decir, que genera los nodos hijos de un nodo dado.
        '''
        n_mapa=copy.deepcopy(mapa)
        child_nodes = self.node_neighbors(node, n_mapa)
        return child_nodes

    def node_neighbors(self,node,n_mapa):
        '''
        Verifica si un nodo se puede mover hacia arriba, abajo, izquierda o derecha, y
        si es posible, crea un nodo hijo con la posicion a la que se movio, adicionalmente
        se verifica que el nodo no haya sido visitado anteriormente, mirando su padre.
        '''
        x = node.position[0]
        y = node.position[1]

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
            
        return neighbors


    def check_parent_state(self, node, direction):
        '''
        Returna True o False dependiendo si el nodo se puede mover hacia la dirección dada.
        Se puede mover a una posición siempre y cuando no sea la posición de su padre a menos
        que tenga diferente cantidad de semillas o esferas.
        '''
        if node.parent == None:
            return True
        
        parent_x = node.parent.position[0]
        parent_y = node.parent.position[1]
        parent_seeds=node.parent.seeds
        parent_spheres=node.parent.spheres

        x = node.position[0]
        y = node.position[1]

        if direction=='up':
            if parent_x == x-1:
                if parent_seeds == node.seeds and parent_spheres == node.spheres:
                    return False
                else:
                    return True
            
        
        if direction=='down':
            if parent_x == x+1:
                if parent_seeds == node.seeds and parent_spheres == node.spheres:
                    return False
                else:
                    return True
        
        if direction=='left':
            if parent_y == y-1:
                if parent_seeds == node.seeds and parent_spheres == node.spheres:
                    return False
                else:
                    return True

        if direction=='right':
            if parent_y == y+1:
                if parent_seeds == node.seeds and parent_spheres == node.spheres:
                    return False
                else:
                    return True
                
        return True

        
    def state(self, node, position_x, position_y):
        '''
        Funcion que crea un nodo hijo a partir de un nodo dado, la posición a la que se movio, el numero de
        semillas y esferas. Adicional, actualiza el mapa, dependiendo de las condiciones y añade el costo
        '''
        map = copy.deepcopy(node.map)
        child = None

        
        if map[position_x][position_y] == 3: #freezer
            if(node.seeds>0):
                map[position_x][position_y] = 0
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+COST)
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+FR_COST)

        elif map[position_x][position_y] == 4: #cell
            if(node.seeds>0):
                map[position_x][position_y] = 0
                child = Node(node, (position_x, position_y), map, node.seeds-1, node.spheres, node.cost+COST)
            else:
                child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+CL_COST)

        elif map[position_x][position_y] == 5: # seed
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds+1, node.spheres, node.cost+COST)

        elif map[position_x][position_y] == 6: # sphere
            map[position_x][position_y] = 0
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres+1, node.cost+COST)

        else:
            child = Node(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost+COST)

        return child
        
    def solve(self):
        '''
        Funcion que resuelve el problema de busqueda utilizando el algoritmo de busqueda por amplitud.
        '''

        starting_position = None
        expanded_nodes = 0

        # Se recorre el mapa para encontrar la posicion inicial
        for i in range(len(self.map)):
            for j in range(len(self.map)):
                if self.map[i][j] == 2:
                    starting_position = (i, j)

        # Se crea el nodo inicial y se añade a la cola
        initial_node = Node(None, starting_position, self.map, 0, 0)
        
        queue = [initial_node]
        finished = False

        # Se expanden nodos hasta que se encuentre la solucion
        while not finished:
            # Se revisa si el primer nodo de la cola es la solucion
            if queue[0].spheres == 2:
                finished = True
            else:
                expanded_nodes += 1
                # Implementacion de la cola de prioridad para la busqueda por costo uniforme
                # Se expande el primer nodo de la cola y se añaden sus hijos al final de la cola
                # Luego se ordena la cola por costo de menor a mayor

                # queue[1:] -> todos los nodos menos el primero
                queue = queue[1:] + self.expand_node(queue[0],self.map)
                queue.sort(key=lambda x: x.cost) # Ordena la cola por el costo de cada nodo

        # Se reconstruye el camino de la solucion
        solution = queue[0]
        path = []   # camino recorrido
        maps = []   # los mapas de cada nodo

        # Se recorren todos los padres del nodo solucion y se añaden al camino y los mapas
        while solution.parent is not None:
            path.append(solution.position)
            maps.append(solution.map)
            solution = solution.parent

        path.append(solution.position)
        path.reverse()  # Se invierte el camino para que quede en el orden correcto

        maps.append(solution.map)
        maps.reverse()  # Se invierte el camino para que quede en el orden correcto

        # Se retorna el camino, el numero de nodos expandidos, los mapas de los nodos solucion y el costo total
        return path, expanded_nodes, maps, queue[0].cost
    

