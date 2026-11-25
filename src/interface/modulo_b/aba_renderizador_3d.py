"""
Aba 1: Renderizador 3D & Diagnóstico da Partição Modular (B0.2 e B0.4) — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.interface.modulo_b.grafico_3d import construir_figura_3d_classe_modular
from src.modulo_b.modulo_b_numeros import (
    consultar_por_residuo,
    formatar_resumo_b0,
)


def renderizar_aba_3d(
    modelo_ativo: dict[str, Any],
    resultado_b0: dict[str, Any],
    opcoes_3d: dict[str, Any],
) -> None:
    """
    Renderiza a Aba 1 do Módulo B:
    - Alerta com detalhes da classe de resíduo C_j destacada (consulta determinística B0.4);
    - Figura interativa 3D da árvore vascular destacando os segmentos de C_j;
    - Checklist de Validação da Partição B0.2 e Discussão Crítica B0.4;
    - Formulação matemática aplicada (Algoritmo da Divisão Euclidiana, Partição e PCP);
    - Resumo matemático textual expansível da Parte B0.
    """
    m: int = int(resultado_b0["modulo_m"])
    total_e: int = int(resultado_b0["total_segmentos_E"])
    resto_destaque: int = int(opcoes_3d["resto_destaque"])
    val: dict[str, Any] = resultado_b0["validacao_particao"]
    pcp: dict[str, Any] = resultado_b0["casa_dos_pombos"]
    disc: dict[str, str] = resultado_b0["discussao_b04"]

    consulta_ativa = consultar_por_residuo(
        segmentos=modelo_ativo["segmentos"],
        resto_j=resto_destaque,
        m=m,
    )
    exemplos_str = ", ".join(str(idx) for idx in consulta_ativa["exemplos_ids"])

    st.info(
        f"**Classe Destacada ${consulta_ativa['classe']}$** — "
        f"**Congruência:** ${consulta_ativa['expressao_congruencia']}$ | "
        f"**Função Hash:** `{consulta_ativa['funcao_hash']}` | "
        f"**Cardinalidade $|{consulta_ativa['classe']}|$:** `{consulta_ativa['quantidade']}` segmentos | "
        f"**Comprimento 3D Médio:** `{consulta_ativa['comprimento_3d_medio']:.7f}` | "
        f"**Raio Médio:** `{consulta_ativa['raio_medio']:.7f}` | "
        f"**Primeiros IDs:** `[{exemplos_str}]`"
    )

    fig_3d = construir_figura_3d_classe_modular(
        modelo_a=modelo_ativo,
        resultado_b0=resultado_b0,
        resto_destaque=resto_destaque,
        colorir_todas_classes=opcoes_3d["colorir_todas_classes"],
        espessura_proporcional=opcoes_3d["espessura_proporcional"],
        fator_espessura=opcoes_3d["fator_espessura"],
        mostrar_pontos_medios=opcoes_3d["mostrar_pontos_medios"],
        mostrar_entrada=opcoes_3d["mostrar_entrada"],
    )
    st.plotly_chart(fig_3d, width="stretch")

    col_diag1, col_diag2 = st.columns(2)

    with col_diag1:
        st.subheader("Checklist de Validação B0.2 e Consulta Determinística B0.4")
        if val["particao_valida"]:
            st.success(
                f"**Validação da Partição B0.2 Aprovada:** {'; '.join(val['mensagens'])}"
            )
        else:
            for msg in val["mensagens"]:
                st.error(f"Inconsistência: {msg}")

        st.markdown(
            f"""
- **Não-vacuidade das classes ($C_j \\neq \\varnothing$):** `{m}` classes verificadas → **{'OK' if val['classes_nao_vazias'] else 'ERRO'}**
- **Disjunção dois a dois ($C_j \\cap C_k = \\varnothing, \\forall j \\neq k$):** `{val['num_pares_verificados']}` pares verificados com `set` → **{'OK' if val['disjuntas_dois_a_dois'] else 'ERRO'}**
- **Soma das cardinalidades ($\\sum_{{j=0}}^{{{m - 1}}} |C_j| = |E|$):** soma `{val['soma_cardinalidades']}` vs. $|E| = {val['total_segmentos_E']}` → **{'OK' if val['soma_igual_total'] else 'ERRO'}**
- **Cobertura exata da união ($\\bigcup_{{j=0}}^{{{m - 1}}} C_j = E$):** cardinalidade `|{val['cardinalidade_uniao']}|` → **{'OK' if val['uniao_cobre_universo'] else 'ERRO'}**
- **Limite do Princípio da Casa dos Pombos (B0.3):** $\\max |C_j| = {pcp['max_observado']} \\ge \\lceil {total_e}/{m} \\rceil = {pcp['limite_inferior_pcp']}` → **{'CONFIRMADO' if pcp['desigualdade_confirmada'] else 'ERRO'}**
- **Conexão com o Módulo D:** {disc['conexao_modulo_d']}
- **Limitação Anatômica (Critério de Pertinência):** O índice $i$ decorre da ordem de gravação na seção `LINES` do VTK; logo, $C_j$ espalha-se pela árvore sem isolar uma região fisiológica específica.
            """
        )

    with col_diag2:
        st.subheader("Formulação Matemática Aplicada (B0.1 a B0.4)")
        st.markdown(
            rf"""
Para o conjunto de segmentos $E = \{{0, 1, \dots, |E| - 1\}}$ indexados na ordem da seção `LINES` e módulo inteiro $m = {m} > 0$:

1. **Algoritmo da Divisão Euclidiana e Operador `%` em Python:**
   $$\forall i \in \mathbb{{Z}},\; \exists!\, (q, j) \in \mathbb{{Z}}^2 \text{{ tal que }} i = m \cdot q + j, \quad 0 \le j < m$$
   Em Python, para $m > 0$, `j = i % m` retorna exatamente o resto euclidiano não-negativo $j \in \{{0, \dots, {m - 1}\}}$.

2. **Classes de Congruência Módulo $m$ e Partição de $E$ (B0.1 e B0.2):**
   $$C_j = \{{i \in E : i \equiv j \pmod{{{m}}}\}}, \qquad C_j \neq \varnothing,\qquad C_j \cap C_k = \varnothing \;(j \neq k),\qquad \bigcup_{{j=0}}^{{{m - 1}}} C_j = E$$

3. **Princípio da Casa dos Pombos Generalizado (B0.3):**
   Distribuindo $N = |E| = {total_e}$ segmentos (*pombos*) em $m = {m}$ classes (*gavetas*):
   $$\max_{{0 \le j < {m}}} |C_j| \ge \left\lceil \frac{{|E|}}{{{m}}} \right\rceil = \left\lceil \frac{{{total_e}}}{{{m}}} \right\rceil = {pcp['limite_inferior_pcp']}$$
            """
        )

    with st.expander("📄 Visualizar Resumo Matemático Textual (Parte B0 — Teoria dos Números)"):
        st.code(formatar_resumo_b0(resultado_b0), language="text")
