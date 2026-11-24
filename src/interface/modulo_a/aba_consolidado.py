"""
Aba 2: Consolidação dos 6 Modelos (Tabela 1) — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.interface.cache_dados import obter_consolidado_em_cache
from src.modulo_a.modulo_a_vtk import gerar_tabela_consolidada


def renderizar_aba_consolidado(pasta_informada: str) -> None:
    """
    Renderiza a Aba 2 do Módulo A:
    - Tabela consolidada dos 6 arquivos VTK comparada com a Tabela 1 de referência;
    - Botão para salvar em disco (`resultados/tabela_consolidada_6_modelos.csv`);
    - Botão para download direto do CSV consolidado.
    """
    st.subheader("Consolidação dos 6 Modelos VTK vs. Tabela 1 de Referência")
    st.markdown(
        "Comparação automática de $|V|$, $|E|$, Terminais ($T$), Bifurcações ($B$) e "
        "Ponto de Entrada calculados diretamente dos 6 arquivos `.vtk` frente à Tabela 1 do enunciado."
    )

    try:
        linhas_consolidadas = obter_consolidado_em_cache(pasta_informada)
        df_consolidado = pd.DataFrame(linhas_consolidadas)

        st.dataframe(
            df_consolidado,
            width="stretch",
            hide_index=True,
        )

        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            if st.button(
                "💾 Salvar em resultados/tabela_consolidada_6_modelos.csv",
                width="stretch",
            ):
                gerar_tabela_consolidada(
                    pasta_modelos=pasta_informada,
                    caminho_saida="resultados/tabela_consolidada_6_modelos.csv",
                )
                st.success(
                    "Arquivo salvo com sucesso em `resultados/tabela_consolidada_6_modelos.csv`!"
                )

        with col_btn2:
            csv_bytes_consolidado = df_consolidado.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Baixar tabela_consolidada_6_modelos.csv",
                data=csv_bytes_consolidado,
                file_name="tabela_consolidada_6_modelos.csv",
                mime="text/csv",
                width="stretch",
            )

    except FileNotFoundError as erro_pasta:
        st.warning(
            f"Não foi possível consolidar os 6 modelos a partir de `{pasta_informada}`: {erro_pasta}"
        )
