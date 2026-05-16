# SEP - IEEE 39 Barras

Arquivos de entrada para o trabalho de Sistemas Eletricos de Potencia usando ANAREDE V13 e ANAFAS.

## Arquivos principais

- `ieee39_base.pwf`: caso base ANAREDE, cargas 100% potencia constante.
- `ieee39_zip.pwf`: caso ZIP `40Z, 40I, 20P`.
- `ieee39_zip_carga_110.pwf`: caso ZIP com cargas aumentadas em 10%.
- `ieee39_base.ana`: caso ANAFAS para curto-circuito.
- `ieee39_falta_barra4.ana`: caso ANAFAS para falta FT na barra 4.
- `CODEX.md`: notas tecnicas detalhadas sobre formato PWF e erros ja corrigidos.

## Organizacao da pasta

- Raiz: arquivos finais de simulacao e documentacao curta.
- `archive/`: copias antigas preservadas para rastreabilidade.
- `docs/`: PDFs de enunciado, comandos e codigos de execucao.
- `results/`: relatorios gerados pelo ANAREDE e tabelas CSV extraidas.
- `tools/`: instaladores e utilitarios auxiliares.

## Padrao ANAREDE V13 validado

O ANAREDE V13 exigiu formato de colunas fixas para `DBAR` e `DLIN`.

Regras que funcionaram:

- Encerrar cada bloco de dados com `99999`.
- Usar `EXLF` para executar o fluxo de potencia.
- Nao usar `DGLO`/`BASE 100.0` neste PWF; a V13 rejeitou esse bloco com `SELKOD-0100`.
- Final funcional:

```text
99999
EXLF
FIM
```

## Caso base validado

O arquivo `ieee39_base.pwf` foi aceito pelo ANAREDE V13 e convergiu.

Resultado informado pelo ANAREDE:

```text
CONVERGENCIA FINAL
iteracoes: 3
erro max P: 0.02 MW na barra 6
erro max Q: 0.02 Mvar na barra 6
erro max tensao: 0.000 %
```

Os avisos `INPBUS-0925` apenas indicam area em branco; o ANAREDE adiciona as barras na area 001 automaticamente.

## Casos convergidos

- `ieee39_base.pwf`: convergiu.
- `ieee39_zip.pwf`: convergiu.
- `ieee39_zip_carga_110.pwf`: convergiu.

## Casos ZIP

Os arquivos `ieee39_zip.pwf` e `ieee39_zip_carga_110.pwf` foram atualizados para usar o mesmo `DBAR` e `DLIN` em colunas fixas do caso base validado.

O bloco ZIP usa o codigo `DCAR`, que e o codigo aceito pelo ANAREDE para carga funcional:

```text
DCAR
(tp) ( no) C (tp) ( no) C (tp) ( no) C (tp) ( no)   (A) (B) (C) (D) (Vmn)
AREA     1                                           40  40  40  40 60.0
99999
```

Interpretacao usada no trabalho: `A=40` e `C=40` representam as parcelas de corrente constante; `B=40` e `D=40` representam as parcelas de impedancia constante. A parcela restante e potencia constante, logo `20% P`, `40% I`, `40% Z`.

## Proximos passos

1. Usar os CSVs em `results/` para preencher as tabelas do relatorio:
   - ZIP vs. base;
   - ZIP carga 110% vs. ZIP original.
2. Depois disso, validar os arquivos ANAFAS.

## Resultados extraidos

Os arquivos `RESULTADO_BASE.TXT`, `RESULTADO_ZIP.TXT` e `RESULTADO_ZIP_110.TXT` foram processados para CSVs em `results/`.

Arquivos principais:

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

Extracao validada:

- 39 barras por caso.
- 46 ramos por caso.

## Observacoes de formato

No `DLIN`, os valores originais em pu foram convertidos para o formato em porcento/Mvar usado pelo ANAREDE:

- `Rpu * 100 -> R%`
- `Xpu * 100 -> X%`
- `Bpu * 100 MVA -> Mvar`

Exemplo:

```text
0.0035 pu -> .35 %
0.0411 pu -> 4.11 %
0.6987 pu em 100 MVA -> 69.87 Mvar
```
