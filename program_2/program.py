"""
IS 350 Program 1

Python version: 2.7

# Scope
Build BST and AVL trees

# Credentials
Student: Kyrylo Krysko
Date started: 10/14/2021

8
6
10
5
7
9
11
"""
import math
import os

# Common variables
program_root = os.path.dirname(os.path.abspath(__file__))


class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
        self.nodes_count = 0

    # Basic
    def insert(self, data):

        new_node = Node(data)
        self.nodes_count += 1

        if not self.root:
            self.root = new_node

        else:
            current_node = self.root

            while True:
                if data < current_node.data:
                    # Left
                    if not current_node.left:
                        current_node.left = new_node
                        return
                    else:
                        current_node = current_node.left
                else:
                    # Right
                    if not current_node.right:
                        current_node.right = new_node
                        return
                    else:
                        current_node = current_node.right

    def lookup(self, data):

        if not self.root:
            return

        current_node = self.root

        while current_node:
            if data < current_node.data:
                current_node = current_node.left
            elif data > current_node.data:
                current_node = current_node.right
            elif data == current_node.data:
                return current_node

        return

    # Service
    def get_node_height(self, node):

        if node is None:
            return 0

        leftAns = self.get_node_height(node.left)
        rightAns = self.get_node_height(node.right)

        return max(leftAns, rightAns) + 1

    def get_tree_height(self):

        return self.get_node_height(self.root) - 1

    def count_levels(self):

        return int(math.floor(math.log(self.nodes_count, 2) + 1))

    def print_tree(self):

        if not self.root:
            print '>> Empty tree'
            return

        lines, a, b, c = self.build_strings(self.root)
        for line in lines:
            print(line)

    def build_strings(self, node):
        """
        Returns list of strings, width, height, and horizontal coordinate of the root
        """

        # No child
        if node.right is None and node.left is None:
            line = '{}'.format(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child
        if node.right is None:
            lines, n, p, x = self.build_strings(node.left)
            s = '{}'.format(node.data)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child
        if node.left is None:
            lines, n, p, x = self.build_strings(node.right)
            s = '{}'.format(node.data)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children
        left, n, p, x = self.build_strings(node.left)
        right, m, q, y = self.build_strings(node.right)
        s = '{}'.format(node.data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


def main():

    test_case_number = '4'
    input_1_file_path = '{0}/data/input/test_case_{1}/input_{1}_1.txt'.format(program_root, test_case_number)
    input_2_file_path = '{0}/data/input/test_case_{1}/input_{1}_2.txt'.format(program_root, test_case_number)

    with open(input_1_file_path, 'r') as data:
        input_1 = data.readlines()

    with open(input_2_file_path, 'r') as data:
        input_2 = data.readlines()

    tree = BinarySearchTree()

    for number in input_1:
        tree.insert(int(number))
        # print tree.get_height()

    # Insert results
    tree.print_tree()

    for code in input_2:
        action, number = code.split(' ')
        number = int(number)

        if action == 'I':
            tree.insert(number)

    tree.print_tree()
    print tree.get_tree_height()


main()

