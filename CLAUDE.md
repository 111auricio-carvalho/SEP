# CLAUDE.md

## Contexto do trabalho

**Disciplina:** Sistemas Elétricos de Potência — UFT  
**Trabalho:** Simulação Computacional 2026/1  
**Prazo:** 17/06/2026  
**E-mail do autor:** mauricio.carvalho@mail.uft.edu.br  
**Enunciado:** `simulação_2026_1 (1).pdf` (na raiz do repositório)

**Sistema elétrico:** IEEE 39 Barras (New England, 10 geradores)  
**Base:** 100 MVA, 60 Hz  
**Programas:** ANAREDE (fluxo de potência) e ANAFAS (curto-circuito)

---

## Objetivo geral

1. **Caso base:** todas as cargas como 100% potência constante.
2. **Caso ZIP `40, 40, 20`:** 40% impedância constante, 40% corrente constante, 20% potência constante.
   - Comparar ZIP vs. base.
   - Variante com cargas aumentadas em 10% (`ieee39_zip_carga_110.pwf`).
3. **ANAFAS base:** níveis de curto-circuito (FT, FF, FFT, simétrico) em todas as barras.
4. **ANAFAS específico:** falta FT na barra 4 — tensões durante a falta e corrente de falta.

Entrega: relatório escrito (AVA) + arquivos-fonte das simulações.

---

## Estado atual dos arquivos

### `ieee39_base.pwf` — Caso base ANAREDE

**O que tem:**
- Seção `DBAR`: todas as 39 barras declaradas corretamente.
- Seção `DLIN`: 28 linhas de transmissão declaradas.
- Barra swing: barra 31 (tipo 3), associada ao gerador 2 — correto conforme PDF.
- `DGLO BASE 100.0` e `EXEC` presentes.

**Problemas identificados:**
- **Transformadores ausentes.** O `DLIN` contém apenas linhas; não há seção `DTRF` nem
  entradas de transformadores/taps. Os seguintes ramos constam no PDF e estão faltando:

  | Par de barras | Tipo           |
  |:---:|:---:|
  | 12–11 | Transformador  |
  | 12–13 | Transformador  |
  | 6–31  | Transformador  |
  | 10–32 | Transformador  |
  | 19–33 | Transformador  |
  | 20–34 | Transformador  |
  | 22–35 | Transformador  |
  | 23–36 | Transformador  |
  | 25–37 | Transformador  |
  | 2–30  | Transformador  |
  | 29–38 | Transformador  |
  | 19–20 | Linha/transformador |

- **Carga reativa da barra 24:** arquivo tem `92.2 Mvar`; PDF indica `-92.0 Mvar`.
  Verificar se o sinal negativo é geração reativa ou convenção diferente. Tratar o PDF
  como fonte primária até confirmação.

**Ação necessária:** adicionar os transformadores (seção `DTRF` ou parâmetros de tap no
`DLIN` conforme documentação do ANAREDE) e corrigir/verificar a barra 24.

---

### `ieee39_zip.pwf` — Caso ZIP ANAREDE

**O que tem:**
- `TITU` e `DLOD` com as 17 barras de carga, cada uma com `20.0 40.0 40.0`.
- Placeholders `(Utilizar as mesmas barras/linhas do ieee39_base.pwf)` em vez de dados reais.

**Problemas identificados:**
- **Arquivo incompleto:** faltam as seções `DBAR`, `DLIN` (e `DTRF`) com os dados reais.
  O arquivo não pode ser executado como está.
- **Ordem dos campos `DLOD`:** os três valores provavelmente seguem a ordem interna do
  ANAREDE `(potência%, corrente%, impedância%)`, ou seja `20.0 40.0 40.0` = 20% P,
  40% I, 40% Z — que corresponde ao modelo `40Z 40I 20P` do grupo. **Confirmar na
  documentação do ANAREDE antes de usar como resultado final.**

**Ação necessária:** copiar as seções `DBAR`, `DLIN` (e `DTRF` quando completada) do
`ieee39_base.pwf` para este arquivo, mantendo o `DLOD` e o modelo ZIP.

---

### `ieee39_base.ana` — Caso base ANAFAS

**O que tem:**
- `DANA` com título.
- `DMAC` com reatâncias subtransitórias dos 10 geradores (barras 30–39).
- `DALT FAUL 4 FT` — linha de falta na barra 4 (caso específico, não base).

**Problemas identificados:**
- **Arquivo mistura caso base e caso específico:** o `DALT FAUL 4 FT` é para o caso
  específico (falta FT na barra 4), mas está no arquivo "base".
- **Seção `DBAR` ausente:** tem apenas o placeholder. O ANAFAS precisa dos dados de
  barra ou importação do `.pwf`.
- **Falta a varredura de barras para o caso base:** o caso base de curto-circuito exige
  aplicar falta em **cada uma das 39 barras** sequencialmente (FT, FF, FFT, simétrico),
  não apenas na barra 4.
