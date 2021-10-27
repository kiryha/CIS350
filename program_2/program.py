"""
IS 350 Program 1
Python version: 2.7

# Scope
Build BST and AVL trees
The User will provide several Test Cases to process by the program.
The program will compare operations performed by BST and AVL trees using two input data files for each Test Case.
The results would be recorded to two output files (for BST and AVL) for each Test Case.
The summary result file will contain all operations for all test cases.

# Data
The source data located in /data/input/test_case_#
The results stored in /data/output/test_case_#

# Credentials
Student: Kyrylo Krysko
Date started: 10/14/2021
"""
import os

# Common variables
program_root = os.path.dirname(os.path.abspath(__file__))
operation_map = {'I': 'Insert', 'S': 'Search', 'D': 'Delete'}
test_names_map = {1: 'Missing Input 2',
                  2: 'Empty Input 2',
                  3: 'Ideal Tree',
                  4: 'Random Searches',
                  5: 'Unbalanced BST',
                  6: 'Perform Inserts',
                  7: 'Perform Deletes',
                  8: 'Perform Searches',
                  9: 'Collisions',
                  10: 'Basic RR',
                  11: 'Basic LL',
                  12: 'Basic RL',
                  13: 'Basic LR'}

# test_names_map = {10: 'Basic RR', 12: 'Basic RL'}  # 10: 'Basic RR', 12: 'Basic RL'


def build_summary_table(values):
    """
    Build a string for operations count
    values = [ [ test case #, name, sum bst, sum avl ], ... ]
    """

    columns = ['Test #', 'Test Title', 'BST', 'AVL']
    sum_bst = sum(value[2] for value in values)
    sum_avl = sum(value[3] for value in values)

    message = '{0:>60}\n\n\n'.format('Summary Operations Count')

    row = "{}{:>12}{:>24}{:>12}{:>12}\n"
    message += row.format('', *columns)
    message += '\n'

    for index, value in enumerate(values):
        message += row.format('', *value)

    message += '\n'
    message += '{:>12}{:>24}{:>12}{:>12}'.format('', 'Total for all cases', sum_bst, sum_avl)

    return message


def build_operation_table(test_case_name, values):
    """
    Build a string for operations count
    """

    tree_names = ['BST', 'AVL']
    operations = ['Search', 'Insert', 'Delete']

    sum_bst = sum(value[0] for value in values)
    sum_avl = sum(value[1] for value in values)

    message = '{0:>34}\n'.format('Operations count for:')
    message += '{0:>34}\n\n\n'.format(test_case_name)

    row = "{:>10}{:>12}{:>12}\n"
    message += row.format('', *tree_names)
    message += '\n'

    for index, value in enumerate(values):
        message += row.format(operations[index], *value)

    message += '\n'
    message += '{:>10}{:>12}{:>12}'.format('Total', sum_bst, sum_avl)
    message += '\n\n'

    return message, sum_bst, sum_avl


