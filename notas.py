# ============================================================
# DESAFIO — O Diário de Classe Caótico
# ============================================================

notas_brutas = [
    {"aluno": "Ana",     "materia": "Matematica", "nota": 8.5},
    {"aluno": "Carlos",  "materia": "Fisica",     "nota": 6.0},
    {"aluno": "Beatriz", "materia": "Quimica",    "nota": 9.0},
    {"aluno": "Joao",    "materia": "Historia",   "nota": 7.5},
    {"aluno": "Mariana", "materia": "Biologia",   "nota": 8.0},
    {"aluno": "Pedro",   "materia": "Matematica", "nota": 5.5},
    {"aluno": "Lucas",   "materia": "Fisica",     "nota": 7.0},
    {"aluno": "Julia",   "materia": "Quimica",    "nota": 6.5},
    {"aluno": "Rafael",  "materia": "Historia",   "nota": 9.5},
    {"aluno": "Sofia",   "materia": "Biologia",   "nota": 10.0},
    {"aluno": "Ana",     "materia": "Fisica",     "nota": 9.0},
    {"aluno": "Carlos",  "materia": "Matematica", "nota": 4.5},
    {"aluno": "Beatriz", "materia": "Matematica", "nota": 7.0},
    {"aluno": "Joao",    "materia": "Quimica",    "nota": 5.0},
    {"aluno": "Mariana", "materia": "Historia",   "nota": 8.5},
    {"aluno": "Pedro",   "materia": "Biologia",   "nota": 6.0},
    {"aluno": "Lucas",   "materia": "Matematica", "nota": 8.0},
    {"aluno": "Julia",   "materia": "Fisica",     "nota": 7.5},
    {"aluno": "Rafael",  "materia": "Quimica",    "nota": 8.0},
    {"aluno": "Sofia",   "materia": "Historia",   "nota": 9.0},
    {"aluno": "Ana",     "materia": "Matematica", "nota": 7.5},
    {"aluno": "Carlos",  "materia": "Fisica",     "nota": 3.0},
    {"aluno": "Beatriz", "materia": "Fisica",     "nota": 8.0},
    {"aluno": "Joao",    "materia": "Matematica", "nota": 6.5},
    {"aluno": "Mariana", "materia": "Quimica",    "nota": 9.5},
    {"aluno": "Pedro",   "materia": "Historia",   "nota": 4.0},
    {"aluno": "Lucas",   "materia": "Biologia",   "nota": 7.0},
    {"aluno": "Julia",   "materia": "Matematica", "nota": 8.5},
    {"aluno": "Rafael",  "materia": "Fisica",     "nota": 6.0},
    {"aluno": "Sofia",   "materia": "Quimica",    "nota": 9.5},
    {"aluno": "Ana",     "materia": "Matematica", "nota": 4.0},
    {"aluno": "Carlos",  "materia": "Matematica", "nota": 5.0},
    {"aluno": "Beatriz", "materia": "Historia",   "nota": 7.5},
    {"aluno": "Joao",    "materia": "Biologia",   "nota": 8.0},
    {"aluno": "Mariana", "materia": "Matematica", "nota": 6.0},
    {"aluno": "Pedro",   "materia": "Fisica",     "nota": 5.5},
    {"aluno": "Lucas",   "materia": "Quimica",    "nota": 9.0},
    {"aluno": "Julia",   "materia": "Historia",   "nota": 8.0},
    {"aluno": "Rafael",  "materia": "Biologia",   "nota": 7.5},
    {"aluno": "Sofia",   "materia": "Matematica", "nota": 10.0},
    {"aluno": "Ana",     "materia": "Quimica",    "nota": 8.0},
    {"aluno": "Carlos",  "materia": "Historia",   "nota": 6.5},
    {"aluno": "Beatriz", "materia": "Biologia",   "nota": 9.5},
    {"aluno": "Joao",    "materia": "Fisica",     "nota": 7.0},
    {"aluno": "Mariana", "materia": "Matematica", "nota": 7.5},
    {"aluno": "Pedro",   "materia": "Quimica",    "nota": 6.0},
    {"aluno": "Lucas",   "materia": "Historia",   "nota": 8.5},
    {"aluno": "Julia",   "materia": "Biologia",   "nota": 9.0},
    {"aluno": "Rafael",  "materia": "Matematica", "nota": 5.0},
    {"aluno": "Sofia",   "materia": "Fisica",     "nota": 8.5},
    {"aluno": "Ana",     "materia": "Historia",   "nota": 9.0},
    {"aluno": "Carlos",  "materia": "Biologia",   "nota": 5.5},
    {"aluno": "Beatriz", "materia": "Matematica", "nota": 8.5},
    {"aluno": "Joao",    "materia": "Quimica",    "nota": 6.0},
    {"aluno": "Mariana", "materia": "Fisica",     "nota": 8.0},
    {"aluno": "Pedro",   "materia": "Historia",   "nota": 7.0},
    {"aluno": "Lucas",   "materia": "Biologia",   "nota": 7.5},
    {"aluno": "Julia",   "materia": "Matematica", "nota": 6.5},
    {"aluno": "Rafael",  "materia": "Quimica",    "nota": 9.0},
    {"aluno": "Sofia",   "materia": "Historia",   "nota": 10.0},
    {"aluno": "Ana",     "materia": "Biologia",   "nota": 8.5},
    {"aluno": "Carlos",  "materia": "Quimica",    "nota": 4.0},
    {"aluno": "Beatriz", "materia": "Fisica",     "nota": 7.0},
    {"aluno": "Joao",    "materia": "Historia",   "nota": 8.5},
    {"aluno": "Mariana", "materia": "Biologia",   "nota": 9.0},
    {"aluno": "Pedro",   "materia": "Matematica", "nota": 6.5},
    {"aluno": "Lucas",   "materia": "Fisica",     "nota": 8.0},
    {"aluno": "Julia",   "materia": "Quimica",    "nota": 7.0},
    {"aluno": "Rafael",  "materia": "Historia",   "nota": 6.0},
    {"aluno": "Sofia",   "materia": "Biologia",   "nota": 9.5},
    {"aluno": "Ana",     "materia": "Matematica", "nota": 9.5},
    {"aluno": "Carlos",  "materia": "Fisica",     "nota": 5.0},
    {"aluno": "Beatriz", "materia": "Quimica",    "nota": 8.0},
    {"aluno": "Joao",    "materia": "Matematica", "nota": 7.0},
    {"aluno": "Mariana", "materia": "Historia",   "nota": 8.5},
    {"aluno": "Pedro",   "materia": "Biologia",   "nota": 5.0},
    {"aluno": "Lucas",   "materia": "Matematica", "nota": 9.0},
    {"aluno": "Julia",   "materia": "Fisica",     "nota": 8.5},
    {"aluno": "Rafael",  "materia": "Quimica",    "nota": 7.5},
    {"aluno": "Sofia",   "materia": "Historia",   "nota": 9.0},
    {"aluno": "Ana",     "materia": "Fisica",     "nota": 8.0},
    {"aluno": "Carlos",  "materia": "Matematica", "nota": 6.0},
    {"aluno": "Beatriz", "materia": "Matematica", "nota": 9.0},
    {"aluno": "Joao",    "materia": "Quimica",    "nota": 5.5},
    {"aluno": "Mariana", "materia": "Fisica",     "nota": 7.0},
    {"aluno": "Pedro",   "materia": "Historia",   "nota": 6.5},
    {"aluno": "Lucas",   "materia": "Biologia",   "nota": 8.0},
    {"aluno": "Julia",   "materia": "Matematica", "nota": 7.5},
    {"aluno": "Rafael",  "materia": "Fisica",     "nota": 8.0},
    {"aluno": "Sofia",   "materia": "Quimica",    "nota": 10.0},
    {"aluno": "Ana",     "materia": "Quimica",    "nota": 9.0},
    {"aluno": "Carlos",  "materia": "Historia",   "nota": 4.5},
    {"aluno": "Beatriz", "materia": "Biologia",   "nota": 8.5},
    {"aluno": "Joao",    "materia": "Fisica",     "nota": 6.5},
    {"aluno": "Mariana", "materia": "Matematica", "nota": 9.0},
    {"aluno": "Pedro",   "materia": "Quimica",    "nota": 5.5},
    {"aluno": "Lucas",   "materia": "Historia",   "nota": 7.0},
    {"aluno": "Julia",   "materia": "Biologia",   "nota": 8.0},
    {"aluno": "Rafael",  "materia": "Matematica", "nota": 6.5},
    {"aluno": "Sofia",   "materia": "Fisica",     "nota": 9.5},
]


