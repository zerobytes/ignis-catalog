# Catálogo Ignis

Catálogo comunitário gratuito de assets para a [Ignis](https://github.com/zerobytes/ignis).
[English](README.md)

Começamos com **20 materiais procedurais editáveis**: 12 mármores, 4 rochas e
4 superfícies básicas. As receitas somam **38.609 bytes**. Veja os arquivos no
[índice de materiais](README.md#browse-and-use).

**[Abrir o portal de assets](https://ignis.web.app/catalog/?lang=pt)** no site da
Ignis, com busca, filtros e prévia interativa pelos shaders nativos da engine.
[Espelho no GitHub Pages](https://zerobytes.github.io/ignis/catalog/?lang=pt).

Baixe o `.ignis-material` e carregue pelo painel **Aparência → Biblioteca de
materiais** de uma Ignis compatível. Cada `asset.json` informa licença, créditos,
origem, hash e requisitos de formato. O material pode continuar procedural em
runtime ou gerar mapas fixos pelo editor. A geração acontece na engine.

## Como manter gratuito

- Receitas pequenas, registros e miniaturas leves no repositório público.
- Pacotes grandes em versões do GitHub Releases ou hospedados pelos autores.
- O catálogo registra links, tamanho/hash e espelhos opcionais. Não precisamos
  centralizar todos os assets e downloads na nossa conta.
- Portal estático no site da Ignis com busca, filtros e prévias; instalação integrada na
  engine em incremento próprio. Nenhum serviço pago foi ativado.

É possível começar sem custo; armazenamento/tráfego ilimitados para sempre não
são uma garantia. [Estratégia e limites oficiais](docs/storage.md).

## Créditos e participação

Assets próprios, metadados e documentação: **CC BY 4.0**. Uso comercial permitido
com créditos, link da licença e indicação de mudanças. Scripts: MIT. A licença
da engine é separada. Contribuições preservam autoria e precisam de licença
aceita, fonte editável e evidência de origem.

A base oferece manifests, busca local, validação de integridade e CI. O portal
visual já está publicado; instalação integrada segue no [roadmap](docs/roadmap.md). Os arquivos
iniciais foram copiados sem alterar bytes. Seus commits de origem na engine
estavam locais/não publicados no momento da transferência, condição registrada
explicitamente; o catálogo inclui as receitas completas. Os exemplos/presets
da engine foram preservados para migração coordenada posterior.

```sh
python3 tools/catalog.py list
python3 tools/catalog.py validate
python3 tools/catalog.py build --check
python3 -m unittest discover -s tests -v
```

[Contribuir](CONTRIBUTING.md) · [Formato](docs/format.md) · [Licenças](LICENSE)
