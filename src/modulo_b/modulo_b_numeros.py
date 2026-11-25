"""
Módulo B — Teoria dos Números Aplicada à Consulta dos Segmentos (Parte B0).
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)

Integra o núcleo matemático de Teoria dos Números (Parte B0: classes de resíduos
módulo m = 7, validação de partição, Princípio da Casa dos Pombos Generalizado
e consulta determinística) aos dados geométricos processados pelo Módulo A
(`src/modulo_a/modulo_a_vtk.py`), sem dependências de interface gráfica
(Streamlit ou Plotly).
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

try:
    from src.modulo_a.modulo_a_vtk import (
        processar_modelo_vtk,
        resolver_pasta_modelos,
        transformar_nome_do_arquivo,
    )
except ImportError:
    import sys

    RAIZ_PROJETO = Path(__file__).resolve().parents[2]
    if str(RAIZ_PROJETO) not in sys.path:
        sys.path.insert(0, str(RAIZ_PROJETO))
    from src.modulo_a.modulo_a_vtk import (
        processar_modelo_vtk,
        resolver_pasta_modelos,
        transformar_nome_do_arquivo,
    )

try:
    from .b0_1_agrupamento_modular import (
        agrupar_segmentos_por_modulo,
        calcular_medias_geometricas_classe,
    )
    from .b0_2_validacao_particao import validar_particao_modular
    from .b0_3_casa_dos_pombos import analisar_principio_casa_dos_pombos
    from .b0_4_consulta_residuos import (
        consultar_por_residuo,
        gerar_discussao_critica_b04,
    )
except ImportError:
    from b0_1_agrupamento_modular import (
        agrupar_segmentos_por_modulo,
        calcular_medias_geometricas_classe,
    )
    from b0_2_validacao_particao import validar_particao_modular
    from b0_3_casa_dos_pombos import analisar_principio_casa_dos_pombos
    from b0_4_consulta_residuos import (
        consultar_por_residuo,
        gerar_discussao_critica_b04,
    )


# ==============================================================================
# Pipeline Completo da Parte B0 (B0.1 + B0.2 + B0.3 + B0.4)
# ==============================================================================

def processar_parte_b0_segmentos(
    segmentos: list[dict[str, Any]],
    m: int = 7,
    nome_arquivo: str = "tree3D_Nterm128.vtk",
    codigo_modelo: str | None = None,
) -> dict[str, Any]:
    """
    Executa encadeadamente as etapas B0.1 (agrupamento modular e estatísticas),
    B0.2 (validação matemática da partição), B0.3 (Princípio da Casa dos Pombos)
    e B0.4 (consultas determinísticas por resíduo e discussão crítica) sobre uma
    lista de segmentos já processada pelo Módulo A.
    """
    codigo = (
        codigo_modelo
        if codigo_modelo is not None
        else transformar_nome_do_arquivo(nome_arquivo)
    )

    agrupamento = agrupar_segmentos_por_modulo(segmentos, m=m)
    validacao_particao = validar_particao_modular(
        agrupamento,
        total_segmentos_esperado=len(segmentos),
    )
    casa_dos_pombos = analisar_principio_casa_dos_pombos(agrupamento)

    # Pré-calcula as consultas determinísticas B0.4 para cada resto j in {0, ..., m-1}
    consultas_por_residuo: dict[int, dict[str, Any]] = {}
    for j in range(m):
        consultas_por_residuo[j] = consultar_por_residuo(
            segmentos=segmentos,
            resto_j=j,
            m=m,
        )

    discussao_b04 = gerar_discussao_critica_b04(
        nome_arquivo=nome_arquivo,
        total_segmentos=len(segmentos),
        m=m,
    )

    return {
        "arquivo": Path(nome_arquivo).name,
        "codigo_modelo": codigo,
        "modulo_m": m,
        "total_segmentos_E": len(segmentos),
        "agrupamento": agrupamento,
        "tabela_classes": agrupamento["tabela_classes"],
        "validacao_particao": validacao_particao,
        "casa_dos_pombos": casa_dos_pombos,
        "consultas_por_residuo": consultas_por_residuo,
        "discussao_b04": discussao_b04,
    }


def processar_parte_b0_modelo(
    modelo_ou_arquivo: dict[str, Any] | str | Path = "tree3D_Nterm128.vtk",
    pasta_modelos: str | Path = "dados_modelos3D/",
    m: int = 7,
) -> dict[str, Any]:
    """
    Executa a Parte B0 integrando-se diretamente ao Módulo A:
    - Se receber um dicionário de modelo já carregado por `processar_modelo_vtk`,
      reutiliza seus segmentos diretamente;
    - Se receber o nome do arquivo (padrão 'tree3D_Nterm128.vtk') ou caminho
      relativo, localiza o arquivo na pasta configurada (`pasta_modelos`) e
      invoca `processar_modelo_vtk` do Módulo A.
    """
    if isinstance(modelo_ou_arquivo, dict):
        modelo_a = modelo_ou_arquivo
    else:
        caminho_informado = Path(modelo_ou_arquivo)
        if caminho_informado.exists() and caminho_informado.is_file():
            caminho_vtk = caminho_informado
        else:
            diretorio = resolver_pasta_modelos(pasta_modelos)
            nome_arq = caminho_informado.name
            if not nome_arq.endswith(".vtk"):
                codigo = transformar_nome_do_arquivo(nome_arq)
                nome_arq = f"tree3D_{codigo}.vtk"
            caminho_vtk = diretorio / nome_arq

        modelo_a = processar_modelo_vtk(caminho_vtk)

    resultado_b0 = processar_parte_b0_segmentos(
        segmentos=modelo_a["segmentos"],
        m=m,
        nome_arquivo=modelo_a["arquivo"],
        codigo_modelo=modelo_a["codigo_modelo"],
    )
    resultado_b0["modelo_a"] = modelo_a
    return resultado_b0


# ==============================================================================
# Exportação CSV e Resumo Textual da Parte B0
# ==============================================================================

def exportar_classes_modulares_csv(
    resultado_ou_tabela: dict[str, Any] | list[dict[str, Any]],
    nome_modelo: str | None = None,
    m: int | None = None,
    caminho_saida: str | Path | None = None,
    pasta_saida: str | Path = "resultados",
) -> Path:
    """
    Requisito B0.1: Exporta a tabela estruturada das classes de resíduos módulo m
    em arquivo CSV (padrão para Nterm128 e m=7:
    `resultados/b0_classes_mod7_Nterm128.csv`).

    Colunas exportadas:
        classe, resto_j, modulo_m, quantidade, comprimento_3d_medio,
        raio_medio, exemplos_ids
    """
    if isinstance(resultado_ou_tabela, dict):
        tabela = resultado_ou_tabela["tabela_classes"]
        if nome_modelo is None:
            nome_modelo = resultado_ou_tabela.get("codigo_modelo", "Nterm128")
        if m is None:
            m = int(resultado_ou_tabela.get("modulo_m", 7))
    else:
        tabela = resultado_ou_tabela
        if nome_modelo is None:
            nome_modelo = "Nterm128"
        if m is None:
            m = int(tabela[0]["modulo_m"]) if tabela else 7

    codigo_limpo = transformar_nome_do_arquivo(str(nome_modelo))

    if caminho_saida is not None:
        destino = Path(caminho_saida)
    else:
        diretorio_saida = Path(pasta_saida)
        destino = diretorio_saida / f"b0_classes_mod{m}_{codigo_limpo}.csv"

    destino.parent.mkdir(parents=True, exist_ok=True)

    colunas = [
        "classe",
        "resto_j",
        "modulo_m",
        "quantidade",
        "comprimento_3d_medio",
        "raio_medio",
        "exemplos_ids",
    ]

    with destino.open("w", newline="", encoding="utf-8") as f_csv:
        escritor = csv.DictWriter(f_csv, fieldnames=colunas)
        escritor.writeheader()
        for item in tabela:
            exemplos = item.get("exemplos_ids", [])
            exemplos_fmt = " ".join(str(idx) for idx in exemplos)
            escritor.writerow(
                {
                    "classe": item["classe"],
                    "resto_j": item["resto_j"],
                    "modulo_m": item["modulo_m"],
                    "quantidade": item["quantidade"],
                    "comprimento_3d_medio": f"{float(item['comprimento_3d_medio']):.7f}",
                    "raio_medio": f"{float(item['raio_medio']):.7f}",
                    "exemplos_ids": exemplos_fmt,
                }
            )

    return destino


def formatar_resumo_b0(resultado_b0: dict[str, Any]) -> str:
    """
    Formata um resumo matemático e crítico completo da Parte B0 para exibição
    no terminal, na interface gráfica e para apoio ao relatório técnico.
    """
    arq = resultado_b0["arquivo"]
    cod = resultado_b0["codigo_modelo"]
    m = resultado_b0["modulo_m"]
    total_e = resultado_b0["total_segmentos_E"]
    tabela = resultado_b0["tabela_classes"]
    val = resultado_b0["validacao_particao"]
    pcp = resultado_b0["casa_dos_pombos"]
    disc = resultado_b0["discussao_b04"]

    linhas = [
        "==============================================================================",
        f"CCO EXPLORER -- RESUMO MATEMATICO (MODULO B / PARTE B0 - MOD {m})",
        "==============================================================================",
        f"Arquivo VTK:                  {arq} ({cod})",
        f"Total de segmentos (|E|):     {total_e}",
        f"Modulo de congruencia (m):    {m}",
        "",
        "------------------------------------------------------------------------------",
        f"B0.1 -- AGRUPAMENTO MODULAR C_j = {{i : i ≡ j (mod {m})}}",
        "------------------------------------------------------------------------------",
        f"{'Classe':<8} | {'Resto j':<7} | {'|C_j|':<6} | {'Comp. 3D Medio':<16} | {'Raio Medio':<14} | {'Exemplos (5 primeiros IDs)'}",
        "-" * 92,
    ]

    for item in tabela:
        linhas.append(
            f"{item['classe']:<8} | "
            f"{item['resto_j']:<7} | "
            f"{item['quantidade']:<6} | "
            f"{item['comprimento_3d_medio']:<16.7f} | "
            f"{item['raio_medio']:<14.7f} | "
            f"{item['exemplos_str']}"
        )

    linhas.extend(
        [
            "",
            "------------------------------------------------------------------------------",
            "B0.2 -- VALIDACAO MATEMATICA DA PARTICAO",
            "------------------------------------------------------------------------------",
            f"Status da Particao:           {val['status']} (valida={val['particao_valida']})",
            f"Disjuncao par a par:          {val['disjuntas_dois_a_dois']} ({val['num_pares_verificados']} pares C_j ∩ C_k = ∅ verificados)",
            f"Soma das cardinalidades:      sum |C_j| = {val['soma_cardinalidades']} == |E| = {val['total_segmentos_E']} ({val['soma_igual_total']})",
            f"Uniao cobre todo E:           |U C_j| = {val['cardinalidade_uniao']} == {val['total_segmentos_E']} ({val['uniao_cobre_universo']})",
            "",
            "------------------------------------------------------------------------------",
            "B0.3 -- PRINCIPIO DA CASA DOS POMBOS GENERALIZADO (PCP)",
            "------------------------------------------------------------------------------",
            f"Pombos (N = |E|):             {pcp['pombos_N']}",
            f"Gavetas (m):                  {pcp['gavetas_m']}",
            f"Limite inferior teorico:      ceil({pcp['pombos_N']} / {pcp['gavetas_m']}) = {pcp['limite_inferior_pcp']}",
            f"Divisao Euclidiana:           {pcp['pombos_N']} = {pcp['gavetas_m']} * {pcp['quociente_euclidiano']} + {pcp['resto_euclidiano']}",
            f"Maior classe observada:       max |C_j| = {pcp['max_observado']} (min |C_j| = {pcp['min_observado']})",
            f"Classes com |C_j| >= {pcp['limite_inferior_pcp']}:      {', '.join(pcp['classes_no_limite'])} ({pcp['qtd_classes_no_limite']} classes)",
            f"Classes com |C_j| <  {pcp['limite_inferior_pcp']}:      {', '.join(pcp['classes_abaixo_limite'])} ({pcp['qtd_classes_abaixo_limite']} classes)",
            f"Confirmacao max |C_j| >= PCP: {pcp['desigualdade_confirmada']} ({pcp['max_observado']} >= {pcp['limite_inferior_pcp']})",
            "",
            "------------------------------------------------------------------------------",
            "B0.4 -- CONSULTA DETERMINISTICA E DISCUSSAO CRITICA",
            "------------------------------------------------------------------------------",
            disc["texto_completo"],
            "==============================================================================",
        ]
    )

    return "\n".join(linhas)


def main() -> None:
    """
    Interface de linha de comando para execução direta da Parte B0 do Módulo B:
    carrega o modelo VTK (padrão `tree3D_Nterm128.vtk`), realiza o agrupamento
    módulo 7, valida a partição e o limite da Casa dos Pombos, exporta o CSV
    `resultados/b0_classes_mod7_Nterm128.csv` e imprime o resumo no terminal.
    """
    parser = argparse.ArgumentParser(
        description="CCO Explorer — Módulo B / Parte B0 (Teoria dos Números e Classes Modulares)"
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
        default="tree3D_Nterm128.vtk",
        help="Nome do modelo VTK a processar (padrão: tree3D_Nterm128.vtk)",
    )
    parser.add_argument(
        "--modulo",
        type=int,
        default=7,
        help="Módulo m para as classes de resíduos (padrão: 7)",
    )
    parser.add_argument(
        "--saida",
        type=str,
        default="resultados",
        help="Pasta de saída para o arquivo CSV (padrão: resultados)",
    )
    args = parser.parse_args()

    resultado_b0 = processar_parte_b0_modelo(
        modelo_ou_arquivo=args.modelo,
        pasta_modelos=args.entrada,
        m=args.modulo,
    )
    caminho_csv = exportar_classes_modulares_csv(
        resultado_b0,
        pasta_saida=args.saida,
    )

    print(formatar_resumo_b0(resultado_b0))
    print(f"\nTabela B0.1 exportada com sucesso em: {caminho_csv}")


if __name__ == "__main__":
    main()
