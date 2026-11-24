"""
Página Principal do Módulo D — Relações, Representações e Propriedades.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_d.aba_d1_d4_relacoes import renderizar_aba_d1_d4
from src.interface.modulo_d.aba_d5_d6_fechos_ordem import renderizar_aba_d5_d6


def renderizar_pagina_modulo_d() -> None:
    """
    Orquestra a página da interface gráfica do Módulo D:
    - Aba D1–D4: Relação pai–filho, matriz 32x32, propriedades e função pai;
    - Aba D5–D6: Fecho transitivo R+, ordem parcial e equivalência modular.
    """
    st.title("🔗 CCO Explorer — Módulo D: Relações, Representações e Propriedades")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Relação Pai–Filho, Matriz de Adjacência, Propriedades, Fecho Transitivo e Ordem Parcial"
    )

    aba_relacoes, aba_fechos = st.tabs(
        [
            "D1 a D4 — Relação Pai–Filho, Matriz 32×32 & Propriedades",
            "D5 e D6 — Fecho Transitivo R⁺, Ordem Parcial & Equivalência",
        ]
    )

    with aba_relacoes:
        renderizar_aba_d1_d4()

    with aba_fechos:
        renderizar_aba_d5_d6()


if __name__ == "__main__":
    renderizar_pagina_modulo_d()
