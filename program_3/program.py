"""
CIS 350 Program 1
Python version: 2.7


# Scope
Build a Minimum Spanning Tree


# Credentials
Student: Kyrylo Krysko
Date started: 11/18/2021
"""
import os
program_root = os.path.dirname(os.path.abspath(__file__))


class Heap:

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def new_min_heap_node(self, vertex_id, weight):
        """
        Create heap node
        """

        return [vertex_id, weight]

    def swap_min_heap_node(self, id_1, id_2):
        """
        Swap nodes
        """

        temp = self.array[id_1]
        self.array[id_1] = self.array[id_2]
        self.array[id_2] = temp

    def min_heapify(self, idx):
        """
        Create Heap
        """

        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right

        # Swap nodes
        if smallest != idx:
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap nodes
            self.swap_min_heap_node(smallest, idx)

            self.min_heapify(smallest)

    # Standard function to extract minimum node from heap
    def extract_min(self):
        """
        Get minimum node
        """

        if self.is_empty():
            return

        # Store the root node
        root = self.array[0]

        # Replace root node with last node
        last_node = self.array[self.size - 1]
        self.array[0] = last_node

        # Update position of last node
        self.pos[last_node[0]] = 0
        self.pos[root[0]] = self.size - 1

        # Reduce heap size and heapify root
        self.size -= 1
        self.min_heapify(0)

        return root

    def is_empty(self):

        if self.size == 0:
            return True
        else:
            return False

    def decrease_key(self, vertex_id, weight):

        # Get index vertex in array
        i = self.pos[vertex_id]

        # Update node weight
        self.array[i][1] = weight

        # Heapify
        while i > 0 and self.array[i][1] < self.array[(i - 1) / 2][1]:
            # Swap current node with  parent
            self.pos[self.array[i][0]] = (i - 1) / 2
            self.pos[self.array[(i - 1) / 2][0]] = i
            self.swap_min_heap_node(i, (i - 1) / 2)
            i = (i - 1) / 2

    def vertex_in_heap(self, vertex_id):
        """
        Check if a vertex in heap
        """

        if self.pos[vertex_id] < self.size:
            return True

        else:
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
        self.adjacency_list = [None] * self.number_of_vertices
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
        vertex.next = self.adjacency_list[vertex_id_2]
        self.adjacency_list[vertex_id_2] = vertex

        # Add vertex ID 2
        vertex = Vertex(vertex_id_2, weight)
        vertex.next = self.adjacency_list[vertex_id_1]
        self.adjacency_list[vertex_id_1] = vertex

    def build_adjacency_string(self):

        graph_string = ''

        for i in range(self.number_of_vertices):
            graph_string += 'Vertex [{}]: '.format(i)
            vertex = self.adjacency_list[i]
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
            vertex = self.adjacency_list[i]
            while vertex:
                graph_dictionary[i][vertex.vertex_id] = vertex.weight
                vertex = vertex.next

        return graph_dictionary

    def build_mst_graph(self):

        # Get the number of vertices in graph
        number_of_vertices = self.number_of_vertices

        # MST data
        weights = []
        parent = []
        min_heap = Heap()
        min_heap.size = number_of_vertices

        # Add vertices to the heap
        for vertex_id in range(number_of_vertices):
            parent.append(-1)
            weights.append(99999)
            min_heap.array.append(min_heap.new_min_heap_node(vertex_id, weights[vertex_id]))
            min_heap.pos.append(vertex_id)

        # Initialize 0 vertex
        min_heap.pos[0] = 0
        weights[0] = 0
        min_heap.decrease_key(0, weights[0])

        # Process MST
        while not min_heap.is_empty():

            # Extract the vertex with minimum distance value
            heap_node = min_heap.extract_min()
            min_value = heap_node[0]

            # Update weights on adjacent vertices
            vertex = self.adjacency_list[min_value]
            while vertex:
                if min_heap.vertex_in_heap(vertex.vertex_id) and vertex.weight < weights[vertex.vertex_id]:

                    weights[vertex.vertex_id] = vertex.weight
                    parent[vertex.vertex_id] = min_value
                    # Update distance in heap
                    min_heap.decrease_key(vertex.vertex_id, weights[vertex.vertex_id])

                    # Construct MST graph
                    self.mst_graph[vertex.vertex_id] = Vertex(min_value, vertex.weight)

                vertex = vertex.next


def validate_data(vertex_id_1, vertex_id_2, weight):

    line_errors = ''

    # Check if number is positive
    if vertex_id_1 < 0:
        line_errors += 'Vertex 1 value is negative integer'

    if vertex_id_2 < 0:
        line_errors += 'Vertex 2 value is negative integer'

    if line_errors != '':
        return line_errors

    else:
        return None

