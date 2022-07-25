import queue
def check(board, r1, c1, r2, c2, q):
    if board[r2][c2] == 'M':
        board[r1][c1] += 1
    elif board[r2][c2] == 'E':
        q.append([r2, c2])
    # return board, q


def bfs(board, r, c):
    m = len(board)
    n = len(board[0])
    board[r][c] = 0
    que = queue.Queue()
    que.put([r, c])
    while not que.empty():
        r, c = que.get()
        q = []
        if r - 1 >= 0:  # up
            check(board, r, c, r - 1, c, q)
            if c - 1 >= 0:  # up left
                check(board, r, c, r - 1, c - 1, q)
            if c + 1 < n:  # up right
                check(board, r, c, r - 1, c + 1, q)
        if r + 1 < m:  # down
            check(board, r, c, r + 1, c, q)
            if c - 1 >= 0:  # down left
                check(board, r, c, r + 1, c - 1, q)
            if c + 1 < n:  # down right
                check(board, r, c, r + 1, c + 1, q)
        if c - 1 >= 0:
            check(board, r, c, r, c - 1, q)
        if c + 1 < n:
            check(board, r, c, r, c + 1, q)

        if board[r][c] == 0:
            board[r][c] = 'B'
            for rc in q:
                que.put(rc)
                board[rc[0]][rc[1]] = 0


def updateBoard(board, click):
    if board[click[0]][click[1]] == 'M':
        board[click[0]][click[1]] = 'X'
    else:
        bfs(board, click[0], click[1])
    return board

print(updateBoard([["E","E","E","E","E"],["E","E","M","E","E"],["E","E","E","E","E"],["E","E","E","E","E"]],[3,0]))