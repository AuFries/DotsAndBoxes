import time
import copy

class Board:

    taken_spots = [] #list of node combinations on board taken. In form [[[r1,c1],[r2,c2]]]
    won_boxes = [] #list of boxes on the board that have already been won

    def __init__(self,dimensions):
        self.rows = int(dimensions[0])
        self.cols = int(dimensions[1])
        self.cursor_pos = [[0,0],[0,1]] #a list containing where the cursor is between 2 points. Starts in the top left. Top point always 2nd
        self.prev_cursor_pos = [[0,0],[0,1]]
        self.cursor_orientation = "h" #h for horizontal, v for vertical
        self.top_left = None
        self.player_controller = None

    def print_board(self,term): #initially prints the board
        top_left = [((term.width - self.cols*5)//2), ((term.height - self.rows*2)//2)] #holds top left of board coords x and y in a list
        self.top_left = top_left
        print(term.move_xy(top_left[0],top_left[1]),end='')

        for i in range(self.rows*2):
            if i % 2 == 0:
                for j in range(self.cols):
                    if i == 0 and j == 0:
                        print("·"+term.lawngreen+"----"+term.normal,end='',flush=True)
                    else:
                        print("·    ",end='',flush=True)
                print(term.move_x(top_left[0]) + term.move_down(2), end='', flush=True)
                time.sleep(0.1)

    def move_player(self,player):
        cursor_pos_copy = copy.deepcopy(self.cursor_pos)
        player.positions.append(cursor_pos_copy)
        self.taken_spots.append(cursor_pos_copy)

    def get_player_color(self): #gets player color from previous cursor position
        for player in self.player_controller.player_list:
            if self.prev_cursor_pos in player.positions:
                return player.color

    def print_taken(self,term,dir=None):
        cursor_o = self.cursor_orientation
        color = self.get_player_color()

        if dir == 'r':
            if cursor_o == 'h':
                cursor_o = 'v'
            else:
                cursor_o = 'h'

        if self.prev_cursor_pos in self.taken_spots:
            if cursor_o == 'h':
                print(eval(color)+"----"+term.normal,end='',flush=True)
            else:
                print(eval(color)+"|"+term.normal,end='',flush=True)
        else:
            if cursor_o == 'h':
                print("    ",end='',flush=True)
            else:
                print(" ",end='',flush=True)

    def fill_box(self,term,player,direction): #fills certain box with player color. direction can be tb, t, b, lr, l, r
        self.player_controller.current_turn = self.player_controller.player_list.index(player)-1 #sets current turn back to player, since they won a box
        if direction == "tb":
            print(term.move_up(1)+term.move_right(1)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
            print(term.move_down(2)+term.move_left(4)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
        elif direction == "t":
            print(term.move_up(1)+term.move_right(1)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
        elif direction == "b":
            print(term.move_down(1)+term.move_right(1)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
        elif direction == "lr":
            print(term.move_up(1)+term.move_left(4)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
            print(term.move_right(1)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
        elif direction == "l":
            print(term.move_up(1)+term.move_left(4)+eval(player.background_color)+'    '+term.normal,end='',flush=True)
        elif direction == "r":
            print(term.move_up(1)+term.move_right(1)+eval(player.background_color)+'    '+term.normal,end='',flush=True)


    def check_won_box(self,term,player):
        cursor_p1_r, cursor_p1_c = self.cursor_pos[0] #row and col of cursor point 1
        cursor_p2_r, cursor_p2_c = self.cursor_pos[1] #row and col of cursor point 2
        taken_list_h_t = [[[cursor_p1_r, cursor_p1_c],[cursor_p2_r, cursor_p2_c]],[[cursor_p1_r, cursor_p1_c],[cursor_p2_r-1, cursor_p2_c-1]],[[cursor_p1_r, cursor_p1_c+1],[cursor_p2_r-1, cursor_p2_c]],[[cursor_p1_r-1, cursor_p1_c],[cursor_p2_r-1, cursor_p2_c]]] #top box
        taken_list_h_b = [[[cursor_p1_r, cursor_p1_c],[cursor_p2_r, cursor_p2_c]],[[cursor_p1_r+1, cursor_p1_c],[cursor_p2_r, cursor_p2_c-1]],[[cursor_p1_r+1, cursor_p1_c],[cursor_p2_r+1, cursor_p2_c]],[[cursor_p1_r+1, cursor_p1_c+1],[cursor_p2_r, cursor_p2_c]]] #bottom box
        taken_list_v_l = [[[cursor_p1_r, cursor_p1_c],[cursor_p2_r, cursor_p2_c]],[[cursor_p1_r-1, cursor_p1_c-1],[cursor_p2_r, cursor_p2_c]],[[cursor_p1_r, cursor_p1_c-1],[cursor_p2_r, cursor_p2_c-1]],[[cursor_p1_r, cursor_p1_c-1],[cursor_p2_r+1, cursor_p2_c]]] #left box
        taken_list_v_r = [[[cursor_p1_r, cursor_p1_c],[cursor_p2_r, cursor_p2_c]],[[cursor_p1_r-1, cursor_p1_c],[cursor_p2_r, cursor_p2_c+1]],[[cursor_p1_r, cursor_p1_c+1],[cursor_p2_r, cursor_p2_c+1]],[[cursor_p1_r, cursor_p1_c],[cursor_p2_r+1, cursor_p2_c+1]]] #right box

        if self.cursor_orientation == 'h':
            top_taken = True
            bottom_taken = True

            for line in taken_list_h_t:
                if line not in self.taken_spots:
                    top_taken = False
            for line in taken_list_h_b:
                if line not in self.taken_spots:
                    bottom_taken = False

            if top_taken and bottom_taken:
                player.score += 2
                self.fill_box(term,player,"tb")
            elif top_taken or bottom_taken:
                player.score += 1
                if top_taken:
                    self.fill_box(term,player,"t")
                else:
                    self.fill_box(term,player,"b")
        else:
            left_taken = True
            right_taken = True

            for line in taken_list_v_l:
                if line not in self.taken_spots:
                    left_taken = False

            for line in taken_list_v_r:
                if line not in self.taken_spots:
                    right_taken = False

            if left_taken and right_taken:
                player.score += 2
                self.fill_box(term,player,"lr")
            elif left_taken or right_taken:
                player.score += 1
                if left_taken:
                    self.fill_box(term,player,"l")
                else:
                    self.fill_box(term,player,"r")

        self.player_controller.update_scores(term,player)


    def update_board(self,player,term,dir): #updates board in cursor direction
        top_left = self.top_left
        cursor_o = self.cursor_orientation
        cursor_p = self.cursor_pos
        print(term.move_xy(cursor_p[0][1]*5 + top_left[0], cursor_p[0][0]*2 + top_left[1]),end='') #vert based on second cursor pos

        if dir == ' ':
            self.move_player(player)
            self.check_won_box(term,player)
        elif dir == 'r':
            if cursor_o == 'h':
                print(term.move_down(1),end='',flush=True)
                self.print_taken(term,dir)
                print(term.move_up(1)+term.lawngreen+"----"+term.normal,end='',flush=True)
            else:
                print(term.move_up(1)+term.lawngreen+"|"+term.normal,end='',flush=True)
                print(term.move_up(1),end='',flush=True)
                self.print_taken(term,dir)
        elif dir == 'w':
            if cursor_o == 'h':
                print(term.move_right(1)+term.lawngreen+"----"+term.normal,end='',flush=True)
                print(term.move_left(4)+term.move_down(2),end='',flush=True)
                self.print_taken(term)
            else:
                print(term.move_down(1),end='',flush=True)
                self.print_taken(term)
                print(term.move_left(1)+term.move_up(2)+term.lawngreen+"|",end='',flush=True)
        elif dir == 'a':
            if cursor_o == 'h':
                print(term.move_right(1)+term.lawngreen+"----"+term.normal,end='',flush=True)
                print(term.move_right(1),end='',flush=True)
                self.print_taken(term)
            else:
                print(term.move_right(5)+term.move_up(1),end='',flush=True)
                self.print_taken(term)
                print(term.move_left(6)+term.lawngreen+"|"+term.normal,end='',flush=True)
        elif dir == 's':
            if cursor_o == 'h':
                print(term.move_right(1)+term.lawngreen+"----"+term.normal,end='',flush=True)
                print(term.move_left(4)+term.move_up(2),end='',flush=True)
                self.print_taken(term)
            else:
                print(term.move_up(3),end='',flush=True)
                self.print_taken(term)
                print(term.move_left(1)+term.move_down(2)+term.lawngreen+"|",end='',flush=True)
        elif dir == 'd':
            if cursor_o == 'h':
                print(term.move_left(4),end='',flush=True)
                self.print_taken(term)
                print(term.move_right(1)+term.lawngreen+"----"+term.normal,end='',flush=True)
            else:
                print(term.move_left(5)+term.move_up(1),end='',flush=True)
                self.print_taken(term)
                print(term.move_right(4)+term.lawngreen+"|"+term.normal,end='',flush=True)
