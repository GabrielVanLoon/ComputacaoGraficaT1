#!/usr/bin/env python3
from src.GameController import GameController
from src.objects import GameObject

def main():
    game = GameController(title="Testing Game Controller", width=1200, height=600, enable3D=False)
    game.start()

if __name__ == '__main__':
    main()