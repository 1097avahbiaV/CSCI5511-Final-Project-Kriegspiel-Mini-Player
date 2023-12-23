# this is a simple atempt at a kriegspiel 
# methodology in mini chess (Micro or Dan Glimme)
import random as r
import copy as c
#
world=0

def swap(board,a,b):
    # a contains original,
    # b contains final
    temp = board[a[0]][a[1]] # original
    board[a[0]][a[1]] = board[b[0]][b[1]]
    board[b[0]][b[1]] = temp
    return board
#
class temp:
    world=0

#
class Micro_Umpire:
    def __init__(self):
        #
        self.whole_BOARD=[['bki','bkn','bbi','brk'],['bpa','___','___','___'],['___','___','___','___'],['___','___','___','wpa'],['wrk','wbi','wkn','wki']]
        self.BOARD=[['bki','bkn','bbi','brk'],['bpa','___','___','___'],['___','___','___','___'],['___','___','___','wpa'],['wrk','wbi','wkn','wki']]
        self.white_BOARD=[['___','___','___','___'],['___','___','___','___'],['___','___','___','___'],['___','___','___','wpa'],['wrk','wbi','wkn','wki']]
        self.black_BOARD=[['bki','bkn','bbi','brk'],['bpa','___','___','___'],['___','___','___','___'],['___','___','___','___'],['___','___','___','___']]
        #
        self.player_moves={'b':[],'w':[]}
        # this is for obect reference
        self.black=None
        self.white=None
        #
        self.winner=None
        # piece reference
        self.black_pieces=['bpa','bbi','bkn','bki','brk']
        self.white_pieces=['wpa','wbi','wkn','wki','wrk']
        #
        self.turn_no=0
        self.turn_limit=100
        #
        # self.isheck=None
        # self.ischeckmate=None
        #
        self.cutoff_limit=1
    
    # mini max algorithm
    def mini_max(self,board,curr_player,curr_depth):
        val, move, piece=self.max(board,curr_player,curr_depth)
        # print('output received')
        # print((val, move, piece))
        return (move,piece)
    
    # max value
    def max(self,board,curr_player,curr_depth):
        global world
        print("\n\n\nentered max function\n\n\n")
        #
        self.BOARD=board
        #
        for i in self.BOARD:
            print(i)
        print(curr_player)
        # move generation
        net_moves={}
        if isinstance(curr_player, Micro_Black):
            for piece in self.black_pieces:
                net_moves[piece]=self.black.moves(piece,self.BOARD)
            net_moves['bki']=self.check('b',net_moves['bki'])
            print('went through check function')
            print('passing possible capture count')
            print(self.black.capture_count)
        elif isinstance(curr_player,Micro_White):
            for piece in self.white.pieces:
                net_moves[piece]=self.white.moves(piece,self.BOARD)
            net_moves['wki']=self.check('w',net_moves['wki'])
            print('went through check function')
            print('passing possible capture count')
            print(self.white.capture_count)
        # 
        
        print(net_moves)
        print(curr_player.capture_count)
        
        #
        if self.cutoff_limit == curr_depth:
            print('limit reached')
            eval_result=self.eval(net_moves,curr_player,curr_player.capture_count)
            # finding the move with highest score
            h_score=0
            right_move=()
            right_piece=''
            for p in eval_result:
                for m in eval_result[p]:
                    if m[0]>h_score:
                        h_score=m[0]
                        right_move=m[1]
                        right_piece=p
                    elif m[0] == h_score:
                        o=r.choice([1,2])
                        if o == 1:
                            pass
                        elif o==2:
                            h_score=m[0]
                            right_move=m[1]
                            right_piece=p
            print((right_move,right_piece,h_score))
            return h_score, right_piece, right_move
        #
        val=float('-inf')
        #
        temp.world=c.deepcopy(self.BOARD)
        #
        for piece in net_moves:
            print("\n\n\n\n\n")
            print(piece)
            self.BOARD=self.whole_BOARD
            if (self.BOARD != temp.world):
                self.BOARD=c.deepcopy(temp.world)
            for action in net_moves[piece]:
                print('new moves')
                self.print_board()
                print(action)
                if (self.BOARD != temp.world):
                    self.BOARD = c.deepcopy(temp.world)
                print(temp.world)
                if isinstance(curr_player,Micro_Black):
                    #
                    # collecting a temporary state to pass on
                    # will reflect the move currently in play across the board
                    temp_world=self.BOARD
                    #
                    temp_world=self.board_update(temp_world, piece, action, 'b')
                    print('updated temp world')
                    for i in temp_world:
                        print(i)
                    #
                    v2, p, move = self.min(temp_world,self.white,curr_depth+1)
                    print((v2, p, move))
                    print("received")
                    print((v2,piece,action))
                    # print(temp.world)
                    if v2>val:
                        print("enter\n")
                        val =v2
                        p=piece
                        move=action
                        print((val,p,move))
                elif isinstance(curr_player,Micro_White):
                    temp_world=self.BOARD
                    temp_world=self.board_update(temp_world, piece, action, 'w')
                    print('updated temp world')
                    for i in temp_world:
                        print(i)
                    # print(temp.world)
                    v2, p, move = self.min(temp_world,self.black,curr_depth+1)
                    print((v2, p, move))
                    print("received")
                    print((v2,piece,action))
                    # print(temp.world)
                    if -v2>val:
                        print("enter\n")
                        # val=v2
                        p=piece
                        move=action
                        print((val,p,move))
        print("outside")
        print((val,p,move))
        return val, move, p

    
    #min value
    def min(self,board,curr_player,curr_depth):
        print("\n\n\nentered min function\n\n\n")
        #
        self.BOARD=board
        #
        for i in self.BOARD:
            print(i)
        print(curr_player)
        # move generation
        # print(curr_player)
        net_moves={}
        print(self.black_pieces)
        if isinstance(curr_player, Micro_Black):
            for piece in self.black_pieces:
                print(piece)
                net_moves[piece]=self.black.moves(piece,self.BOARD)
            
            net_moves['bki']=self.check('b',net_moves['bki'])
            print('went through check function')
            print('passing possible capture count')
            print(self.black.capture_count)
        elif isinstance(curr_player,Micro_White):
            for piece in self.white.pieces:
                net_moves[piece]=self.white.moves(piece,self.BOARD)
            net_moves['wki']=self.check('w',net_moves['wki'])
            print('went through check function')
            print('passing possible capture count')
            print(self.white.capture_count)
        # 
        
        print(net_moves)
        print(curr_player.capture_count)
        
        #
        if self.cutoff_limit == curr_depth:
            print('limit reahced)')
            eval_result=self.eval(net_moves,curr_player,curr_player.capture_count)
            # finding the move with highest score
            h_score=0
            right_move=()
            right_piece=''
            for p in eval_result:
                for m in eval_result[p]:
                    if m[0]>h_score:
                        h_score=m[0]
                        right_move=m[1]
                        right_piece=p
                    elif m[0] == h_score:
                        o=r.choice([1,2])
                        if o == 1:
                            pass
                        elif o==2:
                            h_score=m[0]
                            right_move=m[1]
                            right_piece=p
            print((right_move,right_piece,h_score))
            return h_score, right_piece, right_move
        #
        val=float('inf')
        temp.world=self.BOARD
        for piece in net_moves:
            for action in net_moves[piece]:
                print('\n\n\n\n\n new moves')
                self.BOARD=world
                self.print_board()
                print(action)
                if isinstance(curr_player,Micro_Black):
                    # collecting a temporary state to pass on
                    # will reflect the move currently in play across the board
                    temp_world=self.BOARD
                    temp_world=self.board_update(temp_world, piece, action, 'b')
                    print('updated temp world')
                    # print(temp_world)
                    for i in temp_world:
                        print(i)
                    # 
                    v2, p, move = self.max(temp_world,self.white,curr_depth+1)
                    print((v2, p, move))
                    print("received")
                    print((v2,piece,action))
                    if v2>val:
                        print("enter\n")
                        val =v2
                        p=piece
                        move=action
                        print((val,p,move))
                elif isinstance(curr_player,Micro_White):
                    temp_world=self.BOARD
                    temp_world=self.board_update(temp_world, piece, action, 'w')
                    print('updated temp world')
                    for i in temp_world:
                        print(i)
                    v2, p, move = self.max(temp_world,self.white,curr_depth+1)
                    print((v2, p, move))
                    print("received")
                    print((v2,piece,action))
                    if v2<val:
                        print("enter\n")
                        val =v2
                        p=piece
                        move=action
                        print((val,p,move))
        return val, move, p
    
    # move evaluation function
    def eval(self,all_moves,player,captured):
        print('entered eval')
        print(all_moves)
        print(captured)
        #
        values={}
        #
        piece_value=0
        for piece in all_moves:
            # value assignment
            if piece =='wpa' or piece =='bpa':
                piece_val=100
            elif piece =='wrk' or piece =='brk':
                piece_val=525
            elif piece =='wkn' or piece =='bkn':
                piece_val=350
            elif piece =='wbi' or piece =='bbi':
                piece_val=350
            elif piece =='wki' or piece =='bki':
                piece_val=1000
            mobility=len(all_moves[piece])
            cap=len(captured[piece]) # bonus for a move if there exists positions where pieces can be captured
            #
            if piece not in values:
                values[piece]=[]
            #
            for move in all_moves[piece]:
                v=0
                if move in captured[piece]:
                    v=piece_val*(1.5+cap)*mobility
                else:
                    v=piece_val*mobility
                values[piece].append((v,move))
        return values

    # printing board
    def print_board(self):
        for i in range(5):
            if (i==0):
                print('      1      2      3      4    '*3)
                print(str(i+1)+str(self.white_BOARD[i]) + "   " +str(i+1)+ str(self.BOARD[i]) + "   " +str(i+1)+ str(self.black_BOARD[i]))
            else:
                print(str(i+1)+str(self.white_BOARD[i]) + "   " +str(i+1)+ str(self.BOARD[i]) + "   " +str(i+1)+ str(self.black_BOARD[i]))
    
    # this is the index finder function for each piece
    def index_finder(self,piece):
        for row in self.BOARD:
            if (piece in row) and ((piece in self.black_pieces) or (piece in self.white_pieces)):
                pos=row.index(piece)
                return self.BOARD.index(row),pos
            # else:
            #     return -10,-10
    
    # this function checks for which moves result in a
    # king will be moving to a checked position by the
    # opponent, out of the moves that the king has available to him
    def check(self,player,king_moves):
        print('\n\nentered checked')
        print(player)
        print(self.black)
        if player == 'w':
            #print('entered if condition of player w')
            move=[]
            pieces=self.black_pieces
            #print("this is pieces\n")
            #print(pieces)
            for piece in pieces:
                #print(piece)
                move+=self.black.moves(piece,self.BOARD)
                # print("exit for loop")
            print(move)
            for i in king_moves:
                for j in move:
                    if i == j:
                        print('eliminating possible check areas')
                        # king_moves=king_moves.pop(king_moves.index(i))
                        king_moves.pop(king_moves.index(i))
            return king_moves
        elif player == 'b':
            #print('entered if condition of player w')
            move=[]
            pieces=self.white_pieces
            #print("this is pieces\n")
            #print(pieces)
            for piece in pieces:
                #print(piece)
                move+=self.white.moves(piece,self.BOARD)
                # print("exit for loop")
            print(move)
            for i in king_moves:
                for j in move:
                    if i == j:
                        print('eliminating possible check areas')
                        # king_moves=king_moves.pop(king_moves.index(i))
                        king_moves.pop(king_moves.index(i))
            return king_moves

    def promotion(self,board,piece):
        #if piece == 'wpa' and
        if piece == 'wpa':
            if piece in board[0]:
                i=board[0].index(piece)
                # normally in cases of promotion you are allowed to choose
                if (isinstance(self.black,HumanAgent) or isinstance(self.white,HumanAgent)):
                    print('your pawn has been promoted, you will now swap it out for')
                    print("press 1 for a rook\n press 2 for a knight\npress 3 for a bishop")
                    promoted=int(input())
                    #
                    if promoted == 1:
                        board[0][i]='wrk'
                    elif promoted == 2:
                        board[0][i]='wkn'
                    elif promoted == 3:
                        board[0][i]='wbi'
                else:
                    board[0][i]='wrk' # automatically assigning a rook if the agent is not human
        elif piece == 'bpa':
            if piece in board[4]:
                #
                i=board[0].index(piece)
                # normally in cases of promotion you are allowed to choose
                if (isinstance(self.black,HumanAgent) or isinstance(self.white,HumanAgent)):
                    print('your pawn has been promoted, you will now swap it out for')
                    print("press 1 for a rook\n press 2 for a knight\npress 3 for a bishop")
                    promoted=int(input())
                    #
                    if promoted == 1:
                        board[4][i]='brk'
                    elif promoted == 2:
                        board[4][i]='bkn'
                    elif promoted == 3:
                        board[4][i]='bbi'
                else:
                    board[4][i]='brk'
        else:
            return False

    # checks for any check as result of a move
    def ischeck(self):
        return 0
    
    # checks for checkmate
    def ischeckmate():
        return 0
    
    # checks for captures
    def iscapture(self,board,pos,player):
        r=pos[0]
        c=pos[1]
        if player == 'w':
            if board[r][c] in self.black_pieces:
                print('capture made\n')
                print('piece captured is '+self.BOARD[r][c])
                return True
        elif player == 'b':
            if board[r][c] in self.white_pieces:
                print('capture made\n')
                print('piece captured is '+self.BOARD[r][c])
                return True
        else:
            return False
    
    # updating the board
    def board_update(self, board, piece, move, player):
        #
        r2,c2=self.index_finder(piece)
        #
        r1=move[0]
        c1=move[1]
        #
        print('orginial mvoe is {v1}'.format(v1=(r2,c2)))
        print('move to swap is {v1}'.format(v1=move))
        #
        if self.iscapture(board,[r1,c1],player):
            if player == 'w':
                p1=board[r1][c1]
                #
                t1=c.deepcopy(self.black_pieces)
                #
                print('opp player pieces before capture')
                print(t1)
                t1.pop(board[r1].index(p1))
                print('opp player pieces after capture')
                print(t1)
                print(self.black_pieces)
                #
                # self.black_pieces=t1
            elif player == 'b':
                p1=board[r1][c1]
                #
                t1=c.deepcopy(self.white_pieces)
                #
                print('opp player pieces before capture')
                print(t1)
                t1.pop(board[r1].index(p1))
                print('opp player pieces after capture')
                print(t1)
                print(self.white_pieces)
                #
                # self.white_pieces=t1
            elif isinstance(player,Micro_White):
                print("entered microwhite")
                p1=board[r1][c1]
                # deleting umpires record of piece
                self.black_pieces.pop(self.black_pieces.index(p1))
                # deleting players record of piece
                self.black.pieces.pop(self.black_pieces.index(p1))
            elif isinstance(player,Micro_Black):
                print("entered microblack")
                p1=board[r1][c1]
                self.white_pieces.pop(self.white_pieces.index(p1))
                self.white.pieces.pop(self.white_pieces)
            board[r1][c1] = '___'
        board=swap(board,[r2,c2],move)
        for i in board:
            print(i)
        # update white and black boards
        return board
    

