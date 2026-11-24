"""
Módulo A1 — Leitura e Modelagem Discreta dos Arquivos VTK.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

# ==============================================================================
# A1. Leitura e Modelagem Discreta dos Arquivos VTK
# ==============================================================================

# Ordem dos 6 arquivos VTK fornecidos na pasta zip
ARQUIVOS_MODELOS_VTK: tuple[str, ...] = (
    "tree3D_Nterm016.vtk",
    "tree3D_Nterm032.vtk",
    "tree3D_Nterm064.vtk",
    "tree3D_Nterm128.vtk",
    "tree3D_Nterm256.vtk",
    "tree3D_Nterm512.vtk",
)

# Tabela 1 de referência oficial do enunciado do TP para conferência estrutural
# nterm = quantidade de terminais
# V = quantidade de vértices (vertices)
# E = quantidade de segmentos (edges)
# T = quantidade de terminais (out_degree == 0)
# B = quantidade de bifurcações (out_degree == 2)
TABELA_REFERENCIA: dict[str, dict[str, int]] = {
    "tree3D_Nterm016.vtk": {"nterm": 16, "V": 32, "E": 31, "T": 16, "B": 15},
    "tree3D_Nterm032.vtk": {"nterm": 32, "V": 64, "E": 63, "T": 32, "B": 31},
    "tree3D_Nterm064.vtk": {"nterm": 64, "V": 128, "E": 127, "T": 64, "B": 63},
    "tree3D_Nterm128.vtk": {"nterm": 128, "V": 256, "E": 255, "T": 128, "B": 127},
    "tree3D_Nterm256.vtk": {"nterm": 256, "V": 512, "E": 511, "T": 256, "B": 255},
    "tree3D_Nterm512.vtk": {"nterm": 512, "V": 1024, "E": 1023, "T": 512, "B": 511},
}


def transformar_nome_do_arquivo(nome_arquivo: str) -> str:
    """
    Transforma o nome do arquivo VTK em um código curto (ex.: 'Nterm016') para
    facilitar a identificação e manipulação dos modelos.
    """
    nome_limpo = Path(nome_arquivo).stem
    # Remover prefixo 'tree3D_' se presente, mantendo apenas o código curto
    if nome_limpo.startswith("tree3D_"):
        return nome_limpo.replace("tree3D_", "", 1)
    return nome_limpo


def obter_referencia_modelo(nome_modelo_ou_arquivo: str) -> dict[str, int] | None:
    """
    Busca os valores esperados na Tabela 1 de referência a partir do nome do
    arquivo ('tree3D_Nterm016.vtk') ou do código curto ('Nterm016').

    Retorna um dicionário com os valores esperados ou None se não houver
    """

    nome_base = Path(nome_modelo_ou_arquivo).name
    # Verifica se o nome base está na TABELA_REFERENCIA diretamente
    if nome_base in TABELA_REFERENCIA:
        return dict(TABELA_REFERENCIA[nome_base])
    # Se não, tenta transformar o nome base em código curto e verificar novamente
    codigo = transformar_nome_do_arquivo(nome_base)
    arquivo = f"tree3D_{codigo}.vtk"
    if arquivo in TABELA_REFERENCIA:
        return dict(TABELA_REFERENCIA[arquivo])

    return None


def resolver_pasta_modelos(pasta_modelos: str | Path = "dados_modelos3D/") -> Path:
    """
    Resolve o caminho relativo da pasta contendo os arquivos .vtk sem precisar
    de caminho absoluto.

    Se o diretório padrão 'dados_modelos3D/' for informado e os arquivos
    estiverem em 'data/dados_modelos3D/' (layout padrão), localiza
    automaticamente a subpasta.
    """
    caminho = Path(pasta_modelos)
    # Verifica se o caminho existe e é um diretório válido
    if caminho.exists() and caminho.is_dir():
        return caminho

    # Verifica se a pasta alternativa data/ contém o diretório especificado
    alternativa_data = Path("data") / caminho
    if alternativa_data.exists() and alternativa_data.is_dir():
        return alternativa_data

    # Verifica se a pasta alternativa padrão data/dados_modelos3D/ existe
    alternativa_Padrao = Path("data") / "dados_modelos3D"
    if caminho.name == "dados_modelos3D" and alternativa_Padrao.exists():
        return alternativa_Padrao

    # Se nenhuma das opções acima for válida, retorna o caminho original informado
    return caminho


def listar_arquivos_vtk(pasta_modelos: str | Path = "dados_modelos3D/") -> list[Path]:
    """
    Lista os arquivos .vtk encontrados na pasta configurada, seguindo a
    ordem dos 6 modelos (Nterm016 a Nterm512).
    """
    diretorio = resolver_pasta_modelos(pasta_modelos)
    # Verifica se o diretório existe e é válido antes de listar os arquivos
    if not diretorio.exists() or not diretorio.is_dir():
        return []

    # Lista os arquivos .vtk na ordem dos modelos fornecidos
    # e adiciona quaisquer arquivos extras encontrados na pasta

    arquivos_ordenados: list[Path] = []
    nomes_adicionados: set[str] = set()

    # Adiciona os arquivos na ordem dos modelos
    for nome in ARQUIVOS_MODELOS_VTK:
        caminho_arquivo = diretorio / nome
        if caminho_arquivo.exists() and caminho_arquivo.is_file():
            arquivos_ordenados.append(caminho_arquivo)
            nomes_adicionados.add(caminho_arquivo.name)

    # Adiciona qualquer arquivo .vtk Restante encontrados na pasta
    for arquivo_extra in sorted(diretorio.glob("*.vtk")):
        if arquivo_extra.name not in nomes_adicionados:
            arquivos_ordenados.append(arquivo_extra)

    return arquivos_ordenados


def ler_conteudo_vtk(
    conteudo: str,
    nome_arquivo: str = "modelo.vtk",
) -> dict[str, Any]:
    """
    Requisito A1: Lê o conteúdo textual de um arquivo VTK no formato
    ASCII / DATASET POLYDATA de forma robusta a espaços extras, linhas em
    branco, quebras de linha e cabeçalhos SCALARS / LOOKUP_TABLE em CELL_DATA.

    Extrai:
    - Conjunto de pontos V indexados de 0 a |V| - 1 com coordenadas (x, y, z).
    - Conjunto de segmentos E indexados de 0 a |E| - 1 na ordem exata de LINES,
      armazenando para cada segmento s_i: id (i), extremos orientados (u, v) e
      raio (r_i).
    """
    # Divisão do conteúdo em linhas, ignorando linhas em branco e comentários
    linhas_brutas = conteudo.splitlines()

    # Inicialização de variáveis de controle e armazenamento
    formato_ascii = False
    dataset_polydata = False

    num_pontos_declarado: int | None = None
    tipo_pontos_declarado: str = ""
    num_linhas_declarado: int | None = None
    num_inteiros_linhas_declarado: int | None = None
    num_cell_data_declarado: int | None = None
    nome_atributo_escalar: str = "raio"

    coordenadas_floats: list[float] = []
    registros_lines: list[tuple[int, int, int]] = []
    linhas_malformadas: list[str] = []
    raios_lidos: list[float] = []

    secao_atual: str = "HEADER"

    for linha in linhas_brutas:
        texto = linha.strip()
        if not texto or texto.startswith("#"):
            continue

        tokens = texto.split()
        palavra_chave = tokens[0].upper()

        # Identificação de cabeçalhos de seção do VTK
        if palavra_chave == "ASCII":
            formato_ascii = True
            continue

        if palavra_chave == "DATASET":
            if len(tokens) >= 2 and tokens[1].upper() == "POLYDATA":
                dataset_polydata = True
            continue

        if palavra_chave == "POINTS":
            if len(tokens) >= 2:
                num_pontos_declarado = int(tokens[1])
            if len(tokens) >= 3:
                tipo_pontos_declarado = tokens[2]
            secao_atual = "POINTS"
            continue

        if palavra_chave == "LINES":
            if len(tokens) >= 2:
                num_linhas_declarado = int(tokens[1])
            if len(tokens) >= 3:
                num_inteiros_linhas_declarado = int(tokens[2])
            secao_atual = "LINES"
            continue

        if palavra_chave == "CELL_DATA":
            if len(tokens) >= 2:
                num_cell_data_declarado = int(tokens[1])
            secao_atual = "CELL_DATA"
            continue

        if palavra_chave == "POINT_DATA":
            secao_atual = "POINT_DATA"
            continue

        # Processamento dos dados internos de cada seção
        if secao_atual == "POINTS":
            for tok in tokens:
                coordenadas_floats.append(float(tok))

        elif secao_atual == "LINES":
            # Cada registro na coleção tem o formato: 2 u v
            if len(tokens) == 3:
                try:
                    qtd_vertices = int(tokens[0])
                    u = int(tokens[1])
                    v = int(tokens[2])
                    registros_lines.append((qtd_vertices, u, v))
                except ValueError:
                    linhas_malformadas.append(texto)
            else:
                # Suporte caso haja múltiplos registros ou formato inesperado
                try:
                    inteiros_linha = [int(tok) for tok in tokens]
                    if len(inteiros_linha) >= 3 and inteiros_linha[0] == 2:
                        registros_lines.append(
                            (inteiros_linha[0], inteiros_linha[1], inteiros_linha[2])
                        )
                    else:
                        linhas_malformadas.append(texto)
                except ValueError:
                    linhas_malformadas.append(texto)

        elif secao_atual == "CELL_DATA":
            # Ignora subcabeçalhos SCALARS e LOOKUP_TABLE (case-insensitive)
            if palavra_chave == "SCALARS":
                if len(tokens) >= 2:
                    nome_atributo_escalar = tokens[1]
                continue
            if palavra_chave == "LOOKUP_TABLE":
                continue

            for tok in tokens:
                raios_lidos.append(float(tok))

    # Construção do conjunto/lista de pontos V indexados de 0 a |V| - 1
    pontos: list[dict[str, Any]] = []
    total_triplas = len(coordenadas_floats) // 3
    sobra_floats_pontos = len(coordenadas_floats) % 3

    for idx_ponto in range(total_triplas):
        base = idx_ponto * 3
        x = coordenadas_floats[base]
        y = coordenadas_floats[base + 1]
        z = coordenadas_floats[base + 2]
        pontos.append(
            {
                "id": idx_ponto,
                "x": x,
                "y": y,
                "z": z,
                "coord": (x, y, z),
            }
        )

    # Construção do conjunto/lista de segmentos E indexados de 0 a |E| - 1
    segmentos: list[dict[str, Any]] = []
    for idx_seg, (qtd_vertices, u, v) in enumerate(registros_lines):
        raio_seg: float | None = (
            raios_lidos[idx_seg] if idx_seg < len(raios_lidos) else None
        )
        segmentos.append(
            {
                "id": idx_seg,
                "u": u,
                "v": v,
                "extremos": (u, v),
                "qtd_vertices_registro": qtd_vertices,
                "raio": raio_seg,
            }
        )

    return {
        "arquivo": Path(nome_arquivo).name,
        "codigo_modelo": transformar_nome_do_arquivo(nome_arquivo),
        "cabecalho": {
            "formato_ascii": formato_ascii,
            "dataset_polydata": dataset_polydata,
            "num_pontos_declarado": num_pontos_declarado,
            "tipo_pontos_declarado": tipo_pontos_declarado,
            "num_linhas_declarado": num_linhas_declarado,
            "num_inteiros_linhas_declarado": num_inteiros_linhas_declarado,
            "num_cell_data_declarado": num_cell_data_declarado,
            "nome_atributo_escalar": nome_atributo_escalar,
            "sobra_floats_pontos": sobra_floats_pontos,
            "linhas_malformadas": linhas_malformadas,
            "total_raios_lidos": len(raios_lidos),
        },
        "pontos": pontos,
        "segmentos": segmentos,
        "raios": raios_lidos,
    }


def ler_arquivo_vtk(caminho_arquivo: str | Path) -> dict[str, Any]:
    """
    Requisito A1: Lê um arquivo .vtk a partir do seu caminho relativo no disco.
    """
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo VTK não encontrado: {caminho}")

    conteudo = caminho.read_text(encoding="utf-8", errors="replace")
    dados = ler_conteudo_vtk(conteudo, nome_arquivo=caminho.name)
    dados["caminho_arquivo"] = str(caminho)
    return dados
