from interface import GameInterface
from plots.grafico import Grafico

def main():
    g = Grafico()
    game = GameInterface(g)
    game.loop()

if __name__ == "__main__":
    main()
