"""
Barra Lateral (Controles de Fonte de Dados VTK e Opções de Renderização 3D) — Módulo A.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.interface.cache_dados import (
    carregar_conteudo_upload_em_cache,
    carregar_modelo_em_cache,
)
from src.modulo_a.modulo_a_vtk import (
    listar_arquivos_vtk,
    resolver_pasta_modelos,
)


def renderizar_barra_lateral_modulo_a() -> dict[str, Any]:
    """
    Renderiza os controles na barra lateral para o Módulo A:
    - Seleção da pasta de modelos VTK ou upload de arquivo .vtk avulso;
    - Opções visuais do renderizador 3D (modo de cor, espessura proporcional e escala);
    - Camadas estruturais visíveis (entrada, bifurcações, terminais, pontos médios);
    - Destaque de um segmento específico por identificador i.

    Retorna um dicionário com o modelo ativo processado e as opções selecionadas.
    """
    with st.sidebar:
        st.header("⚙️ Fonte de Dados VTK")
        pasta_informada = st.text_input(
            "Pasta dos modelos VTK:",
            value="dados_modelos3D/",
            help="Informe o caminho relativo da pasta contendo os 6 arquivos .vtk.",
        )

        pasta_resolvida = resolver_pasta_modelos(pasta_informada)
        arquivos_encontrados = listar_arquivos_vtk(pasta_informada)

        if (
            pasta_resolvida.exists()
            and str(pasta_resolvida) != pasta_informada.rstrip("/\\")
        ):
            st.caption(f"📂 Diretório localizado: `{pasta_resolvida.as_posix()}`")

        arquivo_upload = st.file_uploader(
            "Ou envie um arquivo .vtk avulso:",
            type=["vtk"],
            help="Carregue um arquivo .vtk do seu computador para inspeção rápida.",
        )

        usar_upload = False
        if arquivo_upload is not None:
            usar_upload = st.checkbox(
                f"Usar arquivo enviado ({arquivo_upload.name})",
                value=True,
            )

        modelo_ativo: dict[str, Any] | None = None

        if usar_upload and arquivo_upload is not None:
            conteudo_str = arquivo_upload.getvalue().decode("utf-8", errors="replace")
            modelo_ativo = carregar_conteudo_upload_em_cache(
                conteudo_str, arquivo_upload.name
            )
            st.success(f"Modelo carregado via upload: `{arquivo_upload.name}`")
        else:
            if not arquivos_encontrados:
                st.error(
                    f"Nenhum arquivo `.vtk` encontrado em `{pasta_informada}`. "
                    "Verifique o caminho ou faça upload de um arquivo `.vtk`."
                )
                st.stop()

            nomes_opcoes = [arq.name for arq in arquivos_encontrados]
            indice_padrao = (
                nomes_opcoes.index("tree3D_Nterm128.vtk")
                if "tree3D_Nterm128.vtk" in nomes_opcoes
                else 0
            )
            nome_escolhido = st.selectbox(
                "Modelo VTK ativo:",
                options=nomes_opcoes,
                index=indice_padrao,
            )
            caminho_escolhido = next(
                arq for arq in arquivos_encontrados if arq.name == nome_escolhido
            )
            modelo_ativo = carregar_modelo_em_cache(str(caminho_escolhido))

        st.divider()
        st.header("🎨 Opções do Renderizador 3D")

        modo_cor = st.selectbox(
            "Colorir segmentos por:",
            options=[
                "Raio",
                "Comprimento 3D",
                "Cor única (vascular)",
            ],
            index=0,
        )

        espessura_proporcional = st.checkbox(
            "Espessura proporcional ao raio",
            value=True,
            help="Ajusta a largura visual de cada segmento proporcionalmente ao raio r_i.",
        )
        fator_espessura = st.slider(
            "Escala visual de espessura:",
            min_value=0.4,
            max_value=2.5,
            value=1.0,
            step=0.1,
        )

        st.subheader("Camadas Estruturais Visíveis")
        mostrar_entrada = st.checkbox("Ponto de entrada (ID 0)", value=True)
        mostrar_bifurcacoes = st.checkbox("Bifurcações (B)", value=True)
        mostrar_terminais = st.checkbox("Terminais (T)", value=True)
        mostrar_pontos_medios = st.checkbox("Pontos Médios (Mᵢ)", value=False)

        st.divider()
        st.subheader("🔍 Destacar Segmento por ID")
        total_seg = len(modelo_ativo["segmentos"])
        ativar_destaque = st.checkbox(
            "Filtrar/destacar um segmento específico (sᵢ)",
            value=False,
        )
        id_segmento_destaque: int | None = None
        if ativar_destaque and total_seg > 0:
            id_segmento_destaque = int(
                st.number_input(
                    f"ID do segmento i (0 a {total_seg - 1}):",
                    min_value=0,
                    max_value=max(0, total_seg - 1),
                    value=0,
                    step=1,
                )
            )

    return {
        "pasta_informada": pasta_informada,
        "modelo_ativo": modelo_ativo,
        "modo_cor": modo_cor,
        "espessura_proporcional": espessura_proporcional,
        "fator_espessura": fator_espessura,
        "mostrar_entrada": mostrar_entrada,
        "mostrar_bifurcacoes": mostrar_bifurcacoes,
        "mostrar_terminais": mostrar_terminais,
        "mostrar_pontos_medios": mostrar_pontos_medios,
        "id_segmento_destaque": id_segmento_destaque,
    }
