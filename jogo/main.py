# main.py
from interface import GameInterface

def main():
    # escolha quantos jogadores quer (2..4). Pode ajustar aqui:
    game = GameInterface(num_players=3, cells=20)
    game.run()

if __name__ == "__main__":
    main()
