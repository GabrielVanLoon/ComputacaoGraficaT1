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
                { "position":(50,150), "size":(70,70), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": BoxObject,
            "items": [
                { "position":(150, 50), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
                { "position":(150,150), "size":(100,100), "rotate":90, "props": { "hitbox": True } },
                { "position":(150,250), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
                { "position":(275,325), "size":( 48, 48), "rotate":180, "props": { "hitbox": True } },
                { "position":(475,325), "size":( 48, 48), "rotate":0, "props": { "hitbox": True } },
                { "position":(675,325), "size":( 48, 48), "rotate":270, "props": { "hitbox": True } },
                { "position":(875,325), "size":( 48, 48), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": ContainerObject,
            "items": [
                { "position":(150,550), "size":(0.6*100,200), "rotate":90, "props": { "hitbox": True } },
                { "position":(175,325), "size":(150,49), "rotate":0, "props": { "hitbox": True } },
                { "position":(375,325), "size":(150,49), "rotate":0, "props": { "hitbox": True } },
                { "position":(575,325), "size":(150,49), "rotate":0, "props": { "hitbox": True } },
                { "position":(775,325), "size":(150,49), "rotate":180, "props": { "hitbox": True } },
                { "position":(975,325), "size":(150,49), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": ParedeSageObject,
            "items": [
                # { "position":(50,450), "size":(100,100*.4), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": GateObject,
            "items": [
                # { "position":(51,350), "size":(100,60), "rotate":0, "props": { "hitbox": True } },
                # { "position":(350,350), "size":(100,60), "rotate":90, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": RotatorObject,
            "items": [
                { "position":(60,500), "size":(100,100), "rotate":90, "props": { "hitbox": True } },
                # { "position":(400,250), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
                # { "position":(400,350), "size":(100,100), "rotate":45, "props": { "hitbox": True } },
                # { "position":(400,450), "size":(100,100), "rotate":90, "props": { "hitbox": True } },
            ] 
        },
        {
            "type": FlamesObject,
            "items": [
                { "position":(50,600), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
                { "position":(50,50), "size":(100,100), "rotate":0, "props": { "hitbox": True } },
            ] 
        },
    ]

    game = GameController(title="Testing Game Controller", width=1200, height=650, enable3D=False, scheme=scene_scheme)
    game.start()



if __name__ == '__main__':
    main()