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

    def min_heapify(self, id_x):
        """
        Create Heap
        """

        smallest = id_x
        left = 2 * id_x + 1
        right = 2 * id_x + 2

        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right

        # Swap nodes
        if smallest != id_x:
            # Swap positions
            self.pos[self.array[smallest][0]] = id_x
            self.pos[self.array[id_x][0]] = smallest

            # Swap nodes
            self.swap_min_heap_node(smallest, id_x)

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


def validate_connected(graphs_data):
    """
    Check if number of edges more then number of vertices, otherwise consider graph unconnected
    Record result to graph_data dictionary
    :param graphs_data: graph points/weights
    :return:
    """

    for graph_index, graph_data in graphs_data.iteritems():
        if graph_data['edges']:
            if len(graph_data['edges']) < graph_data['properties']['number_of_vertices']:
                graphs_data[graph_index]['errors'].append('Graph is not connected.')


def validate_data(vertex_id_1, vertex_id_2, weight, number_of_vertices):
    """
    Check if graph data is correct, so it is possible to build MST tree

    :param vertex_id_1: vertex 1 value
    :param vertex_id_2: vertex 2 value
    :param weight: edge 1-2 weight
    :param number_of_vertices: total number of vertices in graph
    :return: None if graph is valid, string errors list if not
    """

    line_errors = ''

    # Check if number is positive
    if vertex_id_1 < 0:
        line_errors += 'Vertex 1 value is negative integer'

    if vertex_id_2 < 0:
        line_errors += 'Vertex 2 value is negative integer'

    # Check vertex values
    if vertex_id_1 >= number_of_vertices:
        line_errors += 'Vertex 1 value is grater then number of vertexes'

    # Check vertex values
    if vertex_id_2 >= number_of_vertices:
        line_errors += 'Vertex 2 value is grater then number of vertexes'

    # Check if weight is grater then 0
    if weight <= 0:
        line_errors += 'Vertex value has wrong weight'

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
    graphs_data = {}
    invalid_header = False

    with open(file_path, 'r') as data:
        lines_data = data.readlines()

        for line_index, line in enumerate(lines_data):
            line = line.strip()
            line_content = line.split()

            # Get graph header
            if len(line_content) == 2:

                # Detect new graph
                if graph_index in graphs_data.keys():
                    invalid_header = False
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
                if number_of_vertices <= 0 or number_of_edges <= 0:
                    graphs_data[graph_index]['errors'].append('Header of graph is invalid.')
                    invalid_header = True

            # Skip empty line
            elif len(line_content) == 0:
                continue

            # Parse graph data
            else:

                # Skip validation if header is invalid
                if invalid_header:
                    continue

                vertex_id_1 = int(line_content[0])
                vertex_id_2 = int(line_content[1])
                weight = int(line_content[2])

                # Validate data
                line_errors = validate_data(vertex_id_1, vertex_id_2, weight,
                                            graphs_data[graph_index]['properties']['number_of_vertices'])

                if not line_errors:
                    # Record data
                    graphs_data[graph_index]['edges'].append([vertex_id_1, vertex_id_2, weight])
                else:
                    graphs_data[graph_index]['errors'].append('Line {0} invalid: {1}'.format(line_index+1, line_errors))

    # Validate if graph id connected
    validate_connected(graphs_data)

    return graphs_data


def process_graph(graph_data):
    """
    Create adjacency list of source graph, build MST tree, create adjacency list of MST graph
    :param graph_data: input data for building graph
    :return: processing results strings
    """

    # Build adjacency list for source graph
    number_of_vertices = graph_data['properties']['number_of_vertices']
    edges = graph_data['edges']
    al_graph = Graph(number_of_vertices)

    for edge in edges:
        al_graph.add_edge(edge[0], edge[1], edge[2])

    # Create MST graph
    adjacency_list_src = al_graph.build_adjacency_string()
    al_graph.build_mst_graph()
    mst_string = al_graph.build_mst_string()

    # Build adjacency list for MST graph
    graph = Graph(number_of_vertices)
    for i in range(1, len(al_graph.mst_graph)):
        graph.add_edge(i, al_graph.mst_graph[i].vertex_id, al_graph.mst_graph[i].weight)

    adjacency_list_mst = graph.build_adjacency_string()

    return adjacency_list_src, mst_string, adjacency_list_mst


def run_processing():

    # input_file_version = raw_input('Enter the source file VERSION (1,2,3, etc.): ')
    input_file_version = '7'
    in_file_name = 'MST{}.dat'.format(input_file_version)
    out_file_name = in_file_name.replace('.dat', '.out')
    in_file_path = '{0}/data/input/{1}'.format(program_root, in_file_name)
    out_file_path = '{0}/data/output/{1}'.format(program_root, out_file_name)

    if not os.path.exists(in_file_path):
        print 'ERROR! The file {} does not exist! Please, enter the correct name.'.format(in_file_path)
        return

    graphs_report = ''
    graphs_data = read_data(in_file_path)

    # Create folder for outputs
    if not os.path.exists(os.path.dirname(out_file_path)):
        os.makedirs(os.path.dirname(out_file_path))

    if not graphs_data:
        print 'ERROR parsing source data!'
        return

    for graph_index, graph_data in graphs_data.iteritems():

        if not graph_data['errors'] and graph_data['edges']:
            adjacency_list_src, mst_string, adjacency_list_mst = process_graph(graph_data)

            # Prepare report data
            report_title = 'Full graph {} adjacency list:\n'.format(graph_index)
            report_graph_index = '\nMST graph {}\n'.format(graph_index)
            report_graph_list = 'MST graph {} adjacency list:\n'.format(graph_index)

            # Print report
            print report_title
            print adjacency_list_src
            print report_graph_index
            print mst_string
            print report_graph_list
            print adjacency_list_mst

            # Write report to a file
            graphs_report += report_title
            graphs_report += adjacency_list_src
            graphs_report += report_graph_index
            graphs_report += mst_string
            graphs_report += report_graph_list
            graphs_report += adjacency_list_mst
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
