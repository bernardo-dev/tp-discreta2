"""
Aba D5–D6: Fecho Transitivo, Ordem Parcial e Relação de Equivalência Modular.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_d5_d6() -> None:
    """
    Renderiza a Aba D5–D6 do Módulo D:
    - Fecho transitivo R+ (ancestralidade estrita) para Nterm016;
    - Ordem parcial ⪯ = R+ ∪ {(v, v)} e pares incomparáveis;
    - Relação de equivalência modular i ~ j <=> i ≡ j (mod 7) em Nterm128.
    """
    st.subheader("D5 e D6 — Fecho Transitivo $\\mathcal{R}^+$, Ordem Parcial e Equivalência Modular")
    st.info(
        "Estrutura da interface preparada para os itens **D5 e D6** "
        "(fecho transitivo $\\mathcal{R}^+$, ordem parcial $\\preceq$ em `Nterm016` "
        "e relação de equivalência modular em `Nterm128`).",
        title="Módulo D — Itens D5 e D6 em desenvolvimento",
    )
    st.markdown(
        r"""
### Requisitos Previstos nesta Aba
- **D5.** Construção de $\mathcal{R}^+$ e da relação de ordem parcial $\preceq \;=\; \mathcal{R}^+ \cup \{(v, v) : v \in V\}$ em `Nterm016`, com exemplos de pontos incomparáveis.
- **D6.** Demonstração e verificação da relação de equivalência $i \sim j \iff i \equiv j \pmod 7$ e correspondência com as classes $C_0, \dots, C_6$ do Módulo B.
        """
    )
