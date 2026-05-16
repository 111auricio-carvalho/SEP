# Resumo dos Resultados ANAREDE

## Casos processados

- Caso base: carga 100% potencia constante.
- Caso ZIP: 40% impedancia constante, 40% corrente constante, 20% potencia constante.
- Caso ZIP 110%: mesmo ZIP com cargas aumentadas em 10%.

## Maiores variacoes de tensao - ZIP vs. base

| Barra | Nome | V base | V ZIP | Delta V | Ang base | Ang ZIP | Delta ang |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | BUS 05 | 1.006 | 1.003 | -0.003 | -8.6 | -11.5 | -2.9 |
| 6 | BUS 06 | 1.008 | 1.006 | -0.002 | -7.9 | -10.7 | -2.8 |
| 7 | BUS 07 | 0.997 | 0.995 | -0.002 | -10.1 | -13.0 | -2.9 |
| 8 | BUS 08 | 0.996 | 0.994 | -0.002 | -10.6 | -13.6 | -3.0 |
| 11 | BUS 11 | 1.013 | 1.011 | -0.002 | -6.3 | -9.2 | -2.9 |
| 12 | BUS 12 | 1.001 | 0.999 | -0.002 | -6.2 | -9.3 | -3.1 |
| 13 | BUS 13 | 1.015 | 1.013 | -0.002 | -6.1 | -9.3 | -3.2 |
| 14 | BUS 14 | 1.012 | 1.010 | -0.002 | -7.7 | -11.2 | -3.5 |
| 21 | BUS 21 | 1.033 | 1.031 | -0.002 | -3.8 | -8.4 | -4.6 |
| 25 | BUS 25 | 1.059 | 1.057 | -0.002 | -4.4 | -9.1 | -4.7 |

## Maiores variacoes de tensao - ZIP 110% vs. ZIP

| Barra | Nome | V ZIP | V ZIP 110 | Delta V | Ang ZIP | Ang ZIP 110 | Delta ang |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 39 | GEN 39 | 1.030 | 0.964 | -0.066 | -14.5 | 13.9 | 28.4 |
| 9 | BUS 09 | 1.027 | 0.968 | -0.059 | -14.2 | 6.5 | 20.7 |
| 1 | BUS 01 | 1.048 | 1.000 | -0.048 | -12.9 | 9.2 | 22.1 |
| 8 | BUS 08 | 0.994 | 0.969 | -0.025 | -13.6 | -4.1 | 9.5 |
| 7 | BUS 07 | 0.995 | 0.973 | -0.022 | -13.0 | -4.2 | 8.8 |
| 5 | BUS 05 | 1.003 | 0.986 | -0.017 | -11.5 | -3.5 | 8.0 |
| 4 | BUS 04 | 1.003 | 0.987 | -0.016 | -13.1 | -4.9 | 8.2 |
| 6 | BUS 06 | 1.006 | 0.990 | -0.016 | -10.7 | -3.0 | 7.7 |
| 25 | BUS 25 | 1.057 | 1.042 | -0.015 | -9.1 | 2.1 | 11.2 |
| 3 | BUS 03 | 1.030 | 1.016 | -0.014 | -12.9 | -3.2 | 9.7 |

## Maiores variacoes de fluxo ativo - ZIP vs. base

| Ramo | P base | P ZIP | Delta P | Q base | Q ZIP | Delta Q | Delta perdas MW |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 6-31 c1 | -511.5 | -683.3 | -171.8 | -114.9 | -94.6 | 20.3 | 0.00 |
| 5-6 c1 | -454.3 | -546.5 | -92.2 | -54.6 | -46.0 | 8.6 | 0.19 |
| 4-5 c1 | -136.9 | -216.8 | -79.9 | -6.7 | 3.9 | 10.6 | 0.23 |
| 3-4 c1 | 93.0 | 22.4 | -70.6 | 112.4 | 121.5 | 9.1 | -0.07 |
| 14-15 c1 | 5.1 | 65.9 | 60.8 | -37.9 | -44.1 | -6.2 | 0.08 |
| 15-16 c1 | -314.9 | -259.9 | 55.0 | -153.3 | -163.3 | -10.0 | -0.25 |
| 13-14 c1 | 276.8 | 329.9 | 53.1 | -5.8 | -8.2 | -2.4 | 0.28 |
| 6-11 c1 | -363.8 | -311.0 | 52.8 | -32.4 | -44.7 | -12.3 | -0.24 |
| 10-11 c1 | 365.2 | 316.7 | -48.5 | 70.2 | 78.2 | 8.0 | -0.13 |
| 10-13 c1 | 284.7 | 333.2 | 48.5 | 36.9 | 35.9 | -1.0 | 0.12 |

## Maiores variacoes de fluxo ativo - ZIP 110% vs. ZIP

| Ramo | P ZIP | P ZIP 110 | Delta P | Q ZIP | Q ZIP 110 | Delta Q | Delta perdas MW |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 9-39 c1 | 23.2 | -477.5 | -500.7 | -75.3 | 7.3 | 82.6 | 2.47 |
| 8-9 c1 | 23.4 | -471.9 | -495.3 | -110.9 | 60.1 | 171.0 | 5.39 |
| 6-31 c1 | -683.3 | -192.1 | 491.2 | -94.6 | -204.7 | -110.1 | 0.00 |
| 1-2 c1 | -121.1 | 313.4 | 434.5 | -30.1 | -131.7 | -101.6 | 3.30 |
| 1-39 c1 | 121.1 | -313.4 | -434.5 | 30.2 | 131.7 | 101.5 | 1.09 |
| 2-3 c1 | 333.5 | 623.7 | 290.2 | 98.6 | 107.6 | 9.0 | 3.42 |
| 5-6 c1 | -546.5 | -292.6 | 253.9 | -46.0 | -118.6 | -72.6 | -0.40 |
| 7-8 c1 | 213.5 | -24.9 | -238.4 | -1.3 | 83.9 | 85.2 | -0.14 |
| 5-8 c1 | 329.3 | 106.4 | -222.9 | 57.4 | 139.2 | 81.8 | -0.63 |
| 6-7 c1 | 447.1 | 224.5 | -222.6 | 89.9 | 165.7 | 75.8 | -0.75 |

## Observacoes iniciais

- No caso ZIP, as magnitudes de tensao mudaram pouco em relacao ao caso base; as maiores diferencas ficaram em torno de 0.003 pu.
- No caso ZIP 110%, a maior reducao de tensao ocorreu na barra 39, seguida pelas barras 9 e 1.
- As diferencas angulares foram mais expressivas no aumento de carga de 10%, especialmente nas barras 39, 9 e 1.
- Os ramos 9-39, 8-9, 6-31, 1-2 e 1-39 aparecem entre as maiores variacoes de fluxo ativo no caso ZIP 110%.
