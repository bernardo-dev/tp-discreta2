"""
Cartões Superiores de Métricas Modulares e Validação da Partição — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st


def renderizar_cartoes_metricas(resultado_b0: dict[str, Any]) -> None:
    """
    Renderiza os 6 cartões superiores de métricas do Módulo B (Parte B0):
    Segmentos |E| (Pombos), Módulo m (Gavetas), Limite Inferior do PCP,
    Maior Classe |C_j|, Menor Classe |C_j| e Status da Validação B0.2.
    """
    total_e = int(resultado_b0["total_segmentos_E"])
    m = int(resultado_b0["modulo_m"])
    pcp = resultado_b0["casa_dos_pombos"]
    val = resultado_b0["validacao_particao"]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        st.metric(
            "Segmentos |E|",
            f"{total_e}",
            f"Modelo: {resultado_b0['codigo_modelo']}",
        )

    with col2:
        st.metric(
            "Módulo m",
            f"{m}",
            f"Classes C₀ a C_{m - 1}",
        )

    with col3:
        st.metric(
            "Limite PCP",
            f"{pcp['limite_inferior_pcp']}",
            f"⌈{total_e} / {m}⌉ = {pcp['limite_inferior_pcp']}",
        )

    with col4:
        classes_max = ", ".join(pcp["classes_no_limite"])
        st.metric(
            "Maior Classe |Cⱼ|",
            f"{pcp['max_observado']}",
            f"Atinge em: {classes_max}",
        )

    with col5:
        st.metric(
            "Menor Classe |Cⱼ|",
            f"{pcp['min_observado']}",
            f"⌊{total_e} / {m}⌋ = {pcp['quociente_euclidiano']}",
        )

    with col6:
        status_b02 = val["status"]
        delta_b02 = (
            "100% Partição Válida"
            if val["particao_valida"]
            else "Falha na partição"
        )
        st.metric(
            "Validação B0.2",
            status_b02,
            delta_b02,
            delta_color="normal" if val["particao_valida"] else "inverse",
        )
