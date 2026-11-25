"""
Aba 2: Princípio da Casa dos Pombos (B0.3) & Comparativo Geométrico — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.interface.modulo_b.grafico_3d import (
    construir_grafico_distribuicao_pcp,
    construir_graficos_comparativos_geometria,
)


def renderizar_aba_casa_dos_pombos(resultado_b0: dict[str, Any]) -> None:
    """
    Renderiza a Aba 2 do Módulo B:
    - Alerta conceitual sobre o Critério de Pertinência (utilidade computacional
      como Tabela Hash h(i) = i mod m vs. ausência de significado fisiológico);
    - Gráfico de barras da distribuição de |C_j| com linha horizontal tracejada
      do limite inferior do Princípio da Casa dos Pombos (ceil(|E|/m)) e análise B0.3;
    - Gráficos comparativos de comprimento euclidiano 3D médio e raio médio por classe.
    """
    m: int = int(resultado_b0["modulo_m"])
    total_e: int = int(resultado_b0["total_segmentos_E"])
    pcp: dict[str, Any] = resultado_b0["casa_dos_pombos"]
    disc: dict[str, str] = resultado_b0["discussao_b04"]

    st.subheader(
        f"Distribuição Modular e Princípio da Casa dos Pombos Generalizado (B0.3 — mod {m})"
    )

    st.warning(
        f"{disc['limitacao_fisiologica']}\n\n"
        f"**Nota técnica sobre o operador `%` em Python:** Para divisor inteiro "
        f"positivo $m = {m}$, a operação `j = i % m` implementa diretamente o resto "
        f"não-negativo único do **Algoritmo da Divisão Euclidiana** "
        f"($i = {m}q + j$, com $0 \\le j < {m}$), garantindo que cada identificador "
        f"$i \\in \\{{0, \\dots, {max(0, total_e - 1)}\\}}$ pertença a uma única "
        f"classe de resíduo $C_j$."
    )

    col_graf_pcp, col_texto_pcp = st.columns([3, 2])

    with col_graf_pcp:
        fig_pcp = construir_grafico_distribuicao_pcp(resultado_b0)
        st.plotly_chart(fig_pcp, width="stretch")

    with col_texto_pcp:
        st.subheader("Análise do Limite Inferior (PCP)")
        st.markdown(
            f"""
- **Objetos ("pombos"):** $N = |E| = {pcp['pombos_N']}$ segmentos numerados de $0$ a ${max(0, total_e - 1)}$ na ordem da seção `LINES`.
- **Caixas ("gavetas"):** $m = {pcp['gavetas_m']}$ restos possíveis $\\{{0, 1, \\dots, {m - 1}\\}}$ na divisão por ${m}$.
- **Limite inferior teórico da maior classe:**
  $$\\left\\lceil \\frac{{|E|}}{{{m}}} \\right\\rceil = \\left\\lceil \\frac{{{pcp['pombos_N']}}}{{{pcp['gavetas_m']}}} \\right\\rceil = {pcp['limite_inferior_pcp']}$$
- **Divisão Euclidiana de $|E|$ por $m$:**
  $${pcp['pombos_N']} = {pcp['gavetas_m']} \\times {pcp['quociente_euclidiano']} + {pcp['resto_euclidiano']}$$
- **Confronto com os dados reais:**
  - Maior classe observada: $\\max_{{0 \\le j < {m}}} |C_j| = {pcp['max_observado']}$
  - Classes no limite ($|C_j| \\ge {pcp['limite_inferior_pcp']}$): **{', '.join(pcp['classes_no_limite'])}** ({pcp['qtd_classes_no_limite']} classes com {pcp['max_observado']} segmentos)
  - Demais classes ($|C_j| = {pcp['min_observado']}$): **{', '.join(pcp['classes_abaixo_limite']) if pcp['classes_abaixo_limite'] else 'Nenhuma'}** ({pcp['qtd_classes_abaixo_limite']} classes)
            """
        )
        if pcp["desigualdade_confirmada"]:
            st.success(
                f"**Limite da Casa dos Pombos Verificado:** "
                f"$\\max |C_j| = {pcp['max_observado']} \\ge "
                f"\\lceil {total_e}/{m} \\rceil = {pcp['limite_inferior_pcp']}$."
            )

    st.divider()

    st.subheader("Comparativo Geométrico entre Classes Modulares (Unidades Originais VTK)")
    st.markdown(
        "Comparação do comprimento euclidiano 3D médio e do raio médio de cada classe $C_j$ "
        "frente à média global do modelo (linha tracejada), evidenciando que a partição por "
        "índice de gravação oscila em torno da média global sem especialização anatômica."
    )

    fig_comp, fig_raio = construir_graficos_comparativos_geometria(resultado_b0)
    col_g_comp, col_g_raio = st.columns(2)
    with col_g_comp:
        st.plotly_chart(fig_comp, width="stretch")
    with col_g_raio:
        st.plotly_chart(fig_raio, width="stretch")