class Micro_White(Micro_Umpire):
    def __init__(self,eval_choice):
        super().__init__()
        #self.white_BOARD=[['___','___','___','___'],['___','___','___','___'],['___','___','___','___'],['___','___','___','wpa'],['wrk','wbi','wkn','wki']]
        self.white_BOARD=self.white_BOARD
        self.turn_no=0
        #
        self.pieces=['wpa','wbi','wkn','wki','wrk']
        self.capture_count={'wpa':[],'wbi':[],'wkn':[],'wki':[],'wrk':[]}
        #
        self.eval=eval_choice
        #
        self.opp_pieces={"bpa":[],"bkn":[],"brk":[],"bbi":[],"bki":[]}
        self.opp_pieces_count=5

    def index_finder(self, piece):
        # print('searching for piece {v1}'.format(v1=piece))
        for row in self.white_BOARD:
            # print(row)
            if (piece in row) and (piece in self.pieces):
                # print('found')
                pos=row.index(piece)
                return self.white_BOARD.index(row),pos # returns the index of the row and the column
            # else:
            #     return -10, -10
    
    # function needs to be edited
    def any_capture(self,piece,loc):
        if piece == 'wpa':
            moves=[]
            captures=[]
            # loc returns the pawns current location
            row=loc[0]
            col=loc[1]
            # checks diagonal piece captures
            try:
                # try first diagonal opposite
                if ((col+1<4) and (self.BOARD[row-1][col+1]!='___') and (self.BOARD[row-1][col+1] in self.black_pieces)):
                    moves.append((row-1,col+1))
                    captures.append((row-1,col+1))
                # try second diagonal opposite
                if ((col-1>=0) and (self.BOARD[row-1][col-1]!='___') and (self.BOARD[row-1][col-1] in self.black_pieces)) :
                    moves.append((row-1,col-1))
                    captures.append((row-1,col-1))
            except IndexError:
                pass
            self.capture_count['wpa']=captures
            # print('pawn capture moves are {v1}\n'.format(v1=moves))
            return moves
        #
        elif piece == 'wrk':
            moves=[]
            #
            captures=[]
            # loc returns the collection of maximum and minimum row and column (horizontal and vertical) free space available for rook
            min_row=loc[0]
            max_row=loc[1]
            min_col=loc[2]
            max_col=loc[3]
            row=loc[4] # current position row
            col=loc[5] # current position col
            # the indexerror catches any references made that exist outside of the board dimensions
            try:
                if ((min_col-1>=0) and (self.BOARD[row][min_col-1] != '___') and (self.BOARD[row][min_col-1] in self.black_pieces)):
                    moves.append((row,min_col-1))
                    captures.append((row,min_col-1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[row][max_col+1] != '___') and (self.BOARD[row][max_col+1] in self.black_pieces)):
                    moves.append((row,max_col+1))
                    captures.append((row,max_col+1))
            except IndexError:
                pass
            try:
                if ((min_row-1>=0) and (self.BOARD[min_row-1][col] != '___') and (self.BOARD[min_row-1][col] in self.black_pieces)):
                    moves.append((min_row-1,col))
                    captures.append((min_row-1,col))
            except IndexError:
                pass
            try:
                if ((self.BOARD[max_row+1][col] != '___') and (self.BOARD[max_row+1][col] in self.black_pieces)):
                    moves.append((max_row+1,col))
                    captures.append((max_row+1,col))
            except IndexError:
                pass
            self.capture_count['wrk']=captures
            # print('rook capture moves are {v1}\n'.format(v1=moves))
            return moves
        #
        elif piece == 'wbi':
            moves=[]
            #
            captures=[]
            # loc returns the collection of maximum and minimum row and column number (along both diagonals) free space available for a bishop
            # diag1
            d1_e1_i=loc[0][0]
            d1_e1_j=loc[0][1]
            d1_e2_i=loc[1][0]
            d1_e2_j=loc[1][1]
            # diag2
            d2_e1_i=loc[2][0]
            d2_e1_j=loc[2][1]
            d2_e2_i=loc[3][0]
            d2_e2_j=loc[3][1]
            #
            row=loc[4]
            col=loc[5]
            #
            try:
                if((d1_e1_i-1>=0) and (d1_e1_j-1>=0) and (self.BOARD[d1_e1_i-1][d1_e1_j-1] != '___') and (self.BOARD[d1_e1_i-1][d1_e1_j-1] in self.black_pieces)):
                    moves.append((d1_e1_i-1,d1_e1_j-1))
                    captures.append((d1_e1_i-1,d1_e1_j-1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[d1_e2_i+1][d1_e2_j+1] != '___') and (self.BOARD[d1_e2_i+1][d1_e2_j+1] in self.black_pieces)):
                    moves.append((d1_e2_i+1,d1_e2_j+1))
                    captures.append((d1_e2_i+1,d1_e2_j+1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[d2_e1_i+1][d2_e1_j+1] != '___') and (self.BOARD[d2_e1_i+1][d2_e1_j+1] in self.black_pieces)):
                    moves.append((d2_e1_i+1,d2_e1_j+1))
                    captures.append((d2_e1_i+1,d2_e1_j+1))
            except IndexError:
                pass
            try:
                if ((d2_e2_i-1>=0) and (d2_e2_j-1>=0) and (self.BOARD[d2_e2_i-1][d2_e2_j-1] != '___') and (self.BOARD[d2_e2_i-1][d2_e2_j-1] in self.black_pieces)):
                    moves.append((d2_e2_i-1,d2_e2_j-1))
                    captures.append((d2_e2_i-1,d2_e2_j-1))
            except IndexError:
                pass
            self.capture_count['wbi']=captures
            # print('bishop capture moves are {v1}\n'.format(v1=moves))
            return moves
        elif piece == 'wkn':
            #
            captures=[]
            # loc returns the possible positions the knight can take and checking if there are any enemy pieces in these positions
            # loc contains only valid positoins within the board due to its ordering in the legel_move_generation
            moves=[]
            for pos in loc:
                if (self.BOARD[pos[0]][pos[1]] in self.black_pieces):
                    moves.append(pos)
                    captures.append(pos)
            self.capture_count['wkn']=captures
            # print('knight capture moves are {v1}'.format(v1=moves))
            return moves
        elif piece == 'wki':
            # loc returns current king position
            captures=[]
            # add for check and checkmate clause positoin before adding move
            moves=[]
            for pos in loc:
                if (self.BOARD[pos[0]][pos[1]] in self.black_pieces):
                    moves.append(pos)
                    captures.append(pos)
            self.capture_count['wki']=captures
            # print('king capture moves are {v1}\n'.format(v1=moves))
            return moves


    def legal_move_generation(self,piece,loc):
        row=loc[0]
        col=loc[1]
        legal_moves=[]
        # https://en.wikipedia.org/wiki/Kriegspiel_(chess) -- rules
        if piece == 'wpa':
            # print((row,col))
            # naturally a pawn can only move up ny one tile
            legal_moves=[(row-1,col)]
            # if turn_no is 0, the pawn can be moved two spaces up
            if self.turn_no == 0:
                legal_moves.append((row-2,col))
            # adding any moves that enable captures
            # print(legal_moves)
            legal_moves+=self.any_capture(piece,loc)
            # filtering moves that exceed board limit
            legal_moves=[x for x in legal_moves if ((0<=x[0]<5) or (0<=x[1]<4))]
            #
            return legal_moves
        #
        elif piece == 'wrk':
            # setting base
            max_row=row
            min_row=row
            max_col=col
            min_col=col
            # print((max_row,min_row,max_col,min_col))
            # checking maximum vertical movement in the rows
            for i in range(row-1,-1,-1):
                if self.BOARD[i][col] != '___':
                    min_row=i+1
                    break
            # checking minimum vertical movement in the rows
            for i in range(row+1, 5):
                if self.BOARD[i][col] != '___':
                    max_row=i-1
                    break
            # checking minimum horizontal movement in the columns
            for i in range(col-1,-1,-1):
                if self.BOARD[row][i] != '___':
                    min_col=i+1
                    break
            # checking the maximum horizontal movment in the columns
            for i in range(col+1,4):
                if self.BOARD[row][i] !='___':
                    max_col=i-1
                    break
            # print((max_row,min_row,max_col,min_col))
            #legal_moves=[(row,col)] row and col indicate current real world position
            rk_possible_moves=[(x,col) for x in range(max_row,min_row-1,-1)] # checks for all the possible row positions
            rk_possible_moves+=[(row,x) for x in range(max_col,min_col-1,-1)] # checks for all possible column positions
            #
            moves=self.any_capture(piece, [min_row,max_row,min_col,max_col,row,col])
            legal_moves=rk_possible_moves+moves
            # removing piece original location
            legal_moves=list(set(legal_moves))
            origin=legal_moves.index((row,col))
            legal_moves.pop(origin)
            # return max_row,max_col,
            return legal_moves
        #
        elif piece == 'wbi':
            # for a bishop, I will first check all free spaces available on the diagonal
            # once it hits a natural block, either the board ending or an opponent piece in the way
            # I will call on capture to find out which piece is capturable
            #
            diag1_end1_i=row
            diag1_end1_j=col
            #
            diag2_end1_i=row
            diag2_end1_j=col
            #
            diag1_end2_i=row
            diag1_end2_j=col
            #
            diag2_end2_i=row
            diag2_end2_j=col
            #
            d1_e1_l=[['_','_']]
            d1_e2_l=[['_','_']]
            d2_e1_l=[['_','_']]
            d2_e2_l=[['_','_']]
            #
            # checking the top half of the diagonal space
            while(diag1_end1_j>=0 and diag2_end1_j<4):
                #
                diag1_end1_i-=1
                diag2_end1_i-=1
                #
                diag1_end1_j-=1
                diag2_end1_j+=1
                #
                if((diag1_end1_i<0) or (diag2_end1_i<0)):
                    diag1_end1_i+=1
                    diag2_end1_i+=1
                    #
                    d1_e1_l[0][0]=diag1_end1_i
                    d1_e1_l[0][1]=diag1_end1_j+1
                    #
                    d2_e1_l[0][0]=diag2_end1_i
                    d2_e1_l[0][1]=diag2_end1_j-1
                    break
                # diagonal 1
                if (0<=diag1_end1_j<4):
                    try:
                        if (self.BOARD[diag1_end1_i][diag1_end1_j] == '___'):
                            legal_moves.append((diag1_end1_i,diag1_end1_j))
                        else:
                            d1_e1_l[0][0]=diag1_end1_i
                            d1_e1_l[0][1]=diag1_end1_j
                    except IndexError:
                        pass
                if diag1_end1_j==0:
                    d1_e1_l[0][0]=diag1_end1_i
                    d1_e1_l[0][1]=diag1_end1_j
                # diagonal 2
                if (0<=diag2_end1_j<4):
                    try:
                        if (self.BOARD[diag2_end1_i][diag2_end1_j] == '___'):
                            legal_moves.append((diag2_end1_i,diag2_end1_j))
                        else:
                            d2_e1_l[0][0]=diag1_end1_i
                            d2_e1_l[0][1]=diag1_end1_j
                    except IndexError:
                        pass
                if diag2_end1_j==3:
                    d2_e1_l[0][0]=diag2_end1_i
                    d2_e1_l[0][1]=diag2_end1_j
            #
            # print('top legal_moves are {v1}\n'.format(v1=legal_moves))
            # checking the bottom half of the diagonal space
            while(diag1_end2_j<4 and diag2_end2_j>=0):
                #
                diag1_end2_i+=1
                diag2_end2_i+=1
                #
                diag1_end2_j+=1
                diag2_end2_j-=1
                #
                if((diag1_end2_i>4) or (diag2_end2_i>4)):
                    diag1_end2_i-=1
                    diag2_end2_i-=1
                    #
                    d1_e2_l[0][0]=diag1_end2_i
                    d1_e2_l[0][1]=diag1_end2_j-1
                    #
                    d2_e2_l[0][0]=diag2_end2_i
                    d2_e2_l[0][1]=diag2_end2_j+1
                    break
                #diagonal 1
                if(0<=diag1_end2_j<4):
                    try:
                        if (self.BOARD[diag1_end2_i][diag1_end2_j] == '___'):
                            legal_moves.append((diag1_end2_i,diag1_end2_j))
                        else:
                            d1_e2_l.append((diag1_end2_i,diag1_end2_j))
                    except IndexError:
                        pass
                if(diag1_end2_j==3):
                    d1_e2_l[0][0]=diag1_end2_i
                    d1_e2_l[0][1]=diag1_end2_j
                # diagonal 2
                if (0<=diag2_end2_j<4):
                    try:
                        if (self.BOARD[diag2_end2_i][diag2_end2_j] == '___'):
                            legal_moves.append((diag2_end2_i,diag2_end2_j))
                        else:
                            d2_e2_l.append((diag2_end2_i,diag2_end2_j))
                    except IndexError:
                        pass
                if(diag2_end2_j==0):
                    d2_e2_l[0][0]=diag2_end2_i
                    d2_e2_l[0][1]=diag2_end2_j
            # print('bottom legal_moves are {v1}\n'.format(v1=legal_moves))
            # print(d1_e1_l)
            # print(d2_e1_l)
            # print(d1_e2_l)
            # print(d2_e2_l)
            # 
            moves = self.any_capture(piece,[d1_e1_l[0],d1_e2_l[0],d2_e1_l[0],d2_e2_l[0],row,col])
            #
            legal_moves+=moves
            #
            return legal_moves
        #
        elif piece == 'wkn':
            #kn_possible_locations already contains te possible future locations for the knight to move
            kn_possible_positions = [(row+1,col+2),(row+2,col+1),(row-1,col+2),(row-2,col+1),(row-2,col-1),(row-1,col-2),(row+1,col-2),(row+2,col-1)]
            # print(kn_possible_positions)
            # eliminating moves that lie outside of the board
            result = [x for x in kn_possible_positions if ((0<=x[0]<5) and (0<=x[1]<4))] # eliminating positions that lie outside of the board
            # collecting moves from opponent piece capture
            moves=self.any_capture(piece,result)
            # cleanup of result, which included blocked spaces, moves above collects opponent piece captures, only collecting free space spots
            result=[x for x in result if (self.BOARD[x[0]][x[1]] == '___')] # technically returning all the possible positions, fails to fulfill function objective but hey, it works
            #
            legal_moves=result+moves
            return legal_moves
        #
        elif piece == 'wki':
            # ki_possible_locations contains possible future moves of the king
            ki_possible_positions = [(row+1,col-1),(row+1,col),(row+1,col+1),(row,col-1),(row,col+1),(row-1,col-1),(row-1,col),(row-1,col+1)]
            # eliminating moves that lie outside of the board
            result = [x for x in ki_possible_positions if ((0<=x[0]<5) and (0<=x[1]<4))]
            # collecting moves from opponent piece capture
            moves = self.any_capture(piece,result)
            #
            result = [x for x in result if (self.BOARD[x[0]][x[1]] == '___')]
            return result+moves
        #return 0
    
    def moves(self,piece,board):
        self.BOARD=board
        print('in moves '+piece)
        print(self.BOARD)
        if piece == 'wpa':
            row,col=self.index_finder(piece)
            # print("pawn is located at {v1}".format(v1=(row,col))) 
            move=self.legal_move_generation(piece,(row,col))
            # print('pawn moves are')
            # print(moves)
        elif piece == 'wrk':
            row,col=self.index_finder(piece)
            # print("rook is located at {v1}".format(v1=(row,col))) 
            # print('found rook index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('rook moves are')
            # print(moves)
        elif piece == 'wkn':
            row,col=self.index_finder(piece)
            # print("knight is located at {v1}".format(v1=(row,col))) 
            # print('found knight index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('knight moves are')
            # print(moves)
        elif piece == 'wbi':
            row,col=self.index_finder(piece)
            # print("bishop is located at {v1}".format(v1=(row,col))) 
            # print('found bishop index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('bishop moves are')
            # print(moves)
        elif piece == 'wki':
            row,col=self.index_finder(piece)
            # print("king is located at {v1}".format(v1=(row,col))) 
            # print('found king index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('king moves are')
            # print(moves)
        return move

