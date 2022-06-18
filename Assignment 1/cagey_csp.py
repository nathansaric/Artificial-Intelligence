# =============================
# Student Names: Hannah Larsen, Nathan Saric
# Group ID: Group 13
# Date: February 13, 2022
# =============================
# cagey_csp.py
# desc: A file containing cagey methods that given a cagey board, will construct
# the variables and constraints of the csp and return a csp object and list of variables.

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all variables in the given csp. If you are returning an entire grid's worth of variables
they should be arranged in a linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 20/100 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
|n^2-n-1| n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
import itertools

def binary_ne_grid(cagey_grid):

    # Creating the domain of the binary_ne_grid CSP
    # domain is a list of numbers from 1 to n, where n is the size of the Cagey grid
    domain = []
    for i in range(cagey_grid[0]):
        domain.append(i+1)

    # Creating the variables of the binary_ne_grid CSP 
    # var_array is a list of grid cells from (1,1) to (n,n), where n is the size of the Cagey grid
    # grid_vars is a list of lists that stores each grid row as its own list from row 1 to n, where n is the size of the Cagey grid
    # grid_vars is used for grid cell indexing when creating the constraints of the CSP
    var_array, grid_vars = [], []
    for row in domain:
        grid_vars.append([]) # new row

        for col in domain:
            cell = Variable("Cell({},{})".format(row, col), domain)
            grid_vars[row-1].append(cell)
            var_array.append(cell)

    # Creating the constraints of the binary_ne_grid CSP
    # constraints is a list of lists that stores each pair of grid cells that cannot have the same value as its own list
    # satisfying_tuples is a list of tuples that each pair of grid cells can have that will satisfy the constraints
    constraints = []
    satisfying_tuples = list(itertools.permutations(domain, 2))
    for i in range(len(domain)):
        for j in range(len(domain)):
            for k in range(j + 1, len(domain)):
                
                # constraint_row ensure that a value is not repeated within a given row
                constraint_row = Constraint("C(Cell({},{}), Cell({},{}))".format(i+1, j+1, i+1, k+1), [grid_vars[i][j], grid_vars[i][k]])
                constraint_row.add_satisfying_tuples(satisfying_tuples)
                constraints.append(constraint_row)

                # constraint_col ensures that a values is not repeated within a given column
                constraint_col = Constraint("C(Cell({},{}), Cell({},{}))".format(j+1, i+1, k+1, i+1), [grid_vars[j][i], grid_vars[k][i]])
                constraint_col.add_satisfying_tuples(satisfying_tuples)
                constraints.append(constraint_col)

    # Creating the CSP object for the binary_ne_grid CSP and adding each constraint 
    csp = CSP("{}-Cagey-binary-ne".format(cagey_grid[0]), var_array)
    for constraint in constraints:
        csp.add_constraint(constraint)
    
    # Returns the CSP object and the list of variables
    return csp, var_array

def nary_ad_grid(cagey_grid):
    
    # Creating the domain of the nary_ne_grid CSP
    # domain is a list of numbers from 1 to n, where n is the size of the Cagey grid
    domain = []
    for i in range(cagey_grid[0]):
        domain.append(i+1)

    # Creating the variables of the nary_ne_grid CSP 
    # var_array is a list of grid cells from (1,1) to (n,n), where n is the size of the Cagey grid
    # grid_vars is a list of lists that stores each grid row as its own list from row 1 to n, where n is the size of the Cagey grid
    # grid_vars is used for grid cell indexing when creating the constraints of the CSP
    var_array, grid_vars = [], []
    for row in domain:
        grid_vars.append([]) # new row

        for col in domain:
            cell = Variable("Cell({},{})".format(row, col), domain)
            grid_vars[row-1].append(cell)
            var_array.append(cell)
    
    # Creating the constraints of the nary_ne_grid CSP
    # constraints is a list of lists that stores each row or column in the grid that must have all different values from the domain
    # satisfying_tuples is a list of tuples that each row or column in the grid  can have that will satisfy the constraints
    constraints = []
    satisfying_tuples = list(itertools.permutations(domain, cagey_grid[0]))

    for i in range(len(domain)):
        grid_row, grid_col = [], [] # new row and column

        for j in range(len(domain)):
            grid_row.append(grid_vars[i][j])
            grid_col.append(grid_vars[j][i])

        # constraint_row ensure that a value is not repeated within a given row
        constraint_row = Constraint("C(Row{}))".format(i+1), grid_row)
        constraint_row.add_satisfying_tuples(satisfying_tuples)
        constraints.append(constraint_row)

        # constraint_col ensures that a value is not repeated within a given column
        constraint_col = Constraint("C(Col{}))".format(i+1), grid_col)
        constraint_col.add_satisfying_tuples(satisfying_tuples)
        constraints.append(constraint_col)

    # Creating the CSP object for the nary_ne_grid CSP and adding each constraint 
    csp = CSP("{}-Cagey-nary-ad".format(cagey_grid[0]), var_array)
    for constraint in constraints:
        csp.add_constraint(constraint)
    
    # Returns the CSP object and the list of variables
    return csp, var_array    

