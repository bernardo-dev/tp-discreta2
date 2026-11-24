"""
Cartões Superiores de Métricas Estruturais e Validação — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def renderizar_cartoes_metricas(modelo_ativo: dict[str, Any]) -> None:
    """
    Renderiza os 6 cartões superiores de métricas do modelo VTK ativo:
    Pontos |V|, Segmentos |E|, Terminais (T), Bifurcações (B),
    Ponto de Entrada e Status da Validação A3.
    """
    est = modelo_ativo["estrutura"]
    val = modelo_ativo["validacao"]
    comp = modelo_ativo["comparacao_tabela_1"]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        delta_v = (
            f"Ref Tab.1: {comp['V_esperado']}"
            if comp["possui_referencia"]
            else "Modelo avulso"
        )
        st.metric("Pontos |V|", f"{est['num_pontos_V']}", delta_v)

    with col2:
        delta_e = (
            f"Ref Tab.1: {comp['E_esperado']}"
            if comp["possui_referencia"]
            else "|V| - 1"
        )
        st.metric("Segmentos |E|", f"{est['num_segmentos_E']}", delta_e)

    with col3:
        delta_t = (
            f"Ref Tab.1: {comp['T_esperado']}"
            if comp["possui_referencia"]
            else "out_degree = 0"
        )
        st.metric("Terminais (T)", f"{est['num_terminais_T']}", delta_t)

    with col4:
        delta_b = (
            f"Ref Tab.1: {comp['B_esperado']}"
            if comp["possui_referencia"]
            else "out_degree = 2"
        )
        st.metric("Bifurcações (B)", f"{est['num_bifurcacoes_B']}", delta_b)

    with col5:
        id_ent = est["ponto_entrada_id"]
        texto_ent = f"ID {id_ent}" if id_ent is not None else "N/D"
        delta_ent = (
            "Confirmado ID 0"
            if est["confirmado_id_zero"]
            else "Atenção: ID != 0"
        )
        st.metric("Ponto de Entrada", texto_ent, delta_ent)

    with col6:
        status_a3 = val["status"]
        delta_a3 = (
            "100% Consistente"
            if val["valido"]
            else f"{len(val['inconsistencias'])} erro(s)"
        )
        st.metric(
            "Validação A3",
            status_a3,
            delta_a3,
            delta_color="normal" if val["valido"] else "inverse",
        )
