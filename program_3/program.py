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


class Vertex:
    """ The adjacency list Vertex object """
    def __init__(self, vertex_id, weight):
        self.vertex_id = vertex_id
        self.weight = weight
        self.next = None


class ALGraph:
    """
    Adjacent List representation of a graph
    """
    def __init__(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices
        self.edges = [None] * self.number_of_vertices

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
        # print self.edges[vertex_id_1].vertex_id, self.edges[vertex_id_1].next
        # print self.edges[vertex_id_2].vertex_id, self.edges[vertex_id_2].next

    def build_graph_string(self):

        graph_string = ''

        for i in range(self.number_of_vertices):
            graph_string += 'Vertex [{}]: '.format(i)
            vertex = self.edges[i]
            while vertex:
                graph_string += '({0}, {1}) '.format(vertex.vertex_id, vertex.weight)
                vertex = vertex.next
            graph_string += " \n"

        return graph_string

    def build_graph_dictionary(self):

        graph_dictionary = {}

        for i in range(self.number_of_vertices):
            graph_dictionary[i] = {}
            vertex = self.edges[i]
            while vertex:
                graph_dictionary[i][vertex.vertex_id] = vertex.weight
                vertex = vertex.next

        return graph_dictionary

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
    al_graph = ALGraph(number_of_vertices)

    for edge in edges:
        al_graph.add_edge(edge[0], edge[1], edge[2])

    al_string = al_graph.build_graph_string()
    print al_string

    return al_string


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
        al_string = process_graph(graph_data)
        graphs_report += 'Full graph {} adjacency list\n'.format(graph_index)
        graphs_report += al_string
        graphs_report += '\n'

    if not os.path.exists(os.path.dirname(out_file_path)):
        os.makedirs(os.path.dirname(out_file_path))

    with open(out_file_path, 'w') as data:
        data.write('Program processing {}...\n\n'.format(in_file_name))
        data.write(graphs_report)
        data.write('Program complete!')


if __name__ == "__main__":
    run_processing()
