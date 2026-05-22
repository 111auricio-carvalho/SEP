import csv
import shutil
from pathlib import Path

ROOT = Path(".")
RESULTS = ROOT / "results"
LATEX = RESULTS / "latex"
UFTEX = ROOT / "tools" / "UFTeX"


def read_csv(name):
    with (RESULTS / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def fmt(value, nd=3):
    try:
        return f"{float(value):.{nd}f}"
    except Exception:
        return str(value)


def tex_escape(value):
    text = str(value)
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(ch, ch) for ch in text)


def table(caption, label, headers, rows, align=None, landscape=False, size="\\scriptsize"):
    align = align or ("c" * len(headers))
    lines = []
    if landscape:
        lines.append(r"\begin{landscape}")
    lines.extend([
        size,
        rf"\begin{{longtable}}{{{align}}}",
        rf"\caption{{{tex_escape(caption)}}}\label{{{label}}}\\",
        r"\toprule",
        " & ".join(tex_escape(h) for h in headers) + r" \\",
        r"\midrule",
        r"\endfirsthead",
        rf"\caption[]{{{tex_escape(caption)} (continua)}}\\",
        r"\toprule",
        " & ".join(tex_escape(h) for h in headers) + r" \\",
        r"\midrule",
        r"\endhead",
        r"\midrule",
        rf"\multicolumn{{{len(headers)}}}{{r}}{{Continua na proxima pagina}}\\",
        r"\endfoot",
        r"\bottomrule",
        r"\endlastfoot",
    ])
    for row in rows:
        lines.append(" & ".join(tex_escape(x) for x in row) + r" \\")
    lines.append(r"\end{longtable}")
    if landscape:
        lines.append(r"\end{landscape}")
    lines.append(r"\normalsize")
    return "\n".join(lines)


def copy_uftex_class():
    dst = LATEX / "classe_uftex"
    dst.mkdir(parents=True, exist_ok=True)
    if not (UFTEX / "classe_uftex").exists():
        missing = [name for name in ["uftex.cls", "uftex.ist", "logouft.pdf"] if not (dst / name).exists()]
        if missing:
            raise FileNotFoundError("UFTeX files not found: " + ", ".join(missing))
        return
    for name in ["uftex.cls", "uftex.ist", "logouft.pdf"]:
        shutil.copy2(UFTEX / "classe_uftex" / name, dst / name)


