import csv
from pathlib import Path

R = Path('results')

def read_csv(name):
    with (R / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def fnum(v, nd=3):
    try:
        x = float(v)
    except Exception:
        return str(v)
    return f'{x:.{nd}f}'

def md_table(headers, rows):
    out = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
    for row in rows:
        out.append('| ' + ' | '.join(str(x) for x in row) + ' |')
    return '\n'.join(out)

def top_abs(rows, field, n=10):
    return sorted(rows, key=lambda r: abs(float(r[field])), reverse=True)[:n]

def branch_label(r):
    return f"{r['from_bus']}-{r['to_bus']} c{r['circuit']}"

zip_base_b = read_csv('compare_zip_vs_base_buses.csv')
zip110_zip_b = read_csv('compare_zip110_vs_zip_buses.csv')
zip_base_l = read_csv('compare_zip_vs_base_branches.csv')
zip110_zip_l = read_csv('compare_zip110_vs_zip_branches.csv')
base_b = read_csv('base_buses.csv')
zip_b = read_csv('zip_buses.csv')
zip110_b = read_csv('zip_110_buses.csv')

summary = []
summary.append('# Resumo dos Resultados ANAREDE\n')
summary.append('## Casos processados\n')
summary.append('- Caso base: carga 100% potencia constante.')
summary.append('- Caso ZIP: 40% impedancia constante, 40% corrente constante, 20% potencia constante.')
summary.append('- Caso ZIP 110%: mesmo ZIP com cargas aumentadas em 10%.\n')
summary.append('## Maiores variacoes de tensao - ZIP vs. base\n')
summary.append(md_table(['Barra','Nome','V base','V ZIP','Delta V','Ang base','Ang ZIP','Delta ang'], [
    [r['bus'], r['name'], fnum(r['base_voltage_pu']), fnum(r['zip_voltage_pu']), fnum(r['delta_voltage_pu']), fnum(r['base_angle_deg'],1), fnum(r['zip_angle_deg'],1), fnum(r['delta_angle_deg'],1)]
    for r in top_abs(zip_base_b, 'delta_voltage_pu')
]))
summary.append('\n## Maiores variacoes de tensao - ZIP 110% vs. ZIP\n')
summary.append(md_table(['Barra','Nome','V ZIP','V ZIP 110','Delta V','Ang ZIP','Ang ZIP 110','Delta ang'], [
    [r['bus'], r['name'], fnum(r['zip_voltage_pu']), fnum(r['zip_110_voltage_pu']), fnum(r['delta_voltage_pu']), fnum(r['zip_angle_deg'],1), fnum(r['zip_110_angle_deg'],1), fnum(r['delta_angle_deg'],1)]
    for r in top_abs(zip110_zip_b, 'delta_voltage_pu')
]))
summary.append('\n## Maiores variacoes de fluxo ativo - ZIP vs. base\n')
summary.append(md_table(['Ramo','P base','P ZIP','Delta P','Q base','Q ZIP','Delta Q','Delta perdas MW'], [
    [branch_label(r), fnum(r['base_p_mw'],1), fnum(r['zip_p_mw'],1), fnum(r['delta_p_mw'],1), fnum(r['base_q_mvar'],1), fnum(r['zip_q_mvar'],1), fnum(r['delta_q_mvar'],1), fnum(r['delta_loss_mw'],2)]
    for r in top_abs(zip_base_l, 'delta_p_mw')
]))
summary.append('\n## Maiores variacoes de fluxo ativo - ZIP 110% vs. ZIP\n')
summary.append(md_table(['Ramo','P ZIP','P ZIP 110','Delta P','Q ZIP','Q ZIP 110','Delta Q','Delta perdas MW'], [
    [branch_label(r), fnum(r['zip_p_mw'],1), fnum(r['zip_110_p_mw'],1), fnum(r['delta_p_mw'],1), fnum(r['zip_q_mvar'],1), fnum(r['zip_110_q_mvar'],1), fnum(r['delta_q_mvar'],1), fnum(r['delta_loss_mw'],2)]
    for r in top_abs(zip110_zip_l, 'delta_p_mw')
]))
summary.append('\n## Observacoes iniciais\n')
summary.append('- No caso ZIP, as magnitudes de tensao mudaram pouco em relacao ao caso base; as maiores diferencas ficaram em torno de 0.003 pu.')
summary.append('- No caso ZIP 110%, a maior reducao de tensao ocorreu na barra 39, seguida pelas barras 9 e 1.')
summary.append('- As diferencas angulares foram mais expressivas no aumento de carga de 10%, especialmente nas barras 39, 9 e 1.')
summary.append('- Os ramos 9-39, 8-9, 6-31, 1-2 e 1-39 aparecem entre as maiores variacoes de fluxo ativo no caso ZIP 110%.')
(R / 'relatorio_resumo.md').write_text('\n'.join(summary) + '\n', encoding='utf-8')

full = []
full.append('# Tabelas ANAREDE\n')
full.append('## Tensoes - caso base\n')
full.append(md_table(['Barra','Nome','Tipo','V pu','Ang deg','Pg MW','Qg Mvar','Carga MW','Carga Mvar'], [
    [r['bus'], r['name'], r['type'], fnum(r['voltage_pu']), fnum(r['angle_deg'],1), fnum(r['gen_mw'],1), fnum(r['gen_mvar'],1), fnum(r['load_mw'],1), fnum(r['load_mvar'],1)]
    for r in base_b
]))
full.append('\n## Tensoes - ZIP vs. base\n')
full.append(md_table(['Barra','Nome','V base','V ZIP','Delta V','Ang base','Ang ZIP','Delta ang'], [
    [r['bus'], r['name'], fnum(r['base_voltage_pu']), fnum(r['zip_voltage_pu']), fnum(r['delta_voltage_pu']), fnum(r['base_angle_deg'],1), fnum(r['zip_angle_deg'],1), fnum(r['delta_angle_deg'],1)]
    for r in zip_base_b
]))
full.append('\n## Tensoes - ZIP 110% vs. ZIP\n')
full.append(md_table(['Barra','Nome','V ZIP','V ZIP 110','Delta V','Ang ZIP','Ang ZIP 110','Delta ang'], [
    [r['bus'], r['name'], fnum(r['zip_voltage_pu']), fnum(r['zip_110_voltage_pu']), fnum(r['delta_voltage_pu']), fnum(r['zip_angle_deg'],1), fnum(r['zip_110_angle_deg'],1), fnum(r['delta_angle_deg'],1)]
    for r in zip110_zip_b
]))
full.append('\n## Fluxos - ZIP vs. base\n')
full.append(md_table(['De','Para','Circ','P base','P ZIP','Delta P','Q base','Q ZIP','Delta Q','Perdas base','Perdas ZIP','Delta perdas'], [
    [r['from_bus'], r['to_bus'], r['circuit'], fnum(r['base_p_mw'],1), fnum(r['zip_p_mw'],1), fnum(r['delta_p_mw'],1), fnum(r['base_q_mvar'],1), fnum(r['zip_q_mvar'],1), fnum(r['delta_q_mvar'],1), fnum(r['base_loss_mw'],2), fnum(r['zip_loss_mw'],2), fnum(r['delta_loss_mw'],2)]
    for r in zip_base_l
]))
full.append('\n## Fluxos - ZIP 110% vs. ZIP\n')
full.append(md_table(['De','Para','Circ','P ZIP','P ZIP 110','Delta P','Q ZIP','Q ZIP 110','Delta Q','Perdas ZIP','Perdas ZIP 110','Delta perdas'], [
    [r['from_bus'], r['to_bus'], r['circuit'], fnum(r['zip_p_mw'],1), fnum(r['zip_110_p_mw'],1), fnum(r['delta_p_mw'],1), fnum(r['zip_q_mvar'],1), fnum(r['zip_110_q_mvar'],1), fnum(r['delta_q_mvar'],1), fnum(r['zip_loss_mw'],2), fnum(r['zip_110_loss_mw'],2), fnum(r['delta_loss_mw'],2)]
    for r in zip110_zip_l
]))
(R / 'relatorio_tabelas.md').write_text('\n'.join(full) + '\n', encoding='utf-8')
print('generated', R / 'relatorio_resumo.md', R / 'relatorio_tabelas.md')
