# CLAUDE.md

## Contexto do trabalho

Disciplina: Sistemas Eletricos de Potencia - UFT.

Trabalho: Simulacao Computacional 2026/1.

Programas:

- ANAREDE V13 para fluxo de potencia.
- ANAFAS para curto-circuito.

Sistema:

- IEEE 39 barras, New England, 10 geradores.
- Base: 100 MVA, 60 Hz.
- Enunciado: `docs/simulaçao_2026_1 (1).pdf`.
- Texto extraido do enunciado: `docs/simulacao_2026_1_texto.txt`.

## Requisitos do enunciado

Caso base:

- Fluxo de potencia com cargas 100% potencia constante.
- Tabela de tensao e angulo em cada barra.
- Tabela de fluxos e perdas nos ramos.
- Niveis de curto-circuito em cada barra para faltas FT, FF, FFT e simetrica.

Caso especifico:

- Modelo ZIP `40, 40, 20`.
- Comparar tensoes/angulos contra o caso base.
- Comparar fluxos contra o caso base.
- Simular aumento de 10% de carga no caso ZIP e comparar contra o ZIP original.
- ANAFAS: aplicar falta FT na barra 4 e apresentar tensoes em cada barra e corrente de falta.

## Estado ANAREDE

Arquivos convergidos e regerados apos conferencia com o PDF:

- `ieee39_base.pwf`
- `ieee39_zip.pwf`
- `ieee39_zip_carga_110.pwf`

Dados corrigidos conforme o PDF:

- Barra 31: carga `9.2 MW / 4.6 Mvar`.
- Barra 39: carga `1104 MW / 250 Mvar`.
- No caso ZIP com carga 110%, essas cargas tambem foram multiplicadas por 1.10:
  - Barra 31: `10.1 MW / 5.1 Mvar`.
  - Barra 39: `1214.4 MW / 275.0 Mvar`.

Observacao importante:

- No caso ZIP/ZIP 110%, as cargas reportadas no resultado podem diferir dos valores nominais do `DBAR`, porque o `DCAR` altera a carga efetiva conforme a tensao.
- Foi adicionado `DGEI` aos tres `.pwf`, com grupo 1 nas barras 30 a 39, para corresponder aos simbolos de gerador individualizado do `ieee39_base.lst`. O bloco usa modo automatico `S`.
- Os campos `NBA/Nc` foram preenchidos somente nos GEIs que possuem transformador elevador explicito no `DLIN`: 30-2, 31-6, 32-10, 33-19, 34-20, 35-22, 36-23, 37-25 e 38-29, com `Nc=1`. A barra 39 ficou sem `NBA/Nc` porque no PDF/DLIN ela nao tem transformador elevador explicito; um eventual `INPGEI-0361` apenas para a barra 39 e esperado.

## Padrao PWF validado no ANAREDE V13

- Formato de colunas fixas em `DBAR` e `DLIN`.
- Cada bloco de dados termina com `99999`.
- Executar fluxo com `EXLF`.
- Nao usar `DGLO`/`BASE 100.0`; a V13 rejeitou esse bloco com `SELKOD-0100`.
- Para gerar arquivo de relatorio:

```text
DOPC IMPR
(Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E
QLIM L CREM L CTAP L STEP L NEWT L MOCT L MOCG L MOCF L RCVG L RMON L
FILE L
99999
...
ULOG
4
resultado_nome.txt
EXLF
RELA RBAR RLIN
FIM
```

## Modelo ZIP no ANAREDE

O codigo aceito para carga funcional foi `DCAR`; `DLOD` foi rejeitado com `SELKOD-0100`.

Modelo `40Z, 40I, 20P` usado:

```text
DCAR
(tp) ( no) C (tp) ( no) C (tp) ( no) C (tp) ( no)   (A) (B) (C) (D) (Vmn)
AREA     1                                           40  40  40  40 60.0
99999
```

Interpretacao:

- `A=40`: parcela ativa linear com tensao, corrente constante.
- `B=40`: parcela ativa quadratica com tensao, impedancia constante.
- `C=40`: parcela reativa linear com tensao, corrente constante.
- `D=40`: parcela reativa quadratica com tensao, impedancia constante.
- Parcela restante: 20% potencia constante.

