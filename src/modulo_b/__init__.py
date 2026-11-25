"""
Pacote do Módulo B — Teoria dos Números Aplicada à Consulta dos Segmentos.
Projeto: CCO Explorer (BCC102 — Matemática Discreta II — UFOP)
"""

from __future__ import annotations

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
from .modulo_b_numeros import (
    exportar_classes_modulares_csv,
    formatar_resumo_b0,
    processar_parte_b0_modelo,
    processar_parte_b0_segmentos,
)

__all__ = [
    "agrupar_segmentos_por_modulo",
    "analisar_principio_casa_dos_pombos",
    "calcular_medias_geometricas_classe",
    "consultar_por_residuo",
    "exportar_classes_modulares_csv",
    "formatar_resumo_b0",
    "gerar_discussao_critica_b04",
    "processar_parte_b0_modelo",
    "processar_parte_b0_segmentos",
    "validar_particao_modular",
]
