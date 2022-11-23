from environments.freestyle import Board

board = Board()
to_place = 1

while True:
    board.display()
    print(board.last_placed)
    where = tuple(map(int, input("Enter next pos:").split()))
    board.place(where, to_place)
    to_place *= -1