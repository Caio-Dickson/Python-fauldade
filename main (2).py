# Questão 1 — Automação e Parse de Logs

logs = [
    "2023-10-01 10:00:00 INFO User 105 logged in",
    "2023-10-01 10:05:23 ERROR Database connection failed",
    "2023-10-01 10:07:00 INFO User 105 requested /home",
    "2023-10-01 10:15:00 WARNING Memory usage above 80%",
    "2023-10-01 10:20:00 ERROR Timeout on API gateway",
    "2023-10-01 10:22:00 INFO User 202 logged in",
]

def analisar_logs(lista_logs):
    contagem = {}
    for linha in lista_logs:
        # split separa por espaço; índice [2] é sempre o nível
        nivel = linha.split()[2]
        contagem[nivel] = contagem.get(nivel, 0) + 1
    return contagem

resultado = analisar_logs(logs)
print(resultado)