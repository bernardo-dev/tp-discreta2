"""
Módulo A4 — Identificação Estrutural dos Pontos e Comparação com a Tabela 1.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

try:
    from .a1_leitura_vtk import obter_referencia_modelo
except ImportError:
    from a1_leitura_vtk import obter_referencia_modelo

# ==============================================================================
# A4. Identificação Estrutural dos Pontos e Comparação com a Tabela 1
# ==============================================================================


def identificar_estrutura_pontos(
    pontos: list[dict[str, Any]],
    segmentos: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Requisito A4: Usando apenas laços e contadores simples, calcula o grau de
    entrada (in_degree) e o grau de saída (out_degree) de cada ponto v in V.

    Identifica e verifica nos dados reais (sem apenas assumir):
    - Ponto de entrada: in_degree == 0 e out_degree == 1 (verifica se é o ID 0).
    - Bifurcações (B): pontos internos com out_degree == 2 (e in_degree == 1),
      garantindo que o ponto de entrada não seja confundido com bifurcação.
    - Terminais (T): pontos com out_degree == 0 (e in_degree == 1).
    - Pontos com graus inesperados, caso existam.
    """
    in_degree: dict[int, int] = {}
    out_degree: dict[int, int] = {}

    for p in pontos:
        pid = int(p["id"])
        in_degree[pid] = 0
        out_degree[pid] = 0

    # Contagem de conexões de entrada e de saída por laço simples sobre E
    for seg in segmentos:
        u = int(seg["u"])
        v = int(seg["v"])
        if u in out_degree:
            out_degree[u] = out_degree[u] + 1
        if v in in_degree:
            in_degree[v] = in_degree[v] + 1

    pontos_entrada: list[int] = []
    bifurcacoes: list[int] = []
    terminais: list[int] = []
    pontos_grau_inesperado: list[dict[str, int]] = []

    for p in pontos:
        pid = int(p["id"])
        g_in = in_degree[pid]
        g_out = out_degree[pid]
        g_total = g_in + g_out

        p["in_degree"] = g_in
        p["out_degree"] = g_out
        p["grau_total"] = g_total

        if g_in == 0 and g_out == 1:
            pontos_entrada.append(pid)
            p["tipo"] = "Entrada"
        elif g_in == 1 and g_out == 2:
            bifurcacoes.append(pid)
            p["tipo"] = "Bifurcação"
        elif g_in == 1 and g_out == 0:
            terminais.append(pid)
            p["tipo"] = "Terminal"
        else:
            pontos_grau_inesperado.append(
                {
                    "id": pid,
                    "in_degree": g_in,
                    "out_degree": g_out,
                    "grau_total": g_total,
                }
            )
            p["tipo"] = "Inesperado"

    ponto_entrada_id: int | None = (
        pontos_entrada[0] if len(pontos_entrada) == 1 else None
    )
    confirmado_id_zero: bool = (
        len(pontos_entrada) == 1 and pontos_entrada[0] == 0
    )

    return {
        "num_pontos_V": len(pontos),
        "num_segmentos_E": len(segmentos),
        "num_terminais_T": len(terminais),
        "num_bifurcacoes_B": len(bifurcacoes),
        "ponto_entrada_id": ponto_entrada_id,
        "pontos_entrada": pontos_entrada,
        "confirmado_id_zero": confirmado_id_zero,
        "bifurcacoes_ids": bifurcacoes,
        "terminais_ids": terminais,
        "pontos_grau_inesperado": pontos_grau_inesperado,
        "in_degree": in_degree,
        "out_degree": out_degree,
    }


def comparar_com_tabela_referencia(
    nome_arquivo: str,
    estrutura: dict[str, Any],
) -> dict[str, Any]:
    """
    Requisito A4: Compara |V|, |E|, T, B e o ponto de entrada obtidos a partir
    dos dados reais com a Tabela 1 de referência do TP.
    """
    ref = obter_referencia_modelo(nome_arquivo)

    v_obtido = int(estrutura["num_pontos_V"])
    e_obtido = int(estrutura["num_segmentos_E"])
    t_obtido = int(estrutura["num_terminais_T"])
    b_obtido = int(estrutura["num_bifurcacoes_B"])
    entrada_id = estrutura["ponto_entrada_id"]
    sem_grau_inesperado = len(estrutura["pontos_grau_inesperado"]) == 0

    if ref is None:
        return {
            "possui_referencia": False,
            "coincide_tabela_1": False,
            "nterm_esperado": None,
            "V_esperado": None,
            "E_esperado": None,
            "T_esperado": None,
            "B_esperado": None,
            "V_obtido": v_obtido,
            "E_obtido": e_obtido,
            "T_obtido": t_obtido,
            "B_obtido": b_obtido,
            "ponto_entrada_id": entrada_id,
            "diferencas": ["Modelo avulso fora da Tabela 1 de referência."],
        }

    diferencas: list[str] = []
    if v_obtido != ref["V"]:
        diferencas.append(f"|V| obtido ({v_obtido}) != esperado ({ref['V']})")
    if e_obtido != ref["E"]:
        diferencas.append(f"|E| obtido ({e_obtido}) != esperado ({ref['E']})")
    if t_obtido != ref["T"]:
        diferencas.append(f"T obtido ({t_obtido}) != esperado ({ref['T']})")
    if b_obtido != ref["B"]:
        diferencas.append(f"B obtido ({b_obtido}) != esperado ({ref['B']})")
    if entrada_id != 0:
        diferencas.append(f"Ponto de entrada obtido ({entrada_id}) != esperado (0)")
    if not sem_grau_inesperado:
        diferencas.append(
            f"Existem {len(estrutura['pontos_grau_inesperado'])} pontos com graus inesperados"
        )

    return {
        "possui_referencia": True,
        "coincide_tabela_1": len(diferencas) == 0,
        "nterm_esperado": ref["nterm"],
        "V_esperado": ref["V"],
        "E_esperado": ref["E"],
        "T_esperado": ref["T"],
        "B_esperado": ref["B"],
        "V_obtido": v_obtido,
        "E_obtido": e_obtido,
        "T_obtido": t_obtido,
        "B_obtido": b_obtido,
        "ponto_entrada_id": entrada_id,
        "diferencas": diferencas,
    }
