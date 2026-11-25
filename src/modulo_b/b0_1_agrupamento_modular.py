"""
Módulo B0.1 — Agrupamento por Aritmética Modular e Estatísticas por Classe.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)

Nota sobre o operador `%` em Python e o Algoritmo da Divisão Euclidiana:
    Para qualquer dividendo inteiro `a` e divisor inteiro positivo `b > 0`, o
    Algoritmo da Divisão Euclidiana garante a existência e unicidade de inteiros
    `q` (quociente) e `r` (resto) tais que:
        a = b * q + r,   com  0 <= r < |b|.
    Em Python, o operador `%` (`a % b`) implementa exatamente o resto euclidiano
    não-negativo `r in {0, 1, ..., b - 1}` quando `b > 0` (pois `q = a // b` usa
    divisão piso). Assim, para `b = m = 7`, todo identificador `i in {0, ..., |E|-1}`
    possui um único representante de resto `j = i % 7` em `{0, 1, 2, 3, 4, 5, 6}`,
    o que garante matematicamente que as classes de congruência módulo 7 formam
    uma partição bem definida do conjunto de segmentos E.
"""

from __future__ import annotations

from typing import Any

# ==============================================================================
# B0.1. Agrupamento por Aritmética Modular e Estatísticas por Classe
# ==============================================================================


def calcular_medias_geometricas_classe(
    segmentos_classe: list[dict[str, Any]],
) -> dict[str, float]:
    """
    Calcula explicitamente (por laços elementares, sem bibliotecas externas)
    o comprimento euclidiano 3D médio e o raio médio dos segmentos pertencentes
    a uma classe de resíduo C_j, mantendo as unidades originais do arquivo VTK.
    """
    qtd = len(segmentos_classe)
    if qtd == 0:
        return {
            "comprimento_3d_soma": 0.0,
            "comprimento_3d_medio": 0.0,
            "raio_soma": 0.0,
            "raio_medio": 0.0,
        }

    soma_comprimento = 0.0
    cont_comprimento = 0
    soma_raio = 0.0
    cont_raio = 0

    for seg in segmentos_classe:
        comp = seg.get("comprimento_3d")
        if comp is not None:
            soma_comprimento += float(comp)
            cont_comprimento += 1

        raio = seg.get("raio")
        if raio is not None:
            soma_raio += float(raio)
            cont_raio += 1

    media_comprimento = (
        soma_comprimento / cont_comprimento if cont_comprimento > 0 else 0.0
    )
    media_raio = soma_raio / cont_raio if cont_raio > 0 else 0.0

    return {
        "comprimento_3d_soma": soma_comprimento,
        "comprimento_3d_medio": media_comprimento,
        "raio_soma": soma_raio,
        "raio_medio": media_raio,
    }


def agrupar_segmentos_por_modulo(
    segmentos: list[dict[str, Any]],
    m: int = 7,
    qtd_exemplos: int = 5,
) -> dict[str, Any]:
    """
    Requisito B0.1: Distribui os identificadores dos segmentos i in {0, 1, ..., |E|-1}
    (na ordem da seção LINES do VTK) em m classes de resíduos módulo m:
        C_j = {i : i ≡ j (mod m)},  para j = 0, 1, ..., m - 1.

    Nota sobre `%` em Python:
        O cálculo `j = i % m` (com `m > 0`) segue o Algoritmo da Divisão
        Euclidiana (`i = m * q + j`, com `0 <= j < m`), associando cada
        identificador `i` a exatamente uma gaveta modular `j in {0, ..., m-1}`.

    Retorna um dicionário contendo:
    - `modulo_m`: o módulo utilizado (padrão 7);
    - `total_segmentos`: |E|;
    - `classes_segmentos`: dicionário {j: [segmentos da classe C_j]};
    - `classes_ids`: dicionário {j: [IDs i dos segmentos da classe C_j]};
    - `classes_conjuntos`: dicionário {j: set(IDs da classe C_j)};
    - `tabela_classes`: lista de dicionários estruturados por classe C_0 ... C_{m-1}.
    """
    if m <= 0:
        raise ValueError(f"O módulo m deve ser um inteiro positivo (recebido: {m}).")

    # Inicializa as m "gavetas" fixas correspondentes aos restos 0, 1, ..., m - 1
    classes_segmentos: dict[int, list[dict[str, Any]]] = {}
    classes_ids: dict[int, list[int]] = {}
    for j in range(m):
        classes_segmentos[j] = []
        classes_ids[j] = []

    # Particionamento modular explícito seguindo a ordem de LINES
    for indice_ordem, seg in enumerate(segmentos):
        seg_id = int(seg.get("id", indice_ordem))
        # Pelo Algoritmo da Divisão Euclidiana (i = m*q + j, 0 <= j < m),
        # o operador % do Python produz um único resto j em {0, 1, ..., m-1}.
        resto_j = seg_id % m
        classes_segmentos[resto_j].append(seg)
        classes_ids[resto_j].append(seg_id)

    classes_conjuntos: dict[int, set[int]] = {}
    tabela_classes: list[dict[str, Any]] = []
    total_segmentos = len(segmentos)

    for j in range(m):
        segs_j = classes_segmentos[j]
        ids_j = classes_ids[j]
        classes_conjuntos[j] = set(ids_j)

        medias = calcular_medias_geometricas_classe(segs_j)
        qtd_j = len(ids_j)
        proporcao = (qtd_j / total_segmentos) if total_segmentos > 0 else 0.0
        exemplos = ids_j[:qtd_exemplos]

        tabela_classes.append(
            {
                "classe": f"C_{j}",
                "resto_j": j,
                "modulo_m": m,
                "congruencia": f"i ≡ {j} (mod {m})",
                "quantidade": qtd_j,
                "proporcao": proporcao,
                "percentual": proporcao * 100.0,
                "comprimento_3d_medio": medias["comprimento_3d_medio"],
                "raio_medio": medias["raio_medio"],
                "comprimento_3d_soma": medias["comprimento_3d_soma"],
                "raio_soma": medias["raio_soma"],
                "exemplos_ids": exemplos,
                "exemplos_str": ", ".join(str(idx) for idx in exemplos),
                "ids_segmentos": list(ids_j),
            }
        )

    return {
        "modulo_m": m,
        "total_segmentos": total_segmentos,
        "classes_segmentos": classes_segmentos,
        "classes_ids": classes_ids,
        "classes_conjuntos": classes_conjuntos,
        "tabela_classes": tabela_classes,
    }
