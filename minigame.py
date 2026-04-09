import pygame
import random
import sys

pygame.init()

# ─── Configurações da tela ───────────────────────────────────────────────────
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini-Game — Ports & Adapters Crew")
relogio = pygame.time.Clock()

# ─── Cores ───────────────────────────────────────────────────────────────────
PRETO       = (15,  15,  20)
BRANCO      = (240, 240, 240)
AZUL_JOGADOR= (70,  130, 220)
VERMELHO    = (210,  50,  50)
LARANJA     = (230, 130,  30)
ROXO        = (160,  70, 210)
AMARELO     = (230, 200,  40)
VERDE       = (60,  180,  80)
CINZA       = (120, 120, 130)
CIANO       = (60,  200, 200)

# ─── Fontes ──────────────────────────────────────────────────────────────────
fonte_hud   = pygame.font.SysFont("monospace", 22, bold=True)
fonte_grande= pygame.font.SysFont("monospace", 42, bold=True)
fonte_media = pygame.font.SysFont("monospace", 28, bold=True)

# ─── Configuração de Níveis (Nível 3) ────────────────────────────────────────
NIVEIS = {
    1: {"vel_inimigo": 2,   "qtd_inimigos": 5,  "pontos_prox": 500},
    2: {"vel_inimigo": 3,   "qtd_inimigos": 7,  "pontos_prox": 1000},
    3: {"vel_inimigo": 4,   "qtd_inimigos": 10, "pontos_prox": float("inf")},
}

# ─── Classes ─────────────────────────────────────────────────────────────────

class Jogador:
    def __init__(self):
        self.rect  = pygame.Rect(LARGURA // 2 - 25, ALTURA - 70, 50, 50)
        self.vel   = 5
        self.vidas = 5          # Nível 1: 5 vidas iniciais
        self.cor   = AZUL_JOGADOR

    def mover(self, teclas):
        if teclas[pygame.K_LEFT]  and self.rect.left  > 0:
            self.rect.x -= self.vel
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
            self.rect.x += self.vel
        if teclas[pygame.K_UP]    and self.rect.top   > 0:
            self.rect.y -= self.vel
        if teclas[pygame.K_DOWN]  and self.rect.bottom< ALTURA:
            self.rect.y += self.vel

    def desenhar(self, surf):
        pygame.draw.rect(surf, self.cor, self.rect, border_radius=8)
        # detalhe — cockpit
        pygame.draw.rect(surf, CIANO,
                         pygame.Rect(self.rect.x + 15, self.rect.y + 8, 20, 14),
                         border_radius=4)


class Inimigo:
    """Inimigo base — Nível 2: 3 pontos de vida."""
    LARGURA  = 50
    ALTURA_I = 50
    VIDA_MAX = 3

    def __init__(self, vel):
        x = random.randint(0, LARGURA - self.LARGURA)
        self.rect = pygame.Rect(x, -self.ALTURA_I, self.LARGURA, self.ALTURA_I)
        self.vel  = vel
        self.vida = self.VIDA_MAX
        self.cor  = VERMELHO

    def atualizar(self):
        self.rect.y += self.vel

    def fora_da_tela(self):
        return self.rect.top > ALTURA

    def desenhar(self, surf):
        pygame.draw.rect(surf, self.cor, self.rect, border_radius=6)
        # barra de vida
        proporcao = self.vida / self.VIDA_MAX
        barra_w   = self.rect.width
        pygame.draw.rect(surf, CINZA,
                         (self.rect.x, self.rect.y - 10, barra_w, 6))
        pygame.draw.rect(surf, VERDE,
                         (self.rect.x, self.rect.y - 10, int(barra_w * proporcao), 6))


class EinimigoRapido(Inimigo):
    """Nível 4: velocidade dobrada, cor diferente."""
    VIDA_MAX = 3

    def __init__(self, vel):
        super().__init__(vel * 2)   # velocidade dobrada
        self.cor = LARANJA


class EinimigoGigante(Inimigo):
    """Nível 4: tamanho 80×80, 5 de vida."""
    LARGURA  = 80
    ALTURA_I = 80
    VIDA_MAX = 5

    def __init__(self, vel):
        super().__init__(vel)
        x = random.randint(0, LARGURA - self.LARGURA)
        self.rect = pygame.Rect(x, -self.ALTURA_I, self.LARGURA, self.ALTURA_I)
        self.vida = self.VIDA_MAX
        self.cor  = ROXO


class Projetil:
    """Nível 2: projétil disparado com SPACE."""
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 8, 20)
        self.vel  = -10
        self.cor  = AMARELO

    def atualizar(self):
        self.rect.y += self.vel

    def fora_da_tela(self):
        return self.rect.bottom < 0

    def desenhar(self, surf):
        pygame.draw.rect(surf, self.cor, self.rect, border_radius=4)


# ─── Funções auxiliares ───────────────────────────────────────────────────────

def gerar_inimigos_nivel4(qtd, vel):
    """Gera lista heterogênea de inimigos para o Nível 4."""
    inimigos = []
    for _ in range(qtd):
        sorteio = random.random()
        if sorteio < 0.40:
            inimigos.append(EinimigoRapido(vel))
        elif sorteio < 0.70:
            inimigos.append(EinimigoGigante(vel))
        else:
            inimigos.append(Inimigo(vel))
    return inimigos


def spawn_inimigo(nivel_cfg, usar_nivel4=False):
    vel = nivel_cfg["vel_inimigo"]
    if usar_nivel4:
        sorteio = random.random()
        if sorteio < 0.40:
            return EinimigoRapido(vel)
        elif sorteio < 0.70:
            return EinimigoGigante(vel)
    return Inimigo(vel)


