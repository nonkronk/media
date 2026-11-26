import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 110, 72
fig, ax = new_fig(W, H, width_in=11)
T(ax, 1, 69, 'The gradient that goes back to $h_1$ is multiplied by one factor per step', fs=16, bold=True, ha='left')
# chain
yc = 56.5
xs = [10, 34, 58, 98]
names = [r'$h_1$', r'$h_2$', r'$h_3$', r'$h_t$']
for x, n in zip(xs, names):
    rbox(ax, x, yc, 11, 7.2, PALEGREEN, GREEN, lw=2.0)
    T(ax, x, yc, n, fs=16)
T(ax, 78, yc, '…', fs=20, color=GREY)
# backward arrows (right to left)
pairs = [(98, 78 + 3.5), (78 - 3.5, 58), (58, 34), (34, 10)]
segs = [((98 - 5.8, yc), (78 + 3.8, yc)), ((78 - 3.8, yc), (58 + 5.8, yc)), ((58 - 5.8, yc), (34 + 5.8, yc)), ((34 - 5.8, yc), (10 + 5.8, yc))]
for p0, p1 in segs:
    arrow(ax, p0, p1, color=ORANGE, lw=2.6, ms=17)
for (p0, p1) in [segs[1], segs[2], segs[3]]:
    T(ax, (p0[0] + p1[0]) / 2, yc + 4.6, '× W', fs=15, color=ORANGE, bold=True)
T(ax, 88, yc + 4.6, '× W', fs=15, color=ORANGE, bold=True)
T(ax, 98, yc - 6.0, 'the gradient starts here', fs=14, color=GREY)
T(ax, 1, yc - 6.0, '$h_1$ receives the product', fs=14, color=GREY, ha='left')
# branches
line(ax, [55, 55], [4, 46], color='#dddddd', lw=1.2)
ax.add_patch(Rectangle((1, 45.2), 52, 0.6, fc=ORANGE, ec='none', zorder=3))
ax.add_patch(Rectangle((58, 45.2), 51, 0.6, fc=BLUE, ec='none', zorder=3))
T(ax, 1, 41, 'Factors above 1: the gradient explodes', fs=15.5, bold=True, color=ORANGE, ha='left')
T(ax, 58, 41, 'Factors below 1: the gradient vanishes', fs=15.5, bold=True, color=BLUE, ha='left')
# clipping mini diagram
cx, cy, r = 19, 24, 8.5
th = np.linspace(0, 2 * np.pi, 200)
ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=GREY, lw=1.8, ls=(0, (4, 3)), zorder=2)
d = np.array([0.8, 0.6])
tip_long = np.array([cx, cy]) + 19 * d
tip_clip = np.array([cx, cy]) + r * d
arrow(ax, (cx, cy), tuple(tip_long), color=ORANGE, lw=2.6, ms=17)
arrow(ax, (cx, cy), tuple(tip_clip), color=INK, lw=3.4, ms=17, z=4)
circ(ax, cx, cy, 0.7, INK, INK, z=5)
T(ax, tip_long[0] + 1.2, tip_long[1] + 0.6, 'g', fs=16, color=ORANGE, ha='left', bold=True)
T(ax, cx - r - 1.0, cy - 1.0, 'threshold', fs=14, color=GREY, ha='right')
T(ax, tip_clip[0] + 1.8, tip_clip[1] - 3.2, 'clipped g', fs=14, color=INK, ha='left')
T(ax, 1, 10.5, 'Fix: gradient clipping', fs=15, bold=True, ha='left')
T(ax, 1, 6.0, 'g is scaled down to the threshold, direction kept', fs=14, color=GREY, ha='left')
# fixes list
T(ax, 58, 34, 'Fixes', fs=15, bold=True, ha='left')
items = [('Gated cells (LSTM, GRU)', 'an additive path keeps the gradient alive'),
         ('Identity or orthogonal W, ReLU', 'keeps the factor close to 1'),
         ('Truncated BPTT', 'the gradient goes back only k steps')]
y = 28.0
for a, b in items:
    circ(ax, 59.2, y, 0.9, BLUE, BLUE)
    T(ax, 62, y, a, fs=15, ha='left')
    T(ax, 62, y - 4.3, b, fs=14, color=GREY, ha='left')
    y -= 10.2
print(save_crop(fig, '/tmp/rfig/R6_vanishing_exploding.png'))