def build():
    LATEX.mkdir(parents=True, exist_ok=True)
    copy_uftex_class()

    base_buses = read_csv("base_buses.csv")
    zip_base_buses = read_csv("compare_zip_vs_base_buses.csv")
    zip110_zip_buses = read_csv("compare_zip110_vs_zip_buses.csv")
    zip_base_branches = read_csv("compare_zip_vs_base_branches.csv")
    zip110_zip_branches = read_csv("compare_zip110_vs_zip_branches.csv")

    sections = []
    sections.append(table(
        "Tensoes nas barras - caso base",
        "tab:tensoes-base",
        ["Barra", "Nome", "Tipo", "V (pu)", "Ang. (graus)", "Pg (MW)", "Qg (Mvar)", "Carga P (MW)", "Carga Q (Mvar)"],
        [
            [r["bus"], r["name"], r["type"], fmt(r["voltage_pu"]), fmt(r["angle_deg"], 1),
             fmt(r["gen_mw"], 1), fmt(r["gen_mvar"], 1), fmt(r["load_mw"], 1), fmt(r["load_mvar"], 1)]
            for r in base_buses
        ],
        align="rllrrrrrr",
    ))
    sections.append(table(
        "Comparacao de tensoes - ZIP 40/40/20 vs. caso base",
        "tab:tensoes-zip-base",
        ["Barra", "Nome", "V base", "V ZIP", "Delta V", "Ang. base", "Ang. ZIP", "Delta ang."],
        [
            [r["bus"], r["name"], fmt(r["base_voltage_pu"]), fmt(r["zip_voltage_pu"]),
             fmt(r["delta_voltage_pu"]), fmt(r["base_angle_deg"], 1), fmt(r["zip_angle_deg"], 1),
             fmt(r["delta_angle_deg"], 1)]
            for r in zip_base_buses
        ],
        align="rlrrrrrr",
    ))
    sections.append(table(
        "Comparacao de tensoes - ZIP 110% vs. ZIP original",
        "tab:tensoes-zip110-zip",
        ["Barra", "Nome", "V ZIP", "V ZIP 110%", "Delta V", "Ang. ZIP", "Ang. ZIP 110%", "Delta ang."],
        [
            [r["bus"], r["name"], fmt(r["zip_voltage_pu"]), fmt(r["zip_110_voltage_pu"]),
             fmt(r["delta_voltage_pu"]), fmt(r["zip_angle_deg"], 1), fmt(r["zip_110_angle_deg"], 1),
             fmt(r["delta_angle_deg"], 1)]
            for r in zip110_zip_buses
        ],
        align="rlrrrrrr",
    ))
    sections.append(table(
        "Comparacao de fluxos - ZIP 40/40/20 vs. caso base",
        "tab:fluxos-zip-base",
        ["De", "Para", "Circ.", "P base", "P ZIP", "Delta P", "Q base", "Q ZIP", "Delta Q", "Perdas base", "Perdas ZIP", "Delta perdas"],
        [
            [r["from_bus"], r["to_bus"], r["circuit"], fmt(r["base_p_mw"], 1), fmt(r["zip_p_mw"], 1),
             fmt(r["delta_p_mw"], 1), fmt(r["base_q_mvar"], 1), fmt(r["zip_q_mvar"], 1),
             fmt(r["delta_q_mvar"], 1), fmt(r["base_loss_mw"], 2), fmt(r["zip_loss_mw"], 2),
             fmt(r["delta_loss_mw"], 2)]
            for r in zip_base_branches
        ],
        align="rrcrrrrrrrrr",
        landscape=True,
        size="\\tiny",
    ))
    sections.append(table(
        "Comparacao de fluxos - ZIP 110% vs. ZIP original",
        "tab:fluxos-zip110-zip",
        ["De", "Para", "Circ.", "P ZIP", "P ZIP 110%", "Delta P", "Q ZIP", "Q ZIP 110%", "Delta Q", "Perdas ZIP", "Perdas 110%", "Delta perdas"],
        [
            [r["from_bus"], r["to_bus"], r["circuit"], fmt(r["zip_p_mw"], 1), fmt(r["zip_110_p_mw"], 1),
             fmt(r["delta_p_mw"], 1), fmt(r["zip_q_mvar"], 1), fmt(r["zip_110_q_mvar"], 1),
             fmt(r["delta_q_mvar"], 1), fmt(r["zip_loss_mw"], 2), fmt(r["zip_110_loss_mw"], 2),
             fmt(r["delta_loss_mw"], 2)]
            for r in zip110_zip_branches
        ],
        align="rrcrrrrrrrrr",
        landscape=True,
        size="\\tiny",
    ))

    tex = r"""\documentclass[12pt]{classe_uftex/uftex}
\usepackage{longtable}
\usepackage{pdflscape}
\usepackage{array}

\begin{document}
\mainmatter
\chapter*{Relatorio de Tabelas de Resultados}
\addcontentsline{toc}{chapter}{Relatorio de Tabelas de Resultados}

Este relatorio apresenta apenas as tabelas extraidas dos resultados do ANAREDE para o sistema IEEE 39 barras.

""" + "\n\n".join(sections) + "\n\n\\end{document}\n"
    (LATEX / "relatorio_tabelas.tex").write_text(tex, encoding="utf-8")
    print(LATEX / "relatorio_tabelas.tex")


if __name__ == "__main__":
    build()
