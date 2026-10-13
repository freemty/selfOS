---
name: paper-plot
description: "Use when creating or revising publication figures, experiment plots, comparison charts, or matplotlib visualizations from supplied data or result artifacts."
---

# Paper Plot — Publication Figure Templates

Drop-in matplotlib templates for publication-quality figures. Shared style ensures visual consistency across all figures in a paper.

## Contract

- Plot only supplied data or values read from result artifacts; never invent missing results or error bars.
- Label placeholder/demo values as synthetic and never mix them with reported results.
- Preserve units, metric direction, seeds, uncertainty definition, and missing values.

## Usage

Read `references/templates.md` for the template catalog, 5-tier color palette,
style rules, and LaTeX integration before creating a figure.

1. Pick the closest template from the catalog
2. Copy it + `style.py` from `templates/` (adjacent to this SKILL.md — resolve
   from the loaded skill directory, never a host-specific home path) into the
   project's `figures/` directory
3. Replace the genericized data block with real data; adjust labels and legend
4. Export both PDF (LaTeX) and PNG (slides)
