#!/usr/bin/env python3

from src.GameController import GameController
from src.objects.geometrics.SquareObject import SquareObject
from src.objects.geometrics.TriangleObject import TriangleObject 
from src.objects.geometrics.RectangleObject import RectangleObject 
from src.objects.examples.RunningSquareObject import RunningSquareObject


def main():

    scene_scheme = [
        {
            "type": RunningSquareObject,
            "items": [
                { "position":(50,50), "size":(100,100), "rotate":0 },
            ] 
        },
        {
            "type": SquareObject,
            "items": [
                { "position":(300,300), "size":(50,50), "rotate":0 },
                { "position":(300,400), "size":(50,50), "rotate":45 },
                { "position":(300,100), "size":(100,100), "rotate":15 },
            ] 
        },
        {
            "type": TriangleObject,
            "items": [
                { "position":(600,300), "size":(300,300), "rotate":0 },
                { "position":(900,300), "size":(600,300), "rotate":70 },
            ] 
        },
        {
            "type": RectangleObject,
            "items": [
                { "position":(900,300), "size":(200,200), "rotate":0 },
            ] 
        },
    ]

    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()