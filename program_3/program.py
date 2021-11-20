"""
CIS 350 Program 1
Python version: 2.7


# Scope
Build a Minimum Spanning Tree


# Credentials
Student: Kyrylo Krysko
Date started: 11/18/2021
"""
from collections import defaultdict
import os
program_root = os.path.dirname(os.path.abspath(__file__))


class Heap:

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    # A utility function to swap two nodes of
    # min heap. Needed for min heapify
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped. Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < \
                self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < \
                self.array[smallest][1]:
            smallest = right

        # The nodes to be swapped in min heap
        # if idx is not smallest
        if smallest != idx:
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap nodes
            self.swapMinHeapNode(smallest, idx)

            self.minHeapify(smallest)

    # Standard function to extract minimum node from heap
    def extractMin(self):

        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return

        # Store the root node
        root = self.array[0]

        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist):

        # Get the index of v in  heap array

        i = self.pos[v]

        # Get the node and update its dist value
        self.array[i][1] = dist

        # Travel up while the complete tree is not
        # hepified. This is a O(Logn) loop
        while i > 0 and self.array[i][1] < \
                self.array[(i - 1) / 2][1]:
            # Swap this node with its parent
            self.pos[self.array[i][0]] = (i - 1) / 2
            self.pos[self.array[(i - 1) / 2][0]] = i
            self.swapMinHeapNode(i, (i - 1) / 2)

            # move to parent index
            i = (i - 1) / 2

    # A utility function to check if a given vertex
    # 'v' is in min heap or not
    def isInMinHeap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


class Vertex:
    """ The adjacency list Vertex object """
    def __init__(self, vertex_id, weight):
        self.vertex_id = vertex_id
        self.weight = weight
        self.next = None


class Graph:
    """
    Adjacent List representation of a graph
    """
    def __init__(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices
        self.edges = [None] * self.number_of_vertices
        self.mst_graph = [None] * self.number_of_vertices

    def add_edge(self, vertex_id_1, vertex_id_2, weight):
        """
        Add edge to the list of edges
        :param vertex_id_1: vertex 1 value
        :param vertex_id_2: vertex 2 value
        :param weight: vertex 1-2 weight
        :return:
        """

        # Add vertex ID 1
        vertex = Vertex(vertex_id_1, weight)
        vertex.next = self.edges[vertex_id_2]
        self.edges[vertex_id_2] = vertex

        # Add vertex ID 2
        vertex = Vertex(vertex_id_2, weight)
        vertex.next = self.edges[vertex_id_1]
        self.edges[vertex_id_1] = vertex

    def build_adjacency_string(self):

        graph_string = ''

        for i in range(self.number_of_vertices):
            graph_string += 'Vertex [{}]: '.format(i)
            vertex = self.edges[i]
            while vertex:
                graph_string += '({0}, {1}) '.format(vertex.vertex_id, vertex.weight)
                vertex = vertex.next
            graph_string += " \n"

        return graph_string

    def build_mst_string(self):

        cost = 0
        mst_string = ''

        for i in range(1, self.number_of_vertices):
            vertex = self.mst_graph[i]
            mst_string += 'Edge: {}-{} weight: {}\n'.format(i, vertex.vertex_id, vertex.weight)
            cost += vertex.weight

        mst_string += 'Total cost of MST: {}\n\n'.format(cost)

        return mst_string

    def build_graph_dictionary(self):

        graph_dictionary = {}

        for i in range(self.number_of_vertices):
            graph_dictionary[i] = {}
            vertex = self.edges[i]
            while vertex:
                graph_dictionary[i][vertex.vertex_id] = vertex.weight
                vertex = vertex.next

        return graph_dictionary

    def PrimMST(self):
        # Get the number of vertices in graph
        number_of_vertices = self.number_of_vertices

        # key values used to pick minimum weight edge in cut
        key = []

        # List to store contructed MST
        parent = []

        # minHeap represents set E
        minHeap = Heap()

        # Initialize min heap with all vertices. Key values of all
        # vertices (except the 0th vertex) is is initially infinite
        for vertex_id in range(number_of_vertices):
            parent.append(-1)
            key.append(99999)
            minHeap.array.append(minHeap.newMinHeapNode(vertex_id, key[vertex_id]))
            minHeap.pos.append(vertex_id)

        # Make key value of 0th vertex as 0 so
        # that it is extracted first
        minHeap.pos[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0])

        # Initially size of min heap is equal to V
        minHeap.size = number_of_vertices

        # In the following loop, min heap contains all nodes
        # not yet added in the MST.
        while minHeap.isEmpty() == False:

            # Extract the vertex with minimum distance value
            newHeapNode = minHeap.extractMin()
            min_value = newHeapNode[0]

            # Traverse through all adjacent vertices of u
            # (the extracted vertex) and update their
            # distance values

            vertex = self.edges[min_value]
            while vertex:
                if minHeap.isInMinHeap(vertex.vertex_id) and vertex.weight < key[vertex.vertex_id]:
                    # print 'parent added [{}] : {}    W {}'.format(vertex.vertex_id, min_value, vertex.weight)

                    key[vertex.vertex_id] = vertex.weight
                    parent[vertex.vertex_id] = min_value

                    new_vertex = Vertex(min_value, vertex.weight)
                    self.mst_graph[vertex.vertex_id] = new_vertex

                    # update distance value in min heap also
                    minHeap.decreaseKey(vertex.vertex_id, key[vertex.vertex_id])

                vertex = vertex.next


