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

Observacao: apos a conferencia direta com `docs/simulacao_2026_1_texto.txt`, foram adicionadas as cargas das barras 31 e 39 que constam no PDF. Os tres casos foram rodados novamente no ANAREDE e os resultados foram reextraidos.

## Conferencia com o enunciado

O PDF `docs/simulaçao_2026_1 (1).pdf` pede:

- Caso base ANAREDE com cargas 100% potencia constante.
- Fluxos de potencia e perdas nos ramos.
- Modulo de tensao e angulo em cada barra.
- Caso especifico ZIP `40, 40, 20`, com comparacao contra o caso base.
- Aumento de 10% de carga no caso ZIP e comparacao contra o ZIP original.
- ANAFAS: niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
- ANAFAS especifico: falta FT na barra 4, com tensoes em cada barra e corrente de falta.

Dados corrigidos para aderir ao PDF:

- Barra 31: carga `9.2 MW / 4.6 Mvar`.
- Barra 39: carga `1104 MW / 250 Mvar`.
- No caso `ieee39_zip_carga_110.pwf`, essas cargas tambem foram multiplicadas por 1.10.

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

1. Testar a leitura/simulacao no ANAFAS com os arquivos atuais:
   - `ieee39_base.ana`: base de rede para niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
   - `ieee39_base.lst`: desenho associado ao caso base.
   - `ieee39_falta_barra4.ana`: caso/arquivo operacional para falta FT na barra 4, se ainda for mantido separado.
2. Se o ANAFAS reclamar das barras, preencher explicitamente `VBAS=345` no bloco `DBAR` do `ieee39_base.ana`.
3. Extrair os resultados ANAFAS para montar as tabelas finais de curto-circuito.

## Preparacao ANAFAS atual

Os arquivos `.ana` e `.lst` foram atualizados para usar a mesma topologia do caso ANAREDE validado.

Estado atual do `ieee39_base.ana`:

- Usa o formato textual/secionado do ANAFAS: `TIPO`, `P`, `DBAR`, `DCIR` e `DARE`.
- O bloco `DBAR` contem 39 barras, numeradas de 1 a 39.
- O bloco `DCIR` contem 56 elementos:
  - 34 linhas `1L`.
  - 12 transformadores `1T`.
  - 10 equivalentes de gerador `1G` ligados a barra de referencia `0`.
- As impedancias `R1`, `X1`, `R0` e `X0` foram convertidas dos dados em pu para inteiros em escala `x100`.
  - Exemplo: `0.35`, `4.11`, `1.05`, `12.33` viraram `35`, `411`, `105`, `1233`.
- A topologia e os valores de impedancia foram conferidos contra a versao anterior de `ieee39_base.ana`.
- Nao foram encontrados circuitos duplicados, barras faltantes ou referencias a barras inexistentes.

Ponto de atencao no `ieee39_base.ana`:

- O campo `VBAS` do `DBAR` esta vazio nas 39 barras. O cabecalho preve o campo, e a versao antiga tinha `345`. Se o ANAFAS nao aceitar a base padrao/importada, preencher `345` em todas as barras antes de simular.
- Os taps dos transformadores existem no caso ANAREDE `.pwf`, mas nao ha um campo de tap evidente no formato `DCIR` usado no `.ana`. Para curto-circuito, a primeira tentativa sera com o arquivo atual.

Estado atual do `ieee39_base.lst`:

- O desenho contem 39 barras unicas.
- Foram desenhados os 56 ramos representados no `ieee39_base.ana`.
- Validacoes feitas:
  - IDs `C`, `L` e `U` unicos.
  - Sem barras faltantes ou duplicadas.
  - Referencias `U -> C/L` validas.
  - Segmentos `L -> U` validos.
  - Sem ligacoes/ramos duplicados.
  - Comparacao `.lst` x `.ana`: 56 conexoes no `.lst` e 56 no `.ana`, sem `missing` e sem `extra`.

Como foi verificado:

```powershell
# Contagens basicas do .ana
Select-String -Path ieee39_base.ana -Pattern '^\s*\d+\s+(BUS|GEN)' | Measure-Object
Select-String -Path ieee39_base.ana -Pattern '^\s*\d+\s+\d+\s+1L' | Measure-Object
Select-String -Path ieee39_base.ana -Pattern '^\s*\d+\s+\d+\s+1T' | Measure-Object
Select-String -Path ieee39_base.ana -Pattern '^\s*\d+\s+0\s+1G' | Measure-Object

# Contagens basicas do .lst
Select-String -Path ieee39_base.lst -Pattern '^C' | Measure-Object
Select-String -Path ieee39_base.lst -Pattern '^L' | Measure-Object
Select-String -Path ieee39_base.lst -Pattern '^U' | Measure-Object
```

Mapeamento de maquinas usado nos circuitos equivalentes de gerador:

- Barra 30: Gen10, `x'd = 0.0310`.
- Barra 31: Gen2, `x'd = 0.0697`.
- Barra 32: Gen3, `x'd = 0.0531`.
- Barra 33: Gen4, `x'd = 0.0436`.
- Barra 34: Gen5, `x'd = 0.1320`.
- Barra 35: Gen6, `x'd = 0.0500`.
- Barra 36: Gen7, `x'd = 0.0490`.
- Barra 37: Gen8, `x'd = 0.0570`.
- Barra 38: Gen9, `x'd = 0.0570`.
- Barra 39: Gen1, `x'd = 0.0060`.

Como o enunciado fornece `x'd`, mas nao fornece dados completos de sequencia negativa e zero, a primeira versao dos arquivos ANAFAS assume `X1 = X2 = X0 = x'd`. Essa premissa deve ser mantida no relatorio ou substituida se o professor fornecer os dados de sequencia.

## Resultados extraidos

Os arquivos `RESULTADO_BASE.TXT`, `RESULTADO_ZIP.TXT` e `RESULTADO_ZIP_110.TXT` foram processados para CSVs em `results/`.

Os resultados atuais ja consideram a correcao das cargas das barras 31 e 39.

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
