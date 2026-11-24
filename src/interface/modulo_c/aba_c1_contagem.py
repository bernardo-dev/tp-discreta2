"""
Aba C1: Técnicas de Contagem e Princípio da Inclusão–Exclusão Geométrico.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_c1() -> None:
    """
    Renderiza a Aba C1 do Módulo C:
    - Relações combinatórias entre T, B, |V| e |E|;
    - Combinações de terminais C(T, 2) e princípio multiplicativo B × T;
    - Princípio da Inclusão–Exclusão geométrico em Nterm128.
    """
    st.subheader("C1 — Técnicas de Contagem e Inclusão–Exclusão Geométrica")
    st.info(
        "Estrutura da interface preparada para a **Parte C1 (Técnicas de Contagem)** "
        "com combinações de terminais $\\binom{T}{2}$, pares $(b, t)$ e inclusão–exclusão "
        "sobre as medianas de raio e comprimento 3D.",
        title="Módulo C — Parte C1 em desenvolvimento",
    )
    st.markdown(
        r"""
### Requisitos Previstos nesta Aba
- **C1.1.** Relações estruturais entre $T$, $B$, $|V|$ e $|E|$ nos 6 modelos VTK.
- **C1.2.** Seleção não ordenada de dois terminais: $\binom{T}{2}$ para `Nterm016` e `Nterm128`.
- **C1.3.** Pares ordenados $(b, t)$ pelo Princípio Multiplicativo ($B \cdot T$).
- **C1.4.** Inclusão–Exclusão em `Nterm128` com conjuntos $A = \{i : r_i \ge r_{\text{med}}\}$ e $B = \{i : \ell_i \ge \ell_{\text{med}}\}$, verificando $|A \cup B| = |A| + |B| - |A \cap B|$.
        """
    )
