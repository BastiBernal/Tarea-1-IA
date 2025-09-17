def reconstruct_path(current_node):
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
    return path[::-1]

def valid_move(maze, position):
    x, y = position
    rows, cols = maze.shape

    possible_moves = [
        (0, 1), (0, -1),       # Right, Left
        (1, 0), (-1, 0)        # Down, Up
    ]

    return [
        (x + nx, y + ny) for nx, ny in possible_moves
        if 0 <= x + nx < rows and 0 <= y + ny < cols
        and maze[x + nx, y + ny] != 1
    ]