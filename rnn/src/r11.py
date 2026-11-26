import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
import pandas as pd
d = pd.read_csv('/tmp/ett/ETTh1.csv', parse_dates=['date'])
s = 9129
y = d['HUFL'].values[s:s + 193]          # 192 hours + the target hour
assert d.date[s + 192].hour == 9 and abs(y[192] + 4.489) < 0.01
W, H = 116, 78
fig, ax = new_fig(W, H, width_in=11.5)
T(ax, 1, 75.5, 'Forecasting the next hour of load from the last 7 days', fs=16, bold=True, ha='left')
T(ax, 1, 71.2, 'Hourly load of an electricity transformer (ETTh1 data, July 2017)', fs=14, color=GREY, ha='left')
a2 = fig.add_axes([11 / W, 32 / H, 103 / W, 35.5 / H])
n = np.arange(193)
a2.axvspan(24, 192, color=PALEBLUE, lw=0, zorder=0)
a2.plot(n[:25], y[:25], color=FAINT, lw=2.0, zorder=3)
a2.plot(n[24:192], y[24:192], color=BLUE, lw=2.2, zorder=3)
a2.plot(n[191:193], y[191:193], color=FAINT, lw=1.6, ls=(0, (2, 2)), zorder=3)
a2.set_xlim(0, 232); a2.set_ylim(-23, 35)
ticks = [24 * k for k in range(1, 9)]
a2.set_xticks(ticks); a2.set_xticklabels(['−7 d', '−6 d', '−5 d', '−4 d', '−3 d', '−2 d', '−1 d', 'target'])
a2.spines['bottom'].set_bounds(0, 192)
a2.set_yticks([-10, 0, 10, 20])
a2.tick_params(labelsize=13.5, colors=GREY, length=3)
a2.grid(True, axis='y', color='#eeeeee', lw=1.0); a2.set_axisbelow(True)
for sp in ('top', 'right'): a2.spines[sp].set_visible(False)
for sp in ('left', 'bottom'): a2.spines[sp].set_color(LIGHT)
a2.set_ylabel('load', fontsize=14, color=GREY, labelpad=2)
# window bracket and label
a2.plot([24, 192], [29.5, 29.5], color=BLUE, lw=2.0)
a2.plot([24, 24], [28.3, 30.7], color=BLUE, lw=2.0); a2.plot([192, 192], [28.3, 30.7], color=BLUE, lw=2.0)
a2.text(108, 32.2, 'input window: 168 hours (7 days)', ha='center', va='center', fontsize=14.5, fontweight='bold', color=INK)
a2.text(12, 26.5, 'older data,\nnot used', ha='center', va='center', fontsize=13, color=GREY, linespacing=1.15)
# marks
for xx, lab, ha in [(24, 'same hour last week', 'left'), (168, 'same hour yesterday', 'center')]:
    a2.plot([xx, xx], [-14.5, y[xx] - 1.5], color=GREY, lw=1.4, zorder=2)
    a2.scatter([xx], [y[xx]], s=60, color=GREY, zorder=5, edgecolor='white', linewidth=1.5)
    a2.text(xx - (0.5 if ha == 'left' else 0), -17.5, lab, ha=ha, va='center', fontsize=13.5, color=INK)
a2.scatter([192], [y[192]], s=150, facecolor='white', edgecolor=ORANGE, linewidth=3.0, zorder=6)
a2.text(198, y[192], 'next hour:\nthe value\nto predict', ha='left', va='center', fontsize=13.5, color=ORANGE, fontweight='bold', linespacing=1.15)
# model row
T(ax, 1, 22.8, 'Model: two stacked GRU layers and one output unit', fs=15, bold=True, ha='left')
ym = 11.0
boxes = [(16, 28, 'Input: 168 hourly vectors', PALEBLUE, BLUE, False), (43.5, 17, 'GRU 64', PALEGREEN, GREEN, True),
         (65.5, 17, 'GRU 64', PALEGREEN, GREEN, True), (86, 14, 'Dense 1', PALEYEL, YEL, True), (107, 16, 'Next hour', 'white', ORANGE, True)]
for cx, w, t, fc, ec, b in boxes:
    rbox(ax, cx, ym, w, 8.6, fc, ec, lw=2.0)
    T(ax, cx, ym, t, fs=14.5 if not b else 15, bold=b)
for a, b in [(30.5, 34.7), (52.2, 56.7), (74.2, 78.7), (93.2, 98.5)]:
    arrow(ax, (a, ym), (b, ym), color=GREY, lw=2.2, ms=15)
print(save_crop(fig, '/tmp/rfig/R11_etth1_gru.png'))
