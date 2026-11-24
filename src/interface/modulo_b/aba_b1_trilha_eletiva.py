"""
Aba B1: Trilha Eletiva — Teoria dos Números Aplicada à Consulta de Segmentos.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st


def renderizar_aba_b1() -> None:
    """
    Renderiza a Aba B1 do Módulo B:
    - Trilha 1: Algoritmo de Euclides e Teorema Chinês do Resto (recomendada);
    - Trilha 2: Primalidade e consulta de segmentos;
    - Trilha 3: Congruências lineares e reorganização de índices.
    """
    st.subheader("B1 — Trilha Eletiva de Teoria dos Números")
    st.info(
        "Estrutura da interface preparada para a **Parte B1 (Trilha Eletiva)** "
        "aplicada aos modelos `Nterm128` e `Nterm512`.",
        title="Módulo B — Parte B1 em desenvolvimento",
    )
    st.markdown(
        r"""
### Trilhas Eletivas Disponíveis no Enunciado
1. **Trilha 1 — Algoritmo de Euclides e Teorema Chinês do Resto (Recomendada):**
   Consultas simultâneas $i \equiv 1 \pmod 4$ e $i \equiv 2 \pmod 5$, verificação de $\text{mdc}(4, 5) = 1$ e classe equivalente módulo $20$.
2. **Trilha 2 — Primalidade e Consulta de Segmentos:**
   Seleção de identificadores primos $0 \le i < |E|$ por divisão até $\lfloor\sqrt{i}\rfloor$ ou Crivo de Eratóstenes.
3. **Trilha 3 — Congruências Lineares e Reorganização de Índices:**
   Bijeção $h(i) = (a i + b) \bmod 7$ com $\text{mdc}(a, 7) = 1$.
        """
    )
