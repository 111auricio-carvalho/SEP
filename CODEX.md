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

Depois da validacao original, foi adicionado bloco `DGEI` aos tres `.pwf`, com grupo 1 nas barras 30 a 39, para corresponder aos simbolos de gerador individualizado do `ieee39_base.lst`. O bloco usa modo automatico `S`.

Os campos `NBA/Nc` do `DGEI` foram preenchidos somente quando existe transformador elevador explicito no `DLIN`: 30-2, 31-6, 32-10, 33-19, 34-20, 35-22, 36-23, 37-25 e 38-29, todos com `Nc=1`. A barra 39 foi mantida sem `NBA/Nc`, pois no PDF/DLIN ela aparece conectada por linhas 1-39 e 9-39, sem transformador elevador dedicado. Assim, um eventual aviso `INPGEI-0361` apenas para a barra 39 e aceitavel e evita associar o GEI a uma linha comum.

Resultados brutos:

- `RESULTADO_BASE.TXT`
- `RESULTADO_ZIP.TXT`
- `RESULTADO_ZIP_110.TXT`

## Extracao de resultados ANAREDE

Depois de rodar os PWFs no ANAREDE:

```powershell
python .\results\extract_results.py
python .\results\generate_latex.py
```

O extrator mantem a ultima ocorrencia de cada barra e ramo. Isso evita duplicacao quando o ANAREDE concatena mais de uma execucao no mesmo TXT.

Saidas principais:

- `results/latex/relatorio_tabelas.tex`
- `results/latex/classe_uftex/uftex.cls`
- `results/latex/classe_uftex/logouft.pdf`
- CSVs de barras, ramos e comparacoes em `results/`

O relatorio LaTeX usa os arquivos minimos da classe UFTeX copiados de `https://github.com/UFTeX/UFTeX.git`.

Extracao validada:

- 39 barras por caso.
- 46 ramos por caso.

## Proximo passo

Testar leitura/simulacao no ANAFAS:

- `ieee39_base.ana`: niveis de curto-circuito FT, FF, FFT e simetrica em todas as barras.
- `ieee39_base.lst`: desenho associado ao caso base.
- `ieee39_falta_barra4.ana`: falta FT na barra 4, tensoes em todas as barras e corrente de falta.

## ANAFAS - estado atual

Arquivos:

- `ieee39_base.ana`: arquivo primario de rede ANAFAS.
- `ieee39_base.lst`: desenho associado ao caso base.
- `ieee39_falta_barra4.ana`: copia operacional do arquivo primario de rede ANAFAS para testar a falta FT na barra 4 pelo modo interativo.

O `ieee39_base.ana` atual usa o formato textual/secionado do ANAFAS:

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
- `ieee39_base.lst` contem 39 barras unicas e representa as mesmas 56 conexoes do `.ana`.
- No `.lst`, os IDs `C`, `L` e `U` sao unicos; referencias `U -> C/L` e segmentos `L -> U` foram conferidos.
- Comparacao `.lst` x `.ana`: 56 conexoes no `.lst` e 56 no `.ana`, sem `missing` e sem `extra`.

No `DCIR`, as impedancias foram convertidas para inteiros em escala `x100`:

- `R% = Rpu * 100`
- `X% = Xpu * 100`
- `R0% = R0pu * 100`
- `X0% = X0pu * 100`

Exemplo:

```text
0.35  4.11  1.05  12.33  ->  35  411  105  1233
```

Pontos de atencao:

- O campo `VBAS` do `DBAR` foi preenchido com `345 kV` nas 39 barras, coerente com a representacao usual do IEEE 39 barras como sistema New England 345 kV e com o arquivo especifico `ieee39_falta_barra4.ana`.
- Os taps dos transformadores existem no caso ANAREDE `.pwf`, mas nao ha campo de tap evidente no formato `DCIR` usado no `.ana`.
- A falta FT na barra 4 deve ser configurada no estudo do ANAFAS ou por arquivo batch/macro separado, nao dentro do arquivo primario de rede.

O mapeamento de geradores foi alinhado com a tabela do PDF. O mapeamento correto e pelo `GenN` informado na tabela de barras:

- Barra 30 -> Gen10 -> `x'd = 0.0310`
- Barra 31 -> Gen2 -> `x'd = 0.0697`
- Barra 32 -> Gen3 -> `x'd = 0.0531`
- Barra 33 -> Gen4 -> `x'd = 0.0436`
- Barra 34 -> Gen5 -> `x'd = 0.1320`
- Barra 35 -> Gen6 -> `x'd = 0.0500`
- Barra 36 -> Gen7 -> `x'd = 0.0490`
- Barra 37 -> Gen8 -> `x'd = 0.0570`
- Barra 38 -> Gen9 -> `x'd = 0.0570`
- Barra 39 -> Gen1 -> `x'd = 0.0060`

Premissas ANAFAS ainda pendentes de validacao no programa:

- O enunciado fornece `x'd`, mas nao fornece valores explicitos de sequencia negativa e zero para as maquinas; a versao atual usa `X1 = X2 = X0 = x'd`.
- Para linhas, a sequencia positiva vem da tabela do PDF; a sequencia zero foi estimada como `R0 = 4R1`, `X0 = 4X1`, `B0 = B1/4`.
- Para transformadores, a sequencia zero depende da ligacao dos enrolamentos. O arquivo atual ainda deve ser validado no ANAFAS e ajustado conforme as mensagens do programa.
- A susceptancia de linha foi omitida na primeira tentativa ANAFAS para reduzir risco de erro de formato no `DCIR`; o curto-circuito inicial fica dominado pelas impedancias serie.


                                                                                                                                        
  Como Validar                                                                                                                            
                                                                                                                                          
  1. ANAREDE convergiu.                                                                                                                   
     O caso base, ZIP e ZIP 110% têm solução de fluxo de potência convergida. Isso valida numericamente os resultados de tensão, ângulo,  
     fluxo e perdas.                                                                                                                      
  2. Tensões ficaram em faixa plausível.                                                                                                  
     No IEEE 39 barras, tensões próximas de 1.0 pu são esperadas. Quedas maiores aparecem com aumento de carga, especialmente em barras   
     mais carregadas ou eletricamente distantes.                                                                                          
  3. ZIP vs. base muda pouco.                                                                                                             
     Isso é esperado porque o modelo ZIP ajusta a carga conforme a tensão. Como as tensões ficaram próximas de 1 pu, a diferença entre    
     carga potência constante e ZIP 40Z/40I/20P tende a ser pequena.                                                                      
  4. ZIP 110% muda mais.                                                                                                                  
     Aumentar carga em 10% aumenta corrente nos ramos, aumenta perdas e tende a reduzir tensões. Isso deve aparecer nas tabelas.          
  5. ANAFAS base gerou todos os tipos de curto.                                                                                           
     A tabela com FT, FF, FFT e simétrica para 39 barras atende à Tabela 3 do enunciado.                                                  
  6. Falta FT na barra 4.                                                                                                                 
     A corrente de falta ficou 6.370 kA. A tensão da fase A na barra 4 vai a 0 pu, o que é exatamente esperado numa falta fase-terra      
     franca na fase A.