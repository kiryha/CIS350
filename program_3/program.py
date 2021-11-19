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


def read_data(file_path):
    """
    Read input data from file, convert to a dictionary of graphs:
        {index_of_graph: [ edge, ... ], ...}
        where edge = [ node_id_1, node_id_2, edge weight]

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
                graphs_data[index] = []

            # Skip empty line
            elif len(line_content) == 0:
                continue

            # Parse graph data
            else:
                graphs_data[index].append(line_content)
    
    return graphs_data

                
def run_processing():

    file_path = '{0}/data/input/MST2.dat'.format(program_root)
    graphs_data = read_data(file_path)

    if not graphs_data:
        return

    for edges in graphs_data.values():
        print edges


if __name__ == "__main__":
    run_processing()