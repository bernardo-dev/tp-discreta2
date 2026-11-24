"""
Ponto de Entrada Principal da Interface Gráfica — CCO Explorer.
Disciplina: BCC102 — Matemática Discreta II (UFOP)

Orquestra a navegação entre os cinco módulos do Trabalho Prático (A, B, C, D e E),
mantendo cada módulo e suas respectivas abas organizados em `src/interface/`.
"""

from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="CCO Explorer — Matemática Discreta II (UFOP)",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

paginas = {
    "Módulos do CCO Explorer": [
        st.Page(
            "src/interface/modulo_a/pagina_modulo_a.py",
            title="Módulo A — Modelagem e Geometria 3D",
            icon=":material/account_tree:",
            url_path="modulo_a",
            default=True,
            help=(
                "Leitura dos 6 modelos VTK, cálculo de comprimento euclidiano 3D e ponto médio, "
                "validação estrutural A3, identificação de pontos A4 e renderizador 3D interativo."
            ),
        ),
        st.Page(
            "src/interface/modulo_b/pagina_modulo_b.py",
            title="Módulo B — Teoria dos Números",
            icon=":material/tag:",
            url_path="modulo_b",
            help=(
                "Agrupamento por classes de congruência módulo 7, validação de partição, "
                "Princípio da Casa dos Pombos (B0) e Trilha Eletiva (B1)."
            ),
        ),
        st.Page(
            "src/interface/modulo_c/pagina_modulo_c.py",
            title="Módulo C — Contagem e Recorrências",
            icon=":material/functions:",
            url_path="modulo_c",
            help=(
                "Técnicas de contagem combinatória, Princípio da Inclusão–Exclusão geométrico (C1) "
                "e resolução e validação de relações de recorrência (C2)."
            ),
        ),
        st.Page(
            "src/interface/modulo_d/pagina_modulo_d.py",
            title="Módulo D — Relações e Propriedades",
            icon=":material/hub:",
            url_path="modulo_d",
            help=(
                "Relação pai–filho, matriz de adjacência 32×32 (Nterm016), propriedades, "
                "função pai, fecho transitivo R⁺, ordem parcial e equivalência modular."
            ),
        ),
        st.Page(
            "src/interface/modulo_e/pagina_modulo_e.py",
            title="Módulo E — Integração e Resumo",
            icon=":material/assignment_turned_in:",
            url_path="modulo_e",
            help=(
                "Integração dos módulos, geração do Resumo Matemático CCO Explorer (Seção 8.2) "
                "e acompanhamento dos testes mínimos de aceitação (T1 a T7)."
            ),
        ),
    ]
}

navegacao = st.navigation(paginas, position="sidebar")
navegacao.run()
