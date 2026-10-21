#!/usr/bin/env python3
"""Gera um CSV de chamados FICTÍCIOS para testar o relatório de SLA."""
import csv
import random
from datetime import datetime, timedelta

from sla_report import SLA_HORAS

random.seed(42)  # resultado reproduzível

CATEGORIAS = ["Acesso/Senha", "Rede", "Software", "Hardware", "Impressora", "Sistemas internos"]
PRIORIDADES = ["Crítica", "Alta", "Média", "Baixa"]
PESOS = [5, 20, 50, 25]


def gerar(qtd: int = 300, arquivo: str = "chamados.csv") -> None:
    inicio = datetime(2026, 8, 3, 8, 0)
    with open(arquivo, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "categoria", "prioridade", "aberto_em", "resolvido_em"])
        for i in range(1, qtd + 1):
            prioridade = random.choices(PRIORIDADES, weights=PESOS)[0]
            aberto = inicio + timedelta(minutes=random.randint(0, 8 * 7 * 24 * 60))
            # tempo de resolução varia em torno do SLA (alguns estouram)
            horas = SLA_HORAS[prioridade] * random.uniform(0.2, 1.5)
            resolvido = aberto + timedelta(hours=horas)
            w.writerow([
                f"CH-{i:04d}",
                random.choice(CATEGORIAS),
                prioridade,
                aberto.isoformat(timespec="seconds"),
                resolvido.isoformat(timespec="seconds"),
            ])
    print(f"{qtd} chamados fictícios gerados em {arquivo}")


if __name__ == "__main__":
    gerar()
