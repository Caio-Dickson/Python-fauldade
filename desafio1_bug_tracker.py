"""
Desafio 1: O Rastreador de Bugs
Pandas + Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# ─────────────────────────────────────────
# 1. CRIAR O DATAFRAME (simulando CSV)
# ─────────────────────────────────────────

dados = {
    "Bug_ID": [f"BUG-{str(i).zfill(3)}" for i in range(1, 21)],
    "Módulo": [
        "Backend", "Frontend", "DB", "Backend", "Frontend",
        "DB", "Backend", "Frontend", "Backend", "DB",
        "Frontend", "Backend", "DB", "Frontend", "Backend",
        "DB", "Frontend", "Backend", "DB", "Frontend",
    ],
    "Severidade": [
        "Alta", "Média", "Baixa", "Alta", "Alta",
        "Média", "Baixa", "Alta", "Média", "Alta",
        "Baixa", "Alta", "Média", "Alta", "Baixa",
        "Alta", "Média", "Baixa", "Alta", "Média",
    ],
    "Tempo_Resolucao_Horas": [
        12.5, 8.0, -3.0, 24.0, 6.5,
        None, 15.0, 9.5, 30.0, 18.0,
        4.0, 22.0, None, 7.5, -1.5,
        20.0, 5.0, 11.0, 27.5, 3.5,
    ],
}

df = pd.DataFrame(dados)

print("=" * 55)
print("   RASTREADOR DE BUGS — RELATÓRIO MENSAL")
print("=" * 55)
print(f"\n📋 Dataset original ({len(df)} registros):\n")
print(df.to_string(index=False))

# ─────────────────────────────────────────
# 2. LIMPAR OS DADOS (imputação)
# ─────────────────────────────────────────

# Substituir negativos por NaN para tratamento uniforme
df["Tempo_Resolucao_Horas"] = df["Tempo_Resolucao_Horas"].apply(
    lambda x: np.nan if isinstance(x, float) and x < 0 else x
)

# Calcular média dos valores válidos
media_geral = df["Tempo_Resolucao_Horas"].mean()

# Quantidade de registros problemáticos antes da imputação
qtd_invalidos = df["Tempo_Resolucao_Horas"].isna().sum()

# Imputação: substituir NaN pela média geral
df["Tempo_Resolucao_Horas"] = df["Tempo_Resolucao_Horas"].fillna(media_geral)

print(f"\n🔧 Limpeza de dados:")
print(f"   • Registros com valor inválido (negativo ou nulo): {qtd_invalidos}")
print(f"   • Média geral usada na imputação: {media_geral:.2f} horas")
print(f"   • Todos os valores agora são válidos ✓")

# ─────────────────────────────────────────
# 3. AGRUPAR E ANALISAR
# ─────────────────────────────────────────

resumo = (
    df.groupby("Módulo")["Tempo_Resolucao_Horas"]
    .mean()
    .sort_values(ascending=False)
    .round(2)
)

print(f"\n📊 Tempo médio de resolução por Módulo (horas):\n")
for modulo, tempo in resumo.items():
    barra = "█" * int(tempo / 1.5)
    print(f"   {modulo:<10} {tempo:>6.2f}h  {barra}")

# ─────────────────────────────────────────
# 4. PLOTAR O GRÁFICO
# ─────────────────────────────────────────

CORES = {
    "Backend":  "#4f8ef7",
    "Frontend": "#f97b4f",
    "DB":       "#4fc97b",
}

cores_barras = [CORES.get(m, "#aaaaaa") for m in resumo.index]

fig, ax = plt.subplots(figsize=(9, 6))
fig.patch.set_facecolor("#0f1117")
ax.set_facecolor("#1a1d27")

barras = ax.bar(
    resumo.index,
    resumo.values,
    color=cores_barras,
    width=0.5,
    edgecolor="#ffffff22",
    linewidth=0.8,
)

# Rótulos de valor sobre as barras
for barra, valor in zip(barras, resumo.values):
    ax.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height() + 0.4,
        f"{valor:.1f}h",
        ha="center",
        va="bottom",
        color="white",
        fontsize=12,
        fontweight="bold",
    )

# Linha de média geral
ax.axhline(
    media_geral,
    color="#ffcc00",
    linestyle="--",
    linewidth=1.4,
    label=f"Média geral: {media_geral:.1f}h",
)

# Estilo dos eixos
ax.set_title(
    "Tempo Médio de Resolução de Bugs por Módulo",
    color="white",
    fontsize=15,
    fontweight="bold",
    pad=16,
)
ax.set_xlabel("Módulo", color="#aaaaaa", fontsize=11)
ax.set_ylabel("Tempo Médio (horas)", color="#aaaaaa", fontsize=11)
ax.tick_params(colors="white", labelsize=11)
for spine in ax.spines.values():
    spine.set_edgecolor("#333344")
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.0fh"))
ax.set_ylim(0, resumo.max() * 1.25)

legend = ax.legend(facecolor="#1a1d27", edgecolor="#555566", labelcolor="white", fontsize=10)

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/desafio1_bug_tracker.png", dpi=150, bbox_inches="tight")
plt.show()

print("\n✅ Gráfico salvo como 'desafio1_bug_tracker.png'")
print("=" * 55)
