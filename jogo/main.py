from jogo.interface import GameInterface
from plots.grafico import Grafico

def main():
    grafico = Grafico()
    jogo = GameInterface(grafico)
    jogo.loop()  # Loop principal do pygame

if __name__ == "__main__":
    main()
