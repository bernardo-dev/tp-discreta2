"""
Testes Automatizados com Pytest — Módulo A (CCO Explorer).
Disciplina: BCC102 — Matemática Discreta II (UFOP)

Cobre os testes mínimos de aceitação T1 e T2 do enunciado, além de casos
sintéticos conhecidos para geometria 3D (comprimento euclidiano e ponto médio),
detecção de inconsistências em A3 e exportação de arquivos CSV.
"""

from __future__ import annotations

import csv
import math
import os
from pathlib import Path

import pytest

from src.modulo_a.modulo_a_vtk import (
    ARQUIVOS_MODELOS_VTK,
    TABELA_REFERENCIA,
    calcular_comprimento,
    calcular_ponto_medio,
    exportar_segmentos_csv,
    gerar_tabela_consolidada,
    processar_conteudo_vtk,
    processar_modelo_vtk,
    processar_todos_modelos,
    resolver_pasta_modelos,
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


# ==============================================================================
# Teste de Aceitação T1: Leitura e Validação A3 de todos os 6 arquivos VTK
# ==============================================================================

@pytest.mark.parametrize("nome_arquivo", ARQUIVOS_MODELOS_VTK)
def test_t1_leitura_e_validacao_6_arquivos_vtk(nome_arquivo: str) -> None:
    """
    T1: O programa processa todos os seis arquivos VTK sem alterações manuais
    de dados e aprova todos os critérios de validação A3.
    """
    pasta = obter_diretorio_modelos()
    caminho_vtk = pasta / nome_arquivo
    assert caminho_vtk.exists(), f"Arquivo VTK não encontrado: {caminho_vtk}"

    resultado = processar_modelo_vtk(caminho_vtk)
    validacao = resultado["validacao"]

    assert validacao["valido"] is True, (
        f"Falha na validação A3 para {nome_arquivo}: {validacao['inconsistencias']}"
    )
    assert validacao["status"] == "OK"
    assert validacao["contagem_pontos_ok"] is True
    assert validacao["contagem_segmentos_ok"] is True
    assert validacao["extremos_validos"] is True
    assert validacao["raios_completos"] is True
    assert len(validacao["inconsistencias"]) == 0


# ==============================================================================
# Teste de Aceitação T2: Igualdade Exata de |V|, |E|, T, B e Entrada ID 0
# ==============================================================================

@pytest.mark.parametrize("nome_arquivo", ARQUIVOS_MODELOS_VTK)
def test_t2_igualdade_exata_tabela_1_e_ponto_entrada(nome_arquivo: str) -> None:
    """
    T2: As quantidades de pontos (|V|), segmentos (|E|), terminais (T),
    bifurcações (B) e o ponto de entrada (ID 0) coincidem exatamente com a
    Tabela 1 de referência do TP.
    """
    pasta = obter_diretorio_modelos()
    resultado = processar_modelo_vtk(pasta / nome_arquivo)

    estrutura = resultado["estrutura"]
    comparacao = resultado["comparacao_tabela_1"]
    esperado = TABELA_REFERENCIA[nome_arquivo]

    assert estrutura["num_pontos_V"] == esperado["V"]
    assert estrutura["num_segmentos_E"] == esperado["E"]
    assert estrutura["num_terminais_T"] == esperado["T"]
    assert estrutura["num_bifurcacoes_B"] == esperado["B"]

    # Verifica topologia real: ponto de entrada único com ID 0 (in=0, out=1)
    assert estrutura["ponto_entrada_id"] == 0
    assert estrutura["confirmado_id_zero"] is True
    assert estrutura["pontos_entrada"] == [0]
    assert len(estrutura["pontos_grau_inesperado"]) == 0

    # Verifica que o ponto de entrada não foi confundido com bifurcação
    assert 0 not in estrutura["bifurcacoes_ids"]
    assert 0 not in estrutura["terminais_ids"]

    # Identidade estrutural da árvore: |V| = 1 + B + T e |E| = |V| - 1
    assert (
        estrutura["num_pontos_V"]
        == 1 + estrutura["num_bifurcacoes_B"] + estrutura["num_terminais_T"]
    )
    assert estrutura["num_segmentos_E"] == estrutura["num_pontos_V"] - 1
    assert comparacao["coincide_tabela_1"] is True


# ==============================================================================
# Verificação Sintética da Geometria 3D (Comprimento 3D e Ponto Médio)
# ==============================================================================

def test_geometria_3d_caso_sintetico_conhecido() -> None:
    """
    Verifica explicitamente as fórmulas do comprimento euclidiano 3D (l_i) e
    do ponto médio 3D (M_i) em um caso sintético conhecido:
      - P0 = (0.0, 0.0, 0.0)
      - P1 = (3.0, 4.0, 12.0) -> comprimento = sqrt(9 + 16 + 144) = 13.0
                              -> ponto médio = (1.5, 2.0, 6.0)
      - P2 = (3.0, 8.0, 15.0) -> de P1 a P2: dx=0, dy=4, dz=3 -> comprimento = 5.0
                              -> ponto médio = (3.0, 6.0, 13.5)
      - P3 = (1.0, 4.0, 12.0) -> de P1 a P3: dx=-2, dy=0, dz=0 -> comprimento = 2.0
                              -> ponto médio = (2.0, 4.0, 12.0)
    """
    p0 = (0.0, 0.0, 0.0)
    p1 = (3.0, 4.0, 12.0)
    assert math.isclose(calcular_comprimento(p0, p1), 13.0, rel_tol=1e-12)
    assert calcular_ponto_medio(p0, p1) == (1.5, 2.0, 6.0)

    vtk_sintetico = """# vtk DataFile Version 3.0
Arvore Sintetica de Teste
ASCII
DATASET POLYDATA
POINTS 4 float
0.0 0.0 0.0
3.0 4.0 12.0
3.0 8.0 15.0
1.0 4.0 12.0

LINES 3 9
2 0 1
2 1 2
2 1 3

CELL_DATA 3
scalars raio float
LOOKUP_TABLE default
0.80
0.50
0.40
"""
    resultado = processar_conteudo_vtk(vtk_sintetico, nome_arquivo="sintetico.vtk")
    assert resultado["validacao"]["valido"] is True

    segs = resultado["segmentos"]
    assert len(segs) == 3

    # Segmento 0: (0 -> 1)
    assert segs[0]["id"] == 0
    assert segs[0]["extremos"] == (0, 1)
    assert math.isclose(segs[0]["raio"], 0.80, rel_tol=1e-9)
    assert math.isclose(segs[0]["comprimento_3d"], 13.0, rel_tol=1e-9)
    assert segs[0]["ponto_medio"] == (1.5, 2.0, 6.0)

    # Segmento 1: (1 -> 2)
    assert segs[1]["id"] == 1
    assert segs[1]["extremos"] == (1, 2)
    assert math.isclose(segs[1]["raio"], 0.50, rel_tol=1e-9)
    assert math.isclose(segs[1]["comprimento_3d"], 5.0, rel_tol=1e-9)
    assert segs[1]["ponto_medio"] == (3.0, 6.0, 13.5)

    # Segmento 2: (1 -> 3)
    assert segs[2]["id"] == 2
    assert segs[2]["extremos"] == (1, 3)
    assert math.isclose(segs[2]["raio"], 0.40, rel_tol=1e-9)
    assert math.isclose(segs[2]["comprimento_3d"], 2.0, rel_tol=1e-9)
    assert segs[2]["ponto_medio"] == (2.0, 4.0, 12.0)

    # Estrutura dos 4 pontos: 0 = Entrada, 1 = Bifurcação, 2 e 3 = Terminais
    est = resultado["estrutura"]
    assert est["ponto_entrada_id"] == 0
    assert est["bifurcacoes_ids"] == [1]
    assert est["terminais_ids"] == [2, 3]
    assert len(est["pontos_grau_inesperado"]) == 0


def test_validacao_a3_detecta_inconsistencias() -> None:
    """
    Garante que o validador A3 reporta inconsistências quando um identificador
    em LINES não existe em POINTS ou quando falta raio em CELL_DATA.
    """
    vtk_invalido = """# vtk DataFile Version 3.0
VTK com inconsistencias
ASCII
DATASET POLYDATA
POINTS 2 float
0.0 0.0 0.0
1.0 1.0 1.0
LINES 2 6
2 0 1
2 1 99
CELL_DATA 2
scalars raio float
LOOKUP_TABLE default
0.5
"""
    resultado = processar_conteudo_vtk(vtk_invalido, nome_arquivo="invalido.vtk")
    val = resultado["validacao"]

    assert val["valido"] is False
    assert val["status"] == "INCONSISTENTE"
    assert val["extremos_validos"] is False
    assert val["raios_completos"] is False
    assert len(val["inconsistencias"]) >= 2


def test_exportacao_csvs_obrigatorios(tmp_path: Path) -> None:
    """
    Verifica a geração dos arquivos CSV obrigatórios do Módulo A:
    1. tabela_consolidada_6_modelos.csv
    2. segmentos_<nome_modelo>.csv com as colunas:
       id, u, v, raio, comprimento_3d, mx, my, mz
    """
    pasta = obter_diretorio_modelos()

    caminho_consolidado = tmp_path / "tabela_consolidada_6_modelos.csv"
    linhas = gerar_tabela_consolidada(
        pasta_modelos=pasta,
        caminho_saida=caminho_consolidado,
    )
    assert caminho_consolidado.exists()
    assert len(linhas) == 6

    modelos = processar_todos_modelos(pasta_modelos=pasta)
    caminho_seg = exportar_segmentos_csv(
        modelos[0],
        nome_modelo="Nterm016",
        pasta_saida=tmp_path,
    )
    assert caminho_seg.exists()
    assert caminho_seg.name == "segmentos_Nterm016.csv"

    with caminho_seg.open("r", encoding="utf-8") as f_csv:
        leitor = csv.DictReader(f_csv)
        assert leitor.fieldnames == [
            "id",
            "u",
            "v",
            "raio",
            "comprimento_3d",
            "mx",
            "my",
            "mz",
        ]
        registros = list(leitor)
        assert len(registros) == 31
