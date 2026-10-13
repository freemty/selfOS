# Paper Plot Templates Reference

## Style Foundation

All templates import from a shared `style.py` that sets:
- **Font**: Palatino body + STIX Math (matches arxiv `mathpazo` / `newtxtext`)
- **Palette**: 5-tier color system — `brand → medium → paper → soft → mute`
- **Defaults**: tight_layout, 300 DPI, PDF/PNG dual export

## Available Templates

| Template | Use case |
|----------|----------|
| `bar_vertical.py` | Comparing models/methods on a single metric |
| `bar_horizontal.py` | Many categories, long labels |
| `boxplot_gradient.py` | Distribution comparison with family-grouped colors |
| `line_multi.py` | Training curves, scaling laws (linear axes) |
| `line_broken_axis.py` | When one data point is an outlier |
| `line_logx.py` | Compute scaling (FLOPs on x-axis) |
| `line_loglog.py` | Power-law relationships |
| `scatter_isoflops.py` | IsoFLOPs-style with contour lines |
| `heatmap.py` | Attention maps, confusion matrices |
| `radar.py` | Multi-dimensional capability comparison |

## Color Palette (5 tiers)

```python
PALETTE = {
    'brand':  ['#4285F4', '#EA4335', '#FBBC05', '#34A853', '#FF6D01', '#46BDC6'],
    'medium': ['#5B9CF6', '#ED6B5E', '#FCC934', '#5CB876', '#FF8A3D', '#6BCDD5'],
    'paper':  ['#7AB3F8', '#F09080', '#FDD663', '#7FC896', '#FFa76E', '#8EDDE4'],
    'soft':   ['#A8CEF9', '#F4B5A8', '#FDE492', '#A8DAB5', '#FFC49E', '#B3EBF0'],
    'mute':   ['#D3E7FC', '#F9DAD3', '#FEF1C7', '#D3EDD8', '#FFE2CF', '#D9F5F8'],
}
```

Default: `paper` tier. Switch in one line: `colors = PALETTE['medium']`.

## Usage Pattern

```bash
# 1. Copy template + style to your figures directory
cp <loaded-skill-dir>/templates/{style.py,bar_vertical.py} ./figures/

# 2. Edit data block in the template
# 3. Run
python figures/bar_vertical.py

# Output: figures/bar_vertical.pdf + figures/bar_vertical.png
```

## When Creating a New Figure

1. Pick the closest template from the table above
2. Copy it + `style.py` to your project's `figures/` directory
3. Replace the genericized data block with real data
4. Adjust title, axis labels, legend
5. Export as both PDF (for LaTeX `\includegraphics`) and PNG (for slides)

## Style Rules for Paper Figures

- **No grid lines** unless data is dense (>20 points)
- **Legend outside** plot area when >3 series
- **Font size**: axis labels 11pt, tick labels 9pt, title 12pt
- **Aspect ratio**: default 6×4 inches; wide plots 8×3
- **Color**: never rely on color alone — add markers or patterns for accessibility
- **Error bars**: always show when available (std or 95% CI)

## Integration with LaTeX

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/bar_vertical.pdf}
  \caption{...}
  \label{fig:bar-vertical}
\end{figure}
```

## Template Directory

Templates live in `templates/` adjacent to this `SKILL.md`. Resolve them from the loaded skill directory rather than assuming a Claude- or Codex-specific home path.
