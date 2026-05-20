"""
Desafio 2: Dashboard do Engenheiro de Qualidade
Streamlit — Full Stack Python

Execute com:
    streamlit run desafio2_dashboard_qa.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date, timedelta
import random

# ─────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────

st.set_page_config(
    page_title="Dashboard QA — Commits",
    page_icon="🐛",
    layout="wide",
)

# CSS customizado para aparência profissional
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f1117; }
    [data-testid="stSidebar"]          { background-color: #1a1d27; }
    [data-testid="metric-container"]   { background-color: #1e2130; border-radius: 10px; padding: 12px; }
    h1, h2, h3 { color: #e0e6f0 !important; }
    .stRadio label { color: #b0bcd0 !important; }
    .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATASET DE COMMITS (simulado)
# ─────────────────────────────────────────

@st.cache_data
def gerar_dataset():
    random.seed(42)
    np.random.seed(42)

    desenvolvedores = ["Ana Lima", "Bruno Costa", "Carla Dias", "Daniel Melo", "Elisa Nunes"]
    inicio = date(2025, 4, 1)
    fim    = date(2025, 6, 30)

    dias_uteis = [
        inicio + timedelta(days=d)
        for d in range((fim - inicio).days + 1)
        if (inicio + timedelta(days=d)).weekday() < 5
    ]

    registros = []
    for dev in desenvolvedores:
        # Cada dev tem uma "tendência" diferente de gerar bugs
        fator_bug = random.uniform(0.05, 0.30)
        for dia in random.sample(dias_uteis, k=random.randint(30, 55)):
            linhas_add = random.randint(20, 400)
            linhas_rem = random.randint(5, int(linhas_add * 0.7))
            # Bugs correlacionados com volume de código
            bugs = np.random.poisson(linhas_add * fator_bug * 0.05)
            registros.append({
                "Data": pd.Timestamp(dia),
                "Desenvolvedor": dev,
                "Linhas_Adicionadas": linhas_add,
                "Linhas_Removidas": linhas_rem,
                "Bugs_Gerados": int(bugs),
            })

    df = pd.DataFrame(registros).sort_values("Data").reset_index(drop=True)
    return df

df = gerar_dataset()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────

st.sidebar.image(
    "https://img.icons8.com/fluency/48/bug.png",
    width=48,
)
st.sidebar.title("🔍 Filtros")
st.sidebar.markdown("---")

devs = sorted(df["Desenvolvedor"].unique())
dev_selecionado = st.sidebar.radio(
    "Selecione o Desenvolvedor:",
    options=devs,
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.caption("Período: Abril — Junho 2025")
st.sidebar.caption(f"Total de commits no dataset: {len(df)}")

# ─────────────────────────────────────────
# FILTRAGEM
# ─────────────────────────────────────────

df_dev = df[df["Desenvolvedor"] == dev_selecionado].copy()

# ─────────────────────────────────────────
# CABEÇALHO
# ─────────────────────────────────────────

st.title("🐛 Dashboard do Engenheiro de Qualidade")
st.markdown(f"### Desenvolvedor: **{dev_selecionado}**")
st.markdown("---")

# ─────────────────────────────────────────
# MÉTRICAS (KPIs)
# ─────────────────────────────────────────

col1, col2, col3, col4 = st.columns(4)

total_linhas_add  = df_dev["Linhas_Adicionadas"].sum()
total_linhas_rem  = df_dev["Linhas_Removidas"].sum()
total_bugs        = df_dev["Bugs_Gerados"].sum()
total_commits     = len(df_dev)
media_bugs_commit = (total_bugs / total_commits) if total_commits else 0

col1.metric("📝 Commits",            f"{total_commits}")
col2.metric("➕ Linhas Adicionadas", f"{total_linhas_add:,}")
col3.metric("➖ Linhas Removidas",   f"{total_linhas_rem:,}")
col4.metric("🐞 Total de Bugs",      f"{total_bugs}",
            delta=f"Média: {media_bugs_commit:.2f}/commit",
            delta_color="inverse")

st.markdown("---")

# ─────────────────────────────────────────
# GRÁFICO DE LINHAS — Evolução temporal de Bugs
# ─────────────────────────────────────────

st.subheader("📈 Evolução Temporal de Bugs Gerados")

# Agrupar por semana para visualização mais suave
df_weekly = (
    df_dev.set_index("Data")
    .resample("W")["Bugs_Gerados"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(11, 4))
fig.patch.set_facecolor("#0f1117")
ax.set_facecolor("#1a1d27")

ax.fill_between(
    df_weekly["Data"],
    df_weekly["Bugs_Gerados"],
    alpha=0.18,
    color="#4f8ef7",
)
ax.plot(
    df_weekly["Data"],
    df_weekly["Bugs_Gerados"],
    color="#4f8ef7",
    linewidth=2.2,
    marker="o",
    markersize=5,
    markerfacecolor="#ffffff",
    markeredgecolor="#4f8ef7",
    markeredgewidth=1.5,
)

# Linha de média
media_semanal = df_weekly["Bugs_Gerados"].mean()
ax.axhline(media_semanal, color="#ffcc00", linestyle="--", linewidth=1.2,
           label=f"Média semanal: {media_semanal:.1f}")

ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
plt.xticks(rotation=30, color="#aaaaaa", fontsize=9)
plt.yticks(color="#aaaaaa")
ax.set_xlabel("Semana", color="#888888")
ax.set_ylabel("Bugs Gerados", color="#888888")
for spine in ax.spines.values():
    spine.set_edgecolor("#333344")
ax.legend(facecolor="#1a1d27", edgecolor="#555566", labelcolor="white", fontsize=9)
ax.set_ylim(bottom=0)

plt.tight_layout()
st.pyplot(fig)
plt.close()

st.markdown("---")

# ─────────────────────────────────────────
# TABELA DE COMMITS DETALHADA
# ─────────────────────────────────────────

with st.expander("📋 Ver todos os commits de " + dev_selecionado):
    df_exibir = df_dev.copy()
    df_exibir["Data"] = df_exibir["Data"].dt.strftime("%d/%m/%Y")
    st.dataframe(df_exibir, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────
# EXTRA: Botão — Dev com maior média de bugs
# ─────────────────────────────────────────

st.markdown("---")
st.subheader("🏆 Análise Comparativa")

if st.button("🔎 Descobrir quem gerou mais bugs por commit", type="primary"):
    ranking = (
        df.groupby("Desenvolvedor")
        .apply(lambda g: g["Bugs_Gerados"].sum() / len(g))
        .reset_index()
    )
    ranking.columns = ["Desenvolvedor", "Média_Bugs_por_Commit"]
    ranking = ranking.sort_values("Média_Bugs_por_Commit", ascending=False).reset_index(drop=True)

    pior_dev   = ranking.iloc[0]["Desenvolvedor"]
    pior_media = ranking.iloc[0]["Média_Bugs_por_Commit"]

    st.error(
        f"⚠️ **{pior_dev}** tem a maior média de bugs por commit: "
        f"**{pior_media:.2f} bugs/commit**"
    )

    st.markdown("##### Ranking completo:")

    fig2, ax2 = plt.subplots(figsize=(8, 3.5))
    fig2.patch.set_facecolor("#0f1117")
    ax2.set_facecolor("#1a1d27")

    cores = ["#f74f4f" if d == pior_dev else "#4f8ef7" for d in ranking["Desenvolvedor"]]
    ax2.barh(ranking["Desenvolvedor"], ranking["Média_Bugs_por_Commit"],
             color=cores, edgecolor="#ffffff22", height=0.55)

    for i, (_, row) in enumerate(ranking.iterrows()):
        ax2.text(row["Média_Bugs_por_Commit"] + 0.005, i,
                 f'{row["Média_Bugs_por_Commit"]:.2f}',
                 va="center", color="white", fontsize=10)

    ax2.invert_yaxis()
    ax2.set_xlabel("Média de Bugs por Commit", color="#888888")
    plt.xticks(color="#aaaaaa")
    plt.yticks(color="white", fontsize=10)
    for spine in ax2.spines.values():
        spine.set_edgecolor("#333344")
    ax2.set_xlim(0, ranking["Média_Bugs_por_Commit"].max() * 1.25)

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()
