# binary tree search algorithm
import random

def binary_search(query, data, start, stop):
    """
    Run a recursive binary tree search.

    query : the number to search for
    data  : a sorted list of numbers
    start : starting index of range to search
    stop  : end index of range to search
    """
    if start == stop: # empty range
        return -1
    center = start + (stop - start) // 2
    if data[center] == query:
        return center
    elif ...:  # query is to the left of center
        return binary_search(query, data, start, center)
    else:      # query is to the right of center
        return ...


# prepare the index
random.seed(42)
data = [random.randint(1, 100) for i in range(25)]
data.sort()

# run the search
query = int(input('enter a number to search: '))
result = ...
if result > 0:
    print(f'found the number {query} in position {result}')
else:
    print(f'the number {query} was not found')

# tests
assert binary_search(1, [1], 0, 1) == 0
assert binary_search(3, [1,3,4], 0, 3) == 1
assert binary_search(4, [1,2,3,4], 0, 4) == 3
assert binary_search(4, [1,2,3,4,5], 0, 5) == 3
assert binary_search(4, [1,2,3,4,5], 0, 3) == -1
