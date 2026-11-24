"""
Página Principal do Módulo E — Integração, Relatório e Reprodutibilidade.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.modulo_e.aba_resumo_integrado import renderizar_aba_resumo_integrado


def renderizar_pagina_modulo_e() -> None:
    """
    Orquestra a página da interface gráfica do Módulo E:
    - Resumo Matemático Integrado (Seção 8.2);
    - Checklist dos Testes Mínimos de Aceitação (T1 a T7).
    """
    st.title("📋 CCO Explorer — Módulo E: Integração e Reprodutibilidade")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Resumo Matemático Integrado (Seção 8.2) e Testes Mínimos de Aceitação (T1 a T7)"
    )

    (aba_resumo,) = st.tabs(
        [
            "Resumo Matemático Integrado & Testes de Aceitação (T1–T7)",
        ]
    )

    with aba_resumo:
        renderizar_aba_resumo_integrado()


if __name__ == "__main__":
    renderizar_pagina_modulo_e()
