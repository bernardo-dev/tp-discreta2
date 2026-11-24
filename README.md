# CCO Explorer

Este repositório contém o trabalho prático da disciplina **BCC102 — Matemática
Discreta II**, do período 2026.2, do Departamento de Computação da Universidade
Federal de Ouro Preto (UFOP).

O **CCO Explorer** analisa modelos tridimensionais de árvores vasculares geradas
pelo método CCO, representando seus pontos e segmentos com conceitos de
Matemática Discreta e produzindo validações, geometria 3D e visualizações
reproduzíveis. A referência completa do trabalho é o arquivo
[`CCO_Explorer_TP_Matematica_Discreta_II-v2.pdf`](CCO_Explorer_TP_Matematica_Discreta_II-v2.pdf).

Os dados fornecidos estão em `data/dados_modelos3D/`. Cada modelo é um arquivo
VTK com seis variantes de Nterm (16, 32, 64, 128, 256 e 512). Os arquivos PNG
incluídos são apenas ilustrativos; os resultados devem ser calculados a partir
dos VTK.

## Estrutura do projeto

- `src/modulo_a/`: núcleo do Módulo A (leitura VTK, geometria 3D, validação e
  identificação estrutural).
- `src/modulo_a/modulo_a_vtk.py`: interface de linha de comando do Módulo A.
- `app_modulo_a.py`: interface gráfica interativa com Streamlit e Plotly.
- `data/dados_modelos3D/`: modelos VTK e imagens PNG fornecidos.
- `resultados/`: arquivos CSV gerados pelo programa.
- `tests/`: testes automatizados com pytest.
- `requirements.txt`: dependências Python do projeto.

## Requisitos

- Python 3.
- Terminal ou prompt de comandos.
- Os modelos VTK encontrados em `data/dados_modelos3D/`.

Não é necessário instalar bibliotecas adicionais para executar o núcleo do
Módulo A pela linha de comando. Os dados são processados com recursos padrão
do Python.

## Executar apenas pela linha de comando

Execute os comandos a partir da raiz deste repositório.

No Windows (Prompt de Comando ou PowerShell):

```powershell
python src\modulo_a\modulo_a_vtk.py
```

No Linux ou macOS:

```bash
python3 src/modulo_a/modulo_a_vtk.py
```

O comando padrão:

1. processa os seis modelos VTK;
2. gera `resultados/tabela_consolidada_6_modelos.csv`;
3. processa `tree3D_Nterm016.vtk`;
4. gera `resultados/segmentos_Nterm016.csv`;
5. imprime o resumo matemático no terminal.

É possível informar outra pasta de entrada, modelo e pasta de saída:

```powershell
python src\modulo_a\modulo_a_vtk.py --entrada data\dados_modelos3D --modelo tree3D_Nterm128.vtk --saida resultados
```

```bash
python3 src/modulo_a/modulo_a_vtk.py --entrada data/dados_modelos3D --modelo tree3D_Nterm128.vtk --saida resultados
```

Para consultar todas as opções:

```powershell
python src\modulo_a\modulo_a_vtk.py --help
```

Os parâmetros `--entrada`, `--modelo` e `--saida` usam caminhos relativos ao
diretório atual. Assim, o programa não depende de caminhos absolutos específicos
do computador.

## Executar os testes pela linha de comando

Após instalar as dependências do arquivo `requirements.txt`, os testes podem
ser executados com:

```powershell
python -m pytest tests
```

## Interface gráfica com Streamlit

A interface gráfica permite selecionar os modelos VTK, consultar pontos e
segmentos, visualizar a árvore vascular em 3D e exportar os dados processados.
Ela deve ser executada em um ambiente virtual para isolar as dependências.

### 1. Criar o ambiente virtual

Na raiz do repositório, no Windows:

```powershell
python -m venv .venv
```

No Linux ou macOS:

```bash
python3 -m venv .venv
```

### 2. Ativar o ambiente virtual

Windows — Prompt de Comando:

```bat
.venv\Scripts\activate.bat
```

Windows — PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Linux ou macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar as dependências

Com o ambiente virtual ativado, atualize o `pip` e instale todos os pacotes de
`requirements.txt`:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

O arquivo `requirements.txt` inclui:

- `pandas` e `numpy`: manipulação e cálculo dos dados;
- `plotly`: renderização interativa do modelo 3D;
- `streamlit`: interface gráfica;
- `pytest`: testes automatizados.

### 4. Executar a interface gráfica

Ainda na raiz do repositório:

```powershell
python -m streamlit run app_modulo_a.py
```

Ou, usando o executável do ambiente ativo:

```powershell
streamlit run app_modulo_a.py
```

O Streamlit exibirá um endereço local, normalmente `http://localhost:8501`.
Abra esse endereço no navegador. Para encerrar o servidor, pressione `Ctrl+C`
no terminal.

### 5. Desativar o ambiente virtual

Quando terminar:

```powershell
deactivate
```

## Resultados gerados

Os resultados tabulares ficam em `resultados/`. O programa gera:

- `tabela_consolidada_6_modelos.csv`: resumo dos seis modelos;
- `segmentos_Nterm016.csv` ou arquivo equivalente: atributos dos segmentos do
  modelo selecionado.

Os valores exibidos são calculados a partir dos VTK nas unidades originais dos
arquivos. Os raios não são convertidos para metros ou milímetros, pois o
enunciado não define uma unidade física.