
# Termo Solver
Script em Python para solucionar partidas de [term.ooo](https://term.ooo/), criado como ideia para automatizar e estudar estrategias de resolução do jogo.

## Sobre o projeto
Não existe um motivo especial nem uma história mirabolante para esse projeto ter nascido, eu apenas achei que seria legal pensar em uma solução automatizada para partidas de termo.

Atualmente o projeto funciona no terminal e ainda deve passar por modificações, a ideia é melhorar a taxa de sucesso das partidas automaticas mantendo um tempo de resposta rápido.

## Status atual
- Versão inicial jogável no terminal.
- Segunda versão do modo automático.
- Primeira versão da partida assistida.
- Teste para avaliar a eficiência e eficácia do algoritmo.

## Resultado atual
~~Em testes locais de pequena escala, a taxa de sucesso observada esta em torno de **~50%**. Isso se deve ao fato de que ainda não existe nenhuma lógica por trás da palavra da próxima tentativa, é apenas uma escolha aleatória.~~

Atualmente o script consegue finalizar cada partida em cerca de 0.025s com uma precisão maior que **94%**.  O experimento foi realizado usando o modo `--test` com 100000 execuções, gerando uma palavra alvo diferente de maneira aleatória por partida.

```shell
	(venv) PS C:\Codigos\termo-solver> python src/main.py --test 100000
	[100000/100000] palavra: chapa | tentativas: 6 | ✓

	resultado: 94471/100000 (94.5% de acerto) | derrotas: 5529
	tempo médio por partida: 0.024244s

	  1 tentativa(s):  14 (0.0%)
	  2 tentativa(s): █ 3110 (3.1%)
	  3 tentativa(s): ██████████████ 26584 (26.6%)
	  4 tentativa(s): ████████████████████ 35766 (35.8%)
	  5 tentativa(s): ███████████ 20672 (20.7%)
	  6 tentativa(s): ████ 8325 (8.3%)
```
Porém após deixar esse teste executando por vários minutos eu percebi que na verdade não tem sentido em calcular a precisão em mais execuções sendo que a mesma palavra jogada várias vezes sempre terá a mesma sequencia de escolhas em cada tentativa.

Ou seja, para ter esse exato mesmo resultado de **94.5%** em menos tempo bastava executar cada palavra do dicionário, uma por partida e deixar o algoritmo tentar solucionar cada uma

```shell
	(venv) PS C:\Codigos\termo-solver> python src/main.py --test
	[5480 /5480 ] palavra: zurro | tentativas: 6 | ✓

	resultado: 5180/5480 (94.5% de acerto) | derrotas: 300
	tempo médio por partida: 0.022421s

	  1 tentativa(s):  1 (0.0%)
	  2 tentativa(s): █ 169 (3.1%)
	  3 tentativa(s): ██████████████ 1462 (26.7%)
	  4 tentativa(s): ████████████████████ 1953 (35.6%)
	  5 tentativa(s): ███████████ 1132 (20.7%)
	  6 tentativa(s): ████ 463 (8.4%
```
As vezes a vida é dura...

## Modos de execução
O solver possui os modos:
-  `default`: jogo manual no terminal.
-  `assisted`: base do modo assistido (versao inicial).
-  `auto`: tentativas automaticas (versao inicial).

Também é possível executar o teste de acurácia da solução automática com o arg:

-  `test`: executa uma vez com cada palavra disponível no arquivo valid_inputs.txt .

## Como executar

### 1. Clonar o repositorio
```bash

git  clone <URL_DO_REPOSITORIO>

cd  termo-solver

```

### 2. Criar e ativar ambiente virtual (opcional, recomendado)
Windows (PowerShell):
```powershell

python -m venv venv

.\venv\Scripts\Activate.ps1

```

Linux/macOS:
```bash

python3  -m  venv  venv

source  venv/bin/activate

```

### 3. Executar
```bash

python  src/main.py  --mode  default

python  src/main.py  --mode  assisted

python  src/main.py  --mode  auto

python  src/main.py  --test

```

## Feedback no terminal
O retorno das letras usa os simbolos:
-  `#`: letra correta na posicao correta.
-  `*`: letra existe na palavra, mas em outra posicao.
-  `-`: letra ausente na resposta.

## Dicionário
Arquivos principais:
-  `src/dictionary/dict-ptbr.txt`: base de palavras.
-  `src/dictionary/valid-inputs.txt`: entradas validas usadas pelo solver.
-  `src/dictionary/dict-sanitizer.py`: script para gerar entradas validas (5 letras, em minúsculas, sem duplicatas).

Para regenerar o arquivo de entradas validas:

```bash

python  src/dictionary/dict-sanitizer.py

```

## Estrutura do projeto
```text
	src
	├── dictionary
	│   ├── dict-ptbr.txt
	│   ├── dict-sanitizer.py
	│   └── valid-inputs.txt
	├── find-strategy.py
	├── losses
	│   └── losses.txt
	└── main.py
```

## Roadmap
- Melhorar a estratégia de escolha de palavras no modo automático.
- ~~Aumentar a taxa de sucesso acima do baseline atual (90% em 100.000 execuções).~~
- Refatorar trechos do código para uma melhor performance.
- Evoluir da interface exclusivamente em terminal para uma interface visual.