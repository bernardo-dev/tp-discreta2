"""
Testes Automatizados com Pytest — Módulo B / Parte B0 (CCO Explorer).
Disciplina: BCC102 — Matemática Discreta II (UFOP)

Cobre os requisitos funcionais B0.1, B0.2, B0.3 e B0.4 e a parcela B0 do
teste mínimo de aceitação T7 sobre o modelo `tree3D_Nterm128.vtk`.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path

import pytest

from src.modulo_a.modulo_a_vtk import (
    processar_modelo_vtk,
    resolver_pasta_modelos,
)
from src.modulo_b.modulo_b_numeros import (
    agrupar_segmentos_por_modulo,
    analisar_principio_casa_dos_pombos,
    consultar_por_residuo,
    exportar_classes_modulares_csv,
    formatar_resumo_b0,
    gerar_discussao_critica_b04,
    processar_parte_b0_modelo,
    validar_particao_modular,
)


def obter_diretorio_modelos() -> Path:
    """
    Obtém o diretório dos modelos VTK a partir da variável de ambiente
    `CCO_DADOS_DIR` (ou `VTK_DATA_DIR`), utilizando o padrão configurável
    `dados_modelos3D/` caso não esteja definida.
    """
    caminho_env = os.environ.get(
        "CCO_DADOS_DIR",
        os.environ.get("VTK_DATA_DIR", "dados_modelos3D/"),
    )
    return resolver_pasta_modelos(caminho_env)


@pytest.fixture(scope="module")
def resultado_b0_nterm128() -> dict:
    """Carrega e processa a Parte B0 para o modelo obrigatório `tree3D_Nterm128.vtk`."""
    pasta = obter_diretorio_modelos()
    return processar_parte_b0_modelo(
        modelo_ou_arquivo="tree3D_Nterm128.vtk",
        pasta_modelos=pasta,
        m=7,
    )


# ==============================================================================
# Teste de Aceitação T7 (Parte B0): Soma das 7 frequências igual a |E| = 255
# ==============================================================================

def test_t7_b0_soma_frequencias_igual_255_nterm128(
    resultado_b0_nterm128: dict,
) -> None:
    """
    T7 (Parte B0): A soma das 7 frequências das classes modulares C_0 a C_6 é
    exatamente igual ao número de segmentos de `tree3D_Nterm128.vtk` (|E| = 255).
    """
    tabela = resultado_b0_nterm128["tabela_classes"]
    assert len(tabela) == 7
    assert resultado_b0_nterm128["total_segmentos_E"] == 255

    frequencias = [int(item["quantidade"]) for item in tabela]
    assert sum(frequencias) == 255

    # Verifica também os 5 primeiros IDs de cada classe conforme o Algoritmo da Divisão Euclidiana
    for j, item in enumerate(tabela):
        assert item["classe"] == f"C_{j}"
        assert item["resto_j"] == j
        assert item["exemplos_ids"] == [j + 7 * k for k in range(5)]
        assert item["comprimento_3d_medio"] > 0.0
        assert item["raio_medio"] > 0.0


# ==============================================================================
# B0.2: Disjunção par a par e cobertura completa da união
# ==============================================================================

def test_b02_disjuncao_par_a_par_e_uniao_completa(
    resultado_b0_nterm128: dict,
) -> None:
    """
    B0.2: Verifica que todas as 7 classes são disjuntas dois a dois
    (C_j ∩ C_k = ∅ para todo j != k) e que sua união cobre exatamente
    {0, 1, ..., 254}.
    """
    agrupamento = resultado_b0_nterm128["agrupamento"]
    validacao = validar_particao_modular(agrupamento, total_segmentos_esperado=255)

    assert validacao["particao_valida"] is True
    assert validacao["status"] == "OK"
    assert validacao["disjuntas_dois_a_dois"] is True
    assert validacao["soma_igual_total"] is True
    assert validacao["uniao_cobre_universo"] is True
    assert validacao["classes_nao_vazias"] is True
    assert validacao["sem_duplicatas_internas"] is True
    assert validacao["soma_cardinalidades"] == 255
    assert validacao["cardinalidade_uniao"] == 255
    assert validacao["num_pares_verificados"] == 21  # C(7, 2) = 21 pares
    assert len(validacao["conflitos_disjuncao"]) == 0

    # Verificação explícita direta com conjuntos Python (set)
    conjuntos = agrupamento["classes_conjuntos"]
    uniao: set[int] = set()
    for j in range(7):
        uniao = uniao.union(conjuntos[j])
        for k in range(j + 1, 7):
            assert conjuntos[j].isdisjoint(conjuntos[k]), (
                f"Classes C_{j} e C_{k} não são disjuntas!"
            )
            assert (conjuntos[j] & conjuntos[k]) == set()

    assert uniao == set(range(255))


# ==============================================================================
# B0.3: Princípio da Casa dos Pombos Generalizado (PCP)
# ==============================================================================

def test_b03_principio_casa_dos_pombos_nterm128(
    resultado_b0_nterm128: dict,
) -> None:
    """
    B0.3: Verifica o limite inferior do Princípio da Casa dos Pombos
    ceil(255 / 7) == 37, a confirmação de max |C_j| >= 37, e que existem
    exatamente 3 classes de tamanho 37 (C_0, C_1, C_2) e 4 classes de
    tamanho 36 (C_3, C_4, C_5, C_6).
    """
    pcp = resultado_b0_nterm128["casa_dos_pombos"]

    assert pcp["pombos_N"] == 255
    assert pcp["gavetas_m"] == 7
    assert math.ceil(255 / 7) == 37
    assert pcp["limite_inferior_pcp"] == 37
    assert pcp["quociente_euclidiano"] == 36
    assert pcp["resto_euclidiano"] == 3

    assert pcp["max_observado"] == 37
    assert pcp["min_observado"] == 36
    assert pcp["desigualdade_confirmada"] is True
    assert pcp["max_observado"] >= pcp["limite_inferior_pcp"]

    assert pcp["qtd_classes_no_limite"] == 3
    assert pcp["classes_no_limite"] == ["C_0", "C_1", "C_2"]
    assert pcp["qtd_classes_abaixo_limite"] == 4
    assert pcp["classes_abaixo_limite"] == ["C_3", "C_4", "C_5", "C_6"]

    card = pcp["cardinalidades"]
    for j in (0, 1, 2):
        assert card[f"C_{j}"] == 37
    for j in (3, 4, 5, 6):
        assert card[f"C_{j}"] == 36


# ==============================================================================
# B0.4: Consistência da Consulta Determinística por Resíduo e Nota Crítica
# ==============================================================================

@pytest.mark.parametrize("resto_j", list(range(7)))
def test_b04_consistencia_consultar_por_residuo(
    resultado_b0_nterm128: dict,
    resto_j: int,
) -> None:
    """
    B0.4: Verifica que todo elemento retornado por `consultar_por_residuo` para
    o resto j satisfaz `id % 7 == j`, que a quantidade coincide com |C_j| da
    tabela B0.1, e que as médias geométricas coincidem com as da classe C_j.
    """
    segmentos = resultado_b0_nterm128["modelo_a"]["segmentos"]
    tabela = resultado_b0_nterm128["tabela_classes"]
    esperado_classe = tabela[resto_j]

    consulta = consultar_por_residuo(segmentos, resto_j=resto_j, m=7)

    assert consulta["classe"] == f"C_{resto_j}"
    assert consulta["resto_j"] == resto_j
    assert consulta["modulo_m"] == 7
    assert consulta["quantidade"] == esperado_classe["quantidade"]
    assert len(consulta["segmentos"]) == esperado_classe["quantidade"]
    assert len(consulta["ids_segmentos"]) == esperado_classe["quantidade"]

    for seg in consulta["segmentos"]:
        seg_id = int(seg["id"])
        assert (seg_id % 7) == resto_j

    assert math.isclose(
        consulta["comprimento_3d_medio"],
        esperado_classe["comprimento_3d_medio"],
        rel_tol=1e-12,
    )
    assert math.isclose(
        consulta["raio_medio"],
        esperado_classe["raio_medio"],
        rel_tol=1e-12,
    )


def test_b04_validacao_parametros_invalidos_e_discussao(
    resultado_b0_nterm128: dict,
) -> None:
    """
    Garante que `consultar_por_residuo` rejeita restos fora de {0, ..., m-1}
    e que a discussão crítica B0.4 aborda Tabela Hash, Módulo D e a limitação
    anatômica/fisiológica (Critério de Pertinência).
    """
    segmentos = resultado_b0_nterm128["modelo_a"]["segmentos"]

    with pytest.raises(ValueError):
        consultar_por_residuo(segmentos, resto_j=-1, m=7)

    with pytest.raises(ValueError):
        consultar_por_residuo(segmentos, resto_j=7, m=7)

    with pytest.raises(ValueError):
        agrupar_segmentos_por_modulo(segmentos, m=0)

    disc = gerar_discussao_critica_b04("tree3D_Nterm128.vtk", 255, 7)
    assert "Tabela Hash" in disc["mecanismo_hash"]
    assert "Módulo D" in disc["conexao_modulo_d"]
    assert "NÃO permitem concluir" in disc["limitacao_fisiologica"]

    resumo = formatar_resumo_b0(resultado_b0_nterm128)
    assert "B0.1" in resumo
    assert "B0.2" in resumo
    assert "B0.3" in resumo
    assert "B0.4" in resumo


# ==============================================================================
# Exportação CSV da Parte B0
# ==============================================================================

def test_exportacao_csv_b0_classes_mod7(
    resultado_b0_nterm128: dict,
    tmp_path: Path,
) -> None:
    """
    Verifica a exportação do arquivo CSV `b0_classes_mod7_Nterm128.csv` com as
    7 classes e todas as colunas estruturadas exigidas em B0.1.
    """
    caminho_csv = exportar_classes_modulares_csv(
        resultado_b0_nterm128,
        pasta_saida=tmp_path,
    )
    assert caminho_csv.exists()
    assert caminho_csv.name == "b0_classes_mod7_Nterm128.csv"

    with caminho_csv.open("r", encoding="utf-8") as f_csv:
        leitor = csv.DictReader(f_csv)
        assert leitor.fieldnames == [
            "classe",
            "resto_j",
            "modulo_m",
            "quantidade",
            "comprimento_3d_medio",
            "raio_medio",
            "exemplos_ids",
        ]
        linhas = list(leitor)
        assert len(linhas) == 7
        assert sum(int(linha["quantidade"]) for linha in linhas) == 255
