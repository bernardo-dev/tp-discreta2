"""
Aba C2: Relações de Recorrência e Validação nos 6 Modelos VTK.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_c2() -> None:
    """
    Renderiza a Aba C2 do Módulo C:
    - Formulação da relação de recorrência para e_k (Nterm = 16 · 2^k);
    - Resolução por iteração/substituição e equação característica;
    - Confronto entre a forma fechada e os 6 modelos reais.
    """
    st.subheader("C2 — Relações de Recorrência e Validação")
    st.info(
        "Estrutura da interface preparada para a **Parte C2 (Recorrências)** "
        "na sequência $N_{\\text{term}} = 16 \\cdot 2^k$ ($k = 0, \\dots, 5$).",
        title="Módulo C — Parte C2 em desenvolvimento",
    )
    st.markdown(
        r"""
### Requisitos Previstos nesta Aba
- **C2.1.** Tabela evolutiva com $k$, $N_{\text{term}}$, $|V|$, $e_k$, $B$ e $T$ e relação de recorrência com condição inicial.
- **C2.2.** Resolução algébrica por iteração ou substituição.
- **C2.3.** Resolução pelo método da equação característica e confronto com os 6 modelos reais.
- **C2.4.** Segunda relação envolvendo $T$, $B$ ou $|V|$ e discussão dos pressupostos.
        """
    )
