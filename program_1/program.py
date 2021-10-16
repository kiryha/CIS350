"""
CIS 350 Program 1

Python version: 2.7
Read the code from the bottom to top

# Scope
Process and evaluate expressions provided in the input text file
Record processing and evaluation results in output file

Processing includes:
    - Validating input expression for correctness based on provided rules
    - Converting expression from infix to postfix notation and building expression tree from it
    - Print the validation results; the tree; expected output operations;
      tree traversal in prefix, infix and postfix order; expression evaluation results.

Input data files should be located in <script_root>/data/input folder
The resulting data would be saved to <script_root>/data/output

# Data
    - statements1.dat: source file with expressions provided in the assignment
    - statements2.dat: statements1.dat with long dash replaced with minus symbol
    - statements3.dat: additional expressions

# Validation report legend:
    <Unsupported symbol> - there are unsupported symbols in source expression (lowercase, 2 and more characters, etc)
    <Mismatched parenthesis> - incorrect parenthesis, not all opened parenthesis are opened and vice versa
    <Wrong spaces distribution> - only one space around each operator/operand rule is violated
    <Wrong operations> - incorrect expression in terms of operators and operand dependency


# Credentials
Student: Kyrylo Krysko
Date started: 9/16/2021
"""

import os


# Common variables
program_root = os.path.dirname(os.path.abspath(__file__))
precedence = {'(': 1, '+': 2, '-': 2, '*': 3, '/': 3, '^': 4}
operators = ['+', '-', '*', '/', '^']
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
numbers = '0123456789'


# Custom data structure class for the tree
class Node:
    """ The tree node object """
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None


# Data validation
def validate_operations(expression):
    """
    Check that:
        - every operator is followed by a variable or digit
        - every variable and digit is followed by an operator (except last in expression)
        - parenthesis is followed by operand (except last parenthesis in expression)

    Catch cases:
        # ( A + ) B #
        # ( A + B ) C #
        # C B #
        # C + - B #

    :param expression: string input infix expression
    :return: True if expression is valid in terms of operators/operands, False if not
    """

    # Create array of expression symbols without spaces
    symbols = []
    for symbol in expression.split(' '):
        if symbol != '':
            symbols.append(symbol)

    # Check conditions
    for index, symbol in enumerate(symbols):

        # Operator is followed by a variable or digit?
        if symbol in operators:

            # Catch operator at the beginning/end of expression
            if index == 0 or index + 1 == len(symbols):
                return False

            next_symbol = symbols[index+1]
            if not next_symbol.isalpha() and not next_symbol.isdigit() and next_symbol != '(':
                # Skip if next symbol is 2+ long
                if len(next_symbol) > 1:
                    continue
                return False

        # Variable or digit is followed by an operator
        if symbol in alphabet or symbol in numbers:

            # skip last element
            if index + 1 == len(symbols):
                continue

            next_symbol = symbols[index + 1]
            if next_symbol not in operators and next_symbol != ')':
                return False

        # If closing parenthesis not at the end it should follow by operator
        if symbol == ')':

            # skip last element
            if index + 1 == len(symbols):
                continue

            next_symbol = symbols[index + 1]
            if next_symbol not in operators and next_symbol != ')':
                return False

    return True


def validate_symbols(expression):
    """
    Validate if expression consists of single uppercase letter operands and single digits

    :param expression: string input infix expression
    :return: True if expression meets characters requirements, False if not
    """

    for symbol in expression.split(' '):
        if len(symbol) > 1:
            return False

    for symbol in expression.replace(' ', ''):

        if symbol not in operators and symbol not in '()' and symbol not in alphabet and symbol not in numbers:
            return

    return True


def validate_spaces(expression):
    """
    Validate spaces in expression:
         - Should starts/ends with the space,
         - only one space can be between symbols

    :param expression: string source expression
    :return: True if spaces correct, False if not
    """

    # Check if expression starts and ends with a space:
    if not expression.startswith(' ') or not expression.endswith(' '):
        return False

    # Check if there is no 2 or more spaces together
    expression_list = list(expression)
    for index, symbol in enumerate(expression_list):

        # Skip last symbol
        if index + 1 == len(expression_list):
            continue

        if symbol == ' ':
            if expression_list[index + 1] == ' ':
                return False

    return True


def validate_parenthesis(expression):
    """
    Check if a string contains valid parenthesis

    :param expression: string infix expression
    :return: True if parenthesis are valid, False if not
    """

    stack = []

    for character in expression:

        # Check only parenthesis
        if character not in ['(', ')']:
            continue

        if character == ')':
            if stack:
                last_element = stack.pop()
            else:
                last_element = ''

            if last_element != '(':
                return False
        else:
            stack.append(character)

    if not stack:
        return True


