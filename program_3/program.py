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


class Graph:
    """
    Adjacent List representation of a graph
    """
    def __init__(self, number_of_vertices):
        self.number_of_vertices = number_of_vertices
        self.graph = [None] * self.number_of_vertices
        print self.graph

    def add_edge(self, vertex_id_1, vertex_id_2, weight):

        vertex = Vertex(vertex_id_1, weight)
        vertex.next = self.graph[vertex_id_2]
        self.graph[vertex_id_2] = vertex

        vertex = Vertex(vertex_id_2, weight)
        vertex.next = self.graph[vertex_id_1]
        self.graph[vertex_id_1] = vertex

    def build_graph_string(self):

        graph_string = ''

        for i in range(self.number_of_vertices):
            graph_string += 'Vertex [{}]: '.format(i)
            vertex = self.graph[i]
            while vertex:
                graph_string += '({0}, {1}) '.format(vertex.vertex_id, vertex.weight)
                vertex = vertex.next
            graph_string += " \n"

        return graph_string


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
    graph = Graph(number_of_vertices)

    for edge in edges:
        graph.add_edge(edge[0], edge[1], edge[2])

    print graph.build_graph_string()


def run_processing():

    file_path = '{0}/data/input/MST2.dat'.format(program_root)
    graphs_data = read_data(file_path)

    if not graphs_data:
        return

    for graph_data in graphs_data.values():
        # print graph_data['edges']
        process_graph(graph_data)


if __name__ == "__main__":
    run_processing()