"""
Desafio 2: Análise Exploratória + Classificação de Titanic
EDA · Limpeza · Árvore de Decisão
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report

# ─────────────────────────────────────────────────────
# PALETA E ESTILO GLOBAIS
# ─────────────────────────────────────────────────────

DARK_BG  = "#0f1117"
PANEL_BG = "#1a1d27"
CLR_SURV  = "#4fc97b"   # sobreviveu — verde
CLR_MORT  = "#f74f4f"   # não sobreviveu — vermelho

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    PANEL_BG,
    "axes.edgecolor":    "#333344",
    "axes.labelcolor":   "#aabbcc",
    "xtick.color":       "#aabbcc",
    "ytick.color":       "#aabbcc",
    "text.color":        "white",
    "grid.color":        "#2a2d3a",
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
})

# ─────────────────────────────────────────────────────
# 1. CARREGAR DADOS
# ─────────────────────────────────────────────────────

df = sns.load_dataset("titanic")
print("=" * 60)
print("   TITANIC — ANÁLISE EXPLORATÓRIA + CLASSIFICAÇÃO")
print("=" * 60)
print(f"\nShape inicial: {df.shape}")
print(f"Colunas: {list(df.columns)}\n")
print("Valores ausentes por coluna:")
print(df.isnull().sum()[df.isnull().sum() > 0])

# ─────────────────────────────────────────────────────
# 2. LIMPEZA COM PANDAS
# ─────────────────────────────────────────────────────

# 2a. Imputar 'age' pela mediana por classe/sexo (estratégia robusta)
df["age"] = df.groupby(["pclass", "sex"])["age"].transform(
    lambda x: x.fillna(x.median())
)

# 2b. Remover colunas irrelevantes / com muitos nulos
colunas_remover = ["deck", "embark_town", "alive", "who",
                   "adult_male", "alone", "class"]
df.drop(columns=colunas_remover, inplace=True, errors="ignore")

# Remover linhas ainda com nulo (embarked: 2 linhas)
df.dropna(inplace=True)

# 2c. Converter categóricas com get_dummies
df = pd.get_dummies(df, columns=["sex", "embarked"], drop_first=False)

print(f"\nShape após limpeza: {df.shape}")
print(f"Valores nulos restantes: {df.isnull().sum().sum()}")
print(f"\nColunas finais: {list(df.columns)}")

# ─────────────────────────────────────────────────────
# 3. EDA — 3 VISUALIZAÇÕES
# ─────────────────────────────────────────────────────

# Recarregar versão "crua" para os gráficos exploratórios
df_raw = sns.load_dataset("titanic").dropna(subset=["embarked", "age"])

fig = plt.figure(figsize=(17, 5.5), facecolor=DARK_BG)
fig.suptitle("EDA — Titanic: Análise Exploratória de Sobrevivência",
             color="white", fontsize=14, fontweight="bold", y=1.01)

gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.38)

# ── 3a. Barplot: sobreviventes por sexo ─────────────
ax1 = fig.add_subplot(gs[0])
contagem = df_raw.groupby(["sex", "survived"]).size().unstack()
x = np.arange(len(contagem))
w = 0.35
bars0 = ax1.bar(x - w/2, contagem[0], width=w, label="Não sobreviveu",
                color=CLR_MORT, alpha=0.85, edgecolor="#ffffff22")
bars1 = ax1.bar(x + w/2, contagem[1], width=w, label="Sobreviveu",
                color=CLR_SURV, alpha=0.85, edgecolor="#ffffff22")

for bar in list(bars0) + list(bars1):
    ax1.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 5,
             str(int(bar.get_height())),
             ha="center", color="white", fontsize=10, fontweight="bold")

ax1.set_xticks(x)
ax1.set_xticklabels(["Feminino", "Masculino"], fontsize=11)
ax1.set_title("Sobreviventes por Sexo", color="white", fontsize=12, pad=10)
ax1.set_ylabel("Quantidade de Passageiros")
ax1.legend(facecolor=PANEL_BG, edgecolor="#555566", labelcolor="white", fontsize=9)
ax1.grid(axis="y")

# ── 3b. Histograma: idade por sobrevivência ──────────
ax2 = fig.add_subplot(gs[1])
sobreviveu  = df_raw[df_raw["survived"] == 1]["age"].dropna()
nao_sobrev  = df_raw[df_raw["survived"] == 0]["age"].dropna()

ax2.hist(nao_sobrev, bins=28, alpha=0.65, color=CLR_MORT,
         label="Não sobreviveu", edgecolor="#ffffff11")
ax2.hist(sobreviveu, bins=28, alpha=0.65, color=CLR_SURV,
         label="Sobreviveu",     edgecolor="#ffffff11")
ax2.axvline(sobreviveu.median(), color=CLR_SURV,  linestyle="--", linewidth=1.3,
            label=f"Mediana sobrev.: {sobreviveu.median():.0f}a")
ax2.axvline(nao_sobrev.median(), color=CLR_MORT, linestyle="--", linewidth=1.3,
            label=f"Mediana não sobrev.: {nao_sobrev.median():.0f}a")

ax2.set_title("Distribuição de Idade por Sobrevivência", color="white", fontsize=12, pad=10)
ax2.set_xlabel("Idade"); ax2.set_ylabel("Frequência")
ax2.legend(facecolor=PANEL_BG, edgecolor="#555566", labelcolor="white", fontsize=8)
ax2.grid(axis="y")

# ── 3c. Heatmap de correlação ────────────────────────
ax3 = fig.add_subplot(gs[2])
cols_corr = ["survived", "pclass", "age", "sibsp", "parch", "fare"]
corr = df_raw[cols_corr].corr()

mask_upper = np.triu(np.ones_like(corr, dtype=bool), k=1)
im = ax3.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1, aspect="auto")

labels = ["Sobrev.", "Classe", "Idade", "Irmãos/Cônjuge", "Pais/Filhos", "Tarifa"]
ax3.set_xticks(range(len(labels))); ax3.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
ax3.set_yticks(range(len(labels))); ax3.set_yticklabels(labels, fontsize=8)

for i in range(len(labels)):
    for j in range(len(labels)):
        val = corr.values[i, j]
        ax3.text(j, i, f"{val:.2f}", ha="center", va="center",
                 color="white" if abs(val) > 0.4 else "#aabbcc",
                 fontsize=8, fontweight="bold" if abs(val) > 0.3 else "normal")

plt.colorbar(im, ax=ax3, fraction=0.04, pad=0.02).ax.yaxis.set_tick_params(color="white")
ax3.set_title("Heatmap de Correlação", color="white", fontsize=12, pad=10)

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/desafio2_titanic_eda.png",
            dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.show()
plt.close()
print("\n✅ EDA salva em desafio2_titanic_eda.png")

# ─────────────────────────────────────────────────────
# 4. CLASSIFICAÇÃO COM ÁRVORE DE DECISÃO
# ─────────────────────────────────────────────────────

FEATURES = [c for c in df.columns if c != "survived"]
X = df[FEATURES]
y = df["survived"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

dt = DecisionTreeClassifier(max_depth=4, random_state=42)
dt.fit(X_train, y_train)
y_pred = dt.predict(X_test)

# ─────────────────────────────────────────────────────
# 5. VISUALIZAR A ÁRVORE COM export_text
# ─────────────────────────────────────────────────────

arvore_texto = export_text(dt, feature_names=list(X.columns))

print("\n" + "=" * 60)
print("🌳 ESTRUTURA DA ÁRVORE DE DECISÃO (max_depth=4)")
print("=" * 60)
print(arvore_texto)

# ─────────────────────────────────────────────────────
# 6. AS 3 PERGUNTAS MAIS IMPORTANTES
# ─────────────────────────────────────────────────────

importancias = pd.Series(dt.feature_importances_, index=FEATURES)
top3 = importancias.nlargest(3)

perguntas = {
    "sex_male":  "O passageiro é do sexo masculino?",
    "sex_female":"O passageiro é do sexo feminino?",
    "pclass":    "Qual a classe do bilhete? (1ª, 2ª ou 3ª?)",
    "fare":      "Quanto pagou pela passagem?",
    "age":       "Qual a idade do passageiro?",
    "sibsp":     "Viajava com irmãos ou cônjuge a bordo?",
    "parch":     "Viajava com pais ou filhos a bordo?",
    "embarked_S":"Embarcou em Southampton?",
    "embarked_C":"Embarcou em Cherbourg?",
    "embarked_Q":"Embarcou em Queenstown?",
}

print("=" * 60)
print("🔍 AS 3 PERGUNTAS MAIS IMPORTANTES QUE A ÁRVORE APRENDEU")
print("=" * 60)
for rank, (feat, imp) in enumerate(top3.items(), 1):
    pergunta = perguntas.get(feat, f"Qual o valor de '{feat}'?")
    print(f"\n  {rank}ª) {pergunta}")
    print(f"      Feature: '{feat}' | Importância: {imp:.4f} ({imp*100:.1f}%)")

# ─────────────────────────────────────────────────────
# 7. MÉTRICAS FINAIS
# ─────────────────────────────────────────────────────

acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec  = recall_score(y_test, y_pred)

print("\n" + "=" * 60)
print("📊 MÉTRICAS DE AVALIAÇÃO — Árvore de Decisão (max_depth=4)")
print("=" * 60)
print(f"  Acurácia   (Accuracy):  {acc:.4f}  ({acc*100:.2f}%)")
print(f"  Precisão   (Precision): {prec:.4f}  ({prec*100:.2f}%)")
print(f"  Revocação  (Recall):    {rec:.4f}  ({rec*100:.2f}%)")
print()
print(classification_report(y_test, y_pred,
      target_names=["Não Sobreviveu", "Sobreviveu"]))

# ─────────────────────────────────────────────────────
# 8. GRÁFICO: Importância das Features
# ─────────────────────────────────────────────────────

fig2, ax = plt.subplots(figsize=(9, 4.5), facecolor=DARK_BG)
ax.set_facecolor(PANEL_BG)

imp_sorted = importancias[importancias > 0].sort_values()
cores = ["#4f8ef7" if f not in top3.index else "#f9c74f" for f in imp_sorted.index]

barras = ax.barh(imp_sorted.index, imp_sorted.values,
                 color=cores, edgecolor="#ffffff11", height=0.6)

for bar, val in zip(barras, imp_sorted.values):
    ax.text(val + 0.002, bar.get_y() + bar.get_height()/2,
            f"{val:.3f}", va="center", color="white", fontsize=9)

ax.set_title("Importância das Features — Árvore de Decisão Titanic",
             color="white", fontsize=12, pad=12)
ax.set_xlabel("Importância (Gini)", color="#8899aa")
ax.grid(axis="x", alpha=0.3)
for spine in ax.spines.values():
    spine.set_edgecolor("#333344")

from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#f9c74f", label="Top 3 features"),
    Patch(facecolor="#4f8ef7", label="Demais features"),
]
ax.legend(handles=legend_elements, facecolor=PANEL_BG,
          edgecolor="#555566", labelcolor="white", fontsize=9, loc="lower right")

plt.tight_layout()
plt.savefig("/mnt/user-data/outputs/desafio2_titanic_features.png",
            dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.show()
plt.close()
print("✅ Gráfico de features salvo em desafio2_titanic_features.png")
print("=" * 60)
