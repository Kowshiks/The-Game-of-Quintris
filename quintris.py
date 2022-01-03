
from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
from QuintrisGame import *
import time, sys

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()


class ComputerPlayer():
    
    def get_moves(self, quintris):

        # Move commands

        COMMANDS = { "b": quintris.left, "n": quintris.rotate, "m": quintris.right, "h": quintris.hflip }

        move = []

        final_move1 = {}

        final_move2 = {}

        height_move = {}
        line_move = {}
        hole_move = {}
        bump_move = {}

        height_next_move = {}
        line_next_move = {}
        hole_next_move = {}
        bump_next_move = {}

        original_row = quintris.row
        original_column = quintris.col
        original_piece = quintris.piece
        original_state = quintris.state
        next_piece = quintris.next_piece


        find_best_move = {}
        
        # Find the row and column position of the falling piece

        left_shift =  quintris.col
        right_shift = len(quintris.get_board()[0]) - len(quintris.get_piece()[0][0]) - left_shift

        # Append all the possible moves into a list

        # Straight moves

        move.append("bm")
        move.append("h")
        move.append("n")
        move.append("nh")
        move.append("nn")
        move.append("nnh")
        move.append("nnn")
        move.append("nnnh")

        # Left side moves

        for l in range(0,left_shift):
            left_size = "b" * (l + 1)
            move.append(left_size + "h")
            move.append(left_size + "n")
            move.append(left_size + "nh")
            move.append(left_size + "nn")
            move.append(left_size + "nnh")
            move.append(left_size + "nnn")
            move.append(left_size + "nnnh")

        # Right side moves
        
        for r in range(0,right_shift):
            left_size = "m" * (r + 1)
            move.append(left_size + "h")
            move.append(left_size + "n")
            move.append(left_size + "nh")
            move.append(left_size + "nn")
            move.append(left_size + "nnh")
            move.append(left_size + "nnn")
            move.append(left_size + "nnnh")




        for move_list in move:

            height_next_move[move_list] = {}
            line_next_move[move_list] = {}
            hole_next_move[move_list] = {}
            bump_next_move[move_list] = {}

        
        # Iterating over each moves

        
        for move_list in move:

            # Move the piece over each possible move

            for each_move in move_list:
                COMMANDS[each_move]()

            # Check for the next state
            
            
            while not ComputerPlayer.check_collision(*quintris.state, quintris.piece, quintris.row+1, quintris.col):
                quintris.row += 1
            new_state = ComputerPlayer.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)

            '''# Calculate the aggregate height

            agg_height_score = ComputerPlayer.agg_height(self, new_state[0])

            line_count_score = ComputerPlayer.complete_line(self, new_state[0])

            hole_score = ComputerPlayer.holes(self, new_state[0])

            bump_score = ComputerPlayer.bump(self, new_state[0])

            height_move[move_list] = agg_height_score

            line_move[move_list] = line_count_score

            hole_move[move_list] = hole_score

            bump_move[move_list] = bump_score'''

            # Revoke to the original state

            quintris.piece = next_piece
            quintris.row = original_row
            quintris.col = original_column

            quintris.state = new_state

            new_move_state = quintris.state

            # Loop over all possible moves for the next piece

            for move_list_new in move:

                for each_move_new in move_list_new:
                    COMMANDS[each_move_new]()


                find_best_move[move_list_new] = move_list

                while not ComputerPlayer.check_collision(*quintris.state, quintris.piece, quintris.row+1, quintris.col):
                    quintris.row += 1
                new_state = ComputerPlayer.place_piece(*quintris.state, quintris.piece, quintris.row, quintris.col)

                # Calculate aggregate height

                agg_height_score_next = ComputerPlayer.agg_height(self, new_state[0])

                # Calculate complete line score count

                line_count_score_next = ComputerPlayer.complete_line(self, new_state[0])

                # Calculate the hole count sum

                hole_score_next = ComputerPlayer.holes(self, new_state[0])

                # Calculate the bumpiness score

                bump_score_next = ComputerPlayer.bump(self, new_state[0])

                # Add the values to a dictionary

                height_next_move[move_list][move_list_new] = agg_height_score_next

                line_next_move[move_list][move_list_new] = line_count_score_next

                hole_next_move[move_list][move_list_new] = hole_score_next

                bump_next_move[move_list][move_list_new] = bump_score_next

                # Revert back to the original state

                quintris.row = original_row
                quintris.col = original_column
                quintris.piece = next_piece
                quintris.state = new_move_state
            
            # Revert back to the original state
            
            quintris.row = original_row
            quintris.col = original_column
            quintris.piece = original_piece
            quintris.state = original_state
            

        for move_list_1 in move:


            '''height_s = height_move[move_list_1]

            line_s = line_move[move_list_1]

            hole_s = hole_move[move_list_1]

            bump_s = bump_move[move_list_1]

            score = (-0.51066 * height_s) + (0.760666 * line_s) + (-0.35663 * hole_s) + (-0.184483 * bump_s)'''


            score_list = []

            # Calculate the weights of each possible next move


            for move_list_2 in move:



                height_s_next = height_next_move[move_list_1][move_list_2]

                line_s_next = line_next_move[move_list_1][move_list_2]

                hole_s_next = hole_next_move[move_list_1][move_list_2]

                bump_s_next = bump_next_move[move_list_1][move_list_2]

                score_now = (-0.51066 * height_s_next) + (0.760666 * line_s_next) + (-0.35663 * hole_s_next) + (-0.184483 * bump_s_next)                


                score_list.append(score_now)

            score_next = max(score_list)

            final_move1[move_list_1]  = score_next

            #final_move2[move_list_1]  = score
        

        
        quintris.col = original_column
        quintris.piece = original_piece

        # Take the move with the highest value as the next move
        

        best_move_sorted = dict(sorted(final_move1.items(), key=lambda x:x[1], reverse = True))

        pass_move = next(iter(best_move_sorted))

        return pass_move 

        #return random.choice("mnbh") * random.randint(1, 10)
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))
            

            if(index < quintris.col):
                quintris.right()

            elif(index < quintris.row):
                quintris.left()
           
            else:
                quintris.down()


    @staticmethod
    def combine(str1, str2):
        return "".join([ c if c != " " else str2[i] for (i, c) in enumerate(str1) ] )


    @staticmethod
    def place_piece(board, score, piece, row, col):
        return (board[0:row] + \
                [ (board[i+row][0:col] + ComputerPlayer.combine(r, board[i+row][col:col+len(r)]) + board[i+row][col+len(r):] ) for (i, r) in enumerate(piece) ] + \
                board[row+len(piece):], score)
    
    @staticmethod
    def check_collision(board, score, piece, row, col):
       
        return col+len(piece[0]) > QuintrisGame.BOARD_WIDTH or row+len(piece) > QuintrisGame.BOARD_HEIGHT \
            or any( [ any( [ (c != " " and board[i_r+row][col+i_c] != " ") for (i_c, c) in enumerate(r) ] ) for (i_r, r) in enumerate(piece) ] )



    # Calculate the aggregate height score

    def agg_height(self, board):

        score = 0

        for col_range in range(0,len(board[0])):
            for row_range in range(0,len(board)):
                if(board[row_range][col_range] == "x"):
                    score+= (len(board) - row_range) * (len(board) - row_range)
                    break

        return score
    
    # Calculate the complete line score
    
    def complete_line(self, board):
        line_count = 0
        for row_line in board:
            if " " in row_line:
                continue
        else:
            line_count+=1
        
        return line_count


    # Calculate the holes score
    
    def holes(self, board):
        total_hole = 0

        for col_range in range(0,len(board[0])):
            hole = 0
            for row_range in range(0,len(board)):
                if(board[row_range][col_range] == "x"):
                    hole +=1
                if(board[row_range][col_range] == " "):
                    if(hole!=0):
                        total_hole += 1

        return total_hole

    
    # Calculate the bump score

    def bump(self, board):

        height_list = []
        bump_score = 0

        for col_range in range(0,len(board[0])):
            x = 0
            for row_range in range(0,len(board)):
                if(board[row_range][col_range] == "x"):
                    x+=1
                    height_list.append(len(board) - row_range)
                    break
            if(x == 0):
                height_list.append(0)

        for i in range(0,len(height_list)-1):
            bump_score += abs(height_list[i] - height_list[i+1])

        return bump_score




###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



