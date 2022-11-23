from environments.freestyle import Board

board = Board()
to_place = 1

col_map = {1: 'Black', -1: 'White'}

while True:
    board.display()
    print(col_map[to_place], ', your turn.')
    where = tuple(map(int, input("Enter next pos: ").split()))
    board.place(where, to_place)
    is_over = board.is_over()
    to_place *= -1
    if is_over:
        print('The winner is: ', col_map[to_place])