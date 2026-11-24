"""
Funções compartilhadas de cache de dados para a interface Streamlit.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.modulo_a.modulo_a_vtk import (
    gerar_tabela_consolidada,
    processar_conteudo_vtk,
    processar_modelo_vtk,
)


@st.cache_data(show_spinner=False)
def carregar_modelo_em_cache(caminho_str: str) -> dict[str, Any]:
    """Carrega e processa um arquivo VTK do disco com cache do Streamlit."""
    return processar_modelo_vtk(caminho_str)


@st.cache_data(show_spinner=False)
def carregar_conteudo_upload_em_cache(
    conteudo: str,
    nome_arquivo: str,
) -> dict[str, Any]:
    """Processa o conteúdo de um arquivo VTK enviado via upload."""
    return processar_conteudo_vtk(conteudo, nome_arquivo=nome_arquivo)


@st.cache_data(show_spinner=False)
def obter_consolidado_em_cache(pasta_modelos: str) -> list[dict[str, Any]]:
    """Calcula a tabela consolidada dos 6 modelos VTK."""
    return gerar_tabela_consolidada(
        pasta_modelos=pasta_modelos,
        caminho_saida="resultados/tabela_consolidada_6_modelos.csv",
    )
