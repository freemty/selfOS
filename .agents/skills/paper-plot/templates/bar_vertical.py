"""
Vertical bar chart — comparing models/methods on a single metric.
Copy this file + style.py to your figures/ directory, edit the data block, run.
"""
import matplotlib.pyplot as plt
import numpy as np
from style import setup

colors = setup()

# === DATA BLOCK (edit this) ===
methods = ['Method A', 'Method B', 'Method C', 'Method D', 'Method E']
scores = [72.3, 78.1, 81.5, 79.2, 84.7]
errors = [1.2, 0.9, 1.5, 1.1, 0.8]
# ==============================

fig, ax = plt.subplots()

x = np.arange(len(methods))
bars = ax.bar(x, scores, yerr=errors, capsize=3, color=colors[:len(methods)], width=0.6)

ax.set_xticks(x)
ax.set_xticklabels(methods)
ax.set_ylabel('Accuracy (%)')
ax.set_title('Model Comparison on Benchmark X')

ax.set_ylim(bottom=0)

plt.tight_layout()
plt.savefig('bar_vertical.pdf')
plt.savefig('bar_vertical.png')
print('Saved: bar_vertical.pdf, bar_vertical.png')
