"""
Economic simulation for the Ecotoken paper (Evaluation, Economic Simulation).

Two cases, parameterised from public sources (see PARAMS and SOURCES):
  A. 60 MWp utility-scale PV plant in southern Italy, monetising Guarantees
     of Origin (GOs) through the platform (Scope 2 attribute claims only).
  B. Plastic recycling facility outside the EU, monetising carbon credits
     (Verra VMR0007) and plastic credits (Verra PWRM0002).

The platform fee is a swept parameter (2-10 %), not a commercial figure.
All results are illustrative and reproducible: run `python3 model.py`.
"""
import json
import numpy as np

RNG = np.random.default_rng(20260924)

# --------------------------------------------------------------------------
# Parameters: (low, central, high). Currency: EUR for case A, USD for case B.
# --------------------------------------------------------------------------
PV = dict(
    capacity_mw=60.0,
    yield_kwh_kwp=(1400.0, 1500.0, 1800.0),   # fixed tilt ... single-axis tracker, S. Italy
    degradation=0.005,                       # per year
    lifetime=30,
    capex_eur_kw=(650.0, 720.0, 800.0),      # IRENA 2024 Europe avg USD 779/kW
    opex_eur_kw_yr=(10.0, 14.0, 18.0),       # assumption within IRENA-reported ranges
    ppa_eur_mwh=(48.0, 55.0, 65.0),          # Italy utility-scale solar PPA range
    wacc=(0.05, 0.06, 0.07),                 # nominal, assumption
    go_price=(0.3, 1.0, 2.0, 5.0),           # scenarios, EUR/MWh
    go_admin_eur_yr=10_000.0,                # registry/account admin, assumption
)

REC = dict(
    throughput_t=10_000.0,                   # t plastic waste input per year
    recycling_yield=0.80,                    # output/input, assumption
    avoid_tco2_t=(1.0, 1.5, 2.0),            # JRC: 1.49 t CO2e/t mixed polymer waste
    carbon_price_usd=(3.0, 6.34, 15.0),      # EM SOVCM 2025: 2024 avg USD 6.34
    plastic_price_usd=(200.0, 400.0, 800.0), # Verra initial estimates USD 200-800/t
    validation_usd=25_000.0,                 # one-off per standard, assumption
    verification_usd_yr=15_000.0,            # per standard per year, assumption
    issuance_levy_usd=0.23,                  # Verra issuance fee per unit
    retirement_fee_usd=0.02,                 # Verra retirement fee per unit
    crediting_years=10,
    discount=0.08,
)

FEES = (0.02, 0.05, 0.10)


def annuity_factor(r, n):
    return (1 - (1 + r) ** -n) / r


def pv_degraded_energy(yield_kwh_kwp, cap_mw, deg, n):
    """Annual MWh for years 1..n."""
    e0 = yield_kwh_kwp * cap_mw  # kWh/kWp * MWp = MWh
    return np.array([e0 * (1 - deg) ** t for t in range(n)])


def pv_case(yield_=None, capex=None, opex=None, ppa=None, wacc=None,
            go_price=1.0, fee=0.05, p=PV):
    y = yield_ if yield_ is not None else p["yield_kwh_kwp"][1]
    c = capex if capex is not None else p["capex_eur_kw"][1]
    o = opex if opex is not None else p["opex_eur_kw_yr"][1]
    s = ppa if ppa is not None else p["ppa_eur_mwh"][1]
    r = wacc if wacc is not None else p["wacc"][1]
    n = p["lifetime"]
    kw = p["capacity_mw"] * 1000
    e = pv_degraded_energy(y, p["capacity_mw"], p["degradation"], n)
    disc = (1 + r) ** -np.arange(1, n + 1)
    capex_tot = c * kw
    opex_yr = o * kw
    energy_rev = e * s
    go_net = np.maximum(e * go_price * (1 - fee) - p["go_admin_eur_yr"], 0.0)
    npv_base = -capex_tot + np.sum((energy_rev - opex_yr) * disc)
    npv_go = npv_base + np.sum(go_net * disc)
    disc_energy = np.sum(e * disc)
    lcoe = (capex_tot + np.sum(opex_yr * disc)) / disc_energy
    breakeven_ppa = lcoe - np.sum(go_net * disc) / disc_energy
    return dict(
        energy_y1_mwh=e[0],
        energy_rev_y1=energy_rev[0],
        go_net_y1=go_net[0],
        go_share_pct=100 * go_net[0] / energy_rev[0],
        npv_base=npv_base,
        npv_uplift=npv_go - npv_base,
        lcoe=lcoe,
        breakeven_ppa=breakeven_ppa,
    )


def rec_case(throughput=None, avoid=None, cprice=None, pprice=None, fee=0.05,
             with_plastic=True, n_share=1, p=REC):
    """Net environmental revenue; fixed MRV costs shared among n_share facilities
    (aggregation, e.g. a Programme of Activities)."""
    t = throughput if throughput is not None else p["throughput_t"]
    a = avoid if avoid is not None else p["avoid_tco2_t"][1]
    cp = cprice if cprice is not None else p["carbon_price_usd"][1]
    pp = pprice if pprice is not None else p["plastic_price_usd"][1]
    n, r = p["crediting_years"], p["discount"]
    per_unit = p["issuance_levy_usd"] + p["retirement_fee_usd"]
    vcu = t * a
    carbon_net = vcu * (cp * (1 - fee) - per_unit) - p["verification_usd_yr"] / n_share
    plastic_units = t * p["recycling_yield"]
    plastic_net = (plastic_units * (pp * (1 - fee) - per_unit)
                   - p["verification_usd_yr"] / n_share) if with_plastic else 0.0
    n_std = 2 if with_plastic else 1
    upfront = n_std * p["validation_usd"] / n_share
    af = annuity_factor(r, n)
    npv = -upfront + (carbon_net + plastic_net) * af
    return dict(
        vcu_yr=vcu,
        plastic_units_yr=plastic_units,
        carbon_net_yr=carbon_net,
        plastic_net_yr=plastic_net,
        carbon_net_per_t=carbon_net / t,
        total_net_per_t=(carbon_net + plastic_net) / t,
        npv=npv,
    )


