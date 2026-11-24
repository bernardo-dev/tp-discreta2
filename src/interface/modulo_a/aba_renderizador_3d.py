"""
Aba 1: Renderizador 3D & Diagnóstico Estrutural — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.interface.modulo_a.grafico_3d import construir_figura_3d
from src.modulo_a.modulo_a_vtk import formatar_resumo_modelo


def renderizar_aba_3d(
    modelo_ativo: dict[str, Any],
    opcoes_3d: dict[str, Any],
) -> None:
    """
    Renderiza a Aba 1 do Módulo A:
    - Alerta com detalhes do segmento destacado (quando selecionado);
    - Figura interativa 3D da árvore vascular;
    - Checklist de Validação A3 e Topologia A4;
    - Formulação matemática aplicada (A2 e A4);
    - Resumo matemático textual (Padrão Seção 8.2 do TP).
    """
    id_segmento_destaque: int | None = opcoes_3d["id_segmento_destaque"]
    est = modelo_ativo["estrutura"]
    val = modelo_ativo["validacao"]
    comp = modelo_ativo["comparacao_tabela_1"]

    if id_segmento_destaque is not None:
        seg_sel = modelo_ativo["segmentos"][id_segmento_destaque]
        st.info(
            f"**Segmento Destacado $s_{{{seg_sel['id']}}}$** — "
            f"**Extremos orientados:** $(u, v) = ({seg_sel['u']}, {seg_sel['v']})$ | "
            f"**$P_u$:** `({seg_sel['coord_u'][0]:.6f}, {seg_sel['coord_u'][1]:.6f}, {seg_sel['coord_u'][2]:.6f})` | "
            f"**$P_v$:** `({seg_sel['coord_v'][0]:.6f}, {seg_sel['coord_v'][1]:.6f}, {seg_sel['coord_v'][2]:.6f})` | "
            f"**Ponto Médio $M_{{{seg_sel['id']}}}$:** `({seg_sel['mx']:.6f}, {seg_sel['my']:.6f}, {seg_sel['mz']:.6f})` | "
            f"**Raio $r_{{{seg_sel['id']}}}$:** `{seg_sel['raio']:.7f}` | "
            f"**Comprimento 3D $\\ell_{{{seg_sel['id']}}}$:** `{seg_sel['comprimento_3d']:.7f}`"
        )

    fig_3d = construir_figura_3d(
        modelo=modelo_ativo,
        modo_cor=opcoes_3d["modo_cor"],
        espessura_proporcional=opcoes_3d["espessura_proporcional"],
        fator_espessura=opcoes_3d["fator_espessura"],
        mostrar_entrada=opcoes_3d["mostrar_entrada"],
        mostrar_bifurcacoes=opcoes_3d["mostrar_bifurcacoes"],
        mostrar_terminais=opcoes_3d["mostrar_terminais"],
        mostrar_pontos_medios=opcoes_3d["mostrar_pontos_medios"],
        id_segmento_destaque=id_segmento_destaque,
    )
    st.plotly_chart(fig_3d, width="stretch")

    col_diag1, col_diag2 = st.columns(2)

    with col_diag1:
        st.subheader("Checklist de Validação A3 e Topologia A4")
        if val["valido"]:
            st.success(
                f"**Validação A3 Aprovada:** {'; '.join(val['mensagens'])}"
            )
        else:
            for inc in val["inconsistencias"]:
                st.error(f"Inconsistência: {inc}")

        st.markdown(
            f"""
- **Cabeçalho `POINTS` vs. Pontos lidos ($|V|$):** declarado `{val['num_pontos_declarado']}`, lidos `{val['num_pontos_lidos']}` → **{'OK' if val['contagem_pontos_ok'] else 'ERRO'}**
- **Cabeçalho `LINES` vs. Segmentos lidos ($|E|$):** declarado `{val['num_linhas_declarado']}`, lidos `{val['num_segmentos_lidos']}` → **{'OK' if val['contagem_segmentos_ok'] else 'ERRO'}**
- **Cabeçalho `CELL_DATA` vs. Raios lidos:** declarado `{val['num_cell_data_declarado']}`, lidos `{val['num_raios_lidos']}` → **{'OK' if val['raios_completos'] else 'ERRO'}**
- **Existência de todos os extremos $(u, v)$ em $V$:** **{'OK' if val['extremos_validos'] else 'ERRO'}**
- **Ponto de entrada ($in\\_degree = 0, out\\_degree = 1$):** `{est['pontos_entrada']}` (Confirmado ID `0`: **{'Sim' if est['confirmado_id_zero'] else 'Não'}**)
- **Pontos com graus inesperados:** `{len(est['pontos_grau_inesperado'])}`
- **Conferência com a Tabela 1 de referência:** **{'COINCIDE EXATAMENTE' if comp['coincide_tabela_1'] else 'N/A ou Divergente'}**
            """
        )

    with col_diag2:
        st.subheader("Formulação Matemática Aplicada (A2 e A4)")
        st.markdown(
            r"""
Para cada segmento orientado $s_i = (u_i, v_i) \in E$ com extremos $P_{u_i} = (x_u, y_u, z_u)$ e $P_{v_i} = (x_v, y_v, z_v)$:

1. **Comprimento Euclidiano 3D ($\ell_i$):**
   $$\ell_i = \sqrt{(x_v - x_u)^2 + (y_v - y_u)^2 + (z_v - z_u)^2}$$

2. **Ponto Médio Tridimensional ($M_i$):**
   $$M_i = \left(\frac{x_u + x_v}{2},\; \frac{y_u + y_v}{2},\; \frac{z_u + z_v}{2}\right)$$

3. **Classificação Estrutural dos Pontos ($v \in V$) por Graus:**
   - **Entrada (Raiz):** $\text{grau}_{\text{ent}}(v) = 0 \;\wedge\; \text{grau}_{\text{saída}}(v) = 1$ (verificado $v = 0$)
   - **Bifurcação ($B$):** $\text{grau}_{\text{ent}}(v) = 1 \;\wedge\; \text{grau}_{\text{saída}}(v) = 2$
   - **Terminal ($T$):** $\text{grau}_{\text{ent}}(v) = 1 \;\wedge\; \text{grau}_{\text{saída}}(v) = 0$
   - **Identidades na árvore binária com entrada de grau 1:**
     $$|V| = 1 + B + T, \qquad |E| = |V| - 1 = B + T, \qquad B = T - 1$$
            """
        )

    with st.expander("📄 Visualizar Resumo Matemático Textual (Padrão Seção 8.2 do TP)"):
        st.code(formatar_resumo_modelo(modelo_ativo), language="text")
