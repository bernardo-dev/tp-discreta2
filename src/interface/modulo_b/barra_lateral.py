"""
Barra Lateral (Controles de Fonte de Dados VTK, Módulo m e Opções de Renderização 3D) — Módulo B.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

from typing import Any

import streamlit as st

from src.interface.cache_dados import (
    carregar_conteudo_upload_em_cache,
    carregar_modelo_em_cache,
    processar_b0_em_cache,
)
from src.modulo_a.modulo_a_vtk import (
    listar_arquivos_vtk,
    resolver_pasta_modelos,
)


def renderizar_barra_lateral_modulo_b() -> dict[str, Any]:
    """
    Renderiza os controles na barra lateral para o Módulo B (Teoria dos Números):
    - Seleção da pasta de modelos VTK ou upload de arquivo .vtk avulso;
    - Seleção do modelo VTK ativo (padrão oficial da Parte B0: `tree3D_Nterm128.vtk`);
    - Opções visuais do renderizador 3D (modo de exibição das classes, espessura e camadas);
    - Parâmetros modulares (módulo m = 7 e seleção da classe de resíduo C_j destacada).

    Retorna um dicionário com o modelo ativo, o resultado processado da Parte B0
    e as opções selecionadas.
    """
    with st.sidebar:
        st.header("⚙️ Fonte de Dados VTK")
        pasta_informada = st.text_input(
            "Pasta dos modelos VTK:",
            value="dados_modelos3D/",
            key="b0_pasta_modelos",
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
            key="b0_upload_vtk",
            help="Carregue um arquivo .vtk do seu computador para inspeção rápida.",
        )

        usar_upload = False
        if arquivo_upload is not None:
            usar_upload = st.checkbox(
                f"Usar arquivo enviado ({arquivo_upload.name})",
                value=True,
                key="b0_usar_upload",
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
                key="b0_modelo_escolhido",
            )
            caminho_escolhido = next(
                arq for arq in arquivos_encontrados if arq.name == nome_escolhido
            )
            modelo_ativo = carregar_modelo_em_cache(str(caminho_escolhido))

        st.divider()
        st.header("🎨 Opções do Renderizador 3D")

        modo_cor_3d = st.selectbox(
            "Modo de exibição das classes no 3D:",
            options=[
                "Destacar apenas classe selecionada (Cⱼ)",
                "Colorir todas as classes simultaneamente",
            ],
            index=0,
            key="b0_modo_cor_3d",
        )
        colorir_todas_classes = (
            modo_cor_3d == "Colorir todas as classes simultaneamente"
        )

        espessura_proporcional = st.checkbox(
            "Espessura proporcional ao raio",
            value=True,
            key="b0_espessura_prop",
            help="Ajusta a largura visual de cada segmento proporcionalmente ao raio r_i.",
        )
        fator_espessura = st.slider(
            "Escala visual de espessura:",
            min_value=0.4,
            max_value=2.5,
            value=1.0,
            step=0.1,
            key="b0_fator_espessura",
        )

        st.subheader("Camadas Estruturais Visíveis")
        mostrar_entrada = st.checkbox(
            "Ponto de entrada (ID 0)",
            value=True,
            key="b0_mostrar_entrada",
        )
        mostrar_pontos_medios = st.checkbox(
            "Pontos Médios (Mᵢ) da classe destacada",
            value=True,
            key="b0_mostrar_pontos_medios",
        )

        st.divider()
        st.subheader("🔍 Consulta Modular por Classe (B0)")
        modulo_m = int(
            st.number_input(
                "Módulo m (padrão obrigatório B0: m = 7):",
                min_value=2,
                max_value=20,
                value=7,
                step=1,
                key="b0_modulo_m",
                help=(
                    "Define a quantidade m de classes de resíduos "
                    "C_j = {i : i ≡ j (mod m)}."
                ),
            )
        )
        resto_destaque = int(
            st.selectbox(
                f"Destacar classe de resíduo Cⱼ (0 a {modulo_m - 1}):",
                options=list(range(modulo_m)),
                index=0,
                format_func=lambda j: f"Classe C_{j} — i ≡ {j} (mod {modulo_m})",
                key="b0_resto_destaque",
            )
        )

    resultado_b0 = processar_b0_em_cache(
        segmentos=modelo_ativo["segmentos"],
        m=modulo_m,
        nome_arquivo=modelo_ativo["arquivo"],
        codigo_modelo=modelo_ativo["codigo_modelo"],
    )
    resultado_b0["modelo_a"] = modelo_ativo

    return {
        "pasta_informada": pasta_informada,
        "modelo_ativo": modelo_ativo,
        "resultado_b0": resultado_b0,
        "modulo_m": modulo_m,
        "resto_destaque": resto_destaque,
        "colorir_todas_classes": colorir_todas_classes,
        "espessura_proporcional": espessura_proporcional,
        "fator_espessura": fator_espessura,
        "mostrar_entrada": mostrar_entrada,
        "mostrar_pontos_medios": mostrar_pontos_medios,
    }
