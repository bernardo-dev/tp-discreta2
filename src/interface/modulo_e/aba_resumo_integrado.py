"""
Aba E1: Resumo Matemático CCO Explorer Integrado (Seção 8.2) e Testes de Aceitação.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import streamlit as st

from src.interface.cache_dados import carregar_modelo_em_cache
from src.modulo_a.modulo_a_vtk import (
    formatar_resumo_modelo,
    listar_arquivos_vtk,
)


def renderizar_aba_resumo_integrado() -> None:
    """
    Renderiza a Aba do Módulo E com o Resumo Matemático CCO Explorer (Seção 8.2)
    e o painel dos Testes Mínimos de Aceitação (T1 a T7).
    """
    st.subheader("Resumo Matemático CCO Explorer (Padrão Seção 8.2)")

    arquivos = listar_arquivos_vtk("dados_modelos3D/")
    if arquivos:
        nomes = [arq.name for arq in arquivos]
        escolhido = st.selectbox(
            "Selecione o modelo VTK para gerar o Resumo Matemático:",
            options=nomes,
            index=0,
        )
        caminho = next(arq for arq in arquivos if arq.name == escolhido)
        modelo = carregar_modelo_em_cache(str(caminho))
        st.code(formatar_resumo_modelo(modelo), language="text")
    else:
        st.warning("Nenhum arquivo VTK localizado em `dados_modelos3D/`.")

    st.divider()
    st.subheader("Checklist de Testes Mínimos de Aceitação (Seção 10.1)")
    st.markdown(
        """
- **T1 (Módulo A):** O programa processa todos os seis VTK sem alterações manuais de dados — **Implementado e Verificado**
- **T2 (Módulo A):** As quantidades de pontos, segmentos, terminais e bifurcações coincidem com a Tabela 1 — **Implementado e Verificado**
- **T3 (Módulo D):** A matriz pai–filho de `Nterm016` tem dimensões $32 \\times 32$ e o número correto de entradas iguais a 1 — *Previsto no Módulo D*
- **T4 (Módulo D):** A construção de $\\mathcal{R}^+$ para `Nterm016` produz exemplos corretos de ancestralidade indireta — *Previsto no Módulo D*
- **T5 (Módulo C):** A identidade de inclusão–exclusão fecha numericamente nos dados de `Nterm128` — *Previsto no Módulo C*
- **T6 (Módulo C):** A recorrência deduzida reproduz os seis valores observados — *Previsto no Módulo C*
- **T7 (Módulo B):** A soma das sete frequências da parte B0 é igual ao número de segmentos de `Nterm128` e a trilha B1 gera resultado conferível — *Previsto no Módulo B*
        """
    )