def validate_expression(expression):
    """
    Check the expression is meeting requirements:
        - allowed symbols (A-Z, 0-9, +-*/^)
        - parenthesis
        - spaces
        - correct operands and operators


    Combine all found errors into one validation report.
    If there are invalid symbols, skip looking for other errors

    :param expression: string input infix expression
    :return: True/False if expression valid/invalid, string validation report
    """

    result = True
    validation_report = 'Valid Statement'
    error_list = ''

    # Catch incorrect symbols (e.g. long dash) Skip further validation if found
    if not validate_symbols(expression):
        error_list += ' <Unsupported symbol>'
        result = False

    if not validate_parenthesis(expression):
        error_list += ' <Mismatched parenthesis>'
        result = False

    if not validate_spaces(expression):
        error_list += ' <Wrong spaces distribution>'
        result = False

    if not validate_operations(expression):
        error_list += ' <Wrong operations>'
        result = False

    if not result:
        validation_report = 'Invalid Statement: ' + error_list

    return result, validation_report


# Trees manipulations
def build_tree(postfix_expression):
    """
    Build a binary expression tree from postfix expression

    :param postfix_expression: string expression in postfix notation
    :return: binary expression tree
    """

    stack = []

    for symbol in postfix_expression:

        # Operand: simply push into stack
        if symbol not in operators:
            node = Node(symbol)
            stack.append(node)

        # Operator
        else:
            # Pop two top nodes
            node = Node(symbol)
            node1 = stack.pop()
            node2 = stack.pop()

            # make them children
            node.right = node1
            node.left = node2

            # Add this subexpression to stack
            stack.append(node)

    # Only element  will be the root of expression tree
    node = stack.pop()

    return node


def traverse_pre_order(node, preorder_expression=None):
    """
    Traverse expression tree in prefix order

    :param node: root of the tree
    :param preorder_expression: expression in preorder notation
    :return: expression in preorder notation
    """

    if not preorder_expression:
        preorder_expression = ''

    if node:
        # print node.data,
        preorder_expression += node.data
        preorder_expression = traverse_pre_order(node.left, preorder_expression)
        preorder_expression = traverse_pre_order(node.right, preorder_expression)

    return preorder_expression


def traverse_in_order(node, inorder_expression=None):
    """
    Traverse expression tree in infix order

    :param node: root of the tree
    :param inorder_expression: expression in inorder notation
    :return: expression in inorder notation
    """

    if not inorder_expression:
        inorder_expression = ''

    if node:
        inorder_expression = traverse_in_order(node.left, inorder_expression)
        inorder_expression += node.data
        inorder_expression = traverse_in_order(node.right, inorder_expression)

    return inorder_expression


def traverse_post_order(node, postorder_expression=None):
    """
    Traverse expression tree in postfix order

    :param node: root of the tree
    :param postorder_expression: expression in postorder notation
    :return: expression in postorder notation
    """

    if not postorder_expression:
        postorder_expression = ''

    if node:
        postorder_expression = traverse_post_order(node.left, postorder_expression)
        postorder_expression = traverse_post_order(node.right, postorder_expression)
        postorder_expression += node.data

    return postorder_expression


def print_tree(tree):
    """
    Traverse tree in level order and build a tree string for printing/saving to a file

    :param tree: expression stored i a binary tree
    :return: string with tree levels on separate lines
    """

    current_level = [tree]
    tree_string = ''

    while current_level:
        next_level = []

        for node in current_level:
            tree_string += node.data
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)

        tree_string += '\n'
        current_level = next_level

    return tree_string


# Expression processing
def expand_expression(prefix_expression):
    """
    Substitute A-Z letters in expression with numbers

    :param prefix_expression: string prefix expression with letters
    :return: string prefix expression with numbers and inner spaces
    """

    numeric_expression = ''

    for symbol in prefix_expression:

        if symbol in alphabet:
            numeric_expression += ' {}'.format(int(alphabet.index(symbol)) + 1)
        else:
            numeric_expression += ' {}'.format(symbol)

    return numeric_expression.strip()


def evaluate_prefix_expression(prefix_expression):
    """
    Evaluate prefix expression

    :param prefix_expression: string prefix expression with numbers as operands
    :return: string numerical value of solved expression
    """

    stack = []
    prefix_expression = prefix_expression.split(' ')

    # Iterate over the string in reverse order
    for symbol in prefix_expression[::-1]:

        if symbol.isdigit():
            stack.append(int(symbol))

        else:
            operand1 = stack.pop()
            operand2 = stack.pop()

            if symbol == '+':
                stack.append(operand1 + operand2)

            elif symbol == '-':
                stack.append(operand1 - operand2)

            elif symbol == '*':
                stack.append(operand1 * operand2)

            elif symbol == '/':
                if operand2 == 0:  # Catch ZERO division
                    return 'Zero division ERROR!'
                stack.append(operand1 / operand2)

            elif symbol == '^':
                stack.append(pow(operand1, operand2))

    return stack.pop()


