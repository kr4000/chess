#COPYRIGHT KEVIN J REIF
#2020 BRIGHTON MI


from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import PermissionDenied


from mysite.models import model


import json





def get_object(request):
    chess_game_state_instance = model.get_game_state(request.session['id'])

    obj={}
    obj['rows']=json.loads(chess_game_state_instance.field)
    obj['id']= chess_game_state_instance.game_id 
    obj['players_turn']=chess_game_state_instance.players_turn
    obj['message']=chess_game_state_instance.message


    return obj

def new_game(request):
    chess_game_instance=model.new_game()
    request.session["id"] = chess_game_instance.id 


def move(request):
    a_row = request.POST.get("a_row")
    a_col = request.POST.get("a_col")
    b_row = request.POST.get("b_row")
    b_col = request.POST.get("b_col")


    print([a_row,a_col,b_row,b_col])
    #validation
    execute=True
    for i in [a_row,a_col,b_row,b_col]:
        if i is None:
            execute=False
            break
        try:
            x=int(i)
            if x<0 or x>7:
                execute=False

        except:
            execute=False
            break

    if execute:
        model.move(request.session['id'], int(a_row), int(a_col), int(b_row), int(b_col))


def delete_game(request):
    model.delete_game(request.session['id'])


def main_view(request):

    if request.session.test_cookie_worked() or 'id' in request.session:
        if request.method == "GET":
            if "id" not in request.session:
                new_game(request)

        elif request.method == 'POST':      
            if(request.POST.get("function")== "move"):
                move(request)

            elif(request.POST.get("function")== "new_game"):
                delete_game(request)
                new_game(request)

        return render(request, "main_view.html", get_object(request))
    
    return redirect("start_view")


