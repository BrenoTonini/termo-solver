# Termo Solver

Script em Python para solucionar partidas de [term.ooo](https://term.ooo/), criado como ideia para automatizar e estudar estrategias de resolução do jogo.

## Sobre o projeto

Não existe um motivo especial nem uma história mirabolante para esse projeto ter nascido, eu apenas achei que seria legal pensar em uma solução automatizada para partidas de termo.

Atualmente o projeto funciona no terminal e ainda deve passar por modificações, a ideia é melhorar a taxa de sucesso das partidas automaticas.

## Status atual

- Versao inicial jogavel no terminal.
- Primeira versao do modo automático.
- Primeira versao da partida assistida.

## Resultado atual

Em testes locais de pequena escala, a taxa de sucesso observada esta em torno de **~50%**. Isso se deve ao fato de que ainda não existe nenhuma lógica por trás da palavra da próxima tentativa, é apenas uma escolha aleatória.

## Modos de execucao

O solver possui os modos:

- `default`: jogo manual no terminal.
- `assisted`: base do modo assistido (versao inicial).
- `auto`: tentativas automaticas (versao inicial).

Também é possível executar o teste de acurácia da solução automática com o arg:

- `test`: executa o modo auto N vezes.

## Como executar

### 1. Clonar o repositorio

```bash
git clone <URL_DO_REPOSITORIO>
cd termo-solver
```

### 2. Criar e ativar ambiente virtual (opcional, recomendado)

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Executar

```bash
python src/main.py --mode default
python src/main.py --mode assisted
python src/main.py --mode auto
```

## Feedback no terminal

O retorno das letras usa os simbolos:

- `#`: letra correta na posicao correta.
- `*`: letra existe na palavra, mas em outra posicao.
- `-`: letra ausente na resposta.

## Dicionario

Arquivos principais:

- `src/dictionary/dict-ptbr.txt`: base de palavras.
- `src/dictionary/valid-inputs.txt`: entradas validas usadas pelo solver.
- `src/dictionary/dict-sanitizer.py`: script para gerar entradas validas (5 letras, em minusculas, sem duplicatas).

Para regenerar o arquivo de entradas validas:

```bash
python src/dictionary/dict-sanitizer.py
```

## Estrutura do projeto

```text
src/
  main.py
  dictionary/
    dict-ptbr.txt
    valid-inputs.txt
    dict-sanitizer.py
```

## Roadmap

- Melhorar a estrategia de escolha de palavras no modo automatico.
- Aumentar a taxa de sucesso acima do baseline atual (90% em 100.000 execuções).
- Refatorar trechos do código para uma melhor performance.
- Evoluir da interface exclusivamente em terminal para uma interface visual.