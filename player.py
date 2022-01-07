import copy

class Player:

    def __init__(self,color='term.white',background_color=None,name='null'):
        self.color = color
        self.background_color = background_color
        self.name = name
        self.positions = [] #positions sucessfully occupied in sorted order, with each dot representing a coord
        self.score = 0
        self.score_location = None
        self.name_location = None

    def check_valid(self,key,term,board): #checks whether the movement attempt is valid
        cursor_p = board.cursor_pos
        if key == 'w':
            if cursor_p[1][0] - 1 < 0:
                return False
        elif key == 'a':
            if cursor_p[0][1] - 1 < 0:
                return False
        elif key == 's':
            if cursor_p[0][0] + 1 > board.rows - 1:
                return False
        elif key == 'd':
            if cursor_p[1][1] + 1 > board.cols - 1:
                return False
        elif key == ' ':
            if board.cursor_pos in board.taken_spots:
                return False
        return True

    def take_turn(self,term,board):
        key = None
        valid = False
        with term.cbreak():
            while key not in ['w','a','s','d','r',' '] or not valid:
                key = term.inkey()
                valid = self.check_valid(key,term,board)

        cursor_pos_copy = copy.deepcopy(board.cursor_pos)
        board.prev_cursor_pos = cursor_pos_copy
        if key == 'w': #up
            board.cursor_pos[0][0] -= 1
            board.cursor_pos[1][0] -= 1
        elif key == 'a': #left
            board.cursor_pos[0][1] -= 1 #complete
            board.cursor_pos[1][1] -= 1
        elif key == 's': #down
            board.cursor_pos[0][0] += 1
            board.cursor_pos[1][0] += 1
        elif key == 'd': #right
            board.cursor_pos[0][1] += 1
            board.cursor_pos[1][1] += 1
        elif key == 'r': #rotate
            if board.cursor_orientation == 'h':
                board.cursor_pos[0][0] += 1 #complete
                board.cursor_pos[1][1] -= 1
                board.cursor_orientation = 'v'
            else:
                board.cursor_pos[0][0] -= 1 #complete
                board.cursor_pos[1][1] += 1
                board.cursor_orientation = 'h'

        if key == ' ':
            valid = self.check_valid(key,term,board)
        else:
            valid = False

        board.update_board(self,term,key)
        return valid #turn not taken yet if false

class Player_Controller:

    player_list = []

    def __init__(self):
        self.initialize_players()
        self.previous_turn = None
        self.current_turn = 0 #index of current player turn in player_list
        self.turn_taken = False

    def check_won(self):
        pass

    def print_player_scores(self,term,board): #prints player scores immediately and saves score location to be updated by update_scores()
        #p1: 12    p2: 16    p3: 19
        total_name_length = 0
        for player in self.player_list:
            total_name_length += len(player.name)

        string_length = total_name_length + 4*((len(self.player_list)*2)-1)
        print(term.move_xy((term.width//2), (board.top_left[1]-2)) + term.move_left(string_length//2) ,end='',flush=True)

        for player in self.player_list:
            print(eval(player.color) + f"{player.name}: " + term.white + f"{player.score:<2}    ",end='',flush=True)
            r, c = term.get_location()
            player.score_location = [r,c-6]
            player.name_location = [r,c-(8+len(player.name))]

    def initialize_players(self): #TODO fix FUCNTION LATER

        num_players = 2 #ask input for num players
        colors = ['term.red','term.blue'] #just choose random colors later
        names = ['p1','p2'] #ask input for names
        background_colors = ["term.on_red","term.on_blue"]

        for i in range(num_players):
            player = Player(colors[i],background_colors[i],names[i])
            self.player_list.append(player)

    def take_turn(self,term,board):
        self.turn_taken = self.player_list[self.current_turn].take_turn(term,board)
        self.previous_turn = self.current_turn

        if self.current_turn + 1 > len(self.player_list)-1 and self.turn_taken:
            self.current_turn = 0
        elif self.turn_taken:
            self.current_turn += 1

        self.underline_turn(term)

    def underline_turn(self,term):

        if not self.turn_taken:
            return 0

        current_player = self.player_list[self.current_turn] #underline current player
        print(eval(current_player.color) + term.underline + term.move_xy((current_player.name_location[1]),(current_player.name_location[0])) + current_player.name + term.normal,end='',flush=True)

        previous_player = self.player_list[self.previous_turn] #remove underline from previous player
        print(eval(previous_player.color) + term.move_xy((previous_player.name_location[1]),(previous_player.name_location[0])) + previous_player.name + term.normal,end='',flush=True)

    def update_scores(self,term,player):
        print(term.white + term.move_xy((player.score_location[1]),(player.score_location[0])) + str(player.score),end='',flush=True)
