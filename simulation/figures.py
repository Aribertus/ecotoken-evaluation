"""Figures for the Economic Simulation subsection (vector PDF, print-oriented)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from model import PV, pv_case, rec_case

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"

plt.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.edgecolor": INK2,
    "axes.labelcolor": INK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
    "legend.frameon": False, "pdf.fonttype": 42,
})


def fig_pv():
    go = np.linspace(0.0, 5.0, 101)
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    lo, hi = PV["ppa_eur_mwh"][0], PV["ppa_eur_mwh"][2]
    ax.axhspan(lo, hi, color="#f0efeb", zorder=0)
    ax.text(0.08, hi - 1.2, "Italian utility-scale solar PPA range", color=INK2, fontsize=8, va="top")
    styles = [("-", BLUE), ("--", ORANGE), ("-.", AQUA)]
    for (ls, col), y in zip(styles, PV["yield_kwh_kwp"]):
        be = [pv_case(yield_=y, go_price=g, fee=0.05)["breakeven_ppa"] for g in go]
        ax.plot(go, be, ls, color=col, lw=2, label=f"{int(y):,} kWh/kWp")
        ax.text(5.08, be[-1], f"{int(y):,}", color=INK, fontsize=8, va="center")
    ax.set_xlim(0, 5.9)
    ax.set_ylim(30, 68)
    ax.set_xlabel("GO price (EUR/MWh)")
    ax.set_ylabel("Break-even PPA price (EUR/MWh)")
    ax.text(5.08, 47.5, "Specific yield\n(kWh/kWp)", color=INK2, fontsize=7.5, va="bottom")
    fig.tight_layout()
    fig.savefig("figures/fig_pv_breakeven.pdf")
    fig.savefig("figures/fig_pv_breakeven.png", dpi=150)


def fig_rec():
    t = np.array([1000, 1500, 2000, 3000, 5000, 7500, 10_000, 15_000, 20_000, 30_000, 50_000])
    fig, ax = plt.subplots(figsize=(5.2, 3.1))
    for ns, ls, col, lab in [(1, "-", BLUE, "Standalone facility"),
                             (10, "--", ORANGE, "Aggregated (10 facilities)")]:
        v = [rec_case(throughput=x, with_plastic=False, n_share=ns)["carbon_net_per_t"] for x in t]
        ax.plot(t, v, ls, color=col, lw=2, marker="o", ms=4, label=lab)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xscale("log")
    ax.set_xticks([1000, 2000, 5000, 10_000, 20_000, 50_000])
    ax.set_xticklabels(["1k", "2k", "5k", "10k", "20k", "50k"])
    ax.set_xlabel("Facility throughput (t plastic waste per year, log scale)")
    ax.set_ylabel("Net carbon-credit revenue (USD/t)")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig("figures/fig_rec_aggregation.pdf")
    fig.savefig("figures/fig_rec_aggregation.png", dpi=150)


if __name__ == "__main__":
    fig_pv()
    fig_rec()
