# interface.py
import pygame
import time
from config import *
from corrida import Jogador
from eventos import lancar_moeda, obter_frequencias, obter_contadores
from plots.grafico import Grafico

class GameInterface:
    def __init__(self, num_players=2, cells=NUM_CELLS):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Corrida da Moeda - Edição Estratégica")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(FONT_NAME, 20)
        self.bigfont = pygame.font.SysFont(FONT_NAME, 36)

        self.num_players = max(2, min(num_players, MAX_PLAYERS))
        self.cells = cells
        self.players = []
        for i in range(self.num_players):
            name = f"Jogador {i+1}"
            color = PLAYER_COLORS[i % len(PLAYER_COLORS)]
            self.players.append(Jogador(name, color, i))

        self.current_player = 0
        self.finished_count = 0
        self.podium_rank = 0

        # coin animation state
        self.animating = False
        self.anim_start_time = None
        self.anim_duration = COIN_ANIM_MS / 1000.0  # segundos

        # grafico
        self.grafico = Grafico()

        # UI buttons (rects)
        self.btn_flip = pygame.Rect(GAME_AREA_WIDTH + 50, 520, 200, 50)
        self.btn_reset = pygame.Rect(GAME_AREA_WIDTH + 50, 590, 200, 40)

    def draw_board(self):
        # desenha caminho horizontal
        for i in range(self.cells):
            x = BOARD_LEFT + i * CELL_SIZE
            y = BOARD_Y
            rect = pygame.Rect(x, y, CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(self.screen, (200,200,200), rect)
            # número da casa
            num_surf = self.font.render(str(i), True, (40,40,40))
            self.screen.blit(num_surf, (x + 4, y + 4))

    def draw_players(self):
        for p in self.players:
            x = BOARD_LEFT + p.posicao * CELL_SIZE + CELL_SIZE // 2
            y = BOARD_Y + CELL_SIZE // 2
            # deslocar verticalmente por jogador para não sobrepor
            offset_y = (p.idx - (self.num_players-1)/2) * 18
            pygame.draw.circle(self.screen, p.cor, (x, int(y + offset_y)), 12)
            name_surf = self.font.render(p.nome, True, (255,255,255))
            self.screen.blit(name_surf, (x - 18, y + 20 + offset_y))

    def draw_ui(self):
        # painel lateral
        panel_x = GAME_AREA_WIDTH + 20
        self.screen.fill((40,40,40), (GAME_AREA_WIDTH, 0, GRAPH_AREA_WIDTH, WINDOW_HEIGHT))

        title = self.bigfont.render("Estatística da Moeda", True, (255,255,255))
        self.screen.blit(title, (GAME_AREA_WIDTH + 30, 20))

        # jogador da vez
        cp = self.players[self.current_player]
        turn_txt = self.font.render(f"Vez: {cp.nome}", True, (255,255,255))
        self.screen.blit(turn_txt, (GAME_AREA_WIDTH + 30, 80))

        cara, coroa, total = obter_contadores()
        counts_txt = self.font.render(f"Caras: {cara}  Coroas: {coroa}  Total: {total}", True, (255,255,255))
        self.screen.blit(counts_txt, (GAME_AREA_WIDTH + 30, 110))

        # botão lançar
        pygame.draw.rect(self.screen, (100,200,100), self.btn_flip)
        flip_txt = self.font.render("Lançar Moeda", True, (0,0,0))
        self.screen.blit(flip_txt, (self.btn_flip.x + 30, self.btn_flip.y + 15))

        # botão reset
        pygame.draw.rect(self.screen, (200,80,80), self.btn_reset)
        reset_txt = self.font.render("Resetar Jogo", True, (0,0,0))
        self.screen.blit(reset_txt, (self.btn_reset.x + 40, self.btn_reset.y + 10))

        # podium (se já existirem colocados)
        podium_y = 180
        podium_title = self.font.render("Pódio (parcial):", True, (255,255,255))
        self.screen.blit(podium_title, (GAME_AREA_WIDTH + 30, podium_y))
        for p in sorted(self.players, key=lambda x: (x.colocacao is None, x.colocacao)):
            idx = p.colocacao
            if idx is None:
                continue
            text = f"{idx}º - {p.nome}"
            self.screen.blit(self.font.render(text, True, (255,255,0)), (GAME_AREA_WIDTH + 30, podium_y + 20 * idx))

    def start_coin_animation(self):
        self.animating = True
        self.anim_start_time = time.time()

    def update_coin_animation(self):
        """
        Retorna True se a animação terminou neste frame (ou False se ainda animando).
        """
        if not self.animating:
            return False
        elapsed = time.time() - self.anim_start_time
        if elapsed >= self.anim_duration:
            self.animating = False
            return True
        return False

    def handle_flip_result(self):
        # efetua o lançamento real (após animação)
        res = lancar_moeda()  # 'H' ou 'T'
        if res == "H":
            # avança jogador atual
            p = self.players[self.current_player]
            if p.ativo:
                p.posicao += 1
                if p.posicao >= self.cells - 1:
                    # chegou ao fim
                    self.podium_rank += 1
                    p.colocacao = self.podium_rank
                    p.ativo = False
                    self.finished_count += 1
        # atualizar gráfico (matplotlib) chamando grafico.atualizar()
        # aqui chamamos o método que re-desenha o gráfico
        self.grafico.atualizar()
        # passar turno para o próximo jogador ativo
        self.next_turn()

    def next_turn(self):
        # avança até encontrar próximo jogador ativo (ou encerra se todos terminaram)
        if self.finished_count >= self.num_players:
            return
        next_idx = (self.current_player + 1) % self.num_players
        start_idx = next_idx
        while not self.players[next_idx].ativo:
            next_idx = (next_idx + 1) % self.num_players
            # se todos inativos, para
            if next_idx == start_idx:
                return
        self.current_player = next_idx

    def reset_game(self):
        for i, p in enumerate(self.players):
            p.posicao = 0
            p.ativo = True
            p.colocacao = None
        self.current_player = 0
        self.finished_count = 0
        self.podium_rank = 0
        # reiniciar contadores da simulação
        # nota: eventos.sim é o objeto global; vamos reiniciar criando um novo (hack simples)
        from eventos import sim as sim_obj
        sim_obj.cara = 0
        sim_obj.coroa = 0
        sim_obj.total = 0
        self.grafico.atualizar()

    def draw_coin(self):
        # desenha uma "moeda" animada simples dependendo do tempo restante
        center = (GAME_AREA_WIDTH + 150, 420)
        # se animando, fazer um efeito de "flip" (mudar largura)
        if self.animating:
            elapsed = time.time() - self.anim_start_time
            progress = elapsed / self.anim_duration
            # largura oscila entre 26 e 60
            width = int(60 * abs(0.5 - progress) * 2) + 10
            pygame.draw.ellipse(self.screen, (220, 220, 100), (center[0]-width//2, center[1]-30, width, 60))
            text = self.font.render("...", True, (0,0,0))
            self.screen.blit(text, (center[0]-10, center[1]-10))
        else:
            # mostrar a última contagem/estado (cara ou coroa)
            cara, coroa, total = obter_contadores()
            # se houver ao menos 1 lançamento, mostre último valor aproximado por comparar frequências
            if total > 0:
                # mostra proporção de caras numericamente
                txt = f"Caras: {cara}"
            else:
                txt = "Clique em Lançar"
            pygame.draw.circle(self.screen, (220,220,100), center, 30)
            text = self.font.render(txt, True, (0,0,0))
            self.screen.blit(text, (center[0]-40, center[1]-10))

    def run(self):
        running = True
        # desenhar gráfico inicialmente
        self.grafico.atualizar()

        while running:
            self.screen.fill((25,25,25))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if self.btn_flip.collidepoint(mx, my) and not self.animating and self.finished_count < self.num_players:
                        # iniciar animação; o resultado será aplicado quando a animação terminar
                        self.start_coin_animation()
                    elif self.btn_reset.collidepoint(mx, my):
                        self.reset_game()

            # atualizar animação
            if self.animating:
                finished_anim = self.update_coin_animation()
                if finished_anim:
                    # aplicar resultado e atualizar gráfico
                    self.handle_flip_result()
            # desenhar partes
            self.draw_board()
            self.draw_players()
            self.draw_ui()
            self.draw_coin()

            # desenha legenda do gráfico (a janela matplotlib fica separada)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
