# ZERO SUM GAME ANALYSIS (PART 1) - RESULT SPREADS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from new_config import player_colours, profit_gbp, profit_title_block, profit_footer

def load_games(path="AllRecordedGames.csv") -> pd.DataFrame:
    df = pd.read_csv(path, usecols=["game_id", "player", "buy_in", "cash_out"])
    df["player"] = df["player"].str.strip()
    df["profit"] = (df["cash_out"] - df["buy_in"]).round(2)
    return df.sort_values("game_id", kind="stable").reset_index(drop=True)

games = load_games()
colour_of = lambda player: player_colours.get(player, "#888888")

# CHAPTER 1: LUCK VS SKILL

# CUMULATIVE PROFIT BY PLAYER

summary = (games.groupby("player")
                .agg(profit=("profit", "sum"), games=("game_id", "count"))
                .round(2)
                .sort_values("profit")) 

fig, ax = plt.subplots(figsize=(12, 9))

y       = np.arange(len(summary))
colours = [colour_of(p) for p in summary.index]
ax.barh(y, summary["profit"], color=colours, height=0.72, zorder=3)

span = summary["profit"].max() - summary["profit"].min()
for yi, val in zip(y, summary["profit"]):
    ax.text(val + (0.012 * span if val >= 0 else -0.012 * span), yi, profit_gbp(val),
            ha="left" if val >= 0 else "right", va="center",
            color="#110130", fontsize=9, fontweight="bold")

ax.axvline(0, color="#828282", lw=0.8, ls=(0, (4, 4)), alpha=0.7, zorder=2)

ax.set_yticks(y)
ax.set_yticklabels([f"{p}  ({g})" for p, g in zip(summary.index, summary["games"])], fontsize=10)
for lbl, col in zip(ax.get_yticklabels(), colours):
    lbl.set_color(col)
ax.xaxis.set_major_formatter(profit_gbp)
ax.margins(x=0.14, y=0.02)
ax.grid(False, axis="y")
ax.set_xlabel("")

fig.subplots_adjust(top=0.88, bottom=0.06, left=0.13, right=0.96)
profit_title_block(fig, ax, "Current Profit by Player", "Games played in brackets.")
profit_footer(fig)
plt.show()


# SIMULATING A LUCK ONLY WORLD


simulations = 100_000

profit_obs  = games["profit"].to_numpy()
player_list = sorted(games["player"].unique())
n_players   = len(player_list)
player_idx  = games["player"].map({p: i for i, p in enumerate(player_list)}).to_numpy()
game_rows   = list(games.groupby("game_id").indices.values())              
eye         = np.eye(n_players)


def simulate(profit, player_idx, game_rows, n_sims, rng, keep=0):
    totals = np.zeros((n_sims, n_players))
    kept   = np.empty(len(profit))
    for rows in game_rows:
        order    = rng.random((n_sims, len(rows))).argsort(axis=1)  
        shuffled = profit[rows][order]                               
        totals  += shuffled @ eye[player_idx[rows]]                 
        kept[rows] = shuffled[keep]
    return np.round(totals, 2), kept


totals_obs = np.round(np.bincount(player_idx, weights=profit_obs, minlength=n_players), 2)
totals_sim, history = simulate(profit_obs, player_idx, game_rows, simulations,
                               np.random.default_rng(42), keep=0)                       

assert np.allclose(totals_sim.sum(axis=1), profit_obs.sum())
assert np.isclose(totals_obs.sum(), profit_obs.sum())
for rows in game_rows:
    assert np.allclose(np.sort(history[rows]), np.sort(profit_obs[rows]))

print(f"{simulations:,} alternative histories | {games['game_id'].nunique()} games | "
      f"{n_players} players")


# MEASURING SPREAD OF RESULTS - LUCK vs REALITY


def mc_p(n_extreme, n_sims):
    return (n_extreme + 1) / (n_sims + 1)

spread_obs = totals_obs.std()        
spread_sim = totals_sim.std(axis=1)  

n_extreme = int(np.sum(spread_sim >= spread_obs)) 
p_spread  = mc_p(n_extreme, simulations)
mc_error  = np.sqrt(p_spread * (1 - p_spread) / simulations)
lo, hi    = np.percentile(spread_sim, [5, 95])