def build_tree_structure(node):
    """
    Build a string that represents a tree structure
    :param node: tree node
    :return: string, width, height, and horizontal coordinate of the root for printing tree
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
        lines, n, p, x = build_tree_structure(node.left)
        s = '{}'.format(node.data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
        second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
        shifted_lines = [line + u * ' ' for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

    # Only right child
    if node.left is None:
        lines, n, p, x = build_tree_structure(node.right)
        s = '{}'.format(node.data)
        u = len(s)
        first_line = s + x * '_' + (n - x) * ' '
        second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
        shifted_lines = [u * ' ' + line for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

    # Two children
    left, n, p, x = build_tree_structure(node.left)
    right, m, q, y = build_tree_structure(node.right)
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


def increment_operations(operations, action, value=1):
    """
    Count insert, delete and search operations on BST and AVL trees
    """

    operations[action] = operations[action] + value


class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class BSTree:
    operations = 0

    def __init__(self):
        self.primitive_operations = 0

    def insert(self, root, data):

        self.primitive_operations += 1

        if not root:
            return Node(data)

        elif data < root.data:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)

        # Update the height of the parent nodes
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        return root

    def search(self, root, data):

        self.primitive_operations += 1

        # Base Cases: root is null or data is present at root
        if root is None or root.data == data:
            return root

        # Key is greater than root's data
        if root.data < data:
            return self.search(root.right, data)

        # Key is smaller than root's data
        return self.search(root.left, data)

    def delete(self, root, data):

        self.primitive_operations += 1

        # Base Case
        if root is None:
            return root

        if data < root.data:
            root.left = self.delete(root.left, data)

        elif data > root.data:
            root.right = self.delete(root.right, data)

        else:

            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                return temp

            elif root.right is None:
                temp = root.left
                return temp

            temp = self.min_value_node(root.right)
            root.data = temp.data
            root.right = self.delete(root.right, temp.data)

        return root

    def get_height(self, root):
        """
        Get height of a tree
        """

        self.primitive_operations += 1

        if not root:
            return 0

        return root.height

    def min_value_node(self, node):

        current = node

        while current.left is not None:
            self.primitive_operations += 1
            current = current.left

        return current

    def print_tree(self, root):
        """
        Build and return a string representation of a tree
        """

        string = ''

        if not root:
            return '>> Empty tree\n'

        lines, a, b, c = build_tree_structure(root)
        for line in lines:
            # print(line)
            string += '{0}\n'.format(line)

        return string


class AVLTree:
    rotation_type = ''

    def __init__(self):
        self.primitive_operations = 0

    def insert(self, root, data):

        self.primitive_operations += 1

        # Perform BST
        if not root:
            return Node(data)
        elif data < root.data:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)

        # Update parent height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Get balance
        balance = self.get_balance(root)

        # Perform rotations
        # Left Left
        if balance > 1 and data < root.left.data:
            AVLTree.rotation_type += 'Left-Left'
            return self.left_left(root)

        # Right Right
        if balance < -1 and data > root.right.data:
            AVLTree.rotation_type += 'Right-Right'
            return self.right_right(root)

        # Left Right
        if balance > 1 and data > root.left.data:
            AVLTree.rotation_type += 'Left-Right'
            return self.left_right(root)

        # Right Left
        if balance < -1 and data < root.right.data:
            AVLTree.rotation_type += 'Right-Left'
            return self.right_left(root)

        return root

    def search(self, root, data):

        self.primitive_operations += 1

        # Empty tree/ data in root
        if root is None or root.data == data:
            return root

        # Search value > current node data
        if root.data < data:
            return self.search(root.right, data)

        # Search value < current node data
        else:
            return self.search(root.left, data)

    def delete(self, root, data):

        self.primitive_operations += 1

        # Perform BST delete
        if not root:
            return root

        # Delete value < current node data
        elif data < root.data:
            root.left = self.delete(root.left, data)

        # Delete value > current node data
        elif data > root.data:
            root.right = self.delete(root.right, data)

        # Get and delete node if exists
        else:
            if root.left is None:
                temp = root.right
                return temp

            elif root.right is None:
                temp = root.left
                return temp

            temp = self.min_value_node(root.right)
            root.data = temp.data
            root.right = self.delete(root.right, temp.data)

        if root is None:
            return root

        # Update parent height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Get balance
        balance = self.get_balance(root)

        # Perform rotations
        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            AVLTree.rotation_type += 'Left-Left'
            return self.left_left(root)

        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            AVLTree.rotation_type += 'Right-Right'
            return self.right_right(root)

        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            AVLTree.rotation_type += 'Left-Right'
            return self.left_right(root)

        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            AVLTree.rotation_type += 'Right-Left'
            return self.right_left(root)

        return root

    def min_value_node(self, node):
        """
        Gen minimum value from node's subtrees
        """

        current = node

        while current.left is not None:
            self.primitive_operations += 1
            current = current.left

        return current

    def right_right(self, node_3):
        """
        Left rotation
        """

        self.primitive_operations += 1

        node_2 = node_3.right
        temp = node_2.left

        # Perform rotation
        node_2.left = node_3
        node_3.right = temp

        # Update heights
        node_3.height = 1 + max(self.get_height(node_3.left), self.get_height(node_3.right))
        node_2.height = 1 + max(self.get_height(node_2.left), self.get_height(node_2.right))

        # Return the new root
        return node_2

    def left_left(self, node_3):
        """
        Right rotation
        """

        self.primitive_operations += 1

        node_2 = node_3.left
        temp = node_2.right

        # Perform rotation
        node_2.right = node_3
        node_3.left = temp

        # Update heights
        node_3.height = 1 + max(self.get_height(node_3.left), self.get_height(node_3.right))
        node_2.height = 1 + max(self.get_height(node_2.left), self.get_height(node_2.right))

        # Return the new root
        return node_2

    def left_right(self, node):
        """
        Left + Right rotation
        """

        self.primitive_operations += 1

        node.left = self.right_right(node.left)

        return self.left_left(node)

    def right_left(self, node):
        """
        Right + Left rotation
        """

        self.primitive_operations += 1

        node.right = self.left_left(node.right)

        return self.right_right(node)

    def get_height(self, root):
        """
        Return height of a tree
        """

        self.primitive_operations += 1

        if not root:
            return 0

        return root.height

    def get_balance(self, root):
        """
        Calculate balance factor for AVL tree
        """

        if not root:
            self.primitive_operations += 1
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

    def print_tree(self, root):
        """
        Build and return a string representation of a tree
        """

        string = ''

        if not root:
            return '>> Empty tree\n'

        lines, a, b, c = build_tree_structure(root)
        for line in lines:
            string += '{0}\n'.format(line)

        return string


def process_test_case(test_case_number):

    # Pre-defined test cases
    test_case_name = test_names_map[test_case_number]
    input_1_file_path = '{0}/data/input/test_case_{1}/input_{1}_1.txt'.format(program_root, test_case_number)
    input_2_file_path = '{0}/data/input/test_case_{1}/input_{1}_2.txt'.format(program_root, test_case_number)
    output_1_file_path = '{0}/data/output/test_case_{1}/output_{1}_1.txt'.format(program_root, test_case_number)
    output_2_file_path = '{0}/data/output/test_case_{1}/output_{1}_2.txt'.format(program_root, test_case_number)

    # Prepare reports
    bst_message = 'BST Test Case {0}: {1}\n\n'.format(test_case_number, test_case_name)
    avl_message = 'AVL Test Case {0}: {1}\n\n'.format(test_case_number, test_case_name)
    bst_operations = {'S': 0, 'I': 0, 'D': 0}
    avl_operations = {'S': 0, 'I': 0, 'D': 0}

    # Read inputs
    file_error = None
    if not os.path.exists(input_1_file_path):
        file_error = True
        bst_message += 'File read error! Input 1 is missing.\n'
        avl_message += 'File read error! Input 1 is missing.\n'
    if not os.path.exists(input_2_file_path):
        file_error = True
        bst_message += 'File read error! Input 2 is missing.\n'
        avl_message += 'File read error! Input 2 is missing.\n'

    # Process inputs
    if not file_error:

        with open(input_1_file_path, 'r') as data:
            input_1 = data.readlines()

        with open(input_2_file_path, 'r') as data:
            input_2 = data.readlines()

        # Create empty tree objects for BST and AVL
        bst_tree = BSTree()
        avl_tree = AVLTree()
        bst_root = None
        avl_root = None

        bst_message += '### Building tree ###\n'
        avl_message += '### Building tree ###\n'

        # Build a BST and AVL trees
        if input_1:
            for number in input_1:
                number = int(number)
                AVLTree.rotation_type = ''

                # Insert
                bst_root = bst_tree.insert(bst_root, number)
                avl_root = avl_tree.insert(avl_root, number)
                bst_operations['I'] = bst_tree.primitive_operations
                avl_operations['I'] = avl_tree.primitive_operations

                # Report BST
                bst_message += 'Insert: {}\n'.format(number)
                bst_message += bst_tree.print_tree(bst_root)
                bst_message += 'Tree height: {}\n'.format(bst_tree.get_height(bst_root) - 1)
                bst_message += '------------------------\n\n'

                # Report AVL
                avl_message += 'Insert: {}\n'.format(number)
                avl_message += avl_tree.print_tree(avl_root)
                avl_message += 'Rotation operation: {}\n'.format(AVLTree.rotation_type)
                avl_message += 'Tree height: {}\n'.format(avl_tree.get_height(avl_root) - 1)
                avl_message += '------------------------\n\n'


        else:
            # Record input 1 error
            bst_message += 'Data error! Input 1 is empty.\n'
            avl_message += 'Data error! Input 1 is empty.\n'

        bst_message += '### Operations ###\n'
        avl_message += '### Operations ###\n'

        # Preform operations on trees
        if input_2:
            # AVLTree.rotations_count = 0
            for code in input_2:
                action, number = code.split(' ')
                number = int(number)
                AVLTree.rotation_type = ''
                bst_tree.primitive_operations = 0
                avl_tree.primitive_operations = 0

                if action not in operation_map.keys():
                    bst_message += 'Operation error! Wrong action {}, skipped\n'.format(action)
                    avl_message += 'Operation error! Wrong action {}, skipped\n'.format(action)
                    continue

                if action == 'I':
                    bst_root = bst_tree.insert(bst_root, number)
                    avl_root = avl_tree.insert(avl_root, number)
                    bst_operations['I'] += bst_tree.primitive_operations
                    avl_operations['I'] += avl_tree.primitive_operations

                if action == 'S':
                    bst_tree.search(bst_root, number)
                    avl_tree.search(avl_root, number)
                    bst_operations['S'] += bst_tree.primitive_operations
                    avl_operations['S'] += avl_tree.primitive_operations

                if action == 'D':
                    bst_root = bst_tree.delete(bst_root, number)
                    avl_root = avl_tree.delete(avl_root, number)
                    bst_operations['D'] += bst_tree.primitive_operations
                    avl_operations['D'] += avl_tree.primitive_operations

                bst_message += '{0}: {1}\n'.format(operation_map[action], number)
                bst_message += bst_tree.print_tree(bst_root)
                bst_message += 'Tree height: {}\n'.format(bst_tree.get_height(bst_root) - 1)
                bst_message += '------------------------\n'

                avl_message += '{0}: {1}\n'.format(operation_map[action], number)
                avl_message += avl_tree.print_tree(avl_root)
                avl_message += 'Rotation operation: {}\n'.format(AVLTree.rotation_type)
                avl_message += 'Tree height: {}\n'.format(bst_tree.get_height(avl_root) - 1)
                avl_message += '------------------------\n'

        else:
            # Record input 2 error
            bst_message += 'Data error! Input 2 is empty.\n'
            avl_message += 'Data error! Input 2 is empty.\n'

    # Record results
    if not os.path.exists(os.path.dirname(output_1_file_path)):
        os.makedirs(os.path.dirname(output_1_file_path))

    # Operations report
    values = [[bst_operations['S'], avl_operations['S']],
              [bst_operations['I'], avl_operations['I']],
              [bst_operations['D'], avl_operations['D']]]

    operations_message, sum_bst, sum_avl = build_operation_table(test_case_name, values)

    # BST report
    # print bst_message
    with open(output_1_file_path, 'w') as output_1:
        output_1.write(bst_message)
        output_1.write('\n\n')
        output_1.write(operations_message)

    # AVL report
    # print avl_message
    with open(output_2_file_path, 'w') as output_2:
        output_2.write(avl_message)
        output_2.write('\n\n')
        output_2.write(operations_message)

    print operations_message

    return sum_bst, sum_avl


def run_processing():
    """
    The entry point of a program.
    Run trees and reports generation for test cases from test_names_map dictionary.
    """

    # Summary operations data
    summary_file_path = '{0}/data/output/summary_output.txt'.format(program_root)
    values = []

    # Iterate over all test cases
    for test_case_number in test_names_map.keys():

        sum_bst, sum_avl = process_test_case(test_case_number)
        value = [test_case_number, test_names_map[test_case_number], sum_bst, sum_avl]
        values.append(value)

    # Output summary
    summary = build_summary_table(values)
    print summary
    with open(summary_file_path, 'w') as output_1:
        output_1.write(summary)


if __name__ == "__main__":
    run_processing()
