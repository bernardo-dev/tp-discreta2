"""
Interface Gráfica Interativa e Renderizador 3D — Módulo A (CCO Explorer).
Disciplina: BCC102 — Matemática Discreta II (UFOP)

Aplicativo Streamlit + Plotly 3D que consome estritamente o núcleo matemático
puro implementado em `src/modulo_a_vtk.py`. Todos os valores exibidos são
calculados diretamente a partir dos arquivos .vtk, nas unidades originais.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import plotly.colors as pc
import plotly.graph_objects as go
import streamlit as st

from src.modulo_a.modulo_a_vtk import (
    exportar_segmentos_csv,
    transformar_nome_do_arquivo,
    formatar_resumo_modelo,
    gerar_tabela_consolidada,
    listar_arquivos_vtk,
    processar_conteudo_vtk,
    processar_modelo_vtk,
    resolver_pasta_modelos,
)


st.set_page_config(
    page_title="CCO Explorer — Módulo A (Árvores Vasculares 3D)",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# Funções Auxiliares de Cache e Construção do Gráfico 3D (Plotly)
# ==============================================================================

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


def interpolar_cor_escala(valor_norm: float, escala: str = "Turbo") -> str:
    """
    Obtém uma cor RGB da escala contínua do Plotly para um valor normalizado
    no intervalo [0.0, 1.0].
    """
    t = max(0.0, min(1.0, float(valor_norm)))
    cor = pc.sample_colorscale(escala, [t])[0]
    return str(cor)


def construir_figura_3d(
    modelo: dict[str, Any],
    modo_cor: str,
    espessura_proporcional: bool,
    fator_espessura: float,
    mostrar_entrada: bool,
    mostrar_bifurcacoes: bool,
    mostrar_terminais: bool,
    mostrar_pontos_medios: bool,
    id_segmento_destaque: int | None,
) -> go.Figure:
    """
    Constrói a figura interativa 3D usando `go.Scatter3d` com agrupamento de
    segmentos em faixas discretas (usando separadores `None`) para manter alta
    fluidez mesmo em modelos com 1023 segmentos (Nterm512).
    """
    pontos: list[dict[str, Any]] = modelo["pontos"]
    segmentos: list[dict[str, Any]] = modelo["segmentos"]

    fig = go.Figure()

    if not segmentos or not pontos:
        return fig

    # Extração de métricas para normalização de cor e espessura
    raios = np.array([float(s["raio"]) for s in segmentos], dtype=float)
    comprimentos = np.array(
        [float(s["comprimento_3d"]) for s in segmentos], dtype=float
    )

    r_min, r_max = float(np.min(raios)), float(np.max(raios))
    l_min, l_max = float(np.min(comprimentos)), float(np.max(comprimentos))
    amplitude_r = (r_max - r_min) if (r_max - r_min) > 1e-12 else 1.0
    amplitude_l = (l_max - l_min) if (l_max - l_min) > 1e-12 else 1.0

    # Seleção do critério de agrupamento em faixas (bins) para performance WebGL
    num_faixas = 10 if (modo_cor != "Cor única (vascular)" or espessura_proporcional) else 1

    if modo_cor == "Comprimento 3D":
        valores_cor = comprimentos
        v_min_cor, amp_cor = l_min, amplitude_l
        nome_escala = "Viridis"
        titulo_barra_cor = "Comprimento 3D (u.o.)"
    else:
        valores_cor = raios
        v_min_cor, amp_cor = r_min, amplitude_r
        nome_escala = "Plasma"
        titulo_barra_cor = "Raio (u.o.)"

    # Normalização em [0, 1] para cor e para espessura
    norm_cor = (valores_cor - v_min_cor) / amp_cor
    norm_raio = (raios - r_min) / amplitude_r

    if num_faixas == 1:
        indices_faixa = np.zeros(len(segmentos), dtype=int)
    else:
        # Se a cor depende de comprimento ou raio, agrupa pelo critério ativo
        criterio_bin = norm_cor if modo_cor != "Cor única (vascular)" else norm_raio
        indices_faixa = np.clip(
            (criterio_bin * (num_faixas - 1)).astype(int), 0, num_faixas - 1
        )

    # Desenho agrupado dos segmentos vasculares por faixa (com separador None)
    for faixa in range(num_faixas):
        xs: list[float | None] = []
        ys: list[float | None] = []
        zs: list[float | None] = []
        textos_hover: list[str] = []
        raios_faixa: list[float] = []
        cores_norm_faixa: list[float] = []

        for idx_s, seg in enumerate(segmentos):
            if int(indices_faixa[idx_s]) != faixa:
                continue

            coord_u = seg.get("coord_u")
            coord_v = seg.get("coord_v")
            if coord_u is None or coord_v is None:
                continue

            xu, yu, zu = coord_u
            xv, yv, zv = coord_v
            xs.extend([xu, xv, None])
            ys.extend([yu, yv, None])
            zs.extend([zu, zv, None])

            info_seg = (
                f"<b>Segmento s<sub>{seg['id']}</sub></b><br>"
                f"Par orientado (u, v): ({seg['u']}, {seg['v']})<br>"
                f"Raio r<sub>{seg['id']}</sub>: {seg['raio']:.6f}<br>"
                f"Comprimento 3D l<sub>{seg['id']}</sub>: {seg['comprimento_3d']:.6f}<br>"
                f"Ponto médio M<sub>{seg['id']}</sub>: "
                f"({seg['mx']:.5f}, {seg['my']:.5f}, {seg['mz']:.5f})"
            )
            textos_hover.extend([info_seg, info_seg, ""])
            raios_faixa.append(float(norm_raio[idx_s]))
            cores_norm_faixa.append(float(norm_cor[idx_s]))

        if not xs:
            continue

        media_norm_r = float(np.mean(raios_faixa))
        media_norm_c = float(np.mean(cores_norm_faixa))

        if espessura_proporcional:
            largura_linha = max(1.5, (2.0 + 9.0 * media_norm_r) * fator_espessura)
        else:
            largura_linha = max(1.5, 4.0 * fator_espessura)

        if modo_cor == "Cor única (vascular)":
            cor_linha = "#D32F2F"
        else:
            cor_linha = interpolar_cor_escala(media_norm_c, nome_escala)

        fig.add_trace(
            go.Scatter3d(
                x=xs,
                y=ys,
                z=zs,
                mode="lines",
                name="Segmentos Vasculares" if faixa == 0 else f"Faixa {faixa + 1}",
                legendgroup="segmentos",
                showlegend=(faixa == 0),
                line=dict(color=cor_linha, width=largura_linha),
                text=textos_hover,
                hovertemplate="%{text}<extra></extra>",
                opacity=0.88 if id_segmento_destaque is None else 0.32,
            )
        )

    # Barra de cores contínua quando colorido por Raio ou Comprimento 3D
    if modo_cor != "Cor única (vascular)":
        fig.add_trace(
            go.Scatter3d(
                x=[segmentos[0]["mx"]],
                y=[segmentos[0]["my"]],
                z=[segmentos[0]["mz"]],
                mode="markers",
                name=titulo_barra_cor,
                showlegend=False,
                hoverinfo="skip",
                marker=dict(
                    size=0.001,
                    opacity=0.0,
                    color=[float(np.min(valores_cor)), float(np.max(valores_cor))],
                    colorscale=nome_escala,
                    showscale=True,
                    colorbar=dict(
                        title=dict(text=titulo_barra_cor, side="right"),
                        thickness=14,
                        len=0.68,
                        x=1.02,
                    ),
                ),
            )
        )

    # Camada de Pontos Médios M_i (com tooltips completos de segmento)
    if mostrar_pontos_medios:
        mx_lista = [float(s["mx"]) for s in segmentos if s.get("mx") is not None]
        my_lista = [float(s["my"]) for s in segmentos if s.get("my") is not None]
        mz_lista = [float(s["mz"]) for s in segmentos if s.get("mz") is not None]
        textos_medios = [
            (
                f"<b>Ponto Médio M<sub>{s['id']}</sub> (Segmento {s['id']})</b><br>"
                f"Extremos orientados (u, v): ({s['u']}, {s['v']})<br>"
                f"Coordenadas M<sub>{s['id']}</sub>: "
                f"({s['mx']:.6f}, {s['my']:.6f}, {s['mz']:.6f})<br>"
                f"Raio r<sub>{s['id']}</sub>: {s['raio']:.6f}<br>"
                f"Comprimento 3D l<sub>{s['id']}</sub>: {s['comprimento_3d']:.6f}"
            )
            for s in segmentos
            if s.get("mx") is not None
        ]
        fig.add_trace(
            go.Scatter3d(
                x=mx_lista,
                y=my_lista,
                z=mz_lista,
                mode="markers",
                name="Pontos Médios (Mᵢ)",
                marker=dict(
                    size=3.2,
                    color="#CE93D8",
                    symbol="cross",
                    opacity=0.85,
                ),
                text=textos_medios,
                hovertemplate="%{text}<extra></extra>",
            )
        )

    # Função interna para adicionar camada de pontos estruturais classificados
    def adicionar_camada_pontos(
        tipo_filtro: str,
        nome_legenda: str,
        cor_marcador: str,
        simbolo_marcador: str,
        tamanho_marcador: float,
    ) -> None:
        pts_filtrados = [p for p in pontos if p.get("tipo") == tipo_filtro]
        if not pts_filtrados:
            return

        px = [float(p["x"]) for p in pts_filtrados]
        py = [float(p["y"]) for p in pts_filtrados]
        pz = [float(p["z"]) for p in pts_filtrados]
        textos_pts = [
            (
                f"<b>Ponto P<sub>{p['id']}</sub> ({p['tipo']})</b><br>"
                f"ID do ponto: {p['id']}<br>"
                f"Coordenadas (x, y, z): ({p['x']:.6f}, {p['y']:.6f}, {p['z']:.6f})<br>"
                f"Grau de entrada (in_degree): {p['in_degree']}<br>"
                f"Grau de saída (out_degree): {p['out_degree']}<br>"
                f"Classificação estrutural: {p['tipo']}"
            )
            for p in pts_filtrados
        ]
        fig.add_trace(
            go.Scatter3d(
                x=px,
                y=py,
                z=pz,
                mode="markers",
                name=f"{nome_legenda} ({len(pts_filtrados)})",
                marker=dict(
                    size=tamanho_marcador,
                    color=cor_marcador,
                    symbol=simbolo_marcador,
                    line=dict(color="#111827", width=1),
                    opacity=0.96,
                ),
                text=textos_pts,
                hovertemplate="%{text}<extra></extra>",
            )
        )

    if mostrar_entrada:
        adicionar_camada_pontos(
            tipo_filtro="Entrada",
            nome_legenda="Ponto de Entrada (ID 0)",
            cor_marcador="#00E676",
            simbolo_marcador="diamond",
            tamanho_marcador=9.0,
        )

    if mostrar_bifurcacoes:
        adicionar_camada_pontos(
            tipo_filtro="Bifurcação",
            nome_legenda="Bifurcações (B)",
            cor_marcador="#FF9100",
            simbolo_marcador="circle",
            tamanho_marcador=4.5,
        )

    if mostrar_terminais:
        adicionar_camada_pontos(
            tipo_filtro="Terminal",
            nome_legenda="Terminais (T)",
            cor_marcador="#2979FF",
            simbolo_marcador="circle",
            tamanho_marcador=5.2,
        )

    # Caso existam pontos com grau inesperado, sempre destacá-los em magenta
    adicionar_camada_pontos(
        tipo_filtro="Inesperado",
        nome_legenda="Grau Inesperado",
        cor_marcador="#FF00FF",
        simbolo_marcador="x",
        tamanho_marcador=8.0,
    )

    # Destaque opcional de um segmento específico s_i pelo seu ID
    if id_segmento_destaque is not None and 0 <= id_segmento_destaque < len(segmentos):
        seg_d = segmentos[id_segmento_destaque]
        cu = seg_d.get("coord_u")
        cv = seg_d.get("coord_v")
        if cu is not None and cv is not None:
            xu, yu, zu = cu
            xv, yv, zv = cv
            mx, my, mz = seg_d["mx"], seg_d["my"], seg_d["mz"]

            texto_destaque = (
                f"<b>★ SEGMENTO DESTACADO s<sub>{seg_d['id']}</sub></b><br>"
                f"Extremos orientados: u={seg_d['u']} → v={seg_d['v']}<br>"
                f"Raio r<sub>{seg_d['id']}</sub>: {seg_d['raio']:.6f}<br>"
                f"Comprimento 3D l<sub>{seg_d['id']}</sub>: {seg_d['comprimento_3d']:.6f}<br>"
                f"Ponto médio M<sub>{seg_d['id']}</sub>: ({mx:.6f}, {my:.6f}, {mz:.6f})"
            )

            fig.add_trace(
                go.Scatter3d(
                    x=[xu, xv],
                    y=[yu, yv],
                    z=[zu, zv],
                    mode="lines+markers",
                    name=f"★ Segmento s_{seg_d['id']} ({seg_d['u']}→{seg_d['v']})",
                    line=dict(color="#00E5FF", width=11),
                    marker=dict(size=7, color=["#00E676", "#FFEA00"], symbol="diamond"),
                    text=[
                        f"<b>Extremo proximal u={seg_d['u']}</b><br>({xu:.6f}, {yu:.6f}, {zu:.6f})<br>{texto_destaque}",
                        f"<b>Extremo distal v={seg_d['v']}</b><br>({xv:.6f}, {yv:.6f}, {zv:.6f})<br>{texto_destaque}",
                    ],
                    hovertemplate="%{text}<extra></extra>",
                )
            )

            fig.add_trace(
                go.Scatter3d(
                    x=[mx],
                    y=[my],
                    z=[mz],
                    mode="markers",
                    name=f"★ Ponto Médio M_{seg_d['id']}",
                    marker=dict(
                        size=8,
                        color="#FF1744",
                        symbol="diamond-open",
                        line=dict(width=3, color="#FF1744"),
                    ),
                    text=[texto_destaque],
                    hovertemplate="%{text}<extra></extra>",
                )
            )

    fig.update_layout(
        margin=dict(l=0, r=0, t=36, b=0),
        height=650,
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0.0,
            bgcolor="rgba(17, 24, 39, 0.75)",
            font=dict(color="#F9FAFB", size=12),
        ),
        scene=dict(
            aspectmode="data",
            xaxis=dict(
                title="X (unidades originais VTK)",
                backgroundcolor="rgb(15, 23, 42)",
                gridcolor="rgb(51, 65, 85)",
                showbackground=True,
                zerolinecolor="rgb(100, 116, 139)",
            ),
            yaxis=dict(
                title="Y (unidades originais VTK)",
                backgroundcolor="rgb(15, 23, 42)",
                gridcolor="rgb(51, 65, 85)",
                showbackground=True,
                zerolinecolor="rgb(100, 116, 139)",
            ),
            zaxis=dict(
                title="Z (unidades originais VTK)",
                backgroundcolor="rgb(15, 23, 42)",
                gridcolor="rgb(51, 65, 85)",
                showbackground=True,
                zerolinecolor="rgb(100, 116, 139)",
            ),
            camera=dict(
                eye=dict(x=1.45, y=1.45, z=1.15),
            ),
        ),
    )

    return fig


# ==============================================================================
# Interface Principal Streamlit
# ==============================================================================

def main() -> None:
    st.title("🫀 CCO Explorer — Módulo A: Modelagem Discreta e Geometria 3D")
    st.caption(
        "BCC102 — Matemática Discreta II (UFOP) | "
        "Leitura VTK, Geometria Euclidiana 3D, Validação Estrutural e Identificação de Pontos "
        "(unidades originais do VTK)"
    )

    # --------------------------------------------------------------------------
    # Barra Lateral (Controles)
    # --------------------------------------------------------------------------
    with st.sidebar:
        st.header("⚙️ Fonte de Dados VTK")
        pasta_informada = st.text_input(
            "Pasta dos modelos VTK:",
            value="dados_modelos3D/",
            help="Informe o caminho relativo da pasta contendo os 6 arquivos .vtk.",
        )

        pasta_resolvida = resolver_pasta_modelos(pasta_informada)
        arquivos_encontrados = listar_arquivos_vtk(pasta_informada)

        if pasta_resolvida.exists() and str(pasta_resolvida) != pasta_informada.rstrip("/\\"):
            st.caption(f"📂 Diretório localizado: `{pasta_resolvida.as_posix()}`")

        arquivo_upload = st.file_uploader(
            "Ou envie um arquivo .vtk avulso:",
            type=["vtk"],
            help="Carregue um arquivo .vtk do seu computador para inspeção rápida.",
        )

        usar_upload = False
        if arquivo_upload is not None:
            usar_upload = st.checkbox(
                f"Usar arquivo enviado ({arquivo_upload.name})",
                value=True,
            )

        modelo_ativo: dict[str, Any] | None = None

        if usar_upload and arquivo_upload is not None:
            conteudo_str = arquivo_upload.getvalue().decode("utf-8", errors="replace")
            modelo_ativo = carregar_conteudo_upload_em_cache(
                conteudo_str, arquivo_upload.name
            )
            st.success(f"Modelo carregado via upload: `{arquivo_upload.name}`")
        else:
            if not arquivos_encontrados:
                st.error(
                    f"Nenhum arquivo `.vtk` encontrado em `{pasta_informada}`. "
                    "Verifique o caminho ou faça upload de um arquivo `.vtk`."
                )
                st.stop()

            nomes_opcoes = [arq.name for arq in arquivos_encontrados]
            indice_padrao = (
                nomes_opcoes.index("tree3D_Nterm128.vtk")
                if "tree3D_Nterm128.vtk" in nomes_opcoes
                else 0
            )
            nome_escolhido = st.selectbox(
                "Modelo VTK ativo:",
                options=nomes_opcoes,
                index=indice_padrao,
            )
            caminho_escolhido = next(
                arq for arq in arquivos_encontrados if arq.name == nome_escolhido
            )
            modelo_ativo = carregar_modelo_em_cache(str(caminho_escolhido))

        st.divider()
        st.header("🎨 Opções do Renderizador 3D")

        modo_cor = st.selectbox(
            "Colorir segmentos por:",
            options=[
                "Raio",
                "Comprimento 3D",
                "Cor única (vascular)",
            ],
            index=0,
        )

        espessura_proporcional = st.checkbox(
            "Espessura proporcional ao raio",
            value=True,
            help="Ajusta a largura visual de cada segmento proporcionalmente ao raio r_i.",
        )
        fator_espessura = st.slider(
            "Escala visual de espessura:",
            min_value=0.4,
            max_value=2.5,
            value=1.0,
            step=0.1,
        )

        st.subheader("Camadas Estruturais Visíveis")
        mostrar_entrada = st.checkbox("Ponto de entrada (ID 0)", value=True)
        mostrar_bifurcacoes = st.checkbox("Bifurcações (B)", value=True)
        mostrar_terminais = st.checkbox("Terminais (T)", value=True)
        mostrar_pontos_medios = st.checkbox("Pontos Médios (Mᵢ)", value=False)

        st.divider()
        st.subheader("🔍 Destacar Segmento por ID")
        total_seg = len(modelo_ativo["segmentos"])
        ativar_destaque = st.checkbox(
            "Filtrar/destacar um segmento específico (sᵢ)",
            value=False,
        )
        id_segmento_destaque: int | None = None
        if ativar_destaque and total_seg > 0:
            id_segmento_destaque = int(
                st.number_input(
                    f"ID do segmento i (0 a {total_seg - 1}):",
                    min_value=0,
                    max_value=max(0, total_seg - 1),
                    value=0,
                    step=1,
                )
            )

    # --------------------------------------------------------------------------
    # Cartões Superiores de Métricas (|V|, |E|, T, B, Entrada, Validação A3)
    # --------------------------------------------------------------------------
    est = modelo_ativo["estrutura"]
    val = modelo_ativo["validacao"]
    comp = modelo_ativo["comparacao_tabela_1"]

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        delta_v = (
            f"Ref Tab.1: {comp['V_esperado']}"
            if comp["possui_referencia"]
            else "Modelo avulso"
        )
        st.metric("Pontos |V|", f"{est['num_pontos_V']}", delta_v)

    with col2:
        delta_e = (
            f"Ref Tab.1: {comp['E_esperado']}"
            if comp["possui_referencia"]
            else "|V| - 1"
        )
        st.metric("Segmentos |E|", f"{est['num_segmentos_E']}", delta_e)

    with col3:
        delta_t = (
            f"Ref Tab.1: {comp['T_esperado']}"
            if comp["possui_referencia"]
            else "out_degree = 0"
        )
        st.metric("Terminais (T)", f"{est['num_terminais_T']}", delta_t)

    with col4:
        delta_b = (
            f"Ref Tab.1: {comp['B_esperado']}"
            if comp["possui_referencia"]
            else "out_degree = 2"
        )
        st.metric("Bifurcações (B)", f"{est['num_bifurcacoes_B']}", delta_b)

    with col5:
        id_ent = est["ponto_entrada_id"]
        texto_ent = f"ID {id_ent}" if id_ent is not None else "N/D"
        delta_ent = (
            "Confirmado ID 0"
            if est["confirmado_id_zero"]
            else "Atenção: ID != 0"
        )
        st.metric("Ponto de Entrada", texto_ent, delta_ent)

    with col6:
        status_a3 = val["status"]
        delta_a3 = (
            "100% Consistente"
            if val["valido"]
            else f"{len(val['inconsistencias'])} erro(s)"
        )
        st.metric(
            "Validação A3",
            status_a3,
            delta_a3,
            delta_color="normal" if val["valido"] else "inverse",
        )

    # --------------------------------------------------------------------------
    # Abas Principais de Análise
    # --------------------------------------------------------------------------
    aba_3d, aba_consolidado, aba_tabelas = st.tabs(
        [
            "Renderizador 3D & Diagnóstico Estrutural",
            "Consolidação dos 6 Modelos (Tabela 1)",
            "Tabela de Segmentos e Pontos (Exportação CSV)",
        ]
    )

    # ==========================================================================
    # ABA 1: Renderizador 3D e Diagnóstico Estrutural
    # ==========================================================================
    with aba_3d:
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
            modo_cor=modo_cor,
            espessura_proporcional=espessura_proporcional,
            fator_espessura=fator_espessura,
            mostrar_entrada=mostrar_entrada,
            mostrar_bifurcacoes=mostrar_bifurcacoes,
            mostrar_terminais=mostrar_terminais,
            mostrar_pontos_medios=mostrar_pontos_medios,
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

    # ==========================================================================
    # ABA 2: Consolidação dos 6 Modelos
    # ==========================================================================
    with aba_consolidado:
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

    # ==========================================================================
    # ABA 3: Tabela de Segmentos e Pontos + Estatísticas Descritivas
    # ==========================================================================
    with aba_tabelas:
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
                st.success(f"Arquivo exportado com sucesso em `{caminho_salvo.as_posix()}`!")

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
        st.subheader(f"📍 Tabela de Pontos Classificados ($|V| = {len(modelo_ativo['pontos'])}$)")
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


if __name__ == "__main__":
    main()