#
class Micro_Black(Micro_Umpire):
    def __init__(self,eval_choice):
        super().__init__()
        #self.black_BOARD=[['bki','bkn','bbi','brk'],['bpa','___','___','___'],['___','___','___','___'],['___','___','___','___'],['___','___','___','___']]
        self.black_BOARD=self.black_BOARD
        self.turn_no=0
        #
        self.pieces=['bpa','bbi','bkn','bki','brk']
        self.capture_count={'bpa':[],'bbi':[],'bkn':[],'bki':[],'brk':[]}
        #
        self.eval=eval_choice
        #
        self.opp_pieces={"wpa":[],"wkn":[],"wrk":[],"wbi":[],"wki":[]}
        self.opp_pieces_count=5
    
    def index_finder(self, piece):
        # print('searching for piece {v1}'.format(v1=piece))
        for row in self.black_BOARD:
            # print(row)
            if (piece in row) and (piece in self.pieces):
                # print('found')
                pos=row.index(piece)
                return self.black_BOARD.index(row),pos # returns the index of the row and the column
            # else:
            #     return -10,-10
    
    # function needs to be edited
    def any_capture(self,piece,loc):
        if piece == 'bpa':
            moves=[]
            # loc returns the pawns current location
            row=loc[0]
            col=loc[1]
            #
            captures=[]
            # checks diagonal piece captures
            try:
                # try first diagonal opposite
                if ((col+1<4) and (self.BOARD[row+1][col+1]!='___') and (self.BOARD[row+1][col+1] in self.white_pieces)):
                    moves.append((row+1,col+1))
                    captures.append((row+1,col+1))
                # try second diagonal opposite
                if ((col-1>=0) and (self.BOARD[row+1][col-1]!='___') and (self.BOARD[row+1][col-1] in self.white_pieces)) :
                    moves.append((row+1,col-1))
                    captures.append((row+1,col-1))
            except IndexError:
                pass
            self.capture_count['bpa']=captures
            # print('pawn capture moves are {v1}\n'.format(v1=moves))
            return moves
        #
        elif piece == 'brk':
            moves=[]
            #
            captures=[]
            # loc returns the collection of maximum and minimum row and column (horizontal and vertical) free space available for rook
            min_row=loc[0]
            max_row=loc[1]
            min_col=loc[2]
            max_col=loc[3]
            row=loc[4] # current position row
            col=loc[5] # current position col
            # the indexerror catches any references made that exist outside of the board dimensions
            try:
                if ((min_col-1>=0) and (self.BOARD[row][min_col-1] != '___') and (self.BOARD[row][min_col-1] in self.white_pieces)):
                    moves.append((row,min_col-1))
                    captures.append((row,min_col-1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[row][max_col+1] != '___') and (self.BOARD[row][max_col+1] in self.white_pieces)):
                    moves.append((row,max_col+1))
                    captures.append((row,max_col+1))
            except IndexError:
                pass
            try:
                if ((min_row-1>=0) and (self.BOARD[min_row-1][col] != '___') and (self.BOARD[min_row-1][col] in self.white_pieces)):
                    moves.append((min_row-1,col))
                    captures.append((min_row-1,col))
            except IndexError:
                pass
            try:
                if ((self.BOARD[max_row+1][col] != '___') and (self.BOARD[max_row+1][col] in self.white_pieces)):
                    moves.append((max_row+1,col))
                    captures.append((max_row+1,col))
            except IndexError:
                pass
            self.capture_count['brk']=captures
            # print('rook capture moves are {v1}\n'.format(v1=moves))
            return moves
        #
        elif piece == 'bbi':
            moves=[]
            #
            captures=[]
            # loc returns the collection of maximum and minimum row and column number (along both diagonals) free space available for a bishop
            # diag1
            d1_e1_i=loc[0][0]
            d1_e1_j=loc[0][1]
            d1_e2_i=loc[1][0]
            d1_e2_j=loc[1][1]
            # diag2
            d2_e1_i=loc[2][0]
            d2_e1_j=loc[2][1]
            d2_e2_i=loc[3][0]
            d2_e2_j=loc[3][1]
            #
            row=loc[4]
            col=loc[5]
            #
            try:
                if((d1_e1_i-1>=0) and (d1_e1_j-1>=0) and (self.BOARD[d1_e1_i-1][d1_e1_j-1] != '___') and (self.BOARD[d1_e1_i-1][d1_e1_j-1] in self.black_pieces)):
                    moves.append((d1_e1_i-1,d1_e1_j-1))
                    captures.append((d1_e1_i-1,d1_e1_j-1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[d1_e2_i+1][d1_e2_j+1] != '___') and (self.BOARD[d1_e2_i+1][d1_e2_j+1] in self.black_pieces)):
                    moves.append((d1_e2_i+1,d1_e2_j+1))
                    captures.append((d1_e2_i+1,d1_e2_j+1))
            except IndexError:
                pass
            try:
                if ((self.BOARD[d2_e1_i+1][d2_e1_j+1] != '___') and (self.BOARD[d2_e1_i+1][d2_e1_j+1] in self.black_pieces)):
                    moves.append((d2_e1_i+1,d2_e1_j+1))
                    captures.append((d2_e1_i+1,d2_e1_j+1))
            except IndexError:
                pass
            try:
                if ((d2_e2_i-1>=0) and (d2_e2_j-1>=0) and (self.BOARD[d2_e2_i-1][d2_e2_j-1] != '___') and (self.BOARD[d2_e2_i-1][d2_e2_j-1] in self.black_pieces)):
                    moves.append((d2_e2_i-1,d2_e2_j-1))
                    captures.append((d2_e2_i-1,d2_e2_j-1))
            except IndexError:
                pass
            # print('bishop capture moves are {v1}\n'.format(v1=moves))
            self.capture_count['bbi']=captures
            return moves
        elif piece == 'bkn':
            # loc returns the possible positions the knight can take and checking if there are any enemy pieces in these positions
            # loc contains only valid positoins within the board due to its ordering in the legel_move_generation
            moves=[]
            #
            captures=[]
            #
            for pos in loc:
                if (self.BOARD[pos[0]][pos[1]] in self.white_pieces):
                    moves.append(pos)
                    captures.append(pos)
            self.capture_count['bkn']=captures
            # print('knight capture moves are {v1}'.format(v1=moves))
            return moves
        elif piece == 'bki':
            # loc returns current king position
            # add for check and checkmate clause positoin before adding move
            captures=[]
            moves=[]
            for pos in loc:
                if (self.BOARD[pos[0]][pos[1]] in self.white_pieces):
                    moves.append(pos)
                    captures.append(pos)
            # print('king capture moves are {v1}\n'.format(v1=moves))
            self.capture_count['bki']=captures
            return moves

    
    def legal_move_generation(self,piece,loc):
        row=loc[0]
        col=loc[1]
        legal_moves=[]

        # https://en.wikipedia.org/wiki/Kriegspiel_(chess) -- rules
        if piece == 'bpa':
            # print((row,col))
            # naturally a pawn can only move up ny one tile
            legal_moves=[(row+1,col)]
            # if turn_no is 0, the pawn can be moved two spaces up
            if self.turn_no == 0:
                legal_moves.append((row+2,col))
            # adding any moves that enable captures
            # print(legal_moves)
            legal_moves+=self.any_capture(piece,loc)
            # filtering moves that exceed board limit
            legal_moves=[x for x in legal_moves if ((0<=x[0]<5) or (0<=x[1]<4))]
            #
            return legal_moves
        #
        elif piece == 'brk':
            # setting base
            max_row=row
            min_row=row
            max_col=col
            min_col=col
            # print((max_row,min_row,max_col,min_col))
            # checking maximum vertical movement in the rows
            for i in range(row-1,-1,-1):
                if self.BOARD[i][col] != '___':
                    min_row=i+1
                    break
            # checking minimum vertical movement in the rows
            for i in range(row+1, 5):
                if self.BOARD[i][col] != '___':
                    max_row=i-1
                    break
            # checking minimum horizontal movement in the columns
            for i in range(col-1,-1,-1):
                if self.BOARD[row][i] != '___':
                    min_col=i+1
                    break
            # checking the maximum horizontal movment in the columns
            for i in range(col+1,4):
                if self.BOARD[row][i] !='___':
                    max_col=i-1
                    break
            # print((max_row,min_row,max_col,min_col))
            #legal_moves=[(row,col)] row and col indicate current real world position
            rk_possible_moves=[(x,col) for x in range(max_row,min_row-1,-1)] # checks for all the possible row positions
            rk_possible_moves+=[(row,x) for x in range(max_col,min_col-1,-1)] # checks for all possible column positions
            #
            moves=self.any_capture(piece, [min_row,max_row,min_col,max_col,row,col])
            legal_moves=rk_possible_moves+moves
            # removing piece original location
            legal_moves=list(set(legal_moves))
            origin=legal_moves.index((row,col))
            legal_moves.pop(origin)
            # return max_row,max_col,
            return legal_moves
        #
        elif piece == 'bbi':
            # for a bishop, I will first check all free spaces available on the diagonal
            # once it hits a natural block, either the board ending or an opponent piece in the way
            # I will call on capture to find out which piece is capturable
            #
            diag1_end1_i=row
            diag1_end1_j=col
            #
            diag2_end1_i=row
            diag2_end1_j=col
            #
            diag1_end2_i=row
            diag1_end2_j=col
            #
            diag2_end2_i=row
            diag2_end2_j=col
            #
            d1_e1_l=[['_','_']]
            d1_e2_l=[['_','_']]
            d2_e1_l=[['_','_']]
            d2_e2_l=[['_','_']]
            #
            # checking the top half of the diagonal space
            while(diag1_end1_j>=0 and diag2_end1_j<4):
                #
                diag1_end1_i-=1
                diag2_end1_i-=1
                #
                diag1_end1_j-=1
                diag2_end1_j+=1
                #
                if((diag1_end1_i<0) or (diag2_end1_i<0)):
                    diag1_end1_i+=1
                    diag2_end1_i+=1
                    #
                    d1_e1_l[0][0]=diag1_end1_i
                    d1_e1_l[0][1]=diag1_end1_j+1
                    #
                    d2_e1_l[0][0]=diag2_end1_i
                    d2_e1_l[0][1]=diag2_end1_j-1
                    break
                # diagonal 1
                if (0<=diag1_end1_j<4):
                    try:
                        if (self.BOARD[diag1_end1_i][diag1_end1_j] == '___'):
                            legal_moves.append((diag1_end1_i,diag1_end1_j))
                        else:
                            d1_e1_l[0][0]=diag1_end1_i
                            d1_e1_l[0][1]=diag1_end1_j
                    except IndexError:
                        pass
                if diag1_end1_j==0:
                    d1_e1_l[0][0]=diag1_end1_i
                    d1_e1_l[0][1]=diag1_end1_j
                # diagonal 2
                if (0<=diag2_end1_j<4):
                    try:
                        if (self.BOARD[diag2_end1_i][diag2_end1_j] == '___'):
                            legal_moves.append((diag2_end1_i,diag2_end1_j))
                        else:
                            d2_e1_l[0][0]=diag1_end1_i
                            d2_e1_l[0][1]=diag1_end1_j
                    except IndexError:
                        pass
                if diag2_end1_j==3:
                    d2_e1_l[0][0]=diag2_end1_i
                    d2_e1_l[0][1]=diag2_end1_j
            #
            # print('top legal_moves are {v1}\n'.format(v1=legal_moves))
            # checking the bottom half of the diagonal space
            while(diag1_end2_j<4 and diag2_end2_j>=0):
                #
                diag1_end2_i+=1
                diag2_end2_i+=1
                #
                diag1_end2_j+=1
                diag2_end2_j-=1
                #
                if((diag1_end2_i>4) or (diag2_end2_i>4)):
                    diag1_end2_i-=1
                    diag2_end2_i-=1
                    #
                    d1_e2_l[0][0]=diag1_end2_i
                    d1_e2_l[0][1]=diag1_end2_j-1
                    #
                    d2_e2_l[0][0]=diag2_end2_i
                    d2_e2_l[0][1]=diag2_end2_j+1
                    break
                #diagonal 1
                if(0<=diag1_end2_j<4):
                    try:
                        if (self.BOARD[diag1_end2_i][diag1_end2_j] == '___'):
                            legal_moves.append((diag1_end2_i,diag1_end2_j))
                        else:
                            d1_e2_l.append((diag1_end2_i,diag1_end2_j))
                    except IndexError:
                        pass
                if(diag1_end2_j==3):
                    d1_e2_l[0][0]=diag1_end2_i
                    d1_e2_l[0][1]=diag1_end2_j
                # diagonal 2
                if (0<=diag2_end2_j<4):
                    try:
                        if (self.BOARD[diag2_end2_i][diag2_end2_j] == '___'):
                            legal_moves.append((diag2_end2_i,diag2_end2_j))
                        else:
                            d2_e2_l.append((diag2_end2_i,diag2_end2_j))
                    except IndexError:
                        pass
                if(diag2_end2_j==0):
                    d2_e2_l[0][0]=diag2_end2_i
                    d2_e2_l[0][1]=diag2_end2_j
            # print('bottom legal_moves are {v1}\n'.format(v1=legal_moves))
            # print(d1_e1_l)
            # print(d2_e1_l)
            # print(d1_e2_l)
            # print(d2_e2_l)
            # 
            moves = self.any_capture(piece,[d1_e1_l[0],d1_e2_l[0],d2_e1_l[0],d2_e2_l[0],row,col])
            #
            legal_moves+=moves
            #
            return legal_moves
        #
        elif piece == 'bkn':
            #kn_possible_locations already contains te possible future locations for the knight to move
            kn_possible_positions = [(row+1,col+2),(row+2,col+1),(row-1,col+2),(row-2,col+1),(row-2,col-1),(row-1,col-2),(row+1,col-2),(row+2,col-1)]
            # print(kn_possible_positions)
            # eliminating moves that lie outside of the board
            result = [x for x in kn_possible_positions if ((0<=x[0]<5) and (0<=x[1]<4))] # eliminating positions that lie outside of the board
            # collecting moves from opponent piece capture
            moves=self.any_capture(piece,result)
            # cleanup of result, which included blocked spaces, moves above collects opponent piece captures, only collecting free space spots
            result=[x for x in result if (self.BOARD[x[0]][x[1]] == '___')] # technically returning all the possible positions, fails to fulfill function objective but hey, it works
            #
            legal_moves=result+moves
            return legal_moves
        #
        elif piece == 'bki':
            # ki_possible_locations contains possible future moves of the king
            ki_possible_positions = [(row+1,col-1),(row+1,col),(row+1,col+1),(row,col-1),(row,col+1),(row-1,col-1),(row-1,col),(row-1,col+1)]
            # eliminating moves that lie outside of the board
            result = [x for x in ki_possible_positions if ((0<=x[0]<5) and (0<=x[1]<4))]
            # collecting moves from opponent piece capture
            moves = self.any_capture(piece,result)
            #
            result = [x for x in result if (self.BOARD[x[0]][x[1]] == '___')]
            return result+moves
        #return 0

    def moves(self,piece,board):
        self.BOARD=board
        move=[]
        print('in moves '+piece)
        print(self.BOARD)
        if piece == 'bpa':
            row,col=self.index_finder(piece)
            # print("pawn is located at {v1}".format(v1=(row,col))) 
            move=self.legal_move_generation(piece,(row,col))
            # print('pawn moves are')
            # print(moves)
        elif piece == 'brk':
            row,col=self.index_finder(piece)
            # print("rook is located at {v1}".format(v1=(row,col))) 
            # print('found rook index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('rook moves are')
            # print(moves)
        elif piece == 'bkn':
            row,col=self.index_finder(piece)
            # print("knight is located at {v1}".format(v1=(row,col))) 
            # print('found knight index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('knight moves are')
            # print(moves)
        elif piece == 'bbi':
            row,col=self.index_finder(piece)
            # print("bishop is located at {v1}".format(v1=(row,col))) 
            # print('found bishop index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('bishop moves are')
            # print(moves)
        elif piece == 'bki':
            row,col=self.index_finder(piece)
            # print("king is located at {v1}".format(v1=(row,col))) 
            # print('found king index\n')
            move=self.legal_move_generation(piece,(row,col))
            # print('king moves are')
            # print(moves)
        return move