- **Sintaxe `DALT FAUL` a confirmar:** verificar o manual do ANAFAS para o formato
  correto de declaração de falta.

**Ação necessária:** estruturar dois arquivos ANAFAS separados:
- `ieee39_base.ana` → varredura completa das 39 barras (todos os tipos de falta).
- `ieee39_falta_barra4.ana` → falta FT específica na barra 4.

---

### Arquivos que ainda precisam ser criados

| Arquivo | Descrição |
|---|---|
| `ieee39_zip_carga_110.pwf` | Caso ZIP com todas as cargas ×1,10 |
| `ieee39_falta_barra4.ana` | ANAFAS — falta FT na barra 4 (caso específico) |

---

## Referência rápida: formato ANAREDE (`.pwf`)

```
TITU           ← título (opcional, 1 linha)
DBAR           ← declaração de barras
  num tipo_barra nome   tensao_base   V_esp  Pg Pc Qc Qg_max Qg_min
  ...
DLIN           ← linhas de transmissão
  de  para  circ  R  X  Bsh  tap  Tap_min Tap_max
  ...
DTRF           ← transformadores (se separado de DLIN)
  de  para  circ  R  X  tap_inicial tap_min tap_max
  ...
DLOD           ← modelo de carga (ZIP)
  barra  %P  %I  %Z
  ...
DGLO           ← dados globais
BASE 100.0
EXEC           ← executar fluxo de potência
FIM            ← fim do arquivo
```

**Tipos de barra no DBAR:**
- `1` = PQ (carga)
- `2` = PV (gerador com tensão especificada)
- `3` = swing (referência angular)

---

## Referência rápida: formato ANAFAS (`.ana`)

```
DANA           ← cabeçalho do caso
DBAR           ← barras (ou importar do .pwf)
  ...
DMAC           ← dados de máquinas (geradores)
  barra  MVA_base  X1  X2  X0
  ...
DLIN           ← impedâncias de sequência das linhas (se necessário)
  ...
DALT           ← alterações / comandos de falta
FAUL  barra  tipo   ← tipo: FT | FF | FFT | 3F
FIM            ← fim do arquivo
```

**Tipos de falta:**
- `FT`  — fase-terra (monofásica)
- `FF`  — fase-fase (bifásica sem terra)
- `FFT` — fase-fase-terra (bifásica com terra)
- `3F`  — trifásica simétrica

---

## Caso base — ANAREDE: resultados esperados

### Tensões por barra

| Barra | E [pu] | Ângulo [graus] |
|---:|---:|---:|
| 1 | | |
| … | | |
| 39 | | |

### Fluxos e perdas nos ramos

| Da Barra | Para a Barra | P [MW] | Q [Mvar] | PL [MW] | QL [Mvar] |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | | | | |
| … | | | | | |

---

## Caso base — ANAFAS: resultados esperados

| Barra | FT [kA] | FF [kA] | FFT [kA] | Simétrica [kA] |
|---:|---:|---:|---:|---:|
| 1 | | | | |
| … | | | | |
| 39 | | | | |

---

## Caso ZIP `40, 40, 20` — resultados esperados

### Comparação de tensões (ZIP vs. base)

| Barra | E base [pu] | Âng. base [°] | E ZIP [pu] | Âng. ZIP [°] | ΔE [pu] | Δâng. [°] |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | | | | | | |

### Comparação de fluxos (ZIP vs. base)

| De | Para | P base [MW] | Q base [Mvar] | P ZIP [MW] | Q ZIP [Mvar] | ΔP [MW] | ΔQ [Mvar] |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2 | | | | | | |

---

## Caso ZIP + carga 110% — resultados esperados

Comparar vs. caso ZIP original (mesmas tabelas de tensão e fluxo acima).

**Regra para gerar o arquivo:**
- Copiar `ieee39_zip.pwf` → `ieee39_zip_carga_110.pwf`.
- Multiplicar Pc e Qc de cada barra de carga por `1.10` no `DBAR`.
- Manter `DLOD` com `20.0 40.0 40.0` inalterado.
- Não sobrescrever o ZIP original.

---

## Caso específico — ANAFAS: falta FT na barra 4

### Tensões durante a falta

| Barra | E [pu] | Ângulo [graus] |
|---:|---:|---:|
| 1 | | |
| … | | |
| 39 | | |

### Corrente de falta

| Barra da falta | Tipo | Corrente [kA] |
|---:|:---:|---:|
| 4 | FT | |

---

## Próximos passos (ordem recomendada)

1. **Completar `ieee39_base.pwf`:**
   - Levantar dados dos transformadores no PDF (impedâncias e taps).
   - Adicionar seção `DTRF` (ou entradas correspondentes em `DLIN`).
   - Verificar e corrigir a carga reativa da barra 24.

2. **Completar `ieee39_zip.pwf`:**
   - Copiar `DBAR`, `DLIN` e `DTRF` do `ieee39_base.pwf` (já corrigido).
   - Manter o `DLOD` existente.
   - Confirmar a ordem dos campos `DLOD` na documentação do ANAREDE.

