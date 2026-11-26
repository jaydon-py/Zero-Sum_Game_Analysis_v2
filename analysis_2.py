# ZERO SUM GAME ANALYSIS (PART 2) - DISTRIBUTION

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from scipy import stats
from scipy.stats import norm
from matplotlib.colors import to_rgba

from analysis_1 import games
from new_config import player_colours, player_colours2
from new_config import profit_footer, profit_title_block, profit_gbp

all_profits = games["profit"]
mu, std = norm.fit(all_profits)
kde = stats.gaussian_kde(all_profits)
kde_x = np.linspace(all_profits.min() - 2, all_profits.max() + 2, 200)

fig, ax = plt.subplots(figsize=(15, 7))

ax.plot(kde_x, kde(kde_x), color="#3463CE", lw=2, solid_capstyle="round", zorder=3)
ax.plot(kde_x, norm.pdf(kde_x, mu, std), color="#828282", lw=1.2, ls="--", alpha=0.6,
        label=f"Normal fit  μ={mu:.1f}, σ={std:.1f}", zorder=2)
ax.axvline(0, color='#828282', lw=0.8, ls=(0, (4, 4)), alpha=0.6, zorder=1)

ax.xaxis.set_major_formatter(profit_gbp)
ax.set_xlabel("Profit (£)", fontsize=10, labelpad=10)
ax.set_ylabel("Density", fontsize=10, labelpad=10)
ax.grid(False)
ax.margins(x=0.02)
ax.legend(frameon=False, loc="upper right")

fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.97)
profit_title_block(fig, ax, "Profit Distribution",
                   f"{len(all_profits)} results from {games['player'].nunique()} players")
profit_footer(fig)
plt.show()


# INDIVIDUAL PLAYER RESULT DISTRIBUTION - via probability density


profits = games["profit"]
kde_x = np.linspace(profits.min() - 2, profits.max() + 2, 400)

fig, ax = plt.subplots(figsize=(15, 7))

for player, player_profits in games.groupby("player")["profit"]:
    if player_profits.nunique() < 2:
        continue
    ax.plot(kde_x, stats.gaussian_kde(player_profits)(kde_x), color=player_colours2.get(player, "#888888"),
            lw=1.6, alpha=0.8, label=player, solid_capstyle="round")

ax.axvline(0, color='#828282', lw=0.8, ls=(0, (4, 4)), alpha=0.6, zorder=1)

ax.xaxis.set_major_formatter(profit_gbp)
ax.set_xlabel("Profit (£)", fontsize=10, labelpad=10)
ax.set_ylabel("Density", fontsize=10, labelpad=10)
ax.grid(False)
ax.margins(x=0.02)
ax.legend(fontsize=8, ncol=2, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))

fig.subplots_adjust(top=0.84, bottom=0.12, left=0.08, right=0.80)
profit_title_block(fig, ax, "Individual Player Profit Distributions",
                   "Excluding players who have played only 1 game")
profit_footer(fig)
plt.show()


# STOCK CHART


min_players = 4

candles = games.groupby("game_id").agg(
    low=("profit", "min"),
    high=("profit", "max"),
    q1=("profit", lambda s: s.quantile(0.25)),
    q3=("profit", lambda s: s.quantile(0.75)),
    median=("profit", "median"),
    pot=("buy_in", "sum"),
    n=("player", "count"),
).reset_index()

colours = np.where(candles["median"] >= 0, "#5fb49c", "#eb6f92")
fade = np.where(candles["n"] >= min_players, 1.0, 0.3)
x = candles["game_id"].to_numpy()
body_width = 0.6
min_body = (candles["high"].max() - candles["low"].min()) * 0.004

fig = plt.figure(figsize=(14, 8))
gs = gridspec.GridSpec(2, 1, height_ratios=[4, 1], hspace=0.06)
ax = fig.add_subplot(gs[0])
axv = fig.add_subplot(gs[1], sharex=ax)

ax.vlines(x, candles["low"], candles["high"], colors=[to_rgba(c, a) for c, a in zip(colours, fade)], lw=1.1, zorder=2)
ax.bar(x, np.maximum(candles["q3"] - candles["q1"], min_body), bottom=candles["q1"], width=body_width,
       color=[to_rgba(c, 0.85 * a) for c, a in zip(colours, fade)], edgecolor="none", zorder=3)
ax.hlines(candles["median"], x - body_width / 2, x + body_width / 2,
          colors=[to_rgba('#110130', 0.8 * a) for a in fade], lw=1.0, zorder=4)
ax.axhline(0, color='#828282', lw=0.8, ls=(0, (4, 4)), alpha=0.6)

axv.bar(x, candles["pot"], width=body_width, color='#3463CE', alpha=0.45, edgecolor="none")
axv.grid(False)
axv.set_ylabel("Volume (£)", fontsize=9, labelpad=8)

ax.set_ylabel("Profit per player (£)", fontsize=11, labelpad=10)
ax.yaxis.set_major_formatter(profit_gbp)
ax.margins(y=0.08)
ax.set_xlim(x.min() - 1, x.max() + 1)
plt.setp(ax.get_xticklabels(), visible=False)
axv.set_xticks(range(0, x.max() + 1, 5))

fig.subplots_adjust(top=0.85, bottom=0.12, left=0.07, right=0.97)
profit_title_block(fig, ax, "Every game as a candle", "How well is the money in the pot distributed every game?")
profit_footer(fig)
plt.show()

