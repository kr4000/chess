#COPYRIGHT KEVIN J REIF
#2020 BRIGHTON MI



from django.test import TestCase
from mysite.models import model

import json
class ChessTestCase(TestCase):


    def setUp(self):
        pass

    def test(self):

        cg = model.new_game()
        model.move(cg.id, 7, 1, 6, 1)
        print(str(cg))
        print("hello")


        cg1 = model.new_game()


class ChessCheckTest(TestCase):

    def setUp(self):
        pass

    def test(self):

        field=json.loads("[[['black', 'rook'], ['black', 'knight'], ['black', 'bishop'], ['black', 'queen'], ['black', 'king'], ['black', 'bishop'], ['black', 'knight'], ['black', 'rook']], [['black', 'pawn'], ['black', 'pawn'], ['black', 'pawn'], null, null, ['black', 'pawn'], ['black', 'pawn'], ['black', 'pawn']], [null, null, null, ['black', 'pawn'], ['white', 'queen'], null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, null, null, null, null], [null, null, null, null, ['white', 'pawn'], null, null, null], [['white', 'pawn'], ['white', 'pawn'], ['white', 'pawn'], ['white', 'pawn'], null, ['white', 'pawn'], ['white', 'pawn'], ['white', 'pawn']], [['white', 'rook'], ['white', 'knight'], ['white', 'bishop'], null, ['white', 'king'], ['white', 'bishop'], ['white', 'knight'], ['white', 'rook']]]")
        field1=field.copy()
        model.is_check(field, "black")
        model.is_check(field, "white")
        assert field1==field


class ArrayTest(TestCase):

    def setUp(self):
        pass

    def test(self):

        lis1=[1,2,3]
        lis2=lis1.copy()
        lis1[1]=5
        assert lis1!=lis2


        lis1=[1,2,3]
        lis2=lis1.copy()
        lis2[1]=5
        assert lis1!=lis2





class ArrayTest(TestCase):

    def setUp(self):
        pass

    def test(self):

        lis1=[1,2,3]
        lis2=lis1.copy()
        lis1[1]=5
        assert lis1!=lis2


        lis1=[1,2,3]
        lis2=lis1.copy()
        lis2[1]=5
        assert lis1!=lis2

