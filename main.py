import screen as s
import board as b
import player as p
import curses as c

screen = s.Screen()
screen.maximize_console()
term = screen.initialize_blessed()

board = b.Board(screen.ask_dimensions()) #initializes board with dimension
print(term.clear)

player_controller = p.Player_Controller()
board.player_controller = player_controller

with term.hidden_cursor(): #main terminal control loop
    print(term.clear)
    board.print_board(term)
    player_controller.print_player_scores(term,board)

    while not player_controller.check_won():
        player_controller.take_turn(term,board)
