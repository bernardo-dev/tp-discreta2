"""
Módulo A3 — Validação da Representação e Consistência dos Dados.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import math
from typing import Any

# ==============================================================================
# A3. Validação da Representação e Consistência dos Dados
# ==============================================================================


def validar_dados_vtk(dados_vtk: dict[str, Any]) -> dict[str, Any]:
    """
    Requisito A3: Verifica a consistência estrutural e numérica do arquivo VTK:
    1. Se todos os identificadores u e v citados em LINES existem em POINTS.
    2. Se existe exatamente um valor de raio válido para cada segmento lido.
    3. Se a quantidade de pontos e de segmentos lidos coincide com os totais
       declarados no cabeçalho do arquivo VTK.

    Retorna um dicionário estruturado com `valido: bool` e a lista de
    mensagens/inconsistências encontradas.
    """
    cabecalho = dados_vtk.get("cabecalho", {})
    pontos: list[dict[str, Any]] = dados_vtk.get("pontos", [])
    segmentos: list[dict[str, Any]] = dados_vtk.get("segmentos", [])
    raios: list[float] = dados_vtk.get("raios", [])

    inconsistencias: list[str] = []

    num_pontos_lidos = len(pontos)
    num_segmentos_lidos = len(segmentos)
    num_raios_lidos = len(raios)

    num_pontos_decl = cabecalho.get("num_pontos_declarado")
    num_linhas_decl = cabecalho.get("num_linhas_declarado")
    num_cell_data_decl = cabecalho.get("num_cell_data_declarado")
    sobra_floats = cabecalho.get("sobra_floats_pontos", 0)
    linhas_malformadas = cabecalho.get("linhas_malformadas", [])

    # 1. Verificação dos totais declarados no cabeçalho VTK
    contagem_pontos_ok = (
        num_pontos_decl is not None
        and num_pontos_lidos == num_pontos_decl
        and num_pontos_lidos > 0
        and sobra_floats == 0
    )
    if num_pontos_decl is None:
        inconsistencias.append("Cabeçalho POINTS ausente no arquivo VTK.")
    elif num_pontos_lidos != num_pontos_decl:
        inconsistencias.append(
            f"Quantidade de pontos lidos ({num_pontos_lidos}) difere do total "
            f"declarado em POINTS ({num_pontos_decl})."
        )
    if sobra_floats != 0:
        inconsistencias.append(
            f"Coordenadas incompletas em POINTS: sobraram {sobra_floats} valores float."
        )

    contagem_segmentos_ok = (
        num_linhas_decl is not None
        and num_segmentos_lidos == num_linhas_decl
        and num_segmentos_lidos > 0
        and len(linhas_malformadas) == 0
    )
    if num_linhas_decl is None:
        inconsistencias.append("Cabeçalho LINES ausente no arquivo VTK.")
    elif num_segmentos_lidos != num_linhas_decl:
        inconsistencias.append(
            f"Quantidade de segmentos lidos ({num_segmentos_lidos}) difere do "
            f"total declarado em LINES ({num_linhas_decl})."
        )
    if linhas_malformadas:
        inconsistencias.append(
            f"Encontradas {len(linhas_malformadas)} linhas malformadas na seção LINES."
        )

    # 2. Verificação de existência dos identificadores u e v em POINTS
    ids_pontos_validos: set[int] = {int(p["id"]) for p in pontos}
    extremos_inexistentes: list[tuple[int, int, int]] = []
    registros_nao_binarios: list[int] = []
    auto_lacos: list[int] = []

    for seg in segmentos:
        seg_id = int(seg["id"])
        u = int(seg["u"])
        v = int(seg["v"])
        qtd_vert = int(seg.get("qtd_vertices_registro", 2))

        if qtd_vert != 2:
            registros_nao_binarios.append(seg_id)
        if u not in ids_pontos_validos or v not in ids_pontos_validos:
            extremos_inexistentes.append((seg_id, u, v))
        if u == v:
            auto_lacos.append(seg_id)

    extremos_validos = (
        len(extremos_inexistentes) == 0
        and len(registros_nao_binarios) == 0
        and len(auto_lacos) == 0
    )
    if extremos_inexistentes:
        amostra = extremos_inexistentes[:5]
        inconsistencias.append(
            f"Identificadores em LINES fora do conjunto POINTS (ex.: {amostra})."
        )
    if registros_nao_binarios:
        inconsistencias.append(
            f"Registros em LINES com formato diferente de '2 u v' nos segmentos: "
            f"{registros_nao_binarios[:5]}."
        )
    if auto_lacos:
        inconsistencias.append(
            f"Segmentos degenerados com extremo inicial igual ao final (u == v): "
            f"{auto_lacos[:5]}."
        )

    # 3. Verificação da correspondência 1-para-1 de raio por segmento
    raios_invalidos: list[int] = []
    for seg in segmentos:
        r = seg.get("raio")
        if r is None or math.isnan(float(r)) or float(r) <= 0.0:
            raios_invalidos.append(int(seg["id"]))

    raios_completos = (
        num_raios_lidos == num_segmentos_lidos
        and (num_cell_data_decl is None or num_cell_data_decl == num_segmentos_lidos)
        and len(raios_invalidos) == 0
    )
    if num_raios_lidos != num_segmentos_lidos:
        inconsistencias.append(
            f"Quantidade de raios lidos ({num_raios_lidos}) difere da quantidade "
            f"de segmentos ({num_segmentos_lidos})."
        )
    if num_cell_data_decl is not None and num_cell_data_decl != num_segmentos_lidos:
        inconsistencias.append(
            f"Total declarado em CELL_DATA ({num_cell_data_decl}) difere do total "
            f"de segmentos ({num_segmentos_lidos})."
        )
    if raios_invalidos:
        inconsistencias.append(
            f"Segmentos com valor de raio ausente ou não positivo: {raios_invalidos[:5]}."
        )

    valido = len(inconsistencias) == 0
    mensagens = (
        [
            f"OK: {num_pontos_lidos} pontos validados, {num_segmentos_lidos} "
            f"segmentos orientados e {num_raios_lidos} raios consistentes."
        ]
        if valido
        else list(inconsistencias)
    )

    return {
        "valido": valido,
        "status": "OK" if valido else "INCONSISTENTE",
        "inconsistencias": inconsistencias,
        "mensagens": mensagens,
        "contagem_pontos_ok": contagem_pontos_ok,
        "contagem_segmentos_ok": contagem_segmentos_ok,
        "extremos_validos": extremos_validos,
        "raios_completos": raios_completos,
        "num_pontos_lidos": num_pontos_lidos,
        "num_pontos_declarado": num_pontos_decl,
        "num_segmentos_lidos": num_segmentos_lidos,
        "num_linhas_declarado": num_linhas_decl,
        "num_raios_lidos": num_raios_lidos,
        "num_cell_data_declarado": num_cell_data_decl,
    }
