"""
This is the graph module. It contains a minimalistic Graph class.
"""

class Graph:
    """
    A class representing undirected graphs as adjacency lists. 

    Attributes: 
    -----------
    nodes: NodeType
        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string.
        We will usually use a list of integers 1, ..., n.
    graph: dict
        A dictionnary that contains the adjacency list of each node in the form
        graph[node] = [neighbor1, neighbor2, ...]
    nb_nodes: int
        The number of nodes.
    nb_edges: int
        The number of edges. 
    edges: list[tuple[NodeType, NodeType]]
        The list of all edges
    """

    def __init__(self, nodes=[]):
        """
        Initializes the graph with a set of nodes, and no edges. 

        Parameters: 
        -----------
        nodes: list, optional
            A list of nodes. Default is empty.
        """
        self.nodes = nodes 
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
        self.edges = []
        
    def __str__(self):
        """
        Prints the graph as a list of neighbors for each node (one per line)
        """
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output

    def __repr__(self): 
        """
        Returns a representation of the graph with number of nodes and edges.
        """
        return f"<graph.Graph: nb_nodes={self.nb_nodes}, nb_edges={self.nb_edges}>"

    def add_edge(self, node1, node2):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 
        When adding an edge between two nodes, if one of the ones does not exist it is added to the list of nodes.

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        """
        if node1 not in self.graph:
            self.graph[node1] = []
            self.nb_nodes += 1
            self.nodes.append(node1)
        if node2 not in self.graph:
            self.graph[node2] = []
            self.nb_nodes += 1
            self.nodes.append(node2)

        self.graph[node1].append(node2)
        self.graph[node2].append(node1)
        self.nb_edges += 1
        self.edges.append((node1, node2))

    def bfs(self, src, dst): 
        """
        Finds a shortest path from src to dst by BFS.  

        Parameters: 
        -----------
        src: NodeType
            The source node.
        dst: NodeType
            The destination node.

        Output: 
        -------
        path: list[NodeType] | None
            The shortest path from src to dst. Returns None if dst is not reachable from src
        """ 
        file=[src] #création d'une file d'attente pour placer les noeuds à explorer. On y met le noeud source pour préparer première étape
        visited=[src]
        previous_nodes={}
        path=[dst] 
        while len(file)>0: #algorithme va être exécuté tant qu'il reste des noeuds à traiter
            n=file.pop(0) #extraction du premier élément de la file d'attente (va permettre de traiter en largeur)
            if n==dst:
                p=n
                while p !=src:
                    path.insert(0,previous_nodes[p])
                    p=previous_nodes[p]
                return path  
            else:
                for i in self.graph[n]: #ajoute les noeuds adjaçants
                    if i not in visited:
                        file.append(i) #on ajoute à la fin pour que toute une ligne soit d'abord traitée
                        visited.append(i)
                        previous_nodes[i]=n
        return None
        

#ce que est prometteur, c'est les noeuds où tuple[i]==i+1

        

    @classmethod
    def graph_from_file(cls, file_name):
        """
        Reads a text file and returns the graph as an object of the Graph class.

        The file should have the following format: 
            The first line of the file is 'n m'
            The next m lines have 'node1 node2'
        The nodes (node1, node2) should be named 1..n

        Parameters: 
        -----------
        file_name: str
            The name of the file

        Outputs: 
        -----------
        graph: Graph
            An object of the class Graph with the graph from file_name.
        """
        with open(file_name, "r") as file:
            n, m = map(int, file.readline().split())
            graph = Graph(range(1, n+1))
            for _ in range(m):
                edge = list(map(int, file.readline().split()))
                if len(edge) == 2:
                    node1, node2 = edge
                    graph.add_edge(node1, node2) # will add dist=1 by default
                else:
                    raise Exception("Format incorrect")
        return graph

#Tests fct bfs
for i in range(1,20):
    for j in range(i+1,21):
        print(i,j,len(Graph.bfs(Graph.graph_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\graph1.in"),i,j)),Graph.bfs(Graph.graph_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\graph1.in"),i,j))
for i in range(1,20):
    for j in range(i+1,21):
        print(i,j,Graph.bfs(Graph.graph_from_file("C:\\Users\\lisem\\OneDrive\\Documents\\ENSAE\\1A\\ensae-prog24\\input\\graph2.in"),i,j))
