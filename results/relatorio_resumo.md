# Resumo dos Resultados ANAREDE

## Casos processados

- Caso base: carga 100% potencia constante.
- Caso ZIP: 40% impedancia constante, 40% corrente constante, 20% potencia constante.
- Caso ZIP 110%: mesmo ZIP com cargas aumentadas em 10%.

## Maiores variacoes de tensao - ZIP vs. base

| Barra | Nome | V base | V ZIP | Delta V | Ang base | Ang ZIP | Delta ang |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | BUS 05 | 0.983 | 0.988 | 0.005 | 9.2 | 7.8 | -1.4 |
| 6 | BUS 06 | 0.986 | 0.991 | 0.005 | 9.0 | 7.7 | -1.3 |
| 7 | BUS 07 | 0.972 | 0.977 | 0.005 | 8.6 | 7.3 | -1.3 |
| 8 | BUS 08 | 0.969 | 0.974 | 0.005 | 9.1 | 7.8 | -1.3 |
| 4 | BUS 04 | 0.986 | 0.990 | 0.004 | 10.2 | 8.4 | -1.8 |
| 10 | BUS 10 | 1.002 | 1.006 | 0.004 | 12.9 | 11.3 | -1.6 |
| 11 | BUS 11 | 0.995 | 0.999 | 0.004 | 11.6 | 10.1 | -1.5 |
| 12 | BUS 12 | 0.984 | 0.988 | 0.004 | 12.0 | 10.4 | -1.6 |
| 13 | BUS 13 | 0.999 | 1.003 | 0.004 | 12.6 | 10.9 | -1.7 |
| 3 | BUS 03 | 1.016 | 1.019 | 0.003 | 15.0 | 12.5 | -2.5 |

## Maiores variacoes de tensao - ZIP 110% vs. ZIP

| Barra | Nome | V ZIP | V ZIP 110 | Delta V | Ang ZIP | Ang ZIP 110 | Delta ang |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | BUS 05 | 0.988 | 0.994 | 0.006 | 7.8 | -0.6 | -8.4 |
| 6 | BUS 06 | 0.991 | 0.997 | 0.006 | 7.7 | -0.3 | -8.0 |
| 7 | BUS 07 | 0.977 | 0.983 | 0.006 | 7.3 | -1.1 | -8.4 |
| 8 | BUS 08 | 0.974 | 0.980 | 0.006 | 7.8 | -0.9 | -8.7 |
| 9 | BUS 09 | 1.002 | 1.007 | 0.005 | 21.5 | 11.7 | -9.8 |
| 11 | BUS 11 | 0.999 | 1.004 | 0.005 | 10.1 | 1.3 | -8.8 |
| 10 | BUS 10 | 1.006 | 1.010 | 0.004 | 11.3 | 2.2 | -9.1 |
| 12 | BUS 12 | 0.988 | 0.992 | 0.004 | 10.4 | 1.4 | -9.0 |
| 4 | BUS 04 | 0.990 | 0.993 | 0.003 | 8.4 | -1.7 | -10.1 |
| 13 | BUS 13 | 1.003 | 1.006 | 0.003 | 10.9 | 1.5 | -9.4 |

## Maiores variacoes de fluxo ativo - ZIP vs. base

| Ramo | P base | P ZIP | Delta P | Q base | Q ZIP | Delta Q | Delta perdas MW |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6-31 c1 | 568.0 | 488.0 | -80.0 | -178.9 | -175.4 | 3.5 | 0.00 |
| 4-5 c1 | 134.4 | 81.8 | -52.6 | 3.3 | 1.0 | -2.3 | -0.09 |
| 3-4 c1 | 397.5 | 347.9 | -49.6 | 127.3 | 118.5 | -8.8 | -0.50 |
| 14-15 c1 | -138.8 | -93.6 | 45.2 | -44.1 | -42.5 | 1.6 | -0.19 |
| 5-6 c1 | 108.9 | 63.9 | -45.0 | -103.0 | -99.6 | 3.4 | -0.02 |
| 15-16 c1 | -459.2 | -416.6 | 42.6 | -164.8 | -162.0 | 2.8 | -0.34 |
| 13-14 c1 | 100.8 | 136.5 | 35.7 | 8.8 | 6.1 | -2.7 | 0.08 |
| 6-11 c1 | -538.3 | -503.1 | 35.2 | -61.9 | -57.0 | 4.9 | -0.29 |
| 2-25 c1 | -151.4 | -118.8 | 32.6 | 28.1 | 24.3 | -3.8 | -0.59 |
| 10-11 c1 | 526.0 | 493.5 | -32.5 | 118.9 | 108.7 | -10.2 | -0.15 |

## Maiores variacoes de fluxo ativo - ZIP 110% vs. ZIP

| Ramo | P ZIP | P ZIP 110 | Delta P | Q ZIP | Q ZIP 110 | Delta Q | Delta perdas MW |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6-31 c1 | 488.0 | -18.0 | -506.0 | -175.4 | -186.8 | -11.4 | 0.00 |
| 5-6 c1 | 63.9 | -202.3 | -266.2 | -99.6 | -105.9 | -6.3 | 0.07 |
| 4-5 c1 | 81.8 | -147.0 | -228.8 | 1.0 | -3.7 | -4.7 | 0.12 |
| 14-15 c1 | -93.6 | 81.6 | 175.2 | -42.5 | -47.0 | -4.5 | -0.04 |
| 3-4 c1 | 347.9 | 193.2 | -154.7 | 118.5 | 113.6 | -4.9 | -1.07 |
| 13-14 c1 | 136.5 | 288.5 | 152.0 | 6.1 | 3.7 | -2.4 | 0.57 |
| 6-11 c1 | -503.1 | -351.4 | 151.7 | -57.0 | -56.9 | 0.1 | -0.93 |
| 15-16 c1 | -416.6 | -273.8 | 142.8 | -162.0 | -178.1 | -16.1 | -0.83 |
| 10-11 c1 | 493.5 | 354.2 | -139.3 | 108.7 | 93.6 | -15.1 | -0.48 |
| 10-13 c1 | 156.5 | 295.8 | 139.3 | 48.0 | 47.0 | -1.0 | 0.24 |

## Observacoes iniciais

- No caso ZIP, as magnitudes de tensao mudaram pouco em relacao ao caso base; as maiores diferencas ficaram em torno de 0.005 pu.
- No caso ZIP 110%, as maiores quedas relativas de tensao ocorreram nas barras 25, 26, 27 e 28, mas a variacao de modulo ainda ficou pequena.
- As diferencas angulares foram mais expressivas que as diferencas de modulo, especialmente no aumento de carga de 10%.
- Os ramos ligados aos geradores e aos corredores 4-5, 5-6 e 6-31 aparecem entre as maiores variacoes de fluxo ativo no caso ZIP 110%.
