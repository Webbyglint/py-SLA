from datetime import datetime

from sla_report import agrupar, resumir, semana


def chamado(prioridade, horas, estourou, categoria="Rede", aberto=datetime(2026, 8, 3, 9)):
    return {"prioridade": prioridade, "horas": horas, "estourou": estourou,
            "categoria": categoria, "aberto": aberto}


def test_resumir_calcula_cumprimento():
    r = resumir([chamado("Alta", 5, False), chamado("Alta", 10, True)])
    assert r["total"] == 2
    assert r["estourados"] == 1
    assert r["cumprimento"] == 50.0
    assert r["media_horas"] == 7.5


def test_resumir_lista_vazia():
    assert resumir([])["cumprimento"] == 0.0


def test_agrupar_por_categoria():
    cs = [chamado("Alta", 1, False, "Rede"), chamado("Alta", 1, False, "Software")]
    assert set(agrupar(cs, lambda c: c["categoria"])) == {"Rede", "Software"}


def test_semana_iso():
    assert semana(chamado("Alta", 1, False)) == "2026-S32"