print(f"Real spread:                £{spread_obs:.2f}")
print(f"Luck-only spread (average): £{spread_sim.mean():.2f}   (middle 90%: £{lo:.2f} to £{hi:.2f})")
print(f"Histories at least as spread out as reality: {n_extreme:,} of {simulations:,}")
print(f"p = {p_spread:.3f}  (simulation error about ±{mc_error:.3f})")

fig, ax = plt.subplots(figsize=(12, 7.5))

counts, edges = np.histogram(spread_sim, bins=60)
centres = (edges[:-1] + edges[1:]) / 2
width   = edges[1] - edges[0]
ax.bar(centres, counts, width=width * 0.92, zorder=3, alpha=0.85,
       color=np.where(centres >= spread_obs, "#ea819f", "#231e48ff")) 

ax.axvline(spread_obs, color='#ea819f', lw=2.2, zorder=4)

top = counts.max()
ax.text(spread_obs + width, top * 0.97, profit_gbp(spread_obs),
        color='#ea819f', fontsize=11, fontweight="bold", va="top", ha="left")
ax.text(spread_obs + width, top * 0.88, f"{p_spread:.1%} of histories\nare this spread out or more",
        color='#ea819f', fontsize=9.5, va="top", ha="left")

ax.xaxis.set_major_formatter(profit_gbp)
ax.set_xlabel("Standard Deviation, £", fontsize=10, labelpad=10)
ax.set_ylabel("Number of alternative histories", fontsize=10, labelpad=10)
ax.grid(False, axis="x")
ax.margins(x=0.03)

fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.97)
profit_title_block(fig, ax, "Is the Spread of Results Bigger Than Luck?",
                   f"{simulations:,} alternative histories. Visualisation shows standard deviation of all {n_players} player totals")
profit_footer(fig, f"p = {p_spread:.3f}")
plt.show()


# INDIVIDUAL RESULTS


PLAYER = "Jaydon"

if PLAYER not in player_list:
    raise ValueError(f"'{PLAYER}' not found. Choose from: {player_list}")

idx       = player_list.index(PLAYER)
real      = totals_obs[idx]                             
luck      = totals_sim[:, idx]                            
n_games   = int((games["player"] == PLAYER).sum())
games_txt = f"{n_games} game" + ("s" if n_games != 1 else "")

lo, hi    = np.percentile(luck, [2.5, 97.5])              
n_extreme = int(np.sum(np.abs(luck) >= abs(real)))      
p_two     = (n_extreme + 1) / (simulations + 1)
p_txt     = "p < 0.001" if p_two < 0.001 else f"p = {p_two:.3f}"
pctile    = ((luck < real).mean() + 0.5 * (luck == real).mean()) * 100 

print(f"{PLAYER}: {games_txt} played")
print(f"Real total:               {profit_gbp(real)}")
print(f"Luck-only range (95%):    {profit_gbp(lo)} to {profit_gbp(hi)}   (sd £{luck.std():.2f})")
print(f"Reality beats {pctile:.1f}% of luck-only histories")
print(f"As extreme as reality in {n_extreme:,} of {simulations:,} histories  ->  {p_txt} (two-sided)")

fig, ax = plt.subplots(figsize=(12, 7.5))

values, freq = np.unique(luck, return_counts=True)
if len(values) <= 40:
    centres, counts = values, freq
    width = np.diff(values).min() if len(values) > 1 else 1.0
else:
    counts, edges = np.histogram(luck, bins=60)
    centres = (edges[:-1] + edges[1:]) / 2
    width   = edges[1] - edges[0]

in_tail = np.abs(centres) >= abs(real) - 1e-9       
ax.bar(centres, counts, width=width * 0.92, zorder=3, alpha=0.85,
       color=np.where(in_tail, "#eb6f92", "#231e48ff"))

ax.axvline(real, color="#eb6f92", lw=2.2, zorder=4)

ax.xaxis.set_major_formatter(profit_gbp)
ax.set_xlabel(f"{PLAYER}'s total profit (£)", fontsize=10, labelpad=10)
ax.set_ylabel("Number of alternative histories", fontsize=10, labelpad=10)
ax.grid(False, axis="x")
ax.margins(x=0.06)

fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.97)
profit_title_block(fig, ax, f"{PLAYER}: Reality vs Luck",
                   f"{games_txt} played, {simulations:,} alternative histories")
profit_footer(fig, f"95% luck range {profit_gbp(lo)} to {profit_gbp(hi)}  |  {p_txt} (two-sided)")
plt.show()