def desenhar_hud(surf, jogador, pontos, nivel):
    # Pontos
    txt_pontos = fonte_hud.render(f"Pontos: {pontos}", True, BRANCO)
    surf.blit(txt_pontos, (10, 10))

    # Nível
    txt_nivel = fonte_hud.render(f"Nivel: {nivel}", True, CIANO)
    surf.blit(txt_nivel, (10, 38))

    # Vidas como texto (Nível 1)
    coracoes = "♥ " * jogador.vidas
    txt_vidas = fonte_hud.render(f"Vidas: {coracoes}", True, (220, 60, 80))
    surf.blit(txt_vidas, (10, 66))

    # Controles (canto direito)
    controles = fonte_hud.render("SETAS mover | SPACE atirar", True, CINZA)
    surf.blit(controles, (LARGURA - controles.get_width() - 10, 10))


def exibir_mensagem_nivel(surf, nivel):
    """Mostra mensagem de avanço de nível por 2 segundos (Nível 3)."""
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    surf.blit(overlay, (0, 0))

    txt1 = fonte_grande.render(f"NIVEL {nivel}!", True, AMARELO)
    txt2 = fonte_media.render("Velocidade aumentou!", True, BRANCO)
    surf.blit(txt1, (LARGURA // 2 - txt1.get_width() // 2, ALTURA // 2 - 50))
    surf.blit(txt2, (LARGURA // 2 - txt2.get_width() // 2, ALTURA // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(2000)


def tela_game_over(surf, pontos):
    surf.fill(PRETO)
    txt1 = fonte_grande.render("GAME OVER", True, VERMELHO)
    txt2 = fonte_media.render(f"Pontuacao final: {pontos}", True, BRANCO)
    txt3 = fonte_hud.render("Pressione R para jogar novamente ou Q para sair", True, CINZA)
    surf.blit(txt1, (LARGURA // 2 - txt1.get_width() // 2, 180))
    surf.blit(txt2, (LARGURA // 2 - txt2.get_width() // 2, 270))
    surf.blit(txt3, (LARGURA // 2 - txt3.get_width() // 2, 360))
    pygame.display.flip()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_r:
                    return True
                if ev.key == pygame.K_q:
                    pygame.quit(); sys.exit()


# ─── Loop principal ───────────────────────────────────────────────────────────

def jogo():
    jogador   = Jogador()
    inimigos  = []
    projeteis = []
    pontos    = 0
    nivel     = 1
    timer_spawn   = 0
    intervalo_spawn = 80  # frames entre spawns

    while True:
        relogio.tick(60)
        teclas = pygame.key.get_pressed()

        # ── Eventos ──────────────────────────────────────────────────────────
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            # Disparo com SPACE (Nível 2)
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
                px = jogador.rect.centerx - 4
                py = jogador.rect.top
                projeteis.append(Projetil(px, py))

        # ── Lógica ───────────────────────────────────────────────────────────
        jogador.mover(teclas)

        # Spawn de inimigos
        timer_spawn += 1
        if timer_spawn >= intervalo_spawn:
            timer_spawn = 0
            usar_n4 = (nivel == 3)  # no nível máximo usa Nível 4 classes
            cfg = NIVEIS[nivel]
            inimigos.append(spawn_inimigo(cfg, usar_nivel4=usar_n4))

        # Atualizar inimigos
        for ini in inimigos[:]:
            ini.atualizar()
            if ini.fora_da_tela():
                inimigos.remove(ini)
                jogador.vidas -= 1
                if jogador.vidas <= 0:
                    tela_game_over(tela, pontos)
                    return   # reinicia chamando jogo() de novo via main

        # Atualizar projéteis
        for proj in projeteis[:]:
            proj.atualizar()
            if proj.fora_da_tela():
                projeteis.remove(proj)
                continue

            # Colisão projétil × inimigo (Nível 2)
            for ini in inimigos[:]:
                if proj.rect.colliderect(ini.rect):
                    ini.vida -= 1
                    if proj in projeteis:
                        projeteis.remove(proj)
                    if ini.vida <= 0:
                        inimigos.remove(ini)
                        pontos += 100
                    break

        # Colisão jogador × inimigo
        for ini in inimigos[:]:
            if jogador.rect.colliderect(ini.rect):
                inimigos.remove(ini)
                jogador.vidas -= 1
                if jogador.vidas <= 0:
                    reiniciar = tela_game_over(tela, pontos)
                    if reiniciar:
                        return  # volta ao main loop que chama jogo() novamente

        # Progressão de nível (Nível 3) — a cada 500 pontos
        nivel_esperado = min(3, pontos // 500 + 1)
        if nivel_esperado > nivel:
            nivel = nivel_esperado
            exibir_mensagem_nivel(tela, nivel)
            # Ajusta intervalo de spawn conforme nível
            intervalo_spawn = max(30, 80 - (nivel - 1) * 20)

        # ── Desenho ──────────────────────────────────────────────────────────
        tela.fill(PRETO)

        # Grade de fundo sutil
        for gx in range(0, LARGURA, 60):
            pygame.draw.line(tela, (25, 25, 35), (gx, 0), (gx, ALTURA))
        for gy in range(0, ALTURA, 60):
            pygame.draw.line(tela, (25, 25, 35), (0, gy), (LARGURA, gy))

        jogador.desenhar(tela)
        for ini  in inimigos:  ini.desenhar(tela)
        for proj in projeteis: proj.desenhar(tela)

        desenhar_hud(tela, jogador, pontos, nivel)

        pygame.display.flip()


# ─── Entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    while True:
        jogo()
