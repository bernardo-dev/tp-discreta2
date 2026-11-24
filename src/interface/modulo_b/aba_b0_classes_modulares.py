"""
Aba B0: Núcleo Obrigatório — Classes de Congruência Módulo 7 e Casa dos Pombos.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_b0() -> None:
    """
    Renderiza a Aba B0 do Módulo B:
    - Agrupamento por aritmética modular C_j = {i : i ≡ j (mod 7)};
    - Validação da partição;
    - Princípio da Casa dos Pombos.
    """
    st.subheader("B0 — Agrupamento Modular ($m = 7$) e Princípio da Casa dos Pombos")
    st.info(
        "Estrutura da interface preparada para o **Núcleo Obrigatório B0** "
        "(classes de resíduos $C_j = \\{i : i \\equiv j \\pmod{7}\\}$, validação da partição "
        "e limite inferior pelo Princípio da Casa dos Pombos em `Nterm128`).",
        title="Módulo B — Parte B0 em desenvolvimento",
    )
    st.markdown(
        r"""
### Requisitos Previstos nesta Aba
- **B0.1.** Agrupamento por aritmética modular ($m = 7$) com $|C_j|$, comprimento médio e raio médio por classe.
- **B0.2.** Validação da partição: $C_j \cap C_k = \varnothing$ ($j \neq k$) e $\sum_{j=0}^{6} |C_j| = |E|$.
- **B0.3.** Aplicação do Princípio da Casa dos Pombos ($\lceil |E| / 7 \rceil$) e verificação com os dados reais.
- **B0.4.** Discussão sobre consultas determinísticas por classes de resíduos.
        """
    )
