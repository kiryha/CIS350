"""
IS 350 Program 1
Python version: 2.7

# Scope
Build BST and AVL trees

# Credentials
Student: Kyrylo Krysko
Date started: 10/14/2021
"""
import math
import os

# Common variables
program_root = os.path.dirname(os.path.abspath(__file__))


def build_strings(node):
    """
    Returns list of strings, width, height, and horizontal coordinate of the root for printing tree
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
        lines, n, p, x = build_strings(node.left)
        s = '{}'.format(node.data)
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
        second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
        shifted_lines = [line + u * ' ' for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

    # Only right child
    if node.left is None:
        lines, n, p, x = build_strings(node.right)
        s = '{}'.format(node.data)
        u = len(s)
        first_line = s + x * '_' + (n - x) * ' '
        second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
        shifted_lines = [u * ' ' + line for line in lines]
        return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

    # Two children
    left, n, p, x = build_strings(node.left)
    right, m, q, y = build_strings(node.right)
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


class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class BSTree:
    def insert(self, root, data):

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

        # Base Cases: root is null or data is present at root
        if root is None or root.data == data:
            return root

        # Key is greater than root's data
        if root.data < data:
            return self.search(root.right, data)

        # Key is smaller than root's data
        return self.search(root.left, data)

    def delete(self, root, data):

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
                # root = None
                return temp

            elif root.right is None:
                temp = root.left
                # root = None
                return temp

            temp = self.min_value_node(root.right)
            root.data = temp.data
            root.right = self.delete(root.right, temp.data)

        return root

    def get_height(self, root):

        if not root:
            return 0

        return root.height

    def min_value_node(self, node):

        current = node

        while current.left is not None:
            current = current.left

        return current

    def print_tree(self, root):

        if not root:
            print '>> Empty tree'
            return

        lines, a, b, c = build_strings(root)
        for line in lines:
            print(line)


class AVLTree:
    def insert(self, root, data):

        # Perform BST
        if not root:
            return Node(data)
        elif data < root.data:
            root.left = self.insert(root.left, data)
        else:
            root.right = self.insert(root.right, data)

        # Update the height of the parent nodes
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Get the balance factor
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and data < root.left.data:
            return self.left_left(root)

        # Right Right
        if balance < -1 and data > root.right.data:
            return self.right_right(root)

        # Left Right
        if balance > 1 and data > root.left.data:
            return self.left_right(root.left)

        # Right Left
        if balance < -1 and data < root.right.data:
            return self.right_left(root.right)

        return root

    def search(self, root, data):

        # Base Cases: root is null or data is present at root
        if root is None or root.data == data:
            return root

        # Key is greater than root's data
        if root.data < data:
            return self.search(root.right, data)

        # Key is smaller than root's data
        return self.search(root.left, data)

    def delete(self, root, data):

        # Step 1 - Perform standard BST delete
        if not root:
            return root

        elif data < root.data:
            root.left = self.delete(root.left, data)

        elif data > root.data:
            root.right = self.delete(root.right, data)

        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            temp = self.min_value_node(root.right)
            root.data = temp.data
            root.right = self.delete(root.right, temp.data)

        if root is None:
            return root

        # Step 2 - Update the height of the parent node
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Step 3 - Get the balance factor
        balance = self.get_balance(root)

        # Left Left
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.left_left(root)

        # Right Right
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.right_right(root)

        # Left Right
        if balance > 1 and self.get_balance(root.left) < 0:
            return self.left_right(root.left)

        # Right Left
        if balance < -1 and self.get_balance(root.right) > 0:
            return self.right_left(root.right)

        return root

    def min_value_node(self, node):

        current = node

        while current.left is not None:
            current = current.left

        return current

    def right_right(self, node_3):

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
        """ Right rotate """

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

        node.left = self.right_right(node.left)
        return self.left_left(node)

    def right_left(self, node):

        node.right = self.left_left(node.right)
        return self.right_right(node)

    def get_height(self, root):

        if not root:
            return 0

        return root.height

    def get_balance(self, root):

        if not root:
            return 0

        return self.get_height(root.left) - self.get_height(root.right)

    def print_tree(self, root):

        if not root:
            print '>> Empty tree'
            return

        lines, a, b, c = build_strings(root)
        for line in lines:
            print(line)


def main():

    test_case_number = '2'
    test_case_name = 'Test Case Name'
    input_1_file_path = '{0}/data/input/test_case_{1}/input_{1}_1.txt'.format(program_root, test_case_number)
    input_2_file_path = '{0}/data/input/test_case_{1}/input_{1}_2.txt'.format(program_root, test_case_number)

    with open(input_1_file_path, 'r') as data:
        input_1 = data.readlines()

    with open(input_2_file_path, 'r') as data:
        input_2 = data.readlines()

    bst_tree = BSTree()
    avl_tree = AVLTree()
    bst_root = None
    avl_root = None

    # Build a tree
    for number in input_1:
        number = int(number)
        bst_root = bst_tree.insert(bst_root, number)
        avl_root = avl_tree.insert(avl_root, number)

    # Preform operations
    for code in input_2:
        action, number = code.split(' ')
        number = int(number)

        if action == 'I':
            bst_root = bst_tree.insert(bst_root, number)
            avl_root = avl_tree.insert(avl_root, number)

        if action == 'I':
            bst_root = bst_tree.insert(bst_root, number)
            avl_root = avl_tree.insert(avl_root, number)

        if action == 'I':
            bst_root = bst_tree.insert(bst_root, number)
            avl_root = avl_tree.insert(avl_root, number)

    # print '>> BST: '
    # # bst_root = bst_tree.delete(bst_root, 30)
    # # bst_root = bst_tree.insert(bst_root, 25)
    # bst_tree.print_tree(bst_root)
    # print 'tree height = ', bst_tree.get_height(bst_root) - 1
    # print '>> AVL: '
    # avl_tree.print_tree(avl_root)
    # print 'tree height = ', avl_tree.get_height(avl_root) - 1


main()