def cagey_csp_model(cagey_grid):
    
    # Creating the domain of the cagey_csp_model
    # domain is a list of numbers from 1 to n, where n is the size of the Cagey grid
    domain = []
    for i in range(cagey_grid[0]):
        domain.append(i+1)

    # Creating the variables of the cagey_csp_model
    # var_array is a list of grid cells from (1,1) to (n,n), where n is the size of the Cagey grid
    # The csp model is also returned from the binary_ne_grid function to add additional cage constraints
    # grid_vars is a list of lists that stores each grid row as its own list from row 1 to n, where n is the size of the Cagey grid
    # grid_vars is used for grid cell indexing when creating the additional variables and constraints of the CSP
    csp, var_array = binary_ne_grid(cagey_grid)
    grid_vars = [var_array[i:i + cagey_grid[0]] for i in range(0, len(var_array), cagey_grid[0])]

    # Creating the additional cage constraints of the cagey_csp_model
    # constraints is a list of lists that stores all of the cells that belong to a given cage in the grid
    # satisfying_tuples is a list of tuples that the cells of a given cage in the grid can have that will satisfy the constraints
    constraints = []
    cage_num = 0
    
    for cage in cagey_grid[1]:
        satisfying_tuples, cage_cell_vars = [], []
        cage_num += 1
        cage_value = cage[0]
        cage_cells = cage[1]
        operation = cage[2]
        
        for cell in cage_cells:
            cell_row = cell[0] - 1
            cell_col = cell[1] - 1
            cage_cell_vars.append(grid_vars[cell_row][cell_col])

        constraint_cage = Constraint("Cage{}".format(cage_num), cage_cell_vars)

        # Creating additional variable that represents the cage with respect to its value, the operation, and the cage cells
        cage_operand = Variable("Cage_op({}:{}:{})".format(cage_value, operation, cage_cell_vars), cage_cell_vars)
        var_array.append(cage_operand)

        # The cage includes only one cell, so the value of the cell must be equal to the value of the cage
        if len(cage_cells) == 1:
            satisfying_tuples.append([cage_value])

        # The cage includes more than one cell, so the value of the cell and the operation are checked against the cells in the cage
        else:
            tuples = list(itertools.product(domain, repeat=len(cage_cells)))
            for tuple in tuples: 
                if operationCheck(cage_value, tuple, operation):
                    satisfying_tuples.append(tuple)

        constraint_cage.add_satisfying_tuples(satisfying_tuples)
        constraints.append(constraint_cage)
    
    # Adding the additional cage constraints to the binary_ne_grid CSP model
    for constraint in constraints:
        csp.add_constraint(constraint)
    
    # Returns the CSP object and the list of variables
    return csp, var_array    

def operationCheck(cagevalue, tuple, operation):

    # Determines if the sum of the values in the tuple is equal to the cage value
    # Returns true if equal and false otherwise
    if operation == '+':
        addition = 0
        for value in tuple:
            addition += value
        return (addition == cagevalue)
    
    # Determines if there exists a difference of the values in the tuple that is equal to the cage value
    # Returns true if equal and false otherwise
    elif operation == '-':
        for permutation in itertools.permutations(tuple):
            subtraction = permutation[0]
            for value in range(1, len(permutation)):
                subtraction -= permutation[value]
            if subtraction == cagevalue:
                return True
        return False
    
    # Determines if the product of the values in the tuple is equal to the cage value
    # Returns true if equal and false otherwise
    elif operation == '*':
        multiplication = 1
        for value in tuple:
            multiplication *= value
        return (multiplication == cagevalue)

    # Determines if there exists a quotient of the values in the tuple that is equal to the cage value
    # Returns true if equal and false otherwise
    elif operation == '/':
        for permutation in itertools.permutations(tuple):
            division = permutation[0]
            for value in range(1, len(permutation)):
                division /= permutation[value]
            if division == cagevalue:
                return True
        return False
    
    # Determines if any of the operations applied to the values in the tuple is equal to the cage value
    # Returns true if equal and false otherwise
    elif operation == '?':
        if (operationCheck(cagevalue, tuple, '+') or 
            operationCheck(cagevalue, tuple, '-') or 
            operationCheck(cagevalue, tuple, '*') or 
            operationCheck(cagevalue, tuple, '/')):
            return True
        return False