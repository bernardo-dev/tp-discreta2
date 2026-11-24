"""
Aba D1–D4: Relação Pai–Filho, Representações Matriciais, Propriedades e Função Associada.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_d1_d4() -> None:
    """
    Renderiza a Aba D1–D4 do Módulo D:
    - Relação pai–filho R ⊆ V × V, domínio e imagem;
    - Lista de pares e matriz booleana 32 × 32 para Nterm016;
    - Propriedades (reflexiva, simétrica, antissimétrica, transitiva) e R^(-1);
    - Função pai p: V \\ {0} -> V.
    """
    st.subheader("D1 a D4 — Relação Pai–Filho, Matriz $32 \\times 32$, Propriedades e Função Pai")
    st.info(
        "Estrutura da interface preparada para os itens **D1 a D4** "
        "(relação pai–filho $\\mathcal{R}$, matriz $32 \\times 32$ de `Nterm016`, "
        "propriedades e função associada $p: V \\setminus \\{0\\} \\to V$).",
        title="Módulo D — Itens D1 a D4 em desenvolvimento",
    )
    st.markdown(
        r"""
### Requisitos Previstos nesta Aba
- **D1.** Definição explícita de $\mathcal{R} \subseteq V \times V$, $\text{dom}(\mathcal{R})$ e $\text{im}(\mathcal{R})$ para `Nterm016`.
- **D2.** Lista de pares ordenados de $\mathcal{R}$ e matriz completa $A = [a_{uv}]_{32 \times 32}$ para `Nterm016`.
- **D3.** Investigação de reflexividade, simetria, antissimetria e transitividade de $\mathcal{R}$ e $\mathcal{R}^{-1}$.
- **D4.** Verificação da função pai $p: V \setminus \{0\} \to V$ nos dados reais.
        """
    )
