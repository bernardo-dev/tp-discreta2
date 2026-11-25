"""
Módulo B0.2 — Validação Matemática da Partição.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

# ==============================================================================
# B0.2. Validação Matemática da Partição
# ==============================================================================


def validar_particao_modular(
    agrupamento: dict[str, Any],
    total_segmentos_esperado: int | None = None,
) -> dict[str, Any]:
    """
    Requisito B0.2: Verifica programaticamente nos dados reais que as classes
    C_0, C_1, ..., C_{m-1} constituem uma partição matemática válida do conjunto
    de segmentos E = {0, 1, ..., |E| - 1}:
    1. Classes não-vazias (quando |E| >= m): C_j != ∅ para todo j;
    2. Disjunção dois a dois: C_j ∩ C_k = ∅ para todo par j != k (usando `set`);
    3. União completa sem perdas nem duplicatas:
       - Soma das cardinalidades: sum_{j=0}^{m-1} |C_j| == |E|;
       - Igualdade conjuntista: U_{j=0}^{m-1} C_j == {0, 1, ..., |E| - 1}.

    Retorna um relatório booleano e explicativo com o resultado de cada etapa.
    """
    m = int(agrupamento["modulo_m"])
    total_segmentos = (
        int(total_segmentos_esperado)
        if total_segmentos_esperado is not None
        else int(agrupamento["total_segmentos"])
    )
    classes_ids: dict[int, list[int]] = agrupamento["classes_ids"]

    # Construção explícita dos conjuntos C_j e verificação de duplicatas internas
    conjuntos: dict[int, set[int]] = {}
    sem_duplicatas_internas = True
    classes_com_duplicata: list[str] = []

    for j in range(m):
        lista_j = classes_ids.get(j, [])
        conj_j = set(lista_j)
        conjuntos[j] = conj_j
        if len(conj_j) != len(lista_j):
            sem_duplicatas_internas = False
            classes_com_duplicata.append(f"C_{j}")

    # 1. Verificação de não-vacuidade (para |E| >= m, toda classe deve ser não-vazia)
    classes_vazias: list[str] = [
        f"C_{j}" for j in range(m) if len(conjuntos[j]) == 0
    ]
    classes_nao_vazias = (
        len(classes_vazias) == 0 if total_segmentos >= m else True
    )

    # 2. Verificação de disjunção par a par: C_j ∩ C_k = ∅ para todo j < k
    pares_verificados: list[dict[str, Any]] = []
    conflitos_disjuncao: list[dict[str, Any]] = []

    for j in range(m):
        for k in range(j + 1, m):
            intersecao = conjuntos[j].intersection(conjuntos[k])
            par_disjunto = len(intersecao) == 0
            registro_par = {
                "classe_j": f"C_{j}",
                "classe_k": f"C_{k}",
                "j": j,
                "k": k,
                "cardinalidade_intersecao": len(intersecao),
                "elementos_comuns": sorted(intersecao),
                "disjunto": par_disjunto,
            }
            pares_verificados.append(registro_par)
            if not par_disjunto:
                conflitos_disjuncao.append(registro_par)

    disjuntas_dois_a_dois = len(conflitos_disjuncao) == 0

    # 3. Verificação da soma das cardinalidades e da união conjuntista
    soma_cardinalidades = 0
    uniao_conjuntos: set[int] = set()
    for j in range(m):
        soma_cardinalidades += len(classes_ids.get(j, []))
        uniao_conjuntos = uniao_conjuntos.union(conjuntos[j])

    universo_esperado: set[int] = set(range(total_segmentos))
    elementos_faltantes = sorted(universo_esperado.difference(uniao_conjuntos))
    elementos_excedentes = sorted(uniao_conjuntos.difference(universo_esperado))

    soma_igual_total = soma_cardinalidades == total_segmentos
    uniao_cobre_universo = (
        uniao_conjuntos == universo_esperado
        and len(uniao_conjuntos) == total_segmentos
    )

    particao_valida = (
        classes_nao_vazias
        and sem_duplicatas_internas
        and disjuntas_dois_a_dois
        and soma_igual_total
        and uniao_cobre_universo
    )

    mensagens: list[str] = []
    if disjuntas_dois_a_dois:
        mensagens.append(
            f"Disjunção dois a dois confirmada: C_j ∩ C_k = ∅ em todos os "
            f"{len(pares_verificados)} pares (j != k)."
        )
    else:
        mensagens.append(
            f"Falha de disjunção: {len(conflitos_disjuncao)} par(es) com interseção não-vazia."
        )

    if soma_igual_total and uniao_cobre_universo:
        mensagens.append(
            f"Cobertura completa confirmada: sum |C_j| = {soma_cardinalidades} == |E| = {total_segmentos} "
            f"e U C_j == {{0, ..., {max(0, total_segmentos - 1)}}}."
        )
    else:
        mensagens.append(
            f"Falha na cobertura: sum |C_j| = {soma_cardinalidades}, |U C_j| = {len(uniao_conjuntos)}, "
            f"esperado |E| = {total_segmentos}."
        )

    if classes_nao_vazias:
        mensagens.append(
            f"Não-vacuidade confirmada: todas as {m} classes possuem elementos."
        )
    else:
        mensagens.append(f"Atenção: classes vazias detectadas: {classes_vazias}.")

    return {
        "particao_valida": particao_valida,
        "status": "OK" if particao_valida else "INCONSISTENTE",
        "modulo_m": m,
        "total_segmentos_E": total_segmentos,
        "soma_cardinalidades": soma_cardinalidades,
        "cardinalidade_uniao": len(uniao_conjuntos),
        "disjuntas_dois_a_dois": disjuntas_dois_a_dois,
        "soma_igual_total": soma_igual_total,
        "uniao_cobre_universo": uniao_cobre_universo,
        "classes_nao_vazias": classes_nao_vazias,
        "sem_duplicatas_internas": sem_duplicatas_internas,
        "num_pares_verificados": len(pares_verificados),
        "pares_verificados": pares_verificados,
        "conflitos_disjuncao": conflitos_disjuncao,
        "classes_vazias": classes_vazias,
        "classes_com_duplicata": classes_com_duplicata,
        "elementos_faltantes": elementos_faltantes,
        "elementos_excedentes": elementos_excedentes,
        "mensagens": mensagens,
    }
