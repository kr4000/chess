#COPYRIGHT KEVIN J REIF
#2020 BRIGHTON MI


from django.db import models
import datetime
import functools
import re
import json
import traceback
import sys
import copy

class chess_game(models.Model):
    id = models.AutoField(primary_key=True)    
    date_created= models.DateField()
    last_accesed = models.DateField()


class chess_game_state(models.Model):
    id = models.AutoField(primary_key=True)    
    date_created= models.DateField()
    field = models.CharField(max_length=1280)
    players_turn=models.CharField( max_length=5)
    current=models.CharField( max_length=5)
    message=models.CharField(max_length=100)
    game_id = models.ForeignKey(chess_game, on_delete=models.CASCADE)




rows=[
            [("black","rook"),("black","knight"),("black","bishop"),("black","queen"),("black","king"),("black","bishop"),("black","knight"),("black","rook")],
            [("black","pawn"),("black","pawn"),("black","pawn"),("black","pawn"),("black","pawn"),("black","pawn"),("black","pawn"),("black","pawn")],
            [None,None,None,None,None,None,None,None],
            [None,None,None,None,None,None,None,None],
            [None,None,None,None,None,None,None,None],
            [None,None,None,None,None,None,None,None],           
            [("white","pawn"),("white","pawn"),("white","pawn"),("white","pawn"),("white","pawn"),("white","pawn"),("white","pawn"),("white","pawn")],
            [("white","rook"),("white","knight"),("white","bishop"),("white","queen"),("white","king"),("white","bishop"),("white","knight"),("white","rook")],
        ]

utf_chars={
            ("black","rook"):"♜",
            ("black","knight"):"♞",
            ("black","bishop"):"♝",
            ("black","queen"):"♛",
            ("black","king"):"♚",
            ("black","pawn"):"♟",

            ("white","rook"):"♖",
            ("white","knight"):"♘",
            ("white","bishop"):"♗",
            ("white","queen"):"♕",
            ("white","king"):"♔",
            ("white","pawn"):"♙",


}
def move_execute(field, a_row, a_col, b_row, b_col):
    piece=field[a_row][a_col]
    field[a_row][a_col] = None
    field[b_row][b_col] = piece



def is_check(field, players_turn):
    other_player=get_other_player(players_turn)

    players_king=(None, None)

    for y in range(0,8):
        for x in range(0,8):
            if(field[y][x]==(players_turn, "king") or field[y][x]==[players_turn, "king"]):
                players_king=(y,x)

    for y in range(0,8):
        for x in range(0,8):
            if(is_legal(field, other_player, y, x, players_king[0], players_king[1])):
                return True


def is_checkmate(field, players_turn):
    if(not is_check(field, players_turn)):
        return False


    for y1 in range(0,8):
        for x1 in range(0,8):
            for y2 in range(0,8):
                for x2 in range(0,8):
                    if(is_legal(field, players_turn, y1, x1, y2, x2)):
                        new_field = copy.deepcopy(field)
                        move_execute(new_field, y1, x1, y2, x2)
                        if(not is_check(new_field, players_turn )):
                            return False
    return True

    


def get_other_player(players_turn):
    return "white" if players_turn=="black" else "black"

