"""
Aba 3: Tabelas de Classes Modulares, Disjunção e Segmentos (Exportação CSV) — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from src.modulo_b.modulo_b_numeros import exportar_classes_modulares_csv


def renderizar_aba_tabelas(
    modelo_ativo: dict[str, Any],
    resultado_b0: dict[str, Any],
) -> None:
    """
    Renderiza a Aba 3 do Módulo B:
    - Tabela B0.1 das classes de congruência módulo m com estatísticas geométricas e exportação CSV;
    - Tabela B0.2 de verificação de disjunção par a par (C_j ∩ C_k = ∅);
    - Tabela interativa B0.4 de segmentos classificados por resíduo com filtro por classe e busca por ID.
    """
    m: int = int(resultado_b0["modulo_m"])
    tabela_classes: list[dict[str, Any]] = resultado_b0["tabela_classes"]
    val: dict[str, Any] = resultado_b0["validacao_particao"]
    nome_codigo: str = resultado_b0["codigo_modelo"]

    st.subheader(
        f"Tabela das Classes de Congruência Módulo {m} (B0.1) — `{modelo_ativo['arquivo']}`"
    )
    st.markdown(
        "Quantidade $|C_j|$, proporção, comprimento euclidiano 3D médio, raio médio "
        "(nas unidades originais do arquivo VTK) e os 5 primeiros identificadores de cada classe."
    )

    df_classes = pd.DataFrame(
        [
            {
                "Classe": item["classe"],
                "Resto (j)": int(item["resto_j"]),
                "Congruência": item["congruencia"],
                "Quantidade |Cⱼ|": int(item["quantidade"]),
                "Proporção (%)": round(float(item["percentual"]), 2),
                "Comprimento 3D Médio": round(float(item["comprimento_3d_medio"]), 7),
                "Raio Médio": round(float(item["raio_medio"]), 7),
                "Exemplos de IDs (5 primeiros)": item["exemplos_str"],
            }
            for item in tabela_classes
        ]
    )
    st.dataframe(df_classes, width="stretch", hide_index=True)

    nome_csv_b0 = f"b0_classes_mod{m}_{nome_codigo}.csv"
    df_csv_export = pd.DataFrame(
        [
            {
                "classe": item["classe"],
                "resto_j": item["resto_j"],
                "modulo_m": item["modulo_m"],
                "quantidade": item["quantidade"],
                "comprimento_3d_medio": f"{float(item['comprimento_3d_medio']):.7f}",
                "raio_medio": f"{float(item['raio_medio']):.7f}",
                "exemplos_ids": " ".join(str(idx) for idx in item["exemplos_ids"]),
            }
            for item in tabela_classes
        ]
    )

    col_exp1, col_exp2 = st.columns([1, 1])
    with col_exp1:
        if st.button(
            f"💾 Salvar em resultados/{nome_csv_b0}",
            width="stretch",
        ):
            caminho_salvo = exportar_classes_modulares_csv(
                resultado_b0,
                pasta_saida="resultados",
            )
            st.success(
                f"Arquivo exportado com sucesso em `{caminho_salvo.as_posix()}`!"
            )

    with col_exp2:
        csv_bytes_b0 = df_csv_export.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"⬇️ Baixar {nome_csv_b0}",
            data=csv_bytes_b0,
            file_name=nome_csv_b0,
            mime="text/csv",
            width="stretch",
        )

    st.divider()

    # Tabela de Verificação de Disjunção Par a Par (B0.2)
    st.subheader(
        f"Verificação de Disjunção Par a Par ($C_j \\cap C_k = \\varnothing$, "
        f"$\\binom{{{m}}}{{2}} = {val['num_pares_verificados']}$ pares — B0.2)"
    )
    df_pares = pd.DataFrame(
        [
            {
                "Classe Cⱼ": p["classe_j"],
                "Classe Cₖ": p["classe_k"],
                "Cardinalidade |Cⱼ ∩ Cₖ|": int(p["cardinalidade_intersecao"]),
                "Disjuntas (Cⱼ ∩ Cₖ = ∅)": "Sim" if p["disjunto"] else "Não",
            }
            for p in val["pares_verificados"]
        ]
    )
    st.dataframe(df_pares, width="stretch", hide_index=True)

    st.divider()

    # Tabela Interativa de Segmentos Classificados por Resíduo (B0.4)
    st.subheader(
        f"📍 Tabela de Segmentos por Classe de Resíduo ($|E| = {len(modelo_ativo['segmentos'])}$ — B0.4)"
    )
    df_segmentos_mod = pd.DataFrame(
        [
            {
                "id": int(s["id"]),
                "classe": f"C_{int(s['id']) % m}",
                "quociente_q": int(s["id"]) // m,
                "resto_j": int(s["id"]) % m,
                "u": s["u"],
                "v": s["v"],
                "raio": round(float(s["raio"]), 7),
                "comprimento_3d": round(float(s["comprimento_3d"]), 7),
            }
            for s in modelo_ativo["segmentos"]
        ]
    )

    col_fb1, col_fb2 = st.columns([1, 2])
    with col_fb1:
        opcoes_filtro_classe = ["Todas"] + [f"C_{j}" for j in range(m)]
        filtro_classe = st.selectbox(
            f"Filtrar por classe de resíduo (mod {m}):",
            options=opcoes_filtro_classe,
            index=0,
        )
    with col_fb2:
        busca_seg_b0 = st.text_input(
            "Pesquisar segmento por ID, extremo u ou extremo v:",
            value="",
            placeholder="Ex.: 0, 7, 14...",
        )

    df_exibido = df_segmentos_mod
    if filtro_classe != "Todas":
        df_exibido = df_exibido[df_exibido["classe"] == filtro_classe]
    if busca_seg_b0.strip():
        termo = busca_seg_b0.strip()
        mascara = (
            df_exibido["id"].astype(str).str.contains(termo, na=False)
            | df_exibido["u"].astype(str).str.contains(termo, na=False)
            | df_exibido["v"].astype(str).str.contains(termo, na=False)
        )
        df_exibido = df_exibido[mascara]

    st.dataframe(df_exibido, width="stretch", hide_index=True)
