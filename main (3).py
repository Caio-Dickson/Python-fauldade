# Questão 2 — Preparação de Dados Brutos

transacoes = [
    (1, "Infraestrutura", 1500.50),
    (2, "Licenças",       450.00),
    (3, "Infraestrutura", 3200.00),
    (4, "Marketing",      800.00),
    (5, "Licenças",       150.00),
]

# 1. Categorias únicas via set
categorias_unicas = {t[1] for t in transacoes}
print("Categorias únicas:", categorias_unicas)

# 2. Total por categoria via dicionário
total_por_categoria = {}
for id_t, categoria, valor in transacoes:
    total_por_categoria[categoria] = (
        total_por_categoria.get(categoria, 0) + valor
    )

for cat, total in total_por_categoria.items():
    print(f"  {cat}: R$ {total:.2f}")