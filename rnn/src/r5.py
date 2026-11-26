import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 124, 64
fig, ax = new_fig(W, H, width_in=11.5)
# ---- left: gradient reaching each word
T(ax, 1, 60.5, 'The gradient that reaches each word', fs=16, bold=True, ha='left')
T(ax, 1, 55.6, 'when every step multiplies it by 0.9', fs=14, color=GREY, ha='left')
words = [('France', 6.5, 11.5, 0.9 ** 50), ('…', 17.5, 5.0, None), ('and', 25.0, 7.5, 0.9 ** 4),
         ('I', 31.8, 5.0, 0.9 ** 3), ('speak', 39.5, 9.5, 0.9 ** 2), ('fluent', 50.0, 10.5, 0.9), ('?', 59.5, 5.0, None)]
yb = 22.0; hmax = 17.0; yw = 13.5
for w, xx, bw, v in words:
    key = (w == 'France')
    rbox(ax, xx, yw, bw, 6.6, PALEYEL if key else 'white', YEL if key else GREY, lw=2.0 if key else 1.6)
    T(ax, xx, yw, w, fs=15, bold=(w == '?'))
    if v is not None:
        top = yb + hmax * v
        ax.add_patch(Rectangle((xx - 2.2, yb), 4.4, max(hmax * v, 0.12), fc=ORANGE, ec='none', zorder=3))
        T(ax, xx, top + 2.6, ('%.3f' % v) if v < 0.01 else ('%.2f' % v), fs=14.5, color=INK)
line(ax, [1, 62], [yb, yb], color=LIGHT, lw=1.2)
T(ax, 1.0, 6.4, '50 steps back', fs=14, color=GREY, ha='left')
T(ax, 62.0, 6.4, 'next word', fs=14, color=GREY, ha='right')
T(ax, 33.5, 6.4, '…', fs=1, color='white')
# the word that matters
T(ax, 1.0, 49.5, '“France” is needed to predict the last word,', fs=14.5, color=INK, ha='left')
T(ax, 1.0, 45.8, 'but it gets almost no gradient.', fs=14.5, color=INK, ha='left')
# ---- right: chart
line(ax, [66, 66], [3, 58], color='#dddddd', lw=1.2)
T(ax, 70, 60.5, 'How the gradient changes with distance', fs=16, bold=True, ha='left')
T(ax, 70, 55.6, 'one factor per step, 50 steps', fs=14, color=GREY, ha='left')
ax2 = fig.add_axes([79 / W, 9 / H, 40 / W, 41 / H])
n = np.arange(0, 51)
ax2.plot(n, 1.1 ** n, color=ORANGE, lw=3.0)
ax2.plot(n, 1.0 ** n, color=FAINT, lw=2.0, ls=(0, (4, 3)))
ax2.plot(n, 0.9 ** n, color=BLUE, lw=3.0)
ax2.set_yscale('log'); ax2.set_xlim(0, 50); ax2.set_ylim(1e-3, 1e3)
ax2.set_yticks([1e-3, 1e-1, 10, 1e3]); ax2.set_yticklabels(['0.001', '0.1', '10', '1000'])
ax2.set_xticks([0, 10, 20, 30, 40, 50])
ax2.tick_params(labelsize=13.5, colors=GREY, length=3)
ax2.grid(True, color='#eeeeee', lw=1.0, which='major'); ax2.set_axisbelow(True)
for sp in ('top', 'right'): ax2.spines[sp].set_visible(False)
for sp in ('left', 'bottom'): ax2.spines[sp].set_color(LIGHT)
ax2.minorticks_off()
ax2.set_xlabel('steps back', fontsize=14, color=GREY, labelpad=3)
ax2.set_ylabel('size of the gradient', fontsize=14, color=GREY, labelpad=3)
ax2.text(2.0, 1.1 ** 42 * 0.5, 'factor 1.1: explodes\n117 after 50 steps', color=ORANGE, fontsize=14.5, fontweight='bold', va='center', ha='left')
ax2.text(2.0, 0.008, 'factor 0.9: vanishes\n0.005 after 50 steps', color=BLUE, fontsize=14.5, fontweight='bold', va='center', ha='left')
ax2.text(34, 1.9, 'factor 1.0', color=GREY, fontsize=13.5, va='bottom', ha='left')
print(save_crop(fig, '/tmp/rfig/R5_gradient_vs_distance.png'))