def print_postfix_operations(postfix_expression):
    """
    Create and return a string list of operations from postfix expression

    :param postfix_expression: expression in postfix notation
    :return: list of operations
    """

    stack = []
    operations = ''

    for symbol in postfix_expression:

        if symbol in alphabet or symbol in numbers:
            stack.append(symbol)

        elif symbol in operators:

            operand1 = stack.pop()
            operand2 = stack.pop()

            if symbol == '+':
                stack.append(operand2 + operand1 + '+')
                operations += operand2 + operand1 + '+\n'

            elif symbol == '-':
                stack.append(operand2 + operand1 + '-')
                operations += operand2 + operand1 + '-\n'

            elif symbol == '*':
                stack.append(operand2 + operand1 + '*')
                operations += operand2 + operand1 + '*\n'

            elif symbol == '/':
                stack.append(operand2 + operand1 + '/')
                operations += operand2 + operand1 + '/\n'

            elif symbol == '^':
                stack.append(operand2 + operand1 + '^')
                operations += operand2 + operand1 + '^\n'

    return operations


def convert_to_postfix(expression):
    """
    Convert expression from infix to postfix notation

    :param expression: string infix expression
    :return: postfix expression
    """

    stack = []
    postfix_list = []

    for symbol in expression.split():
        if symbol in alphabet or symbol in numbers:
            postfix_list.append(symbol)
        elif symbol == '(':
            stack.append(symbol)
        elif symbol == ')':
            top_symbol = stack.pop()
            while top_symbol != '(':
                postfix_list.append(top_symbol)
                top_symbol = stack.pop()
        else:
            while stack and (precedence[stack[-1]] if stack else None) >= precedence[symbol]:
                postfix_list.append(stack.pop())
            stack.append(symbol)

    while stack:
        postfix_list.append(stack.pop())

    return ''.join(postfix_list)


def process_expression(source_expression):
    """
    Process expression:
        - convert source infix expression to a postfix notation
        - get list of output operations
        - create a tree from postfix expression
        - traverse the tree in prefix, infix and postfix order
        - output results to a file

    :param source_expression: validated expression from the source file
    :return: string expression evaluation report
    """

    # Process expression
    postfix_expression = convert_to_postfix(source_expression)
    operations = print_postfix_operations(postfix_expression)
    tree = build_tree(postfix_expression)
    prefix_expression = traverse_pre_order(tree)
    numeric_expression = expand_expression(prefix_expression)
    result = evaluate_prefix_expression(numeric_expression)

    # Write processing results to an output file
    evaluation_report = 'Expression tree:\n{}'.format(print_tree(tree))
    evaluation_report += 'Prefix notation: {}\n'.format(prefix_expression)
    evaluation_report += 'Infix notation: {}\n'.format(traverse_in_order(tree))
    evaluation_report += 'Postfix notation: {}\n'.format(traverse_post_order(tree))
    evaluation_report += 'Operations:\n{}'.format(operations)
    evaluation_report += 'Final result: {}\n'.format(result)

    return evaluation_report


def validate_and_process(expression):
    """
    Validate if expression meets assignment conditions, run expression processing if it is

    :param expression: string input expression
    :return: string report on validation and processing
    """

    # Remove new line character from string
    expression = expression.rstrip('\n')
    process_report = 'Input Line: #{}#\n'.format(expression)

    # Validate if expression meets conditions
    result, validation_report = validate_expression(expression)
    process_report += validation_report + '\n'

    print 'Current expression: #{}#'.format(expression)

    # Process expression if validated
    if result:
        evaluation_report = process_expression(expression)
        process_report += evaluation_report

    process_report += '\n\n'

    return process_report


def run_processing():
    """
    Main program function:
        - Ask user to enter file version to build input and output file names,
        - Process expression from provided file,
        - Write processing report to an output file.
    """

    output_report = 'Program started...\n'

    # Ask user for a file version. Build input/output file paths avoiding entering the full name for usability.
    input_file_version = raw_input('Enter the source file VERSION (1,2,3, etc.): ')
    input_file_path = '{0}/data/input/statements{1}.dat'.format(program_root, input_file_version)
    output_file_path = '{0}/data/output/output{1}.dat'.format(program_root, input_file_version)

    # Record input file name to output file
    output_report += 'Input file: {}\n'.format(input_file_path)

    # Process input file
    if os.path.exists(input_file_path):

        # Get the expressions data from input file
        with open(input_file_path, 'r') as data:
            expressions_data = data.readlines()

            # Process expressions if data exist, output error if not.
            if expressions_data:
                output_report += 'The content of the file read successfully!\n\n\n'

                for expression in expressions_data:
                    process_report = validate_and_process(expression)
                    output_report += process_report
            else:
                output_report += 'File content error. The input file is empty!\n'

    else:
        output_report += 'File read error. The input file does not exists!\n'

    # Record processing results to a file
    message = 'Expressions processing saved to: {}\n'.format(output_file_path)
    if not os.path.exists(os.path.dirname(output_file_path)):
        os.makedirs(os.path.dirname(output_file_path))

    with open(output_file_path, 'w') as data:
        data.write(output_report)
        data.write(message)
        data.write('Program complete!')

    print message


# The program execution starts here!
if __name__ == "__main__":
    run_processing()