# ============================================================
def gerar_boletins(dados):

    # ── ETAPA 1: Agrupar notas por aluno → por matéria ──────
    agrupado = {}

    for registro in dados:
        aluno   = registro["aluno"]
        materia = registro["materia"]
        nota    = registro["nota"]

        if aluno not in agrupado:
            agrupado[aluno] = {}

        if materia not in agrupado[aluno]:
            agrupado[aluno][materia] = []

        agrupado[aluno][materia].append(nota)

    # ── ETAPA 2: Calcular médias por matéria ────────────────
    boletins = {}

    for aluno, materias in agrupado.items():
        medias_disciplinas = {}

        for materia, notas in materias.items():
            # Copia a lista para não alterar os dados originais
            notas_calc = notas[:]

            # Descarta piores notas até sobrar apenas 2
            while len(notas_calc) >= 3:
                notas_calc.remove(min(notas_calc))

            media = round(sum(notas_calc) / len(notas_calc), 2)
            medias_disciplinas[materia] = media

        # ── ETAPA 3: Média geral e status ───────────────────
        soma_medias = sum(medias_disciplinas.values())
        qtd_materias = len(medias_disciplinas)
        media_geral = round(soma_medias / qtd_materias, 2)

        if media_geral >= 7.0:
            status = "Aprovado"
        elif media_geral >= 5.0:
            status = "Recuperacao"
        else:
            status = "Reprovado"

        boletins[aluno] = {
            "medias_disciplinas": medias_disciplinas,
            "media_geral":        media_geral,
            "status":             status,
        }

    # ── ETAPA 4: Ranking ────────────────────────────────────
    pares = [(aluno, info["media_geral"]) for aluno, info in boletins.items()]

    pares_ordenados = sorted(pares, key=lambda x: (-x[1], x[0]))

    ranking = [aluno for aluno, _ in pares_ordenados]

    return {"boletins": boletins, "ranking": ranking}


# ============================================================
# EXIBIÇÃO DO RESULTADO
# ============================================================
resultado = gerar_boletins(notas_brutas)

print("=" * 60)
print("              BOLETINS DA TURMA")
print("=" * 60)

for posicao, nome in enumerate(resultado["ranking"], start=1):
    boletim = resultado["boletins"][nome]

    icone = {"Aprovado": "✅", "Recuperacao": "⚠️ ", "Reprovado": "❌"}[boletim["status"]]

    print(f"\n{posicao:>2}º  {nome:<10} │ Média Geral: {boletim['media_geral']:>5.2f} │ {icone} {boletim['status']}")
    print(f"    {'─'*50}")

    for materia, media in boletim["medias_disciplinas"].items():
        print(f"    {materia:<12} → {media:.2f}")

print("\n" + "=" * 60)
print("  🏆 RANKING FINAL")
print("=" * 60)

for pos, nome in enumerate(resultado["ranking"], start=1):
    media = resultado["boletins"][nome]["media_geral"]
    print(f"  {pos:>2}º {nome:<10} {media:.2f}")

print("=" * 60)