def read_data(file_path):
    """
    Read input data from file, convert to a dictionary of graphs:
        {index_of_graph: {properties: [number_of_nodes, number_of_edges]
                          edges: [edge_1, ... ]}
        where edge = [ vertex_id_1, vertex_id_2, edge weight]

    :param file_path: path to a file with graph data
    :return: graph dictionary
    """

    # Skip if file not exists
    if not os.path.exists(file_path):
        print '>> ERROR! File not exists!'
        return

    graphs_data = {}
    index = 1  # Keys for graph dictionary

    with open(file_path, 'r') as data:
        graph_data = data.readlines()

        for line in graph_data:
            line = line.strip()
            line_content = line.split()

            # Get graph beginning
            if len(line_content) == 2:

                if index in graphs_data.keys():
                    index += 1

                # Init new graph
                graphs_data[index] = {'properties': {'number_of_vertices': int(line_content[0]),
                                                     'number_of_edges': int(line_content[1])},
                                      'edges': []}

            # Skip empty line
            elif len(line_content) == 0:
                continue

            # Parse graph data
            else:
                graphs_data[index]['edges'].append([int(line_content[0]), int(line_content[1]), int(line_content[2])])

    return graphs_data


def process_graph(graph_data):

    number_of_vertices = graph_data['properties']['number_of_vertices']
    edges = graph_data['edges']
    al_graph = Graph(number_of_vertices)

    for edge in edges:
        al_graph.add_edge(edge[0], edge[1], edge[2])

    al_string = al_graph.build_adjacency_string()
    al_graph.PrimMST()
    mst_string = al_graph.build_mst_string()

    graph = Graph(number_of_vertices)
    for i in range(1, len(al_graph.mst_graph)):
        graph.add_edge(i, al_graph.mst_graph[i].vertex_id, al_graph.mst_graph[i].weight)

    al_mast_string = graph.build_adjacency_string()

    print al_string
    print mst_string
    print al_mast_string

    return al_string, mst_string, al_mast_string


def run_processing():

    in_file_name = 'MST2.dat'
    out_file_name = in_file_name.replace('.dat', '.out')
    in_file_path = '{0}/data/input/{1}'.format(program_root, in_file_name)
    out_file_path = '{0}/data/output/{1}'.format(program_root, out_file_name)

    graphs_report = ''
    graphs_data = read_data(in_file_path)

    if not graphs_data:
        return

    for graph_index, graph_data in graphs_data.iteritems():
        al_string, mst_string, al_mast_string = process_graph(graph_data)
        graphs_report += 'Full graph {} adjacency list:\n'.format(graph_index)
        graphs_report += al_string
        graphs_report += '\nMST graph {}\n'.format(graph_index)
        graphs_report += mst_string
        graphs_report += 'MST graph {} adjacency list:\n'.format(graph_index)
        graphs_report += al_mast_string
        graphs_report += '\n\n'

    if not os.path.exists(os.path.dirname(out_file_path)):
        os.makedirs(os.path.dirname(out_file_path))

    with open(out_file_path, 'w') as data:
        data.write('Program processing {}...\n\n'.format(in_file_name))
        data.write(graphs_report)
        data.write('Program complete!')


if __name__ == "__main__":
    run_processing()