## Resultados ANAREDE

Relatorios brutos:

- `RESULTADO_BASE.TXT`
- `RESULTADO_ZIP.TXT`
- `RESULTADO_ZIP_110.TXT`

CSVs e tabelas:

- `results/base_buses.csv`
- `results/zip_buses.csv`
- `results/zip_110_buses.csv`
- `results/base_branches.csv`
- `results/zip_branches.csv`
- `results/zip_110_branches.csv`
- `results/compare_zip_vs_base_buses.csv`
- `results/compare_zip_vs_base_branches.csv`
- `results/compare_zip110_vs_zip_buses.csv`
- `results/compare_zip110_vs_zip_branches.csv`
- `results/relatorio_resumo.md`
- `results/relatorio_tabelas.md`

Scripts:

- `results/extract_results.py`: extrai barras e ramos dos TXT do ANAREDE.
- `results/generate_reports.py`: gera tabelas Markdown e resumo.

Extracao validada:

- 39 barras por caso.
- 46 ramos por caso.

## Proximo passo

Rodar os casos ANAFAS com os arquivos atuais:

- `ieee39_base.ana`: niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
- `ieee39_base.lst`: desenho associado ao caso base.
- `ieee39_falta_barra4.ana`: falta FT na barra 4, com tensoes em todas as barras e corrente de falta.

## Estado ANAFAS

Arquivos preparados:

- `ieee39_base.ana`
- `ieee39_base.lst`
- `ieee39_falta_barra4.ana`

O `ieee39_base.ana` atual esta no formato textual/secionado do ANAFAS:

- `TIPO`
- `P`
- `DBAR`
- `DCIR`
- `DARE`

Estado validado localmente:

- `DBAR`: 39 barras, sem faltantes e sem duplicadas.
- `DCIR`: 56 elementos:
  - 34 linhas `1L`.
  - 12 transformadores `1T`.
  - 10 equivalentes de gerador `1G` ligados a barra de referencia `0`.
- Nao ha circuitos duplicados.
- Nao ha referencia a barra inexistente.
- Tipos e nomes batem: `1L/LIN`, `1T/TRF`, `1G/GER`.
- `ieee39_base.lst` representa as mesmas 56 conexoes do `.ana`, sem ramos extras ou faltantes.
- No `.lst`, os IDs `C`, `L` e `U` sao unicos; as referencias `U -> C/L` e `L -> U` foram conferidas.

Os dados de impedancia em pu do PDF foram convertidos para inteiros em escala `x100` no `DCIR`. Exemplo: `0.35`, `4.11`, `1.05`, `12.33` viraram `35`, `411`, `105`, `1233`.

Pontos de atencao antes/depois da tentativa no ANAFAS:

- O campo `VBAS` do `DBAR` esta vazio nas 39 barras. A versao antiga tinha `345`; se o ANAFAS reclamar da base de tensao, preencher `345` em todas as barras.
- Os taps dos transformadores estao no caso ANAREDE `.pwf`, mas nao ha campo de tap evidente no formato `DCIR` usado no `.ana`. A primeira tentativa ANAFAS sera com o arquivo atual.
- A falta FT na barra 4 deve ser configurada no estudo do ANAFAS ou em arquivo batch/macro separado, nao misturada no arquivo primario de rede.

Os circuitos de gerador foram corrigidos para mapear cada barra ao `GenN` do enunciado:

- 30/Gen10: `0.0310`
- 31/Gen2: `0.0697`
- 32/Gen3: `0.0531`
- 33/Gen4: `0.0436`
- 34/Gen5: `0.1320`
- 35/Gen6: `0.0500`
- 36/Gen7: `0.0490`
- 37/Gen8: `0.0570`
- 38/Gen9: `0.0570`
- 39/Gen1: `0.0060`

Premissa registrada: como o PDF fornece `x'd`, mas nao traz todos os dados de sequencia negativa/zero, os arquivos usam `X1 = X2 = X0 = x'd` para a primeira validacao no ANAFAS.
