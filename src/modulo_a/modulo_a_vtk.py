"""
Módulo A — Modelagem Discreta, Geometria 3D e Validação dos Dados VTK.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)

Este módulo implementa exclusivamente o núcleo matemático, estrutural e de
exportação tabular (sem dependências de interface gráfica), utilizando apenas
estruturas elementares do Python (listas, dicionários, conjuntos, tuplas,
laços e contadores simples), sem classes de árvores (TreeNode) ou bibliotecas
de grafos.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

try:
    from .a1_leitura_vtk import (
        ARQUIVOS_MODELOS_VTK,
        TABELA_REFERENCIA,
        ler_arquivo_vtk,
        ler_conteudo_vtk,
        listar_arquivos_vtk,
        obter_referencia_modelo,
        resolver_pasta_modelos,
        transformar_nome_do_arquivo,
    )
    from .a2_geometria_3d import (
        calcular_comprimento,
        calcular_estatisticas_descritivas,
        calcular_ponto_medio,
        incorporar_geometria,
    )
    from .a3_validacao import validar_dados_vtk
    from .a4_estrutura import (
        comparar_com_tabela_referencia,
        identificar_estrutura_pontos,
    )
except ImportError:
    from a1_leitura_vtk import (
        ARQUIVOS_MODELOS_VTK,
        TABELA_REFERENCIA,
        ler_arquivo_vtk,
        ler_conteudo_vtk,
        listar_arquivos_vtk,
        obter_referencia_modelo,
        resolver_pasta_modelos,
        transformar_nome_do_arquivo,
    )
    from a2_geometria_3d import (
        calcular_comprimento,
        calcular_estatisticas_descritivas,
        calcular_ponto_medio,
        incorporar_geometria,
    )
    from a3_validacao import validar_dados_vtk
    from a4_estrutura import (
        comparar_com_tabela_referencia,
        identificar_estrutura_pontos,
    )


# ==============================================================================
# Pipeline Completo de Processamento (A1 + A2 + A3 + A4)
# ==============================================================================

def processar_conteudo_vtk(
    conteudo: str,
    nome_arquivo: str = "modelo.vtk",
) -> dict[str, Any]:
    """
    Executa encadeadamente as etapas A1 (leitura), A2 (geometria 3D),
    A3 (validação) e A4 (identificação estrutural e conferência com Tabela 1)
    a partir do conteúdo em texto de um arquivo VTK.
    """
    dados = ler_conteudo_vtk(conteudo, nome_arquivo=nome_arquivo)
    pontos = dados["pontos"]
    segmentos = dados["segmentos"]

    incorporar_geometria(pontos, segmentos)
    validacao = validar_dados_vtk(dados)
    estrutura = identificar_estrutura_pontos(pontos, segmentos)
    comparacao = comparar_com_tabela_referencia(dados["arquivo"], estrutura)

    raios_validos = [
        float(s["raio"]) for s in segmentos if s.get("raio") is not None
    ]
    comprimentos_validos = [
        float(s["comprimento_3d"])
        for s in segmentos
        if s.get("comprimento_3d") is not None
    ]

    estatisticas_raio = calcular_estatisticas_descritivas(raios_validos)
    estatisticas_comprimento = calcular_estatisticas_descritivas(comprimentos_validos)

    return {
        "arquivo": dados["arquivo"],
        "codigo_modelo": dados["codigo_modelo"],
        "cabecalho": dados["cabecalho"],
        "pontos": pontos,
        "segmentos": segmentos,
        "validacao": validacao,
        "estrutura": estrutura,
        "comparacao_tabela_1": comparacao,
        "estatisticas": {
            "raio": estatisticas_raio,
            "comprimento_3d": estatisticas_comprimento,
        },
    }


def processar_modelo_vtk(caminho_arquivo: str | Path) -> dict[str, Any]:
    """
    Executa encadeadamente as etapas A1, A2, A3 e A4 para um arquivo .vtk em disco.
    """
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo VTK não encontrado: {caminho}")

    conteudo = caminho.read_text(encoding="utf-8", errors="replace")
    resultado = processar_conteudo_vtk(conteudo, nome_arquivo=caminho.name)
    resultado["caminho_arquivo"] = str(caminho)
    return resultado


def processar_todos_modelos(
    pasta_modelos: str | Path = "dados_modelos3D/",
) -> list[dict[str, Any]]:
    """
    Processa todos os 6 arquivos VTK da coleção fornecida a partir do diretório
    configurado (padrão 'dados_modelos3D/').
    """
    diretorio = resolver_pasta_modelos(pasta_modelos)
    resultados: list[dict[str, Any]] = []

    for nome_vtk in ARQUIVOS_MODELOS_VTK:
        caminho_vtk = diretorio / nome_vtk
        if not caminho_vtk.exists():
            raise FileNotFoundError(
                f"Arquivo obrigatório '{nome_vtk}' não encontrado em '{diretorio}'."
            )
        resultados.append(processar_modelo_vtk(caminho_vtk))

    return resultados


# ==============================================================================
# Saídas Obrigatórias do Módulo A (Exportação CSV)
# ==============================================================================

def gerar_tabela_consolidada(
    pasta_modelos: str | Path = "dados_modelos3D/",
    caminho_saida: str | Path | None = "resultados/tabela_consolidada_6_modelos.csv",
) -> list[dict[str, Any]]:
    """
    Saída Obrigatória A: Processa os seis modelos VTK, monta a tabela
    consolidada comparando os valores obtidos com a Tabela 1 de referência
    e salva em 'resultados/tabela_consolidada_6_modelos.csv'.
    """
    modelos_processados = processar_todos_modelos(pasta_modelos=pasta_modelos)
    linhas_consolidadas: list[dict[str, Any]] = []

    for mod in modelos_processados:
        est = mod["estrutura"]
        val = mod["validacao"]
        comp = mod["comparacao_tabela_1"]
        stats_r = mod["estatisticas"]["raio"]
        stats_l = mod["estatisticas"]["comprimento_3d"]

        linha = {
            "arquivo_vtk": mod["arquivo"],
            "modelo": mod["codigo_modelo"],
            "nterm_referencia": comp["nterm_esperado"],
            "pontos_V": est["num_pontos_V"],
            "pontos_V_esperado": comp["V_esperado"],
            "segmentos_E": est["num_segmentos_E"],
            "segmentos_E_esperado": comp["E_esperado"],
            "terminais_T": est["num_terminais_T"],
            "terminais_T_esperado": comp["T_esperado"],
            "bifurcacoes_B": est["num_bifurcacoes_B"],
            "bifurcacoes_B_esperado": comp["B_esperado"],
            "ponto_entrada_id": est["ponto_entrada_id"],
            "pontos_grau_inesperado": len(est["pontos_grau_inesperado"]),
            "validacao_a3": val["status"],
            "coincide_tabela_1": comp["coincide_tabela_1"],
            "raio_min": round(stats_r["minimo"], 7),
            "raio_max": round(stats_r["maximo"], 7),
            "raio_medio": round(stats_r["media"], 7),
            "raio_mediana": round(stats_r["mediana"], 7),
            "comprimento_3d_min": round(stats_l["minimo"], 7),
            "comprimento_3d_max": round(stats_l["maximo"], 7),
            "comprimento_3d_medio": round(stats_l["media"], 7),
            "comprimento_3d_mediana": round(stats_l["mediana"], 7),
        }
        linhas_consolidadas.append(linha)

    if caminho_saida is not None and linhas_consolidadas:
        destino = Path(caminho_saida)
        destino.parent.mkdir(parents=True, exist_ok=True)
        colunas = list(linhas_consolidadas[0].keys())
        with destino.open("w", newline="", encoding="utf-8") as f_csv:
            escritor = csv.DictWriter(f_csv, fieldnames=colunas)
            escritor.writeheader()
            escritor.writerows(linhas_consolidadas)

    return linhas_consolidadas


def exportar_segmentos_csv(
    modelo_ou_segmentos: dict[str, Any] | list[dict[str, Any]],
    nome_modelo: str | None = None,
    pasta_saida: str | Path = "resultados",
) -> Path:
    """
    Saída Obrigatória A: Exporta o arquivo CSV completo de segmentos de um
    modelo escolhido ('resultados/segmentos_<nome_modelo>.csv') contendo as
    colunas obrigatórias:
        id, u, v, raio, comprimento_3d, mx, my, mz
    """
    if isinstance(modelo_ou_segmentos, dict):
        segmentos = modelo_ou_segmentos.get("segmentos", [])
        if not nome_modelo:
            nome_modelo = modelo_ou_segmentos.get(
                "codigo_modelo",
                transformar_nome_do_arquivo(modelo_ou_segmentos.get("arquivo", "modelo")),
            )
    else:
        segmentos = modelo_ou_segmentos
        if not nome_modelo:
            nome_modelo = "modelo"

    codigo_limpo = transformar_nome_do_arquivo(str(nome_modelo))
    diretorio_saida = Path(pasta_saida)
    diretorio_saida.mkdir(parents=True, exist_ok=True)
    caminho_csv = diretorio_saida / f"segmentos_{codigo_limpo}.csv"

    colunas = ["id", "u", "v", "raio", "comprimento_3d", "mx", "my", "mz"]

    with caminho_csv.open("w", newline="", encoding="utf-8") as f_csv:
        escritor = csv.DictWriter(f_csv, fieldnames=colunas)
        escritor.writeheader()
        for seg in segmentos:
            escritor.writerow(
                {
                    "id": seg["id"],
                    "u": seg["u"],
                    "v": seg["v"],
                    "raio": f"{float(seg['raio']):.7f}"
                    if seg.get("raio") is not None
                    else "",
                    "comprimento_3d": f"{float(seg['comprimento_3d']):.7f}"
                    if seg.get("comprimento_3d") is not None
                    else "",
                    "mx": f"{float(seg['mx']):.7f}"
                    if seg.get("mx") is not None
                    else "",
                    "my": f"{float(seg['my']):.7f}"
                    if seg.get("my") is not None
                    else "",
                    "mz": f"{float(seg['mz']):.7f}"
                    if seg.get("mz") is not None
                    else "",
                }
            )

    return caminho_csv


def formatar_resumo_modelo(resultado_modelo: dict[str, Any]) -> str:
    """
    Formata um resumo matemático textual do modelo processado (compatível com
    a Seção 8.2 do enunciado do TP CCO Explorer).
    """
    est = resultado_modelo["estrutura"]
    val = resultado_modelo["validacao"]
    comp = resultado_modelo["comparacao_tabela_1"]
    stats_r = resultado_modelo["estatisticas"]["raio"]
    stats_l = resultado_modelo["estatisticas"]["comprimento_3d"]

    linhas = [
        "CCO EXPLORER -- RESUMO MATEMATICO (MODULO A)",
        f"Arquivo:             {resultado_modelo['arquivo']}",
        f"Pontos (|V|):        {est['num_pontos_V']}",
        f"Segmentos (|E|):     {est['num_segmentos_E']}",
        f"Terminais (T):       {est['num_terminais_T']}",
        f"Bifurcacoes (B):     {est['num_bifurcacoes_B']}",
        f"Ponto de entrada:    {est['ponto_entrada_id']} (confirmado ID 0: {est['confirmado_id_zero']})",
        (
            f"Comprimentos 3D:     min={stats_l['minimo']:.6f}, "
            f"max={stats_l['maximo']:.6f}, media={stats_l['media']:.6f}, "
            f"mediana={stats_l['mediana']:.6f} (unidades originais VTK)"
        ),
        (
            f"Raios por segmento:  min={stats_r['minimo']:.6f}, "
            f"max={stats_r['maximo']:.6f}, media={stats_r['media']:.6f}, "
            f"mediana={stats_r['mediana']:.6f} (unidades originais VTK)"
        ),
        f"Conferencia Tab. 1:  {'COINCIDE EXATAMENTE' if comp['coincide_tabela_1'] else 'DIVERGENTE'}",
        f"Validacao A3:        {val['status']} ({'; '.join(val['mensagens'])})",
    ]
    return "\n".join(linhas)


def main() -> None:
    """
    Interface de linha de comando para execução direta do Módulo A:
    processa os 6 modelos VTK, gera a tabela consolidada e exporta os CSVs
    de segmentos.
    """
    parser = argparse.ArgumentParser(
        description="CCO Explorer — Módulo A (Modelagem Discreta e Validação VTK)"
    )
    parser.add_argument(
        "--entrada",
        type=str,
        default="dados_modelos3D/",
        help="Caminho relativo da pasta com os modelos VTK (padrão: dados_modelos3D/)",
    )
    parser.add_argument(
        "--modelo",
        type=str,
        default="tree3D_Nterm016.vtk",
        help="Nome do modelo VTK para exportar os segmentos (padrão: tree3D_Nterm016.vtk)",
    )
    parser.add_argument(
        "--saida",
        type=str,
        default="resultados",
        help="Pasta de saída para os arquivos CSV (padrão: resultados)",
    )
    args = parser.parse_args()

    pasta_saida = Path(args.saida)
    caminho_consolidado = pasta_saida / "tabela_consolidada_6_modelos.csv"
    gerar_tabela_consolidada(
        pasta_modelos=args.entrada,
        caminho_saida=caminho_consolidado,
    )

    diretorio_vtk = resolver_pasta_modelos(args.entrada)
    caminho_modelo = diretorio_vtk / args.modelo
    resultado = processar_modelo_vtk(caminho_modelo)
    caminho_seg = exportar_segmentos_csv(resultado, pasta_saida=pasta_saida)

    print(formatar_resumo_modelo(resultado))
    print(f"\nTabela consolidada salva em: {caminho_consolidado}")
    print(f"Segmentos do modelo salvos em: {caminho_seg}")


if __name__ == "__main__":
    main()
