"""
Página Principal do Módulo C — Contagem e Relações de Recorrência.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_c.aba_c1_contagem import renderizar_aba_c1
from src.interface.modulo_c.aba_c2_recorrencias import renderizar_aba_c2


def renderizar_pagina_modulo_c() -> None:
    """
    Orquestra a página da interface gráfica do Módulo C:
    - Aba C1: Técnicas de contagem e inclusão–exclusão geométrica;
    - Aba C2: Relações de recorrência e validação nos 6 modelos.
    """
    st.title("📊 CCO Explorer — Módulo C: Contagem e Relações de Recorrência")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Combinatória, Princípio da Inclusão–Exclusão e Resolução de Recorrências"
    )

    aba_c1, aba_c2 = st.tabs(
        [
            "Parte C1 — Técnicas de Contagem & Inclusão–Exclusão",
            "Parte C2 — Relações de Recorrência & Validação",
        ]
    )

    with aba_c1:
        renderizar_aba_c1()

    with aba_c2:
        renderizar_aba_c2()


if __name__ == "__main__":
    renderizar_pagina_modulo_c()
