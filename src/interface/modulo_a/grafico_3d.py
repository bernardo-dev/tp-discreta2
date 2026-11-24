"""
Construção do Gráfico Interativo 3D (Plotly) para Árvores Vasculares — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import numpy as np
import plotly.colors as pc
import plotly.graph_objects as go


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
    num_faixas = (
        10 if (modo_cor != "Cor única (vascular)" or espessura_proporcional) else 1
    )

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
                    marker=dict(
                        size=7, color=["#00E676", "#FFEA00"], symbol="diamond"
                    ),
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
