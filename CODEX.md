# CODEX.md

## Contexto

Workspace para o trabalho de Sistemas Eletricos de Potencia com ANAREDE/ANAFAS.

Sistema principal: IEEE 39 barras.

Referencias locais:

- Enunciado: `docs/simulaçao_2026_1 (1).pdf`
- Texto extraido: `docs/simulacao_2026_1_texto.txt`

## ANAREDE V13 - formato que funcionou

O ANAREDE V13 leu corretamente os casos quando os arquivos PWF foram colocados em formato de colunas fixas.

Pontos importantes:

- Cada bloco de dados deve terminar com `99999`.
- Para executar fluxo de potencia, usar `EXLF`, nao `EXEC`.
- O bloco `DGLO` com `BASE 100.0` foi rejeitado pela V13 com `SELKOD-0100`.
- Para gerar relatorio em arquivo, usar `DOPC IMPR` com `FILE L`, depois `ULOG`, `EXLF` e `RELA`.

Bloco de impressao usado:

```text
DOPC IMPR
(Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E (Op) E
QLIM L CREM L CTAP L STEP L NEWT L MOCT L MOCG L MOCF L RCVG L RMON L
FILE L
99999
```

Final funcional:

```text
ULOG
4
resultado_nome.txt
EXLF
RELA RBAR RLIN
FIM
```

## DBAR

O bloco `DBAR` precisa respeitar colunas fixas.

Armadilhas encontradas:

- Usar `345.0` como tensao no campo `TENSAO MOD` fez o ANAREDE ler apenas `5.0`.
- A tensao operativa deve ser informada em milipu no campo `( V)`, por exemplo `1000`, `1048`, `982`.
- Cargas com tres digitos precisam estar alinhadas no campo de carga. Se comecarem uma coluna antes, o primeiro digito cai como `BARRA CONTR.` e gera `INPBUS-0260`.
- Geradores devem ter `Qn/Qm` nos campos corretos. Se `-9999/9999` deslocar, o ANAREDE interpreta `9999` como barra controlada inexistente.

Dados conferidos no PDF:

- Barra 31: carga `9.2 MW / 4.6 Mvar`.
- Barra 39: carga `1104 MW / 250 Mvar`.
- No caso 110%: barra 31 `10.1 MW / 5.1 Mvar`; barra 39 `1214.4 MW / 275.0 Mvar`.

Aviso aceito:

- `INPBUS-0925`: area em branco. O ANAREDE adiciona a barra automaticamente na area 001.

## DLIN

O bloco `DLIN` tambem precisa de colunas fixas.

Conversoes usadas:

- `Rpu * 100 -> R%`
- `Xpu * 100 -> X%`
- `Bpu * 100 MVA -> Mvar`

Exemplo:

- `0.0035 pu -> .35`
- `0.0411 pu -> 4.11`
- `0.6987 pu em 100 MVA -> 69.87`

Alinhamento funcional usado no `DLIN`:

- Barra `DE`: colunas 1-5
- Barra `PARA`: colunas 11-15
- Circuito: coluna 17
- `R%`: colunas 21-26
- `X%`: colunas 27-32
- `Mvar`: colunas 33-38
- `Tap`: colunas 39-43, somente nos ramos com tap

Armadilha:

- Se a susceptancia invade o campo `TAP`, o ANAREDE interpreta a linha como transformador e gera `INPLIN-0340` e `INPLIN-0345`.

## DCAR para modelo ZIP

O codigo correto para carga funcional no ANAREDE e `DCAR`. O codigo `DLOD` foi rejeitado pela V13 com `SELKOD-0100`.

Para o modelo `40Z, 40I, 20P`, usar:

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

Observacao: em casos com `DCAR`, a carga efetiva reportada no resultado pode diferir da carga nominal no `DBAR`, pois depende da tensao.

## Resultado validado

Os tres casos ANAREDE convergiram apos conferencia com o PDF:

- `ieee39_base.pwf`
- `ieee39_zip.pwf`
- `ieee39_zip_carga_110.pwf`

Resultados brutos:

- `RESULTADO_BASE.TXT`
- `RESULTADO_ZIP.TXT`
- `RESULTADO_ZIP_110.TXT`

## Extracao de resultados ANAREDE

Depois de rodar os PWFs no ANAREDE:

```powershell
python .\results\extract_results.py
python .\results\generate_reports.py
```

O extrator mantem a ultima ocorrencia de cada barra e ramo. Isso evita duplicacao quando o ANAREDE concatena mais de uma execucao no mesmo TXT.

Saidas principais:

- `results/relatorio_resumo.md`
- `results/relatorio_tabelas.md`
- CSVs de barras, ramos e comparacoes em `results/`

Extracao validada:

- 39 barras por caso.
- 46 ramos por caso.

## Proximo passo

Validar ANAFAS:

- `ieee39_base.ana`: niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
- `ieee39_falta_barra4.ana`: falta FT na barra 4, tensoes em todas as barras e corrente de falta.
