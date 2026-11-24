"""
Página Principal do Módulo B — Teoria dos Números Aplicada à Consulta dos Segmentos.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_b.aba_b0_classes_modulares import renderizar_aba_b0
from src.interface.modulo_b.aba_b1_trilha_eletiva import renderizar_aba_b1


def renderizar_pagina_modulo_b() -> None:
    """
    Orquestra a página da interface gráfica do Módulo B:
    - Aba B0: Núcleo obrigatório (Classes modulares mod 7 e Casa dos Pombos);
    - Aba B1: Trilha eletiva (Euclides/TCR, Primalidade ou Congruências Lineares).
    """
    st.title("🔢 CCO Explorer — Módulo B: Teoria dos Números e Consultas Modulares")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Classes de Resíduos, Partição Modular, Princípio da Casa dos Pombos e Trilha Eletiva"
    )

    aba_b0, aba_b1 = st.tabs(
        [
            "Parte B0 — Classes Modulares (mod 7) & Casa dos Pombos",
            "Parte B1 — Trilha Eletiva (Euclides/TCR, Primalidade ou Congruências)",
        ]
    )

    with aba_b0:
        renderizar_aba_b0()

    with aba_b1:
        renderizar_aba_b1()


if __name__ == "__main__":
    renderizar_pagina_modulo_b()