3. **Criar `ieee39_zip_carga_110.pwf`:**
   - Partir do `ieee39_zip.pwf` completo e multiplicar cargas por 1,10.

4. **Rodar os três casos no ANAREDE** e exportar tensões e fluxos.

5. **Estruturar `ieee39_base.ana`:**
   - Importar ou reproduzir os dados de barra e rede.
   - Configurar varredura de todas as 39 barras (FT, FF, FFT, 3F).

6. **Criar `ieee39_falta_barra4.ana`:**
   - Declarar falta FT na barra 4.
   - Exportar tensões durante a falta e corrente de falta.

7. **Montar as tabelas comparativas** em Markdown ou CSV.

8. **Redigir o relatório** seguindo a estrutura da seção abaixo.

---

## Estrutura do relatório

1. Identificação da dupla e disciplina.
2. Descrição resumida do sistema IEEE 39 Barras.
3. Metodologia:
   - arquivos usados e ajustes realizados;
   - configuração do caso base;
   - configuração ZIP e justificativa da ordem dos campos `DLOD`;
   - configuração do aumento de 10% de carga;
   - configuração das faltas no ANAFAS.
4. Resultados do caso base: tensões, fluxos/perdas, curtos-circuitos.
5. Resultados do caso ZIP: tensões e comparação com base, fluxos e comparação com base.
6. Resultados do ZIP com carga 110%: comparação com ZIP original.
7. Falta FT na barra 4: tensões durante a falta, corrente de falta.
8. Análise técnica:
   - barras com maiores variações de tensão;
   - ramos com maiores alterações de fluxo/perdas;
   - impacto do modelo ZIP vs. potência constante;
   - impacto do aumento de carga em 10%;
   - interpretação da corrente de falta na barra 4.
9. Conclusões.
10. Anexos: arquivos-fonte relevantes.

---

## Checklist de entrega

### Dados de entrada
- [ ] Levantar impedâncias/taps dos transformadores no PDF.
- [ ] Adicionar transformadores ao `ieee39_base.pwf`.
- [ ] Verificar carga reativa da barra 24 (PDF: −92,0 Mvar; arquivo: 92,2 Mvar).
- [ ] Completar `ieee39_zip.pwf` com `DBAR`, `DLIN` e `DTRF`.
- [ ] Confirmar ordem dos campos `DLOD` na documentação do ANAREDE.
- [ ] Criar `ieee39_zip_carga_110.pwf` (cargas ×1,10, ZIP mantido).

### ANAREDE
- [ ] Rodar caso base e verificar convergência.
- [ ] Exportar tensões do caso base.
- [ ] Exportar fluxos e perdas do caso base.
- [ ] Rodar caso ZIP e verificar convergência.
- [ ] Exportar tensões do caso ZIP.
- [ ] Exportar fluxos do caso ZIP.
- [ ] Montar tabelas comparativas ZIP vs. base.
- [ ] Rodar caso ZIP com carga 110% e verificar convergência.
- [ ] Exportar tensões e fluxos do caso ZIP 110%.
- [ ] Montar tabelas comparativas ZIP 110% vs. ZIP original.

### ANAFAS
- [ ] Estruturar `ieee39_base.ana` com varredura de todas as 39 barras.
- [ ] Rodar curtos FT, FF, FFT e simétrico para cada barra.
- [ ] Exportar tabela de níveis de curto-circuito.
- [ ] Criar `ieee39_falta_barra4.ana` com falta FT na barra 4.
- [ ] Exportar tensões durante a falta e corrente de falta.

### Relatório e entrega
- [ ] Redigir todas as seções do relatório.
- [ ] Preencher todas as tabelas com os resultados simulados.
- [ ] Incluir análise técnica fundamentada.
- [ ] Separar arquivos-fonte para envio no AVA.
- [ ] Preparar explicação oral dos resultados.

---

## Pontos prováveis para avaliação oral

- Diferença entre carga de potência constante e modelo ZIP.
- O significado dos percentuais `40, 40, 20` e a ordem dos campos no ANAREDE.
- Por que a tensão muda quando o modelo de carga muda.
- O que ocorre com tensões e fluxos ao aumentar a carga em 10%.
- Como identificar ramos mais carregados e maiores perdas.
- Diferença entre faltas FT, FF, FFT e simétrica.
- Por que a falta FT na barra 4 produz as correntes e tensões observadas.
- Qual barra é swing/referência no caso e por quê.
- Como os dados de geradores, linhas e transformadores foram inseridos nos programas.

---

## Regras do repositório

- Preservar arquivos originais; criar variantes com nomes explícitos.
- Não sobrescrever resultados sem manter rastreabilidade.
- Preferir tabelas em Markdown ou CSV para facilitar montagem do relatório.
- Registrar no relatório qualquer ajuste feito nos arquivos de entrada.
- Em caso de divergência entre arquivo local e PDF, tratar o PDF como fonte primária
  até confirmação do professor ou de referência oficial.