def is_legal(field, players_turn,a_row, a_col, b_row, b_col):

    

    if a_row<0 or a_row>7 or  a_col<0 or a_col>7  or  b_row<0 or b_row>7 or  b_col<0 or b_col>7:
        return False

    if field[a_row][a_col] is None:
        return False
        
    if field[b_row][b_col] is not None:
        if field[a_row][a_col][0]==field[b_row][b_col][0]:
            return False

    piece=field[a_row][a_col]
    if piece[0]!=players_turn:
        return False




    if(piece==("white","pawn") or piece==["white","pawn"]):
        return (a_col==b_col and (b_row==(a_row-1) or b_row==(a_row-2) and field[a_row-1][b_col] is None)) or \
                ((a_row-1)==b_row and abs(a_col-b_col)==1 and field[b_row][b_col] is not None and field[b_row][b_col][0]=="black")


    if(piece==("black","pawn")) or piece==["black","pawn"]:
        return (a_col==b_col and (b_row==(a_row+1) or b_row==(a_row+2) and field[a_row+1][b_col] is None)) or\
            ((a_row+1)==b_row and abs(a_col-b_col)==1 and field[b_row][b_col] is not None and field[b_row][b_col][0]=="white")



    if(piece[1]=="rook"):
        if(a_col==b_col):
            iy = 1 if b_row>a_row else -1
            for i in range(1,abs(b_row-a_row)):
                if field[a_row+i*iy][a_col] is not None:
                    return False
            return True
        if(a_row==b_row):
            ix = 1 if b_col>a_col else -1
            for i in range(1,abs(b_col-a_col)):
                if field[a_row][a_col+i*ix] is not None:
                    return False
            return True
        return False

    if(piece[1]=="knight"):
        return (a_col-b_col)*(a_row-b_row)  in [-2,2]

    if(piece[1]=="bishop"):
        if (abs(a_col-b_col)-abs(a_row-b_row))!=0:
            return False
        ix = 1 if b_row>a_row else -1
        iy = 1 if b_col>a_col else -1

        for i in range(1, (a_row-b_row)):
            #print(i, a_row+i, a_col+i, a_row-b_row, field[a_row+ix*i][a_col+iy*i])
            if field[a_row+ix*i][a_col+iy*i] is not None:
                return False
        return True
        
    if(piece[1]=="queen"):
        if(a_col==b_col):
            iy = 1 if b_row>a_row else -1
            for i in range(1,abs(b_row-a_row)):
                if field[a_row+i*iy][a_col] is not None:
                    return False
            return True
        if(a_row==b_row):
            ix = 1 if b_col>a_col else -1
            for i in range(1,abs(b_col-a_col)):
                if field[a_row][a_col+i*ix] is not None:
                    return False
            return True
        if(abs(a_row-b_row)==abs(a_col-b_col)):
            ix = 1 if b_row>a_row else -1
            iy = 1 if b_col>a_col else -1

            for i in range(1, (a_row-b_row)):
                #print(i, a_row+i, a_col+i, a_row-b_row, field[a_row+ix*i][a_col+iy*i])
                if field[a_row+ix*i][a_col+iy*i] is not None:
                    return False
            return True




        return False
    if(piece[1]=="king"):
        return (a_col-b_col) in [-1,0,1] and (a_row-b_row) in [-1, 0, 1]

    return False


def delete_game(id):
    chess_game.objects.filter(id=id).delete()

def new_game():
    chess_game_instance = chess_game.objects.create(date_created=datetime.datetime.now(), last_accesed=datetime.datetime.now())
    chess_game_instance.save()
    chess_game_state_instance = chess_game_state.objects.create(date_created=datetime.datetime.now(), field=json.dumps(rows), players_turn="white", current="True", message='',  game_id=chess_game_instance)
    chess_game_state_instance.save()
    return chess_game_instance


get_id = lambda x:id(x)

def move(id, a_row, a_col, b_row, b_col):
    chess_game_instance = chess_game.objects.get(id=id)
    chess_game_state_instance=chess_game_state.objects.get(game_id=id,current="True")


    other_player=get_other_player(chess_game_state_instance.players_turn)
    field= json.loads(chess_game_state_instance.field)

    if (is_legal(field, chess_game_state_instance.players_turn , a_row, a_col, b_row, b_col)):
        chess_game_state_instance.current="False"
        chess_game_state_instance.save()
        move_execute(field, a_row, a_col, b_row, b_col)
        message=""
        check=is_check(field,other_player )
        if(check):
            message="check"
        checkmate =is_checkmate(field, other_player )
        if(checkmate):
            message="checkmate"
        x = chess_game_state.objects.create(date_created=datetime.datetime.now(), field=json.dumps(field), players_turn=other_player, current="True", message=message, game_id=chess_game_instance)
        x.save()

def get_game_state(id):
    chess_game_state_instance = chess_game_state.objects.get(game_id=id,current="True")
    return chess_game_state_instance