def read_data(file_path):
    """
    Read input data from file, convert to a dictionary of graphs:
        {index_of_graph: {properties: [number_of_nodes, number_of_edges]
                          edges: [edge_1, ... ]}
        where edge = [ vertex_id_1, vertex_id_2, edge weight]

    :param file_path: path to a file with graph data
    :return: graph dictionary
    """

    # Store graph data
    graph_index = 1
    # empty_graph = None
    graphs_data = {}

    with open(file_path, 'r') as data:
        lines_data = data.readlines()

        for line_index, line in enumerate(lines_data):
            line = line.strip()
            line_content = line.split()

            # Get graph header
            if len(line_content) == 2:

                if graph_index in graphs_data.keys():
                    graph_index += 1

                # Init new graph
                number_of_vertices = int(line_content[0])
                number_of_edges = int(line_content[1])

                graph_data = {'properties': {'number_of_vertices': number_of_vertices,
                                             'number_of_edges': number_of_edges},
                              'edges': [],
                              'errors': []}

                graphs_data[graph_index] = graph_data

                # Validate header
                if number_of_vertices < 0 or number_of_edges < 0:
                    graphs_data[graph_index]['errors'].append('Header of graph is invalid: negative numbers.')

            # Skip empty line
            elif len(line_content) == 0:
                continue

            # Parse graph data
            else:
                vertex_id_1 = int(line_content[0])
                vertex_id_2 = int(line_content[1])
                weight = int(line_content[2])

                # Validate data
                line_errors = validate_data(vertex_id_1, vertex_id_2, weight)

                if not line_errors:
                    # Record data
                    graphs_data[graph_index]['edges'].append([vertex_id_1, vertex_id_2, weight])
                else:
                    graphs_data[graph_index]['errors'].append('ERROR! Line {0} invalid: {1}'.format(line_index, line_errors))

                # # Reset empty graph
                # empty_graph = None

    return graphs_data


def process_graph(graph_data):

    # Build adjacency list for source graph
    number_of_vertices = graph_data['properties']['number_of_vertices']
    edges = graph_data['edges']
    al_graph = Graph(number_of_vertices)

    for edge in edges:
        al_graph.add_edge(edge[0], edge[1], edge[2])

    # Create MST graph
    al_string = al_graph.build_adjacency_string()
    al_graph.build_mst_graph()
    mst_string = al_graph.build_mst_string()

    # Build adjacency list for MST graph
    graph = Graph(number_of_vertices)
    for i in range(1, len(al_graph.mst_graph)):
        graph.add_edge(i, al_graph.mst_graph[i].vertex_id, al_graph.mst_graph[i].weight)

    al_mst_string = graph.build_adjacency_string()

    return al_string, mst_string, al_mst_string


def run_processing():

    # input_file_version = raw_input('Enter the source file VERSION (1,2,3, etc.): ')
    input_file_version = '2'
    in_file_name = 'MST{}.dat'.format(input_file_version)
    out_file_name = in_file_name.replace('.dat', '.out')
    in_file_path = '{0}/data/input/{1}'.format(program_root, in_file_name)
    out_file_path = '{0}/data/output/{1}'.format(program_root, out_file_name)

    if not os.path.exists(in_file_path):
        print 'ERROR! The file {} does not exist! Please, enter the correct name.'.format(in_file_path)

    graphs_report = ''
    graphs_data = read_data(in_file_path)

    # Create folder for outputs
    if not os.path.exists(os.path.dirname(out_file_path)):
        os.makedirs(os.path.dirname(out_file_path))

    if not graphs_data:
        print 'ERROR parsing source data!'
        return

    for graph_index, graph_data in graphs_data.iteritems():
        print graph_data
        if not graph_data['errors'] and graph_data['edges']:
            al_string, mst_string, al_mst_string = process_graph(graph_data)

            # Prepare report data
            report_title = 'Full graph {} adjacency list:\n'.format(graph_index)
            report_graph_index = '\nMST graph {}\n'.format(graph_index)
            report_graph_list = 'MST graph {} adjacency list:\n'.format(graph_index)

            # Print report
            print report_title
            print al_string
            print report_graph_index
            print mst_string
            print report_graph_list
            print al_mst_string

            # Write report to a file
            graphs_report += report_title
            graphs_report += al_string
            graphs_report += report_graph_index
            graphs_report += mst_string
            graphs_report += report_graph_list
            graphs_report += al_mst_string
            graphs_report += '\n\n'

        else:
            print 'Graph {} input data is invalid!\n'.format(graph_index)
            graphs_report += 'Graph {} input data is invalid!\n'.format(graph_index)

            for error in graph_data['errors']:
                print '{}\n'.format(error)
                graphs_report += '{}\n'.format(error)

            # Catch empty graph
            if not graph_data['edges']:
                print 'Graph edges data is empty'
                graphs_report += 'Graph edges data is empty\n'

            graphs_report += '\n'

    with open(out_file_path, 'w') as data:
        data.write('Program processing {}...\n\n'.format(in_file_name))
        data.write(graphs_report)
        data.write('Program complete!')


if __name__ == "__main__":
    run_processing()
