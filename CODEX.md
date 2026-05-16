# CODEX.md

## Contexto

Workspace para os arquivos do trabalho de Sistemas Eletricos de Potencia com ANAREDE/ANAFAS.

Sistema principal: IEEE 39 barras.

Arquivo base validado no ANAREDE V13:

- `ieee39_base.pwf`

## ANAREDE V13 - formato que funcionou

O ANAREDE V13 leu corretamente o caso quando o arquivo PWF foi colocado em formato de colunas fixas, no estilo dos exemplos oficiais do executor local.

Pontos importantes:

- Cada bloco de dados deve terminar com `99999`.
- Para executar fluxo de potencia, usar `EXLF`, nao `EXEC`.
- O bloco `DGLO` com `BASE 100.0` foi rejeitado pela V13 neste arquivo com `SELKOD-0100`.
- O final funcional do arquivo ficou:

```text
99999
EXLF
FIM
```

## DBAR

O bloco `DBAR` precisa respeitar colunas fixas.

Armadilhas encontradas:

- Usar `345.0` como tensao no campo `TENSAO MOD` fez o ANAREDE ler apenas `5.0`, gerando erro de tensao fora dos limites.
- A tensao operativa deve ser informada em milipu no campo `( V)`, por exemplo:
  - `1000` para 1.000 pu
  - `1048` para 1.048 pu
  - `982` para 0.982 pu
- Cargas com tres digitos precisam estar alinhadas no campo de carga. Se comecarem uma coluna antes, o primeiro digito cai como `BARRA CONTR.` e gera erro `INPBUS-0260`.
- Geradores devem ter `Qn/Qm` nos campos corretos. Se `-9999/9999` deslocar, o ANAREDE interpreta `9999` como barra controlada inexistente.

Avisos ainda aceitos:

- `INPBUS-0925`: area em branco. O ANAREDE adiciona a barra automaticamente na area 001. Nao impediu a convergencia.

## DLIN

O bloco `DLIN` tambem precisa de colunas fixas.

Conversoes usadas:

- R e X foram informados em porcento:
  - `0.0035 pu` -> `.35`
  - `0.0411 pu` -> `4.11`
- Susceptancia foi informada em Mvar:
  - `0.6987 pu` em base 100 MVA -> `69.87`

Armadilha encontrada:

- Se a susceptancia invade o campo `TAP`, o ANAREDE interpreta a linha como transformador e gera erros como:
  - `INPLIN-0340 Valor de tap invalido`
  - `INPLIN-0345 Transformador com susceptancia shunt diferente de zero`

Alinhamento funcional usado no `DLIN`:

- Barra `DE`: colunas 1-5
- Barra `PARA`: colunas 11-15
- Circuito: coluna 17
- `R%`: colunas 21-26
- `X%`: colunas 27-32
- `Mvar`: colunas 33-38
- `Tap`: colunas 39-43, somente nos ramos com tap

## Resultado validado

Depois dos ajustes, o `ieee39_base.pwf` foi aceito pelo ANAREDE V13 e convergiu.

Relatorio de convergencia:

```text
CONVERGENCIA FINAL
iteracoes: 3
erro max P: 0.02 MW na barra 6
erro max Q: 0.02 Mvar na barra 6
erro max tensao: 0.000 %
```

## Proximos passos

1. Rodar/gerar relatorios de tensao de barras do caso base.
2. Rodar/gerar relatorios de fluxos e perdas dos ramos.
3. Aplicar o mesmo padrao de formato ao `ieee39_zip.pwf`.
4. Criar/validar o caso ZIP com carga 110%.
5. Usar os resultados convergidos nas tabelas do relatorio.
