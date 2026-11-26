# NEW CONFIG

# Constants & Variables

player_colours = {
    'Scott' : "#9C9C9C",
    'Jaydon' : "#3463CE",
    'Josh' : "#9C9C9C",
    'Reuben' : "#9C9C9C",
    'Zoltan' : "#9C9C9C",
    'Jack' : "#9C9C9C",
    'Tim' : "#9C9C9C",
    'Tom' : "#9C9C9C",
    'Emily' : "#9C9C9C",
    'Sachin' : "#9C9C9C",
    'Michael' : "#9C9C9C",
    'Josh F' : "#9C9C9C",
    'Arthur' : "#9C9C9C",
    'Sophie' : "#9C9C9C",
    'Katherine' : "#9C9C9C",
    'The Lion' : "#9C9C9C",
    'The V' : "#9C9C9C",
    'Matthew' : "#9C9C9C",
    'Thurley' : "#9C9C9C",
    'Benny' : "#9C9C9C",
    'Ella' : "#9C9C9C",
    'Ben' : "#9C9C9C",
    'Nico' : "#9C9C9C",
    'Alex' : "#9C9C9C",
    'Johnathan' : "#9C9C9C",
    'Solomon' : "#9C9C9C",
    'Charlie' : "#9C9C9C",
    'James' : "#9C9C9C",
    'Will' : "#9C9C9C"


}

player_colours2 = {
    'Scott' : "#3F82FF",
    'Jaydon' : "#27F8AC",
    'Josh' : "#FF7957",
    'Reuben' : "#4B4EA4",
    'Zoltan' : "#6F1067",
    'Jack' : "#D40000",
    'Tim' : "#FCFF33",
    'Tom' : "#9500FF",
    'Emily' : "#E100BB",
    'Sachin' : "#FFA8FF",
    'Michael' : "#FF8C00",
    'Josh F' : "#ABFEFF",
    'Arthur' : "#4CA921",
    'Sophie' : "#763900",
    'Katherine' : "#BFFF00",
    'The Lion' : "#6F0000",
    'The V' : "#6200FF",
    'Matthew' : "#00FF99",
    'Thurley' : "#7B7300",
    'Benny' : "#FF0066",
    'Ella' : "#23AE00",
    'Ben' : "#009DFF",
    'Nico' : "#123953",
    'Alex' : "#528D95",
    'Johnathan' : "#59498B",
    'Solomon' : "#5B5050",
    'Charlie' : "#7A3F3F",
    'James' : "#887D48"

}

def profit_gbp(v, _=None):
    pound = '\u00a3'
    return f'-{pound}{abs(v):,.0f}' if v < 0 else f'{pound}{v:,.0f}'

def profit_title_block(fig, ax, title, subtitle=None):
    fig.text(0.06, 0.965, title, fontsize=20, fontweight='bold', color='#110130', ha='left', va='top')
    if subtitle:
        fig.text(0.06, 0.915, subtitle, fontsize=11.5, color='#2f2e3f', ha='left', va='top')

def profit_footer(fig, text=""):
    fig.text(0.06, 0.015, text, fontsize=8.5, color='#2f2e3f', ha='left')

def soften_axes(ax, ref_y=None, ref_label=None):
    """Light horizontal grid, no top/right spines, muted ticks."""
    ax.grid(axis='y', color='white', alpha=0.08, linewidth=0.6)
    ax.grid(axis='x', visible=False)
    ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_alpha(0.3)
    ax.tick_params(colors='#2f2e3f', labelsize=9, length=3)
    if ref_y is not None:
        ax.axhline(ref_y, color='#2f2e3f', linestyle=(0, (4, 4)),
                   linewidth=0.8, alpha=0.6, label=ref_label)

def soften_legend(ax):
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1.01, 1.0),
                    frameon=False, fontsize=9, labelcolor="#2f2e3f",
                    handlelength=1.5, markerscale=1.2)
    return leg