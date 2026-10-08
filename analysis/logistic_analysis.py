"""Fit logistic growth curves to NetLogo migration-screen output.

Expected CSV columns:
    migration,tick,cell_count

This script supports one or more FBS-specific migration-screen files and produces:
    - fitted logistic curves
    - fitted r and K by migration speed
    - R^2 values
    - tabulated results with speed on rows and FBS on columns

Edit FILES and FBS_VALUES before running.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def logistic(t, r, K, N0):
    exp_rt = np.exp(r * t)
    return (K * N0 * exp_rt) / (K + N0 * (exp_rt - 1))


FILES = [
    "migration_screen_1.csv",
    "migration_screen_5.csv",
    "migration_screen_8.csv",
    "migration_screen_9.csv",
    "migration_screen_9_5FBS.csv",
    "migration_screen_10FBS.csv",
]

FBS_VALUES = [1, 5, 8, 9, 9.5, 10]


def fit_all(files, fbs_values):
    records = []
    fit_results = {}

    for fn, fbs in zip(files, fbs_values):
        df = pd.read_csv(fn)

        for mig, group in df.groupby("migration"):
            t = group["tick"].to_numpy()
            N = group["cell_count"].to_numpy()
            order = np.argsort(t)
            t, N = t[order], N[order]

            N0 = N[0]
            p0 = [0.06, max(N.max(), N0 * 1.01)]

            try:
                popt, _ = curve_fit(
                    lambda tt, r, K: logistic(tt, r, K, N0),
                    t,
                    N,
                    p0=p0,
                    bounds=([0.0, N0], [1.0, np.inf]),
                    maxfev=20000,
                )
            except (RuntimeError, ValueError) as exc:
                print(f"Fit failed for FBS={fbs}, migration={mig}: {exc}")
                continue

            r_fit, K_fit = popt
            N_pred = logistic(t, r_fit, K_fit, N0)
            ss_res = np.sum((N - N_pred) ** 2)
            ss_tot = np.sum((N - np.mean(N)) ** 2)
            r2 = np.nan if ss_tot == 0 else 1 - ss_res / ss_tot
            speed = mig * 20.0

            records.append(
                {
                    "FBS": fbs,
                    "migration": mig,
                    "speed_um_h": speed,
                    "N0": N0,
                    "r": r_fit,
                    "K": K_fit,
                    "R2": r2,
                }
            )

            fit_results[(fbs, mig)] = {
                "r": r_fit,
                "K": K_fit,
                "N0": N0,
                "R2": r2,
                "speed": speed,
            }

    results = pd.DataFrame(records).sort_values(["FBS", "speed_um_h"])
    return results, fit_results


def make_tables(results):
    r_table = results.pivot(index="speed_um_h", columns="FBS", values="r")
    k_table = results.pivot(index="speed_um_h", columns="FBS", values="K")
    r2_table = results.pivot(index="speed_um_h", columns="FBS", values="R2")

    compact = results.copy()
    compact["Fit"] = compact.apply(
        lambda row: f"r={row['r']:.4f}; K={row['K']:.0f}; R²={row['R2']:.3f}",
        axis=1,
    )
    compact_table = compact.pivot(index="speed_um_h", columns="FBS", values="Fit")

    for table in (r_table, k_table, r2_table, compact_table):
        table.index.name = "Speed (µm/h)"
        table.columns.name = "FBS (%)"

    return r_table, k_table, r2_table, compact_table


def plot_fits(files, fbs_values, fit_results):
    global_max = max(pd.read_csv(fn)["cell_count"].max() for fn in files)
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), sharey=True)
    axes = axes.flatten()
    cmap = plt.get_cmap("viridis")

    for idx, (fn, fbs) in enumerate(zip(files, fbs_values)):
        ax = axes[idx]
        df = pd.read_csv(fn)
        migrations = sorted(df["migration"].unique())

        for j, mig in enumerate(migrations):
            if (fbs, mig) not in fit_results:
                continue

            group = df[df["migration"] == mig]
            t = group["tick"].to_numpy()
            N = group["cell_count"].to_numpy()
            order = np.argsort(t)
            t, N = t[order], N[order]

            fit = fit_results[(fbs, mig)]
            t_fit = np.linspace(t.min(), t.max(), 300)
            N_fit = logistic(t_fit, fit["r"], fit["K"], fit["N0"])
            color = cmap(j / max(len(migrations) - 1, 1))

            ax.scatter(t, N, s=7, color=color, alpha=0.35)
            ax.plot(t_fit, N_fit, color=color, linewidth=2, label=f"{fit['speed']:.1f} µm/h")

        ax.set_title(f"FBS = {fbs}%")
        ax.set_xlabel("Time (h)")
        if idx % 3 == 0:
            ax.set_ylabel("Cell count")
        ax.set_ylim(0, global_max * 1.10)
        ax.grid(True, alpha=0.3)
        ax.legend(title="Migration speed", fontsize=7, title_fontsize=8)

    plt.tight_layout()
    plt.show()


def plot_parameters(results):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    for fbs, group in results.groupby("FBS"):
        group = group.sort_values("speed_um_h")
        ax1.plot(group["speed_um_h"], group["r"], marker="o", label=f"{fbs}%")
        ax2.plot(group["speed_um_h"], group["K"], marker="o", label=f"{fbs}%")

    ax1.set_xlabel("Migration speed (µm/h)")
    ax1.set_ylabel("Intrinsic growth rate, r")
    ax1.set_title("Growth rate vs. migration speed")
    ax1.grid(True, alpha=0.3)
    ax1.legend(title="FBS")

    ax2.set_xlabel("Migration speed (µm/h)")
    ax2.set_ylabel("Carrying capacity, K")
    ax2.set_title("Carrying capacity vs. migration speed")
    ax2.grid(True, alpha=0.3)
    ax2.legend(title="FBS")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    results, fit_results = fit_all(FILES, FBS_VALUES)
    r_table, k_table, r2_table, compact_table = make_tables(results)

    print("\nFULL RESULTS\n")
    print(results.round({"speed_um_h": 2, "r": 5, "K": 1, "R2": 4}))
    print("\nINTRINSIC GROWTH RATE r\n")
    print(r_table.round(5))
    print("\nCARRYING CAPACITY K\n")
    print(k_table.round(1))
    print("\nR-SQUARED\n")
    print(r2_table.round(4))
    print("\nCOMBINED FIT TABLE\n")
    print(compact_table)

    results.to_csv("all_logistic_fit_results.csv", index=False)
    r_table.to_csv("logistic_r_table.csv")
    k_table.to_csv("logistic_K_table.csv")
    r2_table.to_csv("logistic_R2_table.csv")
    compact_table.to_csv("logistic_compact_table.csv")

    plot_fits(FILES, FBS_VALUES, fit_results)
    plot_parameters(results)
