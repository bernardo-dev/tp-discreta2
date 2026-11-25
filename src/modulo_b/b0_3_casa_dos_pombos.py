"""
Módulo B0.3 — Princípio da Casa dos Pombos Generalizado (PCP).
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import math
from typing import Any

# ==============================================================================
# B0.3. Princípio da Casa dos Pombos Generalizado (PCP)
# ==============================================================================


def analisar_principio_casa_dos_pombos(
    agrupamento: dict[str, Any],
) -> dict[str, Any]:
    """
    Requisito B0.3: Aplica o Princípio da Casa dos Pombos Generalizado (PCP) à
    distribuição dos segmentos nas classes de resíduos módulo m:
    - Objetos ("pombos"): N = |E| segmentos;
    - Caixas ("gavetas"): m restos possíveis {0, 1, ..., m - 1};
    - Limite inferior teórico da maior classe: ceil(N / m) = math.ceil(|E| / m);
    - Confronto com os dados reais: identifica max(|C_j|), lista quais classes
      atingem ou superam esse limite e verifica a desigualdade max |C_j| >= ceil(N / m).
    """
    m = int(agrupamento["modulo_m"])
    n_pombos = int(agrupamento["total_segmentos"])
    tabela_classes: list[dict[str, Any]] = agrupamento["tabela_classes"]

    limite_inferior_pcp = math.ceil(n_pombos / m) if n_pombos > 0 else 0
    quociente_euclidiano = n_pombos // m
    resto_euclidiano = n_pombos % m

    cardinalidades: dict[str, int] = {}
    max_observado = 0
    min_observado = n_pombos if n_pombos > 0 else 0

    for item in tabela_classes:
        rotulo = str(item["classe"])
        qtd = int(item["quantidade"])
        cardinalidades[rotulo] = qtd
        if qtd > max_observado:
            max_observado = qtd
        if qtd < min_observado:
            min_observado = qtd

    classes_no_limite: list[str] = []
    classes_abaixo_limite: list[str] = []
    detalhamento_classes: list[dict[str, Any]] = []

    for item in tabela_classes:
        rotulo = str(item["classe"])
        qtd = int(item["quantidade"])
        atinge_limite = qtd >= limite_inferior_pcp
        if atinge_limite:
            classes_no_limite.append(rotulo)
        else:
            classes_abaixo_limite.append(rotulo)

        detalhamento_classes.append(
            {
                "classe": rotulo,
                "resto_j": int(item["resto_j"]),
                "quantidade": qtd,
                "limite_pcp": limite_inferior_pcp,
                "atinge_ou_supera_pcp": atinge_limite,
            }
        )

    desigualdade_confirmada = max_observado >= limite_inferior_pcp

    explicacao = (
        f"Ao distribuir N = |E| = {n_pombos} segmentos (pombos) em m = {m} "
        f"classes de resíduos (gavetas), o Princípio da Casa dos Pombos "
        f"Generalizado garante que ao menos uma classe contém pelo menos "
        f"ceil({n_pombos}/{m}) = {limite_inferior_pcp} segmentos. "
        f"Pela Divisão Euclidiana ({n_pombos} = {m} * {quociente_euclidiano} + {resto_euclidiano}), "
        f"observam-se {len(classes_no_limite)} classe(s) com {max_observado} segmentos "
        f"({', '.join(classes_no_limite)}) e {len(classes_abaixo_limite)} classe(s) "
        f"com {min_observado} segmentos ({', '.join(classes_abaixo_limite)}), "
        f"confirmando max |C_j| = {max_observado} >= {limite_inferior_pcp}."
    )

    return {
        "pombos_N": n_pombos,
        "gavetas_m": m,
        "limite_inferior_pcp": limite_inferior_pcp,
        "quociente_euclidiano": quociente_euclidiano,
        "resto_euclidiano": resto_euclidiano,
        "max_observado": max_observado,
        "min_observado": min_observado,
        "desigualdade_confirmada": desigualdade_confirmada,
        "classes_no_limite": classes_no_limite,
        "classes_abaixo_limite": classes_abaixo_limite,
        "qtd_classes_no_limite": len(classes_no_limite),
        "qtd_classes_abaixo_limite": len(classes_abaixo_limite),
        "cardinalidades": cardinalidades,
        "detalhamento_classes": detalhamento_classes,
        "explicacao": explicacao,
    }
