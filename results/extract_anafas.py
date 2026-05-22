import csv
import re
from pathlib import Path

ROOT = Path(".")
RESULTS = ROOT / "results"
BASE = ROOT / "RESULTADO_ANAFAS_BASE.TXT"
FT4 = ROOT / "RESULTADO_ANAFAS_FT_BARRA4.TXT"

case_re = re.compile(r"^\s*\d+\s+(FT|FF|FFT|FFF)\s+(\d+)\s+BUS\s*(\d+)\s+Caso-Base")
bar_re = re.compile(r"^\s*Bar\.\s+(\d+)\s*\(([^)]*)\)\s+TEN\.\(pu\)")


def read_lines(path):
    return path.read_text(encoding="latin-1", errors="replace").splitlines()


def write_csv(path, rows, fieldnames):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_phase_rows(lines, idx):
    rows = {}
    for line in lines[idx:idx + 8]:
        parts = line.split()
        if len(parts) >= 12 and parts[0] in {"A", "B", "C"}:
            rows[parts[0]] = {
                "v_mod": float(parts[1]),
                "v_ang": float(parts[2]),
                "i_mod_a": abs(float(parts[7])),
                "i_ang": float(parts[8]),
            }
        if len(rows) == 3:
            break
    return rows


def parse_base_fault_levels():
    lines = read_lines(BASE)
    rows = {}
    current_case = None
    for i, line in enumerate(lines):
        m = case_re.match(line)
        if m:
            fault, bus = m.group(1), int(m.group(2))
            current_case = (bus, fault)
            rows.setdefault(bus, {"bus": bus, "name": f"BUS {bus:02d}"})
            continue
        if current_case and "TENSAO(pu)" in line and "CORRENTE" in line:
            phase_rows = parse_phase_rows(lines, i + 2)
            if set(phase_rows) == {"A", "B", "C"}:
                bus, fault = current_case
                rows[bus][fault] = max(r["i_mod_a"] for r in phase_rows.values()) / 1000.0
                current_case = None

    out = []
    for bus in sorted(rows):
        r = rows[bus]
        out.append({
            "bus": bus,
            "name": r["name"],
            "ft_ka": round(r.get("FT", 0.0), 4),
            "ff_ka": round(r.get("FF", 0.0), 4),
            "fft_ka": round(r.get("FFT", 0.0), 4),
            "sim_ka": round(r.get("FFF", 0.0), 4),
        })
    write_csv(RESULTS / "anafas_base_fault_levels.csv", out, ["bus", "name", "ft_ka", "ff_ka", "fft_ka", "sim_ka"])
    return out


def parse_ft_barra4():
    lines = read_lines(FT4)
    fault_current = None
    voltages = {}

    for i, line in enumerate(lines):
        if fault_current is None and "TENSAO(pu)" in line and "CORRENTE" in line:
            phase_rows = parse_phase_rows(lines, i + 2)
            if set(phase_rows) == {"A", "B", "C"}:
                fault_current = max(r["i_mod_a"] for r in phase_rows.values()) / 1000.0
        m = bar_re.match(line)
        if m:
            bus = int(m.group(1))
            if bus in voltages:
                continue
            phase_rows = parse_phase_rows(lines, i + 2)
            if set(phase_rows) == {"A", "B", "C"}:
                voltages[bus] = {
                    "bus": bus,
                    "name": f"BUS {bus:02d}",
                    "va_pu": phase_rows["A"]["v_mod"],
                    "anga_deg": phase_rows["A"]["v_ang"],
                    "vb_pu": phase_rows["B"]["v_mod"],
                    "angb_deg": phase_rows["B"]["v_ang"],
                    "vc_pu": phase_rows["C"]["v_mod"],
                    "angc_deg": phase_rows["C"]["v_ang"],
                }

    voltage_rows = [voltages[k] for k in sorted(voltages)]
    write_csv(
        RESULTS / "anafas_ft_barra4_voltages.csv",
        voltage_rows,
        ["bus", "name", "va_pu", "anga_deg", "vb_pu", "angb_deg", "vc_pu", "angc_deg"],
    )
    summary = [{
        "fault": "FT",
        "bus": 4,
        "name": "BUS 04",
        "fault_current_ka": round(fault_current or 0.0, 4),
        "voltage_buses_reported": len(voltage_rows),
    }]
    write_csv(RESULTS / "anafas_ft_barra4_summary.csv", summary, ["fault", "bus", "name", "fault_current_ka", "voltage_buses_reported"])
    return summary, voltage_rows


if __name__ == "__main__":
    base = parse_base_fault_levels()
    summary, voltages = parse_ft_barra4()
    print("anafas_base_fault_levels", len(base))
    print("anafas_ft_barra4_summary", summary[0])
    print("anafas_ft_barra4_voltages", len(voltages))
