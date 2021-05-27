#!/usr/bin/env python3

from src.GameController import GameController
from src.objects.geometrics.SquareObject import SquareObject

from src.objects.geometrics.TriangleObject import TriangleObject 
from src.objects.geometrics.RectangleObject import RectangleObject 

from src.objects.examples.RunningSquareObject import RunningSquareObject
from src.objects.examples.BoucingBallObject import BoucingBallObject

from src.objects.complex.RobotObject import RobotObject
from src.objects.complex.BoxObject import BoxObject
from src.objects.complex.ContainerObject import ContainerObject
from src.objects.complex.ParedeSageObject import ParedeSageObject
from src.objects.complex.GateObject import GateObject
from src.objects.complex.RotatorObject import RotatorObject
from src.objects.complex.FlamesObject import FlamesObject



def main():

    scene_scheme = [
        {
            "type": RobotObject,
            "items": [
                { "position":(100,50), "size":(70,70), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
        # {
        #     "type": BoxObject,
        #     "items": [
        #         { "position":(50,550), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
        #     ] 
        # },
        # {
        #     "type": ContainerObject,
        #     "items": [
        #         { "position":(50,450), "size":(0.35*100,100), "rotate":90, "props": { "hitbox": True } },
        #     ] 
        # },
        # {
        #     "type": ParedeSageObject,
        #     "items": [
        #         { "position":(50,450), "size":(100*.4,300), "rotate":0, "props": { "hitbox": True } },
        #     ] 
        # },
        # {
        #     "type": GateObject,
        #     "items": [
        #         { "position":(50,350), "size":(60,100), "rotate":0, "props": { "hitbox": True } },
        #     ] 
        # },
        # {
        #     "type": RotatorObject,
        #     "items": [
        #         { "position":(50,250), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
        #     ] 
        # },
        {
            "type": FlamesObject,
            "items": [
                { "position":(50,350), "size":(100,100), "rotate":90, "props": { "hitbox": True } },
            ] 
        },
        # {
        #     "type": RunningSquareObject,
        #     "items": [
        #         { "position":(500,500), "size":(200,200), "rotate":0, "props": { "hitbox": True } },
        #     ] 
        # },
        # {
        #     "type": BoucingBallObject,
        #     "items": [
        #         { "position":(50,50), "size":(100,100), "rotate":0, "props": { "hitbox": True }},
        #     ] 
        # },
        # {
        #     "type": SquareObject,
        #     "items": [
        #         { "position":(300,300), "size":(50,50), "rotate":0 },
        #         { "position":(300,400), "size":(50,50), "rotate":45 },
        #         { "position":(300,100), "size":(100,100), "rotate":15 },
        #     ] 
        # },
        # {
        #     "type": TriangleObject,
        #     "items": [
        #         { "position":(600,300), "size":(300,300), "rotate":0 },
        #         { "position":(900,300), "size":(600,300), "rotate":70 },
        #     ] 
        # },
        # {
        #     "type": RectangleObject,
        #     "items": [
        #         { "position":(900,300), "size":(200,200), "rotate":0 },
        #     ] 
        # },
    ]

    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()