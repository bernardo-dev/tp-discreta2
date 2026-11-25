"""
Construção do Gráfico Interativo 3D e Gráficos Modulares (Plotly) — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import numpy as np
import plotly.graph_objects as go

# Paleta de cores vivas e distintas para as classes C_0 a C_{m-1}
PALETA_CLASSES_MODULARES: tuple[str, ...] = (
    "#00E5FF",  # C_0 - Ciano vivo
    "#FF9100",  # C_1 - Laranja vivo
    "#00E676",  # C_2 - Verde esmeralda
    "#FF4081",  # C_3 - Rosa/Magenta vivo
    "#AA00FF",  # C_4 - Roxo intenso
    "#FFEA00",  # C_5 - Amarelo ouro
    "#2979FF",  # C_6 - Azul royal
    "#FF1744",
    "#1DE9B6",
    "#C6FF00",
)


def obter_cor_classe(resto_j: int) -> str:
    """Retorna uma cor viva consistente para a classe de resíduo C_j."""
    return PALETA_CLASSES_MODULARES[int(resto_j) % len(PALETA_CLASSES_MODULARES)]


def construir_figura_3d_classe_modular(
    modelo_a: dict[str, Any],
    resultado_b0: dict[str, Any],
    resto_destaque: int,
    colorir_todas_classes: bool = False,
    espessura_proporcional: bool = True,
    fator_espessura: float = 1.0,
    mostrar_pontos_medios: bool = True,
    mostrar_entrada: bool = True,
) -> go.Figure:
    """
    Constrói a figura interativa 3D usando `go.Scatter3d` para o Consultor B0.4:
    - Destaca os segmentos da classe selecionada C_j = {i : i ≡ j (mod m)} em cor
      viva sobre o restante da árvore vascular translúcida;
    - Evidencia visualmente que a seleção modular espalha-se por toda a árvore
      conforme a ordem de indexação de `LINES` e não isola uma região anatômica única.
    """
    segmentos: list[dict[str, Any]] = modelo_a["segmentos"]
    pontos: list[dict[str, Any]] = modelo_a["pontos"]
    m = int(resultado_b0["modulo_m"])

    fig = go.Figure()
    if not segmentos or not pontos:
        return fig

    raios = np.array([float(s["raio"]) for s in segmentos], dtype=float)
    r_min, r_max = float(np.min(raios)), float(np.max(raios))
    amp_r = (r_max - r_min) if (r_max - r_min) > 1e-12 else 1.0

    if not colorir_todas_classes:
        # 1. Camada de fundo: restante da árvore vascular translúcida (i not≡ j mod m)
        xs_bg: list[float | None] = []
        ys_bg: list[float | None] = []
        zs_bg: list[float | None] = []
        hover_bg: list[str] = []

        for seg in segmentos:
            seg_id = int(seg["id"])
            if (seg_id % m) == resto_destaque:
                continue
            cu = seg.get("coord_u")
            cv = seg.get("coord_v")
            if cu is None or cv is None:
                continue

            xs_bg.extend([cu[0], cv[0], None])
            ys_bg.extend([cu[1], cv[1], None])
            zs_bg.extend([cu[2], cv[2], None])
            txt = (
                f"<b>Segmento s<sub>{seg_id}</sub> (Classe C<sub>{seg_id % m}</sub>)</b><br>"
                f"Resto: {seg_id} mod {m} = {seg_id % m}<br>"
                f"Extremos (u, v): ({seg['u']}, {seg['v']})<br>"
                f"Raio: {seg['raio']:.6f} | Comp. 3D: {seg['comprimento_3d']:.6f}"
            )
            hover_bg.extend([txt, txt, ""])

        if xs_bg:
            fig.add_trace(
                go.Scatter3d(
                    x=xs_bg,
                    y=ys_bg,
                    z=zs_bg,
                    mode="lines",
                    name=f"Demais classes (i ≢ {resto_destaque} mod {m})",
                    line=dict(
                        color="rgba(148, 163, 184, 0.35)",
                        width=max(1.5, 2.6 * fator_espessura),
                    ),
                    text=hover_bg,
                    hovertemplate="%{text}<extra></extra>",
                    opacity=0.28,
                )
            )

        # 2. Camada em destaque vivo: segmentos da classe C_j selecionada
        cor_destaque = obter_cor_classe(resto_destaque)
        consulta_j = resultado_b0["consultas_por_residuo"][resto_destaque]
        segs_classe = consulta_j["segmentos"]

        num_faixas = 3 if espessura_proporcional and len(segs_classe) > 3 else 1
        for faixa in range(num_faixas):
            xs_fg: list[float | None] = []
            ys_fg: list[float | None] = []
            zs_fg: list[float | None] = []
            hover_fg: list[str] = []
            norm_raios_faixa: list[float] = []

            for seg in segs_classe:
                norm_r = (float(seg["raio"]) - r_min) / amp_r
                idx_faixa = min(num_faixas - 1, int(norm_r * num_faixas))
                if idx_faixa != faixa:
                    continue

                cu = seg.get("coord_u")
                cv = seg.get("coord_v")
                if cu is None or cv is None:
                    continue

                seg_id = int(seg["id"])
                quociente_q = seg_id // m
                xs_fg.extend([cu[0], cv[0], None])
                ys_fg.extend([cu[1], cv[1], None])
                zs_fg.extend([cu[2], cv[2], None])

                txt = (
                    f"<b>★ Classe C<sub>{resto_destaque}</sub> — Segmento s<sub>{seg_id}</sub></b><br>"
                    f"Divisão Euclidiana: {seg_id} = {m}×{quociente_q} + {resto_destaque} "
                    f"(i ≡ {resto_destaque} mod {m})<br>"
                    f"Extremos orientados: ({seg['u']} → {seg['v']})<br>"
                    f"Raio r<sub>{seg_id}</sub>: {seg['raio']:.6f}<br>"
                    f"Comprimento 3D l<sub>{seg_id}</sub>: {seg['comprimento_3d']:.6f}"
                )
                hover_fg.extend([txt, txt, ""])
                norm_raios_faixa.append(norm_r)

            if not xs_fg:
                continue

            media_nr = float(np.mean(norm_raios_faixa))
            largura_fg = (
                max(4.5, (5.0 + 7.0 * media_nr) * fator_espessura)
                if espessura_proporcional
                else max(5.0, 7.5 * fator_espessura)
            )

            fig.add_trace(
                go.Scatter3d(
                    x=xs_fg,
                    y=ys_fg,
                    z=zs_fg,
                    mode="lines",
                    name=(
                        f"★ Classe C_{resto_destaque}: i ≡ {resto_destaque} (mod {m}) "
                        f"[|C_{resto_destaque}| = {len(segs_classe)}]"
                    ),
                    legendgroup=f"classe_{resto_destaque}",
                    showlegend=(faixa == 0),
                    line=dict(color=cor_destaque, width=largura_fg),
                    text=hover_fg,
                    hovertemplate="%{text}<extra></extra>",
                    opacity=1.0,
                )
            )

        # 3. Pontos médios M_i dos segmentos da classe C_j destacada
        if mostrar_pontos_medios and segs_classe:
            mx_fg = [float(s["mx"]) for s in segs_classe if s.get("mx") is not None]
            my_fg = [float(s["my"]) for s in segs_classe if s.get("my") is not None]
            mz_fg = [float(s["mz"]) for s in segs_classe if s.get("mz") is not None]
            hover_m = [
                (
                    f"<b>Ponto Médio M<sub>{s['id']}</sub> (Classe C<sub>{resto_destaque}</sub>)</b><br>"
                    f"ID do segmento: i = {s['id']} ({s['id']} mod {m} = {resto_destaque})<br>"
                    f"Coordenadas: ({s['mx']:.5f}, {s['my']:.5f}, {s['mz']:.5f})"
                )
                for s in segs_classe
                if s.get("mx") is not None
            ]
            fig.add_trace(
                go.Scatter3d(
                    x=mx_fg,
                    y=my_fg,
                    z=mz_fg,
                    mode="markers",
                    name=f"Pontos Médios (Mᵢ de C_{resto_destaque})",
                    marker=dict(
                        size=4.5,
                        color=cor_destaque,
                        symbol="diamond",
                        line=dict(color="#0F172A", width=1),
                    ),
                    text=hover_m,
                    hovertemplate="%{text}<extra></extra>",
                )
            )
    else:
        # Modo alternativo: colorir todas as m classes simultaneamente
        for j in range(m):
            consulta_j = resultado_b0["consultas_por_residuo"][j]
            segs_j = consulta_j["segmentos"]
            cor_j = obter_cor_classe(j)

            xs_j: list[float | None] = []
            ys_j: list[float | None] = []
            zs_j: list[float | None] = []
            hover_j: list[str] = []

            for seg in segs_j:
                cu = seg.get("coord_u")
                cv = seg.get("coord_v")
                if cu is None or cv is None:
                    continue
                seg_id = int(seg["id"])
                xs_j.extend([cu[0], cv[0], None])
                ys_j.extend([cu[1], cv[1], None])
                zs_j.extend([cu[2], cv[2], None])
                txt = (
                    f"<b>Classe C<sub>{j}</sub> — Segmento s<sub>{seg_id}</sub></b><br>"
                    f"Congruência: {seg_id} ≡ {j} (mod {m})<br>"
                    f"Raio: {seg['raio']:.6f} | Comp. 3D: {seg['comprimento_3d']:.6f}"
                )
                hover_j.extend([txt, txt, ""])

            if not xs_j:
                continue

            em_destaque = j == resto_destaque
            fig.add_trace(
                go.Scatter3d(
                    x=xs_j,
                    y=ys_j,
                    z=zs_j,
                    mode="lines",
                    name=f"{'★ ' if em_destaque else ''}C_{j} (|C_{j}|={len(segs_j)})",
                    line=dict(
                        color=cor_j,
                        width=(7.5 if em_destaque else 3.8) * fator_espessura,
                    ),
                    text=hover_j,
                    hovertemplate="%{text}<extra></extra>",
                    opacity=1.0 if em_destaque else 0.72,
                )
            )

    # Ponto de Entrada (ID 0) para referência espacial da raiz da árvore
    if mostrar_entrada:
        pts_entrada = [p for p in pontos if p.get("tipo") == "Entrada"]
        if pts_entrada:
            p0 = pts_entrada[0]
            fig.add_trace(
                go.Scatter3d(
                    x=[float(p0["x"])],
                    y=[float(p0["y"])],
                    z=[float(p0["z"])],
                    mode="markers",
                    name="Ponto de Entrada (ID 0)",
                    marker=dict(
                        size=8.5,
                        color="#00E676",
                        symbol="diamond",
                        line=dict(color="#111827", width=1.5),
                    ),
                    text=[
                        f"<b>Ponto de Entrada P₀</b><br>"
                        f"Coordenadas: ({p0['x']:.6f}, {p0['y']:.6f}, {p0['z']:.6f})"
                    ],
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


def construir_grafico_distribuicao_pcp(resultado_b0: dict[str, Any]) -> go.Figure:
    """
    Constrói o gráfico de barras (Plotly) da distribuição de |C_j| para
    C_0 ... C_{m-1} com uma linha horizontal tracejada em y = ceil(|E|/m)
    rotulada como 'Limite Inferior do PCP (⌈255/7⌉ = 37)'.
    """
    tabela: list[dict[str, Any]] = resultado_b0["tabela_classes"]
    pcp: dict[str, Any] = resultado_b0["casa_dos_pombos"]
    n_pombos = int(pcp["pombos_N"])
    m = int(pcp["gavetas_m"])
    limite_pcp = int(pcp["limite_inferior_pcp"])

    rotulos_x = [f"{item['classe']} (j={item['resto_j']})" for item in tabela]
    quantidades = [int(item["quantidade"]) for item in tabela]

    cores_barras = [
        "#00B8D4" if int(item["quantidade"]) >= limite_pcp else "#5C6BC0"
        for item in tabela
    ]
    textos_hover = [
        (
            f"<b>Classe {item['classe']} — {item['congruencia']}</b><br>"
            f"Quantidade |{item['classe']}|: <b>{item['quantidade']}</b> segmentos "
            f"({item['percentual']:.2f}%)<br>"
            f"Limite inferior PCP: ⌈{n_pombos}/{m}⌉ = {limite_pcp}<br>"
            f"Status PCP: {'Atinge/supera o limite (≥ ' + str(limite_pcp) + ')' if item['quantidade'] >= limite_pcp else 'Abaixo do teto (' + str(item['quantidade']) + ')'}<br>"
            f"Exemplos de IDs: [{item['exemplos_str']}]"
        )
        for item in tabela
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=rotulos_x,
            y=quantidades,
            name="Cardinalidade |Cⱼ|",
            marker=dict(
                color=cores_barras,
                line=dict(color="#E2E8F0", width=1.2),
            ),
            text=[str(q) for q in quantidades],
            textposition="outside",
            hovertext=textos_hover,
            hovertemplate="%{hovertext}<extra></extra>",
        )
    )

    rotulo_linha_pcp = f"Limite Inferior do PCP (⌈{n_pombos}/{m}⌉ = {limite_pcp})"
    fig.add_hline(
        y=limite_pcp,
        line_dash="dash",
        line_color="#FF5252",
        line_width=2.5,
        annotation_text=rotulo_linha_pcp,
        annotation_position="top right",
        annotation_font=dict(color="#FF5252", size=13),
    )

    max_y = max(quantidades + [limite_pcp, 1])
    min_y = max(0, min(quantidades) - 6) if quantidades else 0

    fig.update_layout(
        title=dict(
            text=(
                f"Distribuição de Segmentos por Classe de Resíduo Módulo {m} "
                f"(|E| = {n_pombos})"
            ),
            font=dict(size=16),
        ),
        xaxis_title=f"Classes de Congruência Cⱼ = {{i : i ≡ j (mod {m})}}",
        yaxis_title="Quantidade de Segmentos (|Cⱼ|)",
        yaxis=dict(range=[min_y, max_y + 4]),
        margin=dict(l=20, r=20, t=55, b=30),
        height=390,
        showlegend=False,
    )

    return fig


def construir_graficos_comparativos_geometria(
    resultado_b0: dict[str, Any],
) -> tuple[go.Figure, go.Figure]:
    """
    Constrói dois gráficos de barras comparativos simples (Plotly):
    1. Comprimento 3D médio por classe C_j;
    2. Raio médio por classe C_j.
    Inclui linha tracejada com a média global do modelo para evidenciar que
    as classes oscilam em torno da média global sem especialização anatômica.
    """
    tabela: list[dict[str, Any]] = resultado_b0["tabela_classes"]
    modelo_a: dict[str, Any] | None = resultado_b0.get("modelo_a")

    rotulos_x = [item["classe"] for item in tabela]
    comp_medios = [float(item["comprimento_3d_medio"]) for item in tabela]
    raios_medios = [float(item["raio_medio"]) for item in tabela]
    cores = [obter_cor_classe(int(item["resto_j"])) for item in tabela]

    if modelo_a is not None:
        media_global_comp = float(
            modelo_a["estatisticas"]["comprimento_3d"]["media"]
        )
        media_global_raio = float(modelo_a["estatisticas"]["raio"]["media"])
    else:
        media_global_comp = float(np.mean(comp_medios)) if comp_medios else 0.0
        media_global_raio = float(np.mean(raios_medios)) if raios_medios else 0.0

    # 1. Figura do Comprimento 3D Médio por Classe
    fig_comp = go.Figure()
    fig_comp.add_trace(
        go.Bar(
            x=rotulos_x,
            y=comp_medios,
            name="Comprimento 3D Médio",
            marker=dict(color=cores, line=dict(color="#1E293B", width=1)),
            text=[f"{v:.5f}" for v in comp_medios],
            textposition="outside",
            hovertemplate=(
                "<b>Classe %{x}</b><br>"
                "Comprimento 3D médio: %{y:.7f} (u.o. VTK)<extra></extra>"
            ),
        )
    )
    if media_global_comp > 0:
        fig_comp.add_hline(
            y=media_global_comp,
            line_dash="dot",
            line_color="#F59E0B",
            line_width=2,
            annotation_text=f"Média global |E|: {media_global_comp:.5f}",
            annotation_position="top right",
        )
    max_comp = max(comp_medios + [media_global_comp, 1e-6])
    fig_comp.update_layout(
        title=dict(
            text="Comprimento Euclidiano 3D Médio por Classe (u.o. VTK)",
            font=dict(size=15),
        ),
        xaxis_title="Classe de Resíduo Cⱼ",
        yaxis_title="Comprimento 3D Médio",
        yaxis=dict(range=[0, max_comp * 1.24]),
        margin=dict(l=20, r=20, t=50, b=25),
        height=340,
        showlegend=False,
    )

    # 2. Figura do Raio Médio por Classe
    fig_raio = go.Figure()
    fig_raio.add_trace(
        go.Bar(
            x=rotulos_x,
            y=raios_medios,
            name="Raio Médio",
            marker=dict(color=cores, line=dict(color="#1E293B", width=1)),
            text=[f"{v:.4f}" for v in raios_medios],
            textposition="outside",
            hovertemplate=(
                "<b>Classe %{x}</b><br>"
                "Raio médio: %{y:.7f} (u.o. VTK)<extra></extra>"
            ),
        )
    )
    if media_global_raio > 0:
        fig_raio.add_hline(
            y=media_global_raio,
            line_dash="dot",
            line_color="#F59E0B",
            line_width=2,
            annotation_text=f"Média global |E|: {media_global_raio:.4f}",
            annotation_position="top right",
        )
    max_raio = max(raios_medios + [media_global_raio, 1e-6])
    fig_raio.update_layout(
        title=dict(
            text="Raio Médio por Classe (u.o. VTK)",
            font=dict(size=15),
        ),
        xaxis_title="Classe de Resíduo Cⱼ",
        yaxis_title="Raio Médio",
        yaxis=dict(range=[0, max_raio * 1.24]),
        margin=dict(l=20, r=20, t=50, b=25),
        height=340,
        showlegend=False,
    )

    return fig_comp, fig_raio
