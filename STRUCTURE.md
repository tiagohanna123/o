# Estrutura do Repositório

```
o/
├── data/                           # Dados e resultados
│   ├── SOLUCOES_CONCRETAS.json     # Soluções dos 10 problemas (JSON)
│   ├── scientific_problems_results.json
│   ├── validation_*.json           # Dados de validação por área
│   └── validation_data.csv
│
├── docs/                           # Documentação
│   ├── pdf/                        # Documentos PDF
│   │   ├── INDEX.md                # Índice de PDFs
│   │   ├── SOLUCOES_10_PROBLEMAS.pdf
│   │   ├── framework/              # PDFs do Modelo X
│   │   └── problemas_cientificos/  # PDFs por tema
│   │       ├── cosmologia/
│   │       ├── fisica_fundamental/
│   │       ├── biologia/
│   │       ├── medicina/
│   │       └── tecnologia/
│   ├── images/                     # Imagens e infográficos
│   │   └── infograficos/
│   ├── api-reference.md
│   ├── getting-started.md
│   └── *.md                        # Outros documentos
│
├── examples/                       # Exemplos de uso
│   ├── basic_usage.py
│   ├── quick_start.py
│   └── validation_official.py
│
├── legacy/                         # Versões anteriores
│   └── v1/
│
├── notebooks/                      # Jupyter notebooks
│
├── scripts/                        # Scripts de geração
│   ├── SOLUCOES_CONCRETAS.py      # Cálculo das soluções
│   ├── generate_pdfs.py           # Geração de PDFs
│   ├── gerar_compartilhaveis.py
│   └── scientific_problems_simulation.py
│
├── src/                            # Código fonte principal
│   ├── model_x/                    # Módulo Modelo X
│   │   ├── __init__.py
│   │   ├── entropy_syntropy.py
│   │   ├── energy_modulation.py
│   │   ├── simulation_engine.py
│   │   ├── visualization.py
│   │   └── utils.py
│   └── o_v2.py
│
├── tests/                          # Testes unitários
│   └── test_*.py
│
├── validation/                     # Scripts e resultados de validação
│   ├── validation_*.py
│   └── validation_report*.txt
│
├── .github/                        # GitHub Actions
│   └── workflows/
│
├── README.md                       # Documentação principal
├── SOLUCOES_10_PROBLEMAS.md       # Soluções em Markdown
├── SCIENTIFIC_PROBLEMS_ANALYSIS.md # Análise detalhada
├── requirements.txt
├── setup.py
└── LICENSE
```

## Arquivos Principais

### Soluções dos 10 Problemas
| Arquivo | Descrição |
|---------|-----------|
| `SOLUCOES_10_PROBLEMAS.md` | Documento principal com todas as soluções |
| `SOLUCOES_CONCRETAS.py` | Código Python com derivações |
| `data/SOLUCOES_CONCRETAS.json` | Dados em formato JSON |
| `docs/pdf/SOLUCOES_10_PROBLEMAS.pdf` | Versão PDF |

### Framework Modelo X
| Arquivo | Descrição |
|---------|-----------|
| `src/model_x/` | Implementação do framework |
| `docs/pdf/framework/` | PDFs do modelo teórico |

### Validação
| Arquivo | Descrição |
|---------|-----------|
| `validation/` | Scripts de validação |
| `data/validation_*.json` | Resultados de validação |
