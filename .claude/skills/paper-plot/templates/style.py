"""
Shared matplotlib style for publication-quality figures.
Font: Palatino body + STIX Math (matches arxiv mathpazo/newtxtext).
Palette: 5-tier Google-brand color system.
"""
import matplotlib.pyplot as plt
import matplotlib as mpl

PALETTE = {
    'brand':  ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#FF6D01', '#46BDC6'],
    'medium': ['#5B9CF6', '#ED6B5E', '#FCC934', '#5CB876', '#FF8A3D', '#6BCDD5'],
    'paper':  ['#7AB3F8', '#F09080', '#FDD663', '#7FC896', '#FFa76E', '#8EDDE4'],
    'soft':   ['#A8CEF9', '#F4B5A8', '#FDE492', '#A8DAB5', '#FFC49E', '#B3EBF0'],
    'mute':   ['#D3E7FC', '#F9DAD3', '#FEF1C7', '#D3EDD8', '#FFE2CF', '#D9F5F8'],
}

TIER = 'paper'


def setup(tier=None):
    t = tier or TIER
    colors = PALETTE[t]

    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Palatino', 'Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix',
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 11,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.figsize': (6, 4),
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.prop_cycle': mpl.cycler(color=colors),
        'axes.grid': False,
        'legend.frameon': False,
    })
    return colors