#
class HumanAgent(Micro_Umpire):#
    def __init__(self,color):
        self.color=color
        self.move_history=[]
    
#
def create_human():
    while(True):
        pl_choice=input("Would You like to play?\n enter y or Y for yes\n or any character for no\n")
        if pl_choice == 'y' or pl_choice=='Y':
            color_choice=input('\n enter color of preference\n b for black\n w for white\n')
            if color_choice == 'b' or color_choice == 'w':
                human=HumanAgent(color_choice)
                return human
            else:
                print("\n incorrect option, please try again\n")
        else:
            print(' no human agent is created\n')
            return None

#

def main_game():
    # declaring umpire
    umpire=Micro_Umpire()
    # declaring human agent if human wishes to play
    human=create_human()
    if human is None:
        print(' you have chosen no human agent involvement,\n this will now be a game between two computer agents\n please feel free to exit the process by pressing Ctrl+C\n')
        
        print(" the type of evaluation you would like for your game, press number provided\n 1. 1 for Random\t2. 2 for MiniMax\t")
        print(' this evaluation choice is for the white player\n')
        eval_choice=int(input())
        white_computer=Micro_White(eval_choice)
        print(' this evaluation choice is for the black player\n')
        black_computer=Micro_Black(eval_choice)
        #
        umpire.black=black_computer
        umpire.white=white_computer
    else:
        if human.color == 'b':
            print(' since the human agent is black the agent plays as white\n')
            print(" the type of evaluation you would like for your game, press number provided\n 1. 1 for Random\t2. 2 for MiniMax\t")
            eval_choice=int(input())
            white_computer=Micro_White(eval_choice)
            umpire.black=human
            umpire.white=white_computer

        elif human.color == 'w':
            print(' since the human agent is white the agent plays as black\n')
            print(" the type of evaluation you would like for your game, press number provided\n 1. 1 for Random\t2. 2 for MiniMax\t")
            eval_choice=int(input())
            black_computer=Micro_Black(eval_choice)
            umpire.white=human
            umpire.black=black_computer
        else:
            print('invalid execution\n')
            main_game()

    # game sequences
    print(umpire.black)
    playing=True
    if human is not None:
        if isinstance(umpire.white,HumanAgent):
            while(playing):
                print("this is turn no {v1}".format(v1=umpire.turn_no))
                umpire.print_board()
                #
                if umpire.turn_no %2 ==0:
                    print(' white to play\n')
                    choice=input(" enter a position and move in the form piece,move\n ")
                #
                else:
                    move=umpire.mini_max(umpire.BOARD,'b',0)
                umpire.turn_no+=1
        elif isinstance(umpire.black,HumanAgent):
            while(playing):
                print("this is turn no {v1}".format(v1=umpire.turn_no))
                umpire.print_board()
                #
                if umpire.turn_no %2 ==0:
                    move=umpire.mini_max(umpire.BOARD,'w',0)
                #
                else:
                    print(' black to play\n')
                    choice=input(" enter a position and move in the form piece,move\n ")
                umpire.turn_no+=1
    else:
        while(playing):
            print("\n\n\n new turn {v1}\n\n\n".format(v1=umpire.turn_no))
            umpire.print_board()
            print(umpire.black_pieces)
            print(umpire.black.pieces)
            print(umpire.white_pieces)
            print(umpire.white.pieces)
            #
            if umpire.turn_no>3:
                break
            if umpire.turn_no % 2 ==0:
                move=umpire.mini_max(umpire.BOARD,umpire.white,0)
                umpire.BOARD=umpire.board_update(umpire.BOARD,move[1],move[0],umpire.white)
            elif umpire.turn_no % 2 ==1:
                move=umpire.mini_max(umpire.BOARD,umpire.black,0)
                umpire.BOARD=umpire.board_update(umpire.BOARD,move[1],move[0],umpire.black)
            # break
            umpire.turn_no+=1

        

        




#
if __name__ == "__main__":
    main_game()
 