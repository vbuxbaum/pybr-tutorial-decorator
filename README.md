# PyBR Image Transformer

CLI educacional que demonstra como evoluir um código até chegar em um pipeline de transformações de imagem usando o padrão Decorator.

## Funcionalidades

- Converter uma imagem para preto e branco (`--black-white`)
- Adicionar uma marca d'água grande e semitransparente (`--watermark-text "Seu Texto"`)
- Girar para a esquerda ou direita em qualquer ângulo (`--rotate-degrees 45 --rotate-direction left`)
- Combinar qualquer uma das opções acima em uma única execução

## Instalação

Crie ou atualize o ambiente virtual (Python 3.13+) e instale as dependências de desenvolvimento:

```bash
uv sync --extra dev
uv pip install -e ".[dev]"
```

Caso prefira `venv` manual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Após a instalação, o comando `pybr-image` fica disponível.

## Uso

```bash
pybr-image caminho/para/imagem.jpg \
  --black-white \
  --watermark-text "PyBR 2025" \
  --rotate-degrees 90 \
  --rotate-direction left \
  --output caminho/resultado.jpg
```

Se `--output` não for informado, o resultado é salvo como `{nome}-transformed{extensão}` ao lado do arquivo original.

## Desenvolvimento

Execute a suíte de testes (com o ambiente ativado):

```bash
source .venv/bin/activate
python -m pytest -q
```

Imagens de exemplo estão em `sample_images/` para experimentação.
