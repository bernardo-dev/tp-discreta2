"""
Módulo B0.4 — Consulta Determinística por Classes de Resíduos e Nota Crítica.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

import math
from typing import Any

try:
    from .b0_1_agrupamento_modular import calcular_medias_geometricas_classe
except ImportError:
    from b0_1_agrupamento_modular import calcular_medias_geometricas_classe

# ==============================================================================
# B0.4. Consulta Determinística por Classes de Resíduos e Nota Crítica
# ==============================================================================


def consultar_por_residuo(
    segmentos: list[dict[str, Any]],
    resto_j: int,
    m: int = 7,
) -> dict[str, Any]:
    """
    Requisito B0.4: Executa uma consulta determinística por classe de resíduo,
    retornando todos os segmentos cujo identificador satisfaz:
        i ≡ resto_j (mod m)   <=>   i % m == resto_j,
    além de suas métricas geométricas agregadas (contagem |C_j|, comprimento 3D
    médio e raio médio nas unidades originais do VTK).
    """
    if m <= 0:
        raise ValueError(f"O módulo m deve ser um inteiro positivo (recebido: {m}).")
    if resto_j < 0 or resto_j >= m:
        raise ValueError(
            f"O representante de resto j deve satisfazer 0 <= j < {m} "
            f"(recebido: {resto_j})."
        )

    segmentos_filtrados: list[dict[str, Any]] = []
    ids_filtrados: list[int] = []

    for indice_ordem, seg in enumerate(segmentos):
        seg_id = int(seg.get("id", indice_ordem))
        # Operador % do Python realiza a redução modular euclidiana h(i) = i mod m
        if (seg_id % m) == resto_j:
            segmentos_filtrados.append(seg)
            ids_filtrados.append(seg_id)

    medias = calcular_medias_geometricas_classe(segmentos_filtrados)

    return {
        "classe": f"C_{resto_j}",
        "resto_j": resto_j,
        "modulo_m": m,
        "expressao_congruencia": f"i ≡ {resto_j} (mod {m})",
        "funcao_hash": f"h(i) = i mod {m} = {resto_j}",
        "quantidade": len(segmentos_filtrados),
        "comprimento_3d_medio": medias["comprimento_3d_medio"],
        "raio_medio": medias["raio_medio"],
        "comprimento_3d_soma": medias["comprimento_3d_soma"],
        "raio_soma": medias["raio_soma"],
        "ids_segmentos": ids_filtrados,
        "exemplos_ids": ids_filtrados[:5],
        "segmentos": segmentos_filtrados,
    }


def gerar_discussao_critica_b04(
    nome_arquivo: str = "tree3D_Nterm128.vtk",
    total_segmentos: int = 255,
    m: int = 7,
) -> dict[str, str]:
    """
    Requisito B0.4: Gera um resumo textual estruturado (pronto para exibição
    no terminal/interface e uso no relatório) explicando:
    1. O funcionamento da congruência i ≡ j (mod 7) como mecanismo determinístico
       e reprodutível de consulta/particionamento (análogo a uma Tabela Hash
       h(i) = i mod 7) e o papel do operador `%` (Divisão Euclidiana).
    2. A conexão formal com o Módulo D (demonstração de que ≡ (mod 7) define
       uma relação de equivalência).
    3. A limitação obrigatória (Critério de Pertinência): o identificador i é
       um rótulo computacional da ordem de gravação na seção LINES do VTK e não
       concede significado fisiológico ou anatômico especial às classes C_j.
    """
    limite_pcp = math.ceil(total_segmentos / m) if m > 0 and total_segmentos > 0 else 0

    mecanismo_hash = (
        f"A relação de congruência i ≡ j (mod {m}) atua como uma função de "
        f"endereçamento determinístico h(i) = i mod {m}, análoga a uma Tabela Hash "
        f"com m = {m} compartimentos (buckets). Pelo Algoritmo da Divisão Euclidiana "
        f"(i = {m}q + r, com 0 <= r < {m}), implementado diretamente pelo operador "
        f"`%` do Python para divisor positivo, cada segmento i in {{0, ..., {max(0, total_segmentos - 1)}}} "
        f"do modelo `{nome_arquivo}` é mapeado de forma única, em tempo O(1) e "
        f"totalmente reprodutível para a classe C_j, distribuindo a carga de "
        f"maneira quase uniforme (entre {total_segmentos // m} e {limite_pcp} segmentos por classe)."
    )

    conexao_modulo_d = (
        f"Esta decomposição em {m} classes disjuntas antecipa o Teorema Fundamental "
        f"das Relações de Equivalência: a demonstração formal de que a congruência "
        f"módulo {m} é reflexiva, simétrica e transitiva — e que suas classes de "
        f"equivalência coincidem com a partição C_0, ..., C_{m - 1} validada em B0.2 — "
        f"será retomada e demonstrada no Módulo D."
    )

    limitacao_fisiologica = (
        "NOTA CRÍTICA (CRITÉRIO DE PERTINÊNCIA E LIMITAÇÃO ANATÔMICA): "
        "O identificador sequencial i de cada segmento é apenas um rótulo "
        "computacional definido pela ordem de gravação na seção `LINES` do "
        "arquivo VTK durante a geração da árvore pelo método CCO. Por conseguinte, "
        "o agrupamento modular i mod 7 possui finalidade estritamente computacional "
        "(indexação determinística, amostragem sistemática reproduzível e "
        "balanceamento em memória). Eventuais pequenas variações numéricas no "
        "raio médio ou no comprimento 3D médio entre as classes C_0 a C_6 NÃO "
        "permitem concluir que uma classe modular possua propriedades fisiológicas, "
        "hemodinâmicas ou regiões anatômicas especiais."
    )

    texto_completo = (
        f"1. Consulta Determinística e Tabela Hash (h(i) = i mod {m}):\n"
        f"   {mecanismo_hash}\n\n"
        f"2. Conexão com Relações de Equivalência (Módulo D):\n"
        f"   {conexao_modulo_d}\n\n"
        f"3. {limitacao_fisiologica}"
    )

    return {
        "mecanismo_hash": mecanismo_hash,
        "conexao_modulo_d": conexao_modulo_d,
        "limitacao_fisiologica": limitacao_fisiologica,
        "texto_completo": texto_completo,
    }
