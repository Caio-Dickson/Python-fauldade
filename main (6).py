class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[" "] * 3 for _ in range(3)]
        self.jogador_atual = "X"

    def mostrar_tabuleiro(self):
        print()
        for i, linha in enumerate(self.tabuleiro):
            print(" | ".join(linha))
            if i < 2:
                print("---------")
        print()

    def fazer_jogada(self, linha, col):
        if not (0 <= linha <= 2 and 0 <= col <= 2):
            return "Posição fora dos limites."
        if self.tabuleiro[linha][col] != " ":
            return "Posição já ocupada."
        self.tabuleiro[linha][col] = self.jogador_atual
        self.jogador_atual = "O" if self.jogador_atual == "X" else "X"
        return None

    def verificar_vencedor(self):
        t = self.tabuleiro
        linhas    = t
        colunas   = [[t[l][c] for l in range(3)] for c in range(3)]
        diagonais = [[t[i][i] for i in range(3)], [t[i][2-i] for i in range(3)]]
        for combo in linhas + colunas + diagonais:
            if combo[0] != " " and len(set(combo)) == 1:
                return combo[0]
        if all(t[l][c] != " " for l in range(3) for c in range(3)):
            return "Empate"
        return None

    def jogar(self):
        print("=== Jogo da Velha ===")
        print("Linhas e colunas de 0 a 2\n")
        while True:
            self.mostrar_tabuleiro()
            print(f"Vez do jogador {self.jogador_atual}")
            try:
                linha = int(input("  Linha (0-2): "))
                col   = int(input("  Coluna (0-2): "))
            except ValueError:
                print("Digite apenas números!\n")
                continue

            erro = self.fazer_jogada(linha, col)
            if erro:
                print(f"Jogada inválida: {erro}\n")
                continue

            resultado = self.verificar_vencedor()
            if resultado:
                self.mostrar_tabuleiro()
                if resultado == "Empate":
                    print("Empate!")
                else:
                    print(f"Jogador {resultado} venceu!")
                
                novamente = input("\nJogar novamente? (s/n): ").strip().lower()
                if novamente == "s":
                    self.__init__()
                else:
                    print("Até mais!")
                    break


if __name__ == "__main__":
    jogo = JogoDaVelha()
    jogo.jogar()