# ZERO SUM GAME ANALYSIS (PART 3) - Overall Rating

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats

from new_config import player_colours
from new_config import profit_title_block, profit_footer, soften_axes, soften_legend, profit_gbp
from analysis_1 import games

BASE = 10
EXPECTATION = 5
STARTING_OVR = 40
MIN_GAMES = 5


def calculate_ovr_history(data):
    ratings = {player: STARTING_OVR for player in data["player"].unique()}
    rows = []
    for game_id, game in data.sort_values("game_id", kind="stable").groupby("game_id"):
        n = len(game)
        if n < 2:
            continue
        before = game["player"].map(ratings)
        expected = before.rank(ascending=False)
        actual = game["profit"].rank(ascending=False)
        change = BASE * ((n + 1 - 2 * actual) / (n - 1)) + EXPECTATION * (expected - actual)
        after = (before + change).clip(lower=1)
        ratings.update(zip(game["player"], after))
        rows.append(pd.DataFrame({"game_id": game_id, "player": game["player"].values,
                                  "profit": game["profit"].values, "ovr_change": change.values,
                                  "ovr": after.values}))
    return pd.concat(rows, ignore_index=True)


game_counts = games.groupby("player")["game_id"].nunique()
is_low = games["player"].isin(game_counts[game_counts <= MIN_GAMES].index)
pooled = pd.concat([
    games.loc[~is_low, ["game_id", "player", "profit"]],
    games[is_low].groupby("game_id", as_index=False).agg(profit=("profit", "mean")).assign(player="<5G"),
], ignore_index=True)

df_ovr_individual = calculate_ovr_history(games[["game_id", "player", "profit"]])
df_ovr_history = calculate_ovr_history(pooled)

latest = df_ovr_history.sort_values("game_id", kind="stable").groupby("player")["ovr"]
current_ovr = latest.last().sort_values(ascending=False)
best_ovr = latest.max()[current_ovr.index]

players = current_ovr.index.tolist()
x = np.arange(len(players))
width = 0.4
colours = [player_colours.get(p, "#888888") for p in players]

fig, ax = plt.subplots(figsize=(15, 6))

best_bars = ax.bar(x + width / 2, best_ovr, width=width, color=colours, label="Highest OVR", edgecolor="none", alpha=0.4)
current_bars = ax.bar(x - width / 2, current_ovr, width=width, color=colours, label="Current OVR", edgecolor="none", alpha=0.9)
for bars in (current_bars, best_bars):
    ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=9, fontweight="bold", color='#110130')

soften_axes(ax, ref_y=STARTING_OVR, ref_label="Starting OVR")
soften_legend(ax)

profit_title_block(fig, ax, "Current vs Highest Player OVR", "Excluding players who have played 5 games or less")

ax.set_ylabel("OVR")
ax.set_xticks(x, players, rotation=45, ha="right")
ax.set_ylim(0, max(best_ovr.max(), STARTING_OVR) * 1.15)

fig.subplots_adjust(left=0.06, right=0.83, top=0.84, bottom=0.18)
plt.show()


# How well does OVR correlate to cumulative profit?


corr = pd.DataFrame({
    "ovr": df_ovr_individual.sort_values("game_id", kind="stable").groupby("player")["ovr"].last(),
    "profit": games.groupby("player")["profit"].sum(),
}).dropna()

slope, intercept, r, *_ = stats.linregress(corr["profit"], corr["ovr"])
x_line = np.array([corr["profit"].min(), corr["profit"].max()])
colours = [player_colours.get(p, "#888888") for p in corr.index]

fig, ax = plt.subplots(figsize=(12, 7))

ax.scatter(corr["profit"], corr["ovr"], c=colours, s=85, edgecolor="white", linewidth=0.7, zorder=3)
for player, colour in zip(corr.index, colours):
    ax.annotate(player, (corr.at[player, "profit"], corr.at[player, "ovr"]), xytext=(6, 6),
                textcoords="offset points", color=colour, fontsize=9, fontweight="bold")
ax.plot(x_line, intercept + slope * x_line, color="#ebbcba", lw=1.8, ls="--", label="Linear regression")

soften_axes(ax)
soften_legend(ax)

profit_title_block(fig, ax, "Player OVR vs Cumulative Profit", "Relationship between current rating and cumulative profit")
ax.set_xlabel("Cumulative Profit (£)")
ax.set_ylabel("Current OVR")
profit_footer(fig, f"Pearson correlation: r = {r:.3f}")

fig.subplots_adjust(left=0.09, right=0.83, top=0.84, bottom=0.12)
plt.show()


# OVR and PROFIT OVER TIME


def align_axes(ax_left, ax_right, left_ref, right_ref=0, pad=0.10, f_min=0.08, f_max=0.92):
    def extents(ax, ref):
        lo, hi = ax.dataLim.y0, ax.dataLim.y1
        return max(ref - lo, 0), max(hi - ref, 0)

    below_l, above_l = extents(ax_left, left_ref)
    below_r, above_r = extents(ax_right, right_ref)

    f = max(below_l / ((below_l + above_l) or 1),
            below_r / ((below_r + above_r) or 1))
    f = min(max(f, f_min), f_max)

    for ax, ref, below, above in [(ax_left, left_ref, below_l, above_l),
                                  (ax_right, right_ref, below_r, above_r)]:
        span = max(below / f, above / (1 - f)) * (1 + pad)
        ax.set_ylim(ref - f * span, ref + (1 - f) * span)

PLAYER = "Jaydon"

if PLAYER not in df_ovr_history["player"].values:
    raise ValueError(f"'{PLAYER}' not found. Choose from: {sorted(df_ovr_history['player'].unique())}")

history = df_ovr_history[df_ovr_history["player"] == PLAYER].sort_values("game_id").copy()
history["cumulative_profit"] = history["profit"].cumsum()

colour_ovr = player_colours.get(PLAYER, "#c4a7e7")
colour_profit = "#f6c177"
line_kw = dict(lw=1.6, alpha=0.95, marker="o", ms=3.5, mew=0, solid_capstyle="round", zorder=3)

fig, ax1 = plt.subplots(figsize=(12, 7))
ax2 = ax1.twinx()

ax1.plot(history["game_id"], history["ovr"], color=colour_ovr, **line_kw)
ax1.axhline(STARTING_OVR, color='#828282', lw=0.8, ls=(0, (4, 4)), alpha=0.5)

ax2.plot(history["game_id"], history["cumulative_profit"], color=colour_profit, **line_kw)
ax2.fill_between(history["game_id"], 0, history["cumulative_profit"], color=colour_profit, alpha=0.06, zorder=1)

ax1.set_ylabel("OVR", color=colour_ovr, fontsize=11, labelpad=10)
ax2.set_ylabel("Cumulative Profit (£)", color=colour_profit, fontsize=11, labelpad=12)
ax1.tick_params(axis="y", colors=colour_ovr)
ax2.tick_params(axis="y", colors=colour_profit)
ax2.grid(False)
ax2.yaxis.set_major_formatter(profit_gbp)
ax1.set_xlabel("Game number", fontsize=10, labelpad=10)
ax1.set_xticks(range(0, games["game_id"].max() + 1, 5))

align_axes(ax1, ax2, left_ref=STARTING_OVR, right_ref=0)

x_min, x_max = history["game_id"].min(), history["game_id"].max()
x_pad = max(3, (x_max - x_min) * 0.10)
ax1.set_xlim(x_min - 1, x_max + x_pad)

last = history.iloc[-1]


def axes_frac(ax, y):
    lo, hi = ax.get_ylim()
    return (y - lo) / (hi - lo)


f_ovr = axes_frac(ax1, last["ovr"])
f_profit = axes_frac(ax2, last["cumulative_profit"])

gap = 0.06
if abs(f_ovr - f_profit) < gap:
    mid = (f_ovr + f_profit) / 2
    f_ovr, f_profit = (mid + gap / 2, mid - gap / 2) if f_ovr >= f_profit else (mid - gap / 2, mid + gap / 2)

tag_x = x_max + x_pad * 0.12
tag_kw = dict(xycoords=ax1.get_xaxis_transform(), fontsize=11, fontweight="bold", va="center", ha="left",
              bbox=dict(boxstyle="round,pad=0.25", fc='#110130', ec="none", alpha=0.85))
ax1.annotate(f"{last['ovr']:.0f}", xy=(tag_x, f_ovr), color=colour_ovr, **tag_kw)
ax1.annotate(f"£{last['cumulative_profit']:.2f}", xy=(tag_x, f_profit), color=colour_profit, **tag_kw)

fig.subplots_adjust(top=0.84, bottom=0.11, left=0.08, right=0.90)
profit_title_block(fig, ax1, f"{PLAYER}: rating vs. results", f"OVR and cumulative profit over {len(history)} games played")
profit_footer(fig)
plt.show()