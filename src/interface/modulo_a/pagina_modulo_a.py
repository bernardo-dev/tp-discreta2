"""
Página Principal do Módulo A — Modelagem Discreta, Geometria 3D e Validação VTK.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_a.aba_consolidado import renderizar_aba_consolidado
from src.interface.modulo_a.aba_renderizador_3d import renderizar_aba_3d
from src.interface.modulo_a.aba_tabelas import renderizar_aba_tabelas
from src.interface.modulo_a.barra_lateral import renderizar_barra_lateral_modulo_a
from src.interface.modulo_a.cartoes_metricas import renderizar_cartoes_metricas


def renderizar_pagina_modulo_a() -> None:
    """
    Orquestra a página completa da interface gráfica do Módulo A:
    - Cabeçalho da página;
    - Barra lateral de seleção de dados VTK e opções do renderizador 3D;
    - Cartões superiores de métricas (|V|, |E|, T, B, Entrada, Validação A3);
    - Três abas principais (Renderizador 3D, Consolidação dos 6 Modelos e Tabelas/CSV).
    """
    st.title("🫀 CCO Explorer — Módulo A: Modelagem Discreta e Geometria 3D")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Leitura VTK, Geometria Euclidiana 3D, Validação Estrutural e Identificação de Pontos "
        "(unidades originais do VTK)"
    )

    opcoes_lateral = renderizar_barra_lateral_modulo_a()
    modelo_ativo = opcoes_lateral["modelo_ativo"]
    pasta_informada = opcoes_lateral["pasta_informada"]

    renderizar_cartoes_metricas(modelo_ativo)

    aba_3d, aba_consolidado, aba_tabelas = st.tabs(
        [
            "Renderizador 3D & Diagnóstico Estrutural",
            "Consolidação dos 6 Modelos (Tabela 1)",
            "Tabela de Segmentos e Pontos (Exportação CSV)",
        ]
    )

    with aba_3d:
        renderizar_aba_3d(modelo_ativo=modelo_ativo, opcoes_3d=opcoes_lateral)

    with aba_consolidado:
        renderizar_aba_consolidado(pasta_informada=pasta_informada)

    with aba_tabelas:
        renderizar_aba_tabelas(modelo_ativo=modelo_ativo)


if __name__ == "__main__":
    renderizar_pagina_modulo_a()
