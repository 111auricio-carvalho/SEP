import csv
import re
from pathlib import Path

ROOT = Path('.')
RESULTS = ROOT / 'results'
CASES = {
    'base': ROOT / 'RESULTADO_BASE.TXT',
    'zip': ROOT / 'RESULTADO_ZIP.TXT',
    'zip_110': ROOT / 'RESULTADO_ZIP_110.TXT',
}

bus_re = re.compile(r'^\s*(\d+)\s+(BUS|GEN)\s+(\d+)\s+(\d)\s+([0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)\s+[-0-9.]+\s+[-0-9.]+\s+([-0-9.]+)\s+([-0-9.]+)')
branch_re = re.compile(r'^\s+9999\.0\s+9999\.0\s+9999\.0\s+[-0-9.]+%\s+(\d+)\s+(BUS|GEN)\s+(\d+)\s+(\d+)\s+([-0-9.]+)\s+([-0-9.]+)\s+([-0-9.]+)(?:\s+[-0-9.]+F?)?\s+([-0-9.]+)\s+([-0-9.]+)')


def read_text(path):
    return path.read_text(encoding='latin-1', errors='replace').splitlines()


def parse_case(path):
    buses = []
    branches = []
    current_bus = None
    current_name = None
    in_bus_report = False
    in_complete = False
    for line in read_text(path):
        if 'RELATORIO DE BARRAS CA DO SISTEMA' in line:
            in_bus_report = True
            in_complete = False
            continue
        if 'RELATORIO COMPLETO DO SISTEMA' in line:
            in_bus_report = False
            in_complete = True
            current_bus = None
            current_name = None
            continue
        if in_bus_report:
            m = bus_re.match(line)
            if m:
                num = int(m.group(1))
                name = f'{m.group(2)} {int(m.group(3)):02d}' if m.group(2) == 'BUS' else f'{m.group(2)} {int(m.group(3))}'
                buses.append({
                    'bus': num,
                    'name': name,
                    'type': int(m.group(4)),
                    'voltage_pu': float(m.group(5)),
                    'angle_deg': float(m.group(6)),
                    'gen_mw': float(m.group(7)),
                    'gen_mvar': float(m.group(8)),
                    'load_mw': float(m.group(9)),
                    'load_mvar': float(m.group(10)),
                })
        elif in_complete:
            m_bus = re.match(r'^\s*(\d+)\s+\d+\s+\d\s+([0-9.]+)\s+', line)
            if m_bus:
                current_bus = int(m_bus.group(1))
                current_name = None
                continue
            m_name = re.match(r'^\s+(BUS|GEN)\s+(\d+)\s+', line)
            if m_name and current_bus is not None:
                current_name = f'{m_name.group(1)} {int(m_name.group(2)):02d}' if m_name.group(1) == 'BUS' else f'{m_name.group(1)} {int(m_name.group(2))}'
                continue
            m = branch_re.match(line)
            if m and current_bus is not None:
                to_bus = int(m.group(1))
                if current_bus > to_bus:
                    continue
                branches.append({
                    'from_bus': current_bus,
                    'from_name': current_name or '',
                    'to_bus': to_bus,
                    'to_name': f'{m.group(2)} {int(m.group(3)):02d}' if m.group(2) == 'BUS' else f'{m.group(2)} {int(m.group(3))}',
                    'circuit': int(m.group(4)),
                    'p_mw': float(m.group(5)),
                    'q_mvar': float(m.group(6)),
                    'mva': float(m.group(7)),
                    'loss_mw': float(m.group(8)),
                    'loss_mvar': float(m.group(9)),
                })
    return buses, branches


def write_csv(path, rows, fieldnames):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

all_buses = {}
all_branches = {}
for case, path in CASES.items():
    buses, branches = parse_case(path)
    all_buses[case] = {r['bus']: r for r in buses}
    all_branches[case] = {(r['from_bus'], r['to_bus'], r['circuit']): r for r in branches}
    write_csv(RESULTS / f'{case}_buses.csv', buses, ['bus','name','type','voltage_pu','angle_deg','gen_mw','gen_mvar','load_mw','load_mvar'])
    write_csv(RESULTS / f'{case}_branches.csv', branches, ['from_bus','from_name','to_bus','to_name','circuit','p_mw','q_mvar','mva','loss_mw','loss_mvar'])

# bus comparisons
for a, b, outname in [('base','zip','compare_zip_vs_base_buses.csv'), ('zip','zip_110','compare_zip110_vs_zip_buses.csv')]:
    rows = []
    for bus in sorted(set(all_buses[a]) & set(all_buses[b])):
        ra, rb = all_buses[a][bus], all_buses[b][bus]
        rows.append({
            'bus': bus,
            'name': rb['name'],
            f'{a}_voltage_pu': ra['voltage_pu'],
            f'{b}_voltage_pu': rb['voltage_pu'],
            'delta_voltage_pu': round(rb['voltage_pu'] - ra['voltage_pu'], 6),
            f'{a}_angle_deg': ra['angle_deg'],
            f'{b}_angle_deg': rb['angle_deg'],
            'delta_angle_deg': round(rb['angle_deg'] - ra['angle_deg'], 6),
        })
    write_csv(RESULTS / outname, rows, list(rows[0].keys()) if rows else [])

for a, b, outname in [('base','zip','compare_zip_vs_base_branches.csv'), ('zip','zip_110','compare_zip110_vs_zip_branches.csv')]:
    rows = []
    for key in sorted(set(all_branches[a]) & set(all_branches[b])):
        ra, rb = all_branches[a][key], all_branches[b][key]
        rows.append({
            'from_bus': key[0],
            'to_bus': key[1],
            'circuit': key[2],
            f'{a}_p_mw': ra['p_mw'],
            f'{b}_p_mw': rb['p_mw'],
            'delta_p_mw': round(rb['p_mw'] - ra['p_mw'], 6),
            f'{a}_q_mvar': ra['q_mvar'],
            f'{b}_q_mvar': rb['q_mvar'],
            'delta_q_mvar': round(rb['q_mvar'] - ra['q_mvar'], 6),
            f'{a}_loss_mw': ra['loss_mw'],
            f'{b}_loss_mw': rb['loss_mw'],
            'delta_loss_mw': round(rb['loss_mw'] - ra['loss_mw'], 6),
        })
    write_csv(RESULTS / outname, rows, list(rows[0].keys()) if rows else [])

print('buses', {k: len(v) for k,v in all_buses.items()})
print('branches', {k: len(v) for k,v in all_branches.items()})
