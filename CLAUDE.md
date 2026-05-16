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

Validar e rodar os casos ANAFAS:

- `ieee39_base.ana`: niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
- `ieee39_falta_barra4.ana`: falta FT na barra 4, com tensoes em todas as barras e corrente de falta.
