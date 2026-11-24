"""
Aba 3: Tabela de Segmentos e Pontos (Exportação CSV) — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.modulo_a.modulo_a_vtk import (
    exportar_segmentos_csv,
    transformar_nome_do_arquivo,
)


def renderizar_aba_tabelas(modelo_ativo: dict[str, Any]) -> None:
    """
    Renderiza a Aba 3 do Módulo A:
    - Estatísticas descritivas geométricas (raio e comprimento euclidiano 3D);
    - Tabela interativa de segmentos com busca e exportação CSV;
    - Tabela interativa de pontos classificados com filtro por tipo e busca por ID.
    """
    st.subheader(
        f"Estatísticas Descritivas Geométricas — `{modelo_ativo['arquivo']}` (Unidades Originais VTK)"
    )

    stats_r = modelo_ativo["estatisticas"]["raio"]
    stats_l = modelo_ativo["estatisticas"]["comprimento_3d"]

    df_stats = pd.DataFrame(
        [
            {
                "Atributo Geométrico": "Raio (rᵢ)",
                "Quantidade |E|": int(stats_r["quantidade"]),
                "Mínimo": round(stats_r["minimo"], 7),
                "Máximo": round(stats_r["maximo"], 7),
                "Média": round(stats_r["media"], 7),
                "Mediana": round(stats_r["mediana"], 7),
                "Desvio Padrão": round(stats_r["desvio_padrao"], 7),
                "Soma Total": round(stats_r["soma"], 7),
            },
            {
                "Atributo Geométrico": "Comprimento Euclidiano 3D (lᵢ)",
                "Quantidade |E|": int(stats_l["quantidade"]),
                "Mínimo": round(stats_l["minimo"], 7),
                "Máximo": round(stats_l["maximo"], 7),
                "Média": round(stats_l["media"], 7),
                "Mediana": round(stats_l["mediana"], 7),
                "Desvio Padrão": round(stats_l["desvio_padrao"], 7),
                "Soma Total": round(stats_l["soma"], 7),
            },
        ]
    )
    st.dataframe(df_stats, width="stretch", hide_index=True)

    st.divider()

    # Tabela Interativa de Segmentos
    st.subheader(f"Tabela de Segmentos ($|E| = {len(modelo_ativo['segmentos'])}$)")
    df_segmentos = pd.DataFrame(
        [
            {
                "id": s["id"],
                "u": s["u"],
                "v": s["v"],
                "raio": round(float(s["raio"]), 7),
                "comprimento_3d": round(float(s["comprimento_3d"]), 7),
                "mx": round(float(s["mx"]), 7),
                "my": round(float(s["my"]), 7),
                "mz": round(float(s["mz"]), 7),
            }
            for s in modelo_ativo["segmentos"]
        ]
    )

    busca_seg = st.text_input(
        "Pesquisar segmento (filtra por ID do segmento, extremo u ou extremo v):",
        value="",
        placeholder="Ex.: 0, 12, 24...",
    )
    if busca_seg.strip():
        termo = busca_seg.strip()
        mascara = (
            df_segmentos["id"].astype(str).str.contains(termo, na=False)
            | df_segmentos["u"].astype(str).str.contains(termo, na=False)
            | df_segmentos["v"].astype(str).str.contains(termo, na=False)
        )
        df_segmentos_exibido = df_segmentos[mascara]
    else:
        df_segmentos_exibido = df_segmentos

    st.dataframe(df_segmentos_exibido, width="stretch", hide_index=True)

    nome_codigo = transformar_nome_do_arquivo(modelo_ativo["arquivo"])
    nome_csv_seg = f"segmentos_{nome_codigo}.csv"

    col_exp1, col_exp2 = st.columns([1, 1])
    with col_exp1:
        if st.button(
            f"💾 Salvar em resultados/{nome_csv_seg}",
            width="stretch",
        ):
            caminho_salvo = exportar_segmentos_csv(
                modelo_ativo,
                nome_modelo=nome_codigo,
                pasta_saida="resultados",
            )
            st.success(
                f"Arquivo exportado com sucesso em `{caminho_salvo.as_posix()}`!"
            )

    with col_exp2:
        csv_bytes_seg = df_segmentos.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇️ Baixar {nome_csv_seg}",
            data=csv_bytes_seg,
            file_name=nome_csv_seg,
            mime="text/csv",
            width="stretch",
        )

    st.divider()

    # Tabela Interativa de Pontos Classificados
    st.subheader(
        f"📍 Tabela de Pontos Classificados ($|V| = {len(modelo_ativo['pontos'])}$)"
    )
    df_pontos = pd.DataFrame(
        [
            {
                "id": p["id"],
                "x": round(float(p["x"]), 7),
                "y": round(float(p["y"]), 7),
                "z": round(float(p["z"]), 7),
                "in_degree": p["in_degree"],
                "out_degree": p["out_degree"],
                "grau_total": p["grau_total"],
                "tipo": p["tipo"],
            }
            for p in modelo_ativo["pontos"]
        ]
    )

    col_fp1, col_fp2 = st.columns([1, 2])
    with col_fp1:
        filtro_tipo_ponto = st.selectbox(
            "Filtrar por classificação estrutural:",
            options=["Todos", "Entrada", "Bifurcação", "Terminal", "Inesperado"],
            index=0,
        )
    with col_fp2:
        busca_ponto = st.text_input(
            "Pesquisar ponto por ID:",
            value="",
            placeholder="Ex.: 0, 6, 15...",
        )

    df_pontos_exibido = df_pontos
    if filtro_tipo_ponto != "Todos":
        df_pontos_exibido = df_pontos_exibido[
            df_pontos_exibido["tipo"] == filtro_tipo_ponto
        ]
    if busca_ponto.strip():
        df_pontos_exibido = df_pontos_exibido[
            df_pontos_exibido["id"]
            .astype(str)
            .str.contains(busca_ponto.strip(), na=False)
        ]

    st.dataframe(df_pontos_exibido, width="stretch", hide_index=True)