def rec_plastic_only_npv(pprice, fee=0.05, p=REC):
    """NPV of the plastic-credit stream alone (one standard's MRV costs)."""
    per_unit = p["issuance_levy_usd"] + p["retirement_fee_usd"]
    net = p["throughput_t"] * p["recycling_yield"] * (pprice * (1 - fee) - per_unit) - p["verification_usd_yr"]
    return -p["validation_usd"] + net * annuity_factor(p["discount"], p["crediting_years"])


def tri(lo, mid, hi, size):
    return RNG.triangular(lo, mid, hi, size)


def monte_carlo(n=20_000):
    out = {}
    # Case A: NPV uplift from GOs, GO price uniform-log between 0.3 and 5
    go = np.exp(RNG.uniform(np.log(0.3), np.log(5.0), n))
    y = tri(*PV["yield_kwh_kwp"], n)
    fee = RNG.uniform(0.02, 0.10, n)
    ppa = tri(*PV["ppa_eur_mwh"], n)
    capex = tri(*PV["capex_eur_kw"], n)
    opex = tri(*PV["opex_eur_kw_yr"], n)
    wacc = tri(*PV["wacc"], n)
    upl, share, npvb = [], [], []
    for i in range(n):
        res = pv_case(y[i], capex[i], opex[i], ppa[i], wacc[i], go[i], fee[i])
        upl.append(res["npv_uplift"]); share.append(res["go_share_pct"]); npvb.append(res["npv_base"])
    upl, share, npvb = map(np.array, (upl, share, npvb))
    marginal = npvb < 0
    rescued = marginal & (npvb + upl >= 0)
    out["pv"] = dict(
        npv_uplift_p10_p50_p90=np.percentile(upl, [10, 50, 90]).tolist(),
        go_share_pct_p10_p50_p90=np.percentile(share, [10, 50, 90]).tolist(),
        frac_base_npv_negative=float(marginal.mean()),
        frac_of_negative_rescued_by_go=float(rescued.sum() / max(marginal.sum(), 1)),
    )
    # Case B
    a = tri(*REC["avoid_tco2_t"], n)
    cp = tri(*REC["carbon_price_usd"], n)
    pp = tri(*REC["plastic_price_usd"], n)
    fee = RNG.uniform(0.02, 0.10, n)
    c_only = np.array([rec_case(avoid=a[i], cprice=cp[i], fee=fee[i], with_plastic=False)["npv"] for i in range(n)])
    both = np.array([rec_case(avoid=a[i], cprice=cp[i], pprice=pp[i], fee=fee[i])["npv"] for i in range(n)])
    out["rec"] = dict(
        npv_carbon_only_p10_p50_p90=np.percentile(c_only, [10, 50, 90]).tolist(),
        npv_carbon_plus_plastic_p10_p50_p90=np.percentile(both, [10, 50, 90]).tolist(),
        frac_carbon_only_negative=float((c_only < 0).mean()),
    )
    return out


def main():
    results = {"pv_scenarios": [], "rec_scenarios": [], "rec_size": []}
    for g in PV["go_price"]:
        for f in FEES:
            r = pv_case(go_price=g, fee=f)
            results["pv_scenarios"].append(dict(go_price=g, fee=f, **{k: float(v) for k, v in r.items()}))
    # yield sensitivity at central GO price
    results["pv_yield"] = [dict(yield_=y, **{k: float(v) for k, v in pv_case(yield_=y, go_price=1.0).items()})
                           for y in PV["yield_kwh_kwp"]]
    for cp in REC["carbon_price_usd"]:
        for pp in REC["plastic_price_usd"]:
            r = rec_case(cprice=cp, pprice=pp)
            results["rec_scenarios"].append(dict(carbon_price=cp, plastic_price=pp, **{k: float(v) for k, v in r.items()}))
    results["rec_plastic_only"] = [dict(plastic_price=pp, npv=float(rec_plastic_only_npv(pp)))
                                   for pp in REC["plastic_price_usd"]]
    results["rec_carbon_only"] = [dict(carbon_price=cp, **{k: float(v) for k, v in rec_case(cprice=cp, with_plastic=False).items()})
                                  for cp in REC["carbon_price_usd"]]
    for t in [1000, 2000, 5000, 10_000, 20_000, 50_000]:
        for ns in (1, 10):
            r = rec_case(throughput=t, with_plastic=False, n_share=ns)
            results["rec_size"].append(dict(throughput=t, n_share=ns, **{k: float(v) for k, v in r.items()}))
    results["monte_carlo"] = monte_carlo()
    with open("results.json", "w") as fh:
        json.dump(results, fh, indent=1)
    return results


if __name__ == "__main__":
    import pprint
    res = main()
    pprint.pprint(res["monte_carlo"])
