#!/usr/bin/env python3
"""Lê um CSV de chamados e gera um relatório de cumprimento de SLA."""
import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path

# Prazo máximo de resolução (em horas) por prioridade
SLA_HORAS = {"Crítica": 4, "Alta": 8, "Média": 24, "Baixa": 72}


def carregar(caminho: Path) -> list[dict]:
    chamados = []
    with open(caminho, newline="", encoding="utf-8") as f:
        for linha in csv.DictReader(f):
            aberto = datetime.fromisoformat(linha["aberto_em"])
            resolvido = datetime.fromisoformat(linha["resolvido_em"])
            horas = (resolvido - aberto).total_seconds() / 3600
            chamados.append({
                **linha,
                "aberto": aberto,
                "horas": horas,
                "estourou": horas > SLA_HORAS[linha["prioridade"]],
            })
    return chamados


def resumir(chamados: list[dict]) -> dict:
    total = len(chamados)
    estourados = sum(c["estourou"] for c in chamados)
    return {
        "total": total,
        "estourados": estourados,
        "cumprimento": 100 * (total - estourados) / total if total else 0.0,
        "media_horas": sum(c["horas"] for c in chamados) / total if total else 0.0,
    }


def agrupar(chamados: list[dict], chave) -> dict[str, dict]:
    grupos = defaultdict(list)
    for c in chamados:
        grupos[chave(c)].append(c)
    return {k: resumir(v) for k, v in sorted(grupos.items())}


def semana(chamado: dict) -> str:
    ano, sem, _ = chamado["aberto"].isocalendar()
    return f"{ano}-S{sem:02d}"


def tabela(titulo: str, dados: dict[str, dict]) -> str:
    linhas = [
        f"### {titulo}",
        "",
        "| Grupo | Total | Estourados | Cumprimento | Média (h) |",
        "|---|---:|---:|---:|---:|",
    ]
    for nome, r in dados.items():
        linhas.append(
            f"| {nome} | {r['total']} | {r['estourados']} | "
            f"{r['cumprimento']:.1f}% | {r['media_horas']:.1f} |"
        )
    return "\n".join(linhas)


def gerar_relatorio(chamados: list[dict]) -> str:
    geral = resumir(chamados)
    por_categoria = agrupar(chamados, lambda c: c["categoria"])
    pior = min(por_categoria.items(), key=lambda kv: kv[1]["cumprimento"])
    partes = [
        "# Relatório de SLA",
        "",
        f"- **Chamados analisados:** {geral['total']}",
        f"- **Cumprimento geral do SLA:** {geral['cumprimento']:.1f}%",
        f"- **Chamados fora do prazo:** {geral['estourados']}",
        f"- **Categoria mais crítica:** {pior[0]} ({pior[1]['cumprimento']:.1f}%)",
        "",
        tabela("Por prioridade", agrupar(chamados, lambda c: c["prioridade"])),
        "",
        tabela("Por categoria", por_categoria),
        "",
        tabela("Por semana", agrupar(chamados, semana)),
        "",
    ]
    return "\n".join(partes)


def main() -> None:
    parser = argparse.ArgumentParser(description="Relatório de SLA de chamados")
    parser.add_argument("csv", type=Path, help="arquivo CSV de chamados")
    parser.add_argument("-o", "--saida", type=Path, default=Path("relatorio_sla.md"))
    args = parser.parse_args()

    if not args.csv.exists():
        parser.error(f"arquivo '{args.csv}' não encontrado.")

    relatorio = gerar_relatorio(carregar(args.csv))
    args.saida.write_text(relatorio, encoding="utf-8")
    print(relatorio)
    print(f"\nRelatório salvo em {args.saida}")


if __name__ == "__main__":
    main()
