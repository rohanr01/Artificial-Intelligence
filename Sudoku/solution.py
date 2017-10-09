assignments = []



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    #Eliminate values using the naked twins strategy.
   
    #identify possible naked twin candidates 
    possible_candidates = []
    for box in values.keys():
        if(len(values[box]) == 2):
            possible_candidates.append(box)
    
    #find pairs of naked twins from possible candidate list by checking for same values in peer list        
    naked_twins = []
    for b1 in possible_candidates:
        for b2 in peers[b1]:
            if(set(values[b1]) == set(values[b2])):
                naked_twins.append([b1,b2])
    
    #iterate through list of naked twins and delete naked_twin values from common peers
    for nt in range(len(naked_twins)):
        b1 = naked_twins[nt][0]
        b2 = naked_twins[nt][1]
        peers1 = set(peers[b1])
        peers2 = set(peers[b2])
        peers_intersection = peers1 & peers2
        for peer_value in peers_intersection:
            if(len(values[peer_value])>=2):
                for v in values[b1]:
                    values = assign_value(values, peer_value, values[peer_value].replace(v,''))
    
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def grid_values(grid):
    
    #Convert grid into a dict of {square: char} with '123456789' for empties.
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    keys = boxes
    values = list(grid)
    for i in range(len(values)):
        if(values[i] == "."):
            values[i] = "123456789"
    dictionary = dict(zip(keys, values))
    return dictionary

def display(values):
    
    #Display the values as a 2-D grid.
    rows = 'ABCDEFGHI'
    cols = '123456789'
    boxes = cross(rows, cols)
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return



def eliminate(values):
    #for all cells with single values, eliminate these values from their peers
    #first we identify boxes with single values
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    #here we remove these values from the box's peers
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    #When you have a number that only appears in one box amongst it's peers of multi-value boxes, you can solve that box by making that value teh choice for the box 
    #we take lists of peers (rows, columns and squares) and solve for only_choice in each of these lists
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        #Using Eliminate Strategy
        values = eliminate(values)
        # Using the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    
    # Use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    if values is False:
        return False ## Failed earlier
    if all(len(values[b]) == 1 for b in boxes): 
        return values ## Solved!
    n,b = min((len(values[b]), b) for b in boxes if len(values[b]) > 1)
    #print(n)
    for value in values[b]:
        new_sudoku = values.copy()
        new_sudoku[b] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt  

def solve(grid):
    #Solve the sudoku puzzle by first converting the grid to a matrix representation of numbers
    values = grid_values(grid)
    # Use depth first search along with elimination and only_choice algorithms to solve the puzzle
    return search(values)

#define various cells, boxes and lists of peers to use in code
rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

#add in 2 lists of diagonal peer boxes to fulfill the diagonal constraint
diagonal_units = [[r+c for r,c in zip(rows,cols)],[r+c for r,c in zip(rows,cols[::-1])]]
#create master list of all possible peer lists by combining row lists, column lists, square lists and diagonal lists
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
