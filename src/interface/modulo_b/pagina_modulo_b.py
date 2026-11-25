"""
Página Principal do Módulo B — Teoria dos Números Aplicada à Consulta dos Segmentos.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_b.aba_b1_trilha_eletiva import renderizar_aba_b1
from src.interface.modulo_b.aba_casa_dos_pombos import (
    renderizar_aba_casa_dos_pombos,
)
from src.interface.modulo_b.aba_renderizador_3d import renderizar_aba_3d
from src.interface.modulo_b.aba_tabelas import renderizar_aba_tabelas
from src.interface.modulo_b.barra_lateral import renderizar_barra_lateral_modulo_b
from src.interface.modulo_b.cartoes_metricas import renderizar_cartoes_metricas


def renderizar_pagina_modulo_b() -> None:
    """
    Orquestra a página completa da interface gráfica do Módulo B:
    - Cabeçalho da página;
    - Barra lateral de seleção de dados VTK, módulo m e opções do renderizador 3D;
    - Cartões superiores de métricas (|E|, Módulo m, Limite PCP, Maior/Menor Classe, Validação B0.2);
    - Quatro abas principais (Renderizador 3D & Diagnóstico B0, Princípio da Casa dos Pombos,
      Tabelas/CSV e Trilha Eletiva B1).
    """
    st.title("🔢 CCO Explorer — Módulo B: Teoria dos Números e Consultas Modulares")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Classes de Resíduos Módulo 7, Validação Matemática da Partição, "
        "Princípio da Casa dos Pombos Generalizado (B0) e Trilha Eletiva (B1)"
    )

    opcoes_lateral = renderizar_barra_lateral_modulo_b()
    modelo_ativo = opcoes_lateral["modelo_ativo"]
    resultado_b0 = opcoes_lateral["resultado_b0"]

    renderizar_cartoes_metricas(resultado_b0)

    aba_3d, aba_pcp, aba_tabelas, aba_b1 = st.tabs(
        [
            "Renderizador 3D & Diagnóstico da Partição (B0.2 e B0.4)",
            "Princípio da Casa dos Pombos & Geometria (B0.3)",
            "Tabelas de Classes e Segmentos (Exportação CSV — B0.1)",
            "Parte B1 — Trilha Eletiva",
        ]
    )

    with aba_3d:
        renderizar_aba_3d(
            modelo_ativo=modelo_ativo,
            resultado_b0=resultado_b0,
            opcoes_3d=opcoes_lateral,
        )

    with aba_pcp:
        renderizar_aba_casa_dos_pombos(resultado_b0=resultado_b0)

    with aba_tabelas:
        renderizar_aba_tabelas(
            modelo_ativo=modelo_ativo,
            resultado_b0=resultado_b0,
        )

    with aba_b1:
        renderizar_aba_b1()


if __name__ == "__main__":
    renderizar_pagina_modulo_b()
