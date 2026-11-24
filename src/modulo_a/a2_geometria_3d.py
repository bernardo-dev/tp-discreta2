"""
Módulo A2 — Incorporar Geometria Tridimensional (Comprimento Geométrico e Ponto Médio).
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import math
from typing import Any

# ==============================================================================
# A2. Geometria Tridimensional (Comprimento Geométrico e Ponto Médio)
# ==============================================================================


def calcular_comprimento(
    ponto_u: tuple[float, float, float],
    ponto_v: tuple[float, float, float],
) -> float:
    """
    Requisito A2: Calcula o comprimento geometrico entre
    P_u = (x_u, y_u, z_u) e P_v = (x_v, y_v, z_v):
        l_i = sqrt((x_v - x_u)^2 + (y_v - y_u)^2 + (z_v - z_u)^2)
    """
    xu, yu, zu = ponto_u
    xv, yv, zv = ponto_v

    dx = xv - xu
    dy = yv - yu
    dz = zv - zu

    return math.sqrt((dx * dx) + (dy * dy) + (dz * dz))


def calcular_ponto_medio(
    ponto_u: tuple[float, float, float],
    ponto_v: tuple[float, float, float],
) -> tuple[float, float, float]:
    """
    Requisito A2: Calcula explicitamente o ponto médio tridimensional M_i do
    segmento com extremos P_u = (x_u, y_u, z_u) e P_v = (x_v, y_v, z_v):
        M_i = ((x_u + x_v) / 2, (y_u + y_v) / 2, (z_u + z_v) / 2)
    """
    xu, yu, zu = ponto_u
    xv, yv, zv = ponto_v

    mx = (xu + xv) / 2.0
    my = (yu + yv) / 2.0
    mz = (zu + zv) / 2.0

    return (mx, my, mz)


def incorporar_geometria(
    pontos: list[dict[str, Any]],
    segmentos: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Requisito A2: Dados os extremos (u, v), incorpora as
    coordenadas de P_u e P_v, o comprimento euclidiano 3D (l_i) e o ponto médio
    M_i = (mx, my, mz).
    """
    # cria um dicionario, sendo int o ID do ponto e tuple[float, float, float] as coordenadas (x, y, z)
    arvore: dict[int, tuple[float, float, float]] = {}
    for p in pontos:
        arvore[int(p["id"])] = (
            float(p["x"]),
            float(p["y"]),
            float(p["z"]),
        )

    # incorpora o comprimento e o ponto medio em cada segmento da arvore
    for seg in segmentos:
        u = int(seg["u"])
        v = int(seg["v"])

        # se os pontos extremos existirem na arvore, calcula o comprimento e o ponto medio
        if u in arvore and v in arvore:
            coord_u = arvore[u]
            coord_v = arvore[v]

            comprimento = calcular_comprimento(coord_u, coord_v)
            mx, my, mz = calcular_ponto_medio(coord_u, coord_v)

            seg["coord_u"] = coord_u
            seg["coord_v"] = coord_v
            seg["comprimento_3d"] = comprimento
            seg["ponto_medio"] = (mx, my, mz)
            seg["mx"] = mx
            seg["my"] = my
            seg["mz"] = mz
        else:
            seg["coord_u"] = None
            seg["coord_v"] = None
            seg["comprimento_3d"] = None
            seg["ponto_medio"] = None
            seg["mx"] = None
            seg["my"] = None
            seg["mz"] = None

    return segmentos


def calcular_estatisticas_descritivas(valores: list[float]) -> dict[str, float]:
    """
    Calcula estatísticas descritivas (mínimo, máximo, média, mediana, desvio
    padrão e soma) de forma explícita usando laços e ordenação elementar.
    """
    n = len(valores)
    if n == 0:
        return {
            "quantidade": 0.0,
            "minimo": 0.0,
            "maximo": 0.0,
            "media": 0.0,
            "mediana": 0.0,
            "desvio_padrao": 0.0,
            "soma": 0.0,
        }

    ordenados = sorted(float(v) for v in valores)
    minimo = ordenados[0]
    maximo = ordenados[-1]

    soma = 0.0
    for v in ordenados:
        soma += v
    media = soma / n

    meio = n // 2
    if n % 2 == 1:
        mediana = ordenados[meio]
    else:
        mediana = (ordenados[meio - 1] + ordenados[meio]) / 2.0

    soma_quadrados = 0.0
    for v in ordenados:
        diff = v - media
        soma_quadrados += diff * diff
    desvio_padrao = math.sqrt(soma_quadrados / n)

    return {
        "quantidade": float(n),
        "minimo": minimo,
        "maximo": maximo,
        "media": media,
        "mediana": mediana,
        "desvio_padrao": desvio_padrao,
        "soma": soma,
    }
