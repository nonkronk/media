import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 113, 68
fig, ax = new_fig(W, H, width_in=10.5)
words = ['the', 'dogs', 'in', 'the', 'neighborhood', 'are']
xs = [9 + 17.5 * i for i in range(6)]
# ---- row A: feedforward
T(ax, 1, 66, 'Feedforward network with a window of 3 words', fs=16, bold=True, ha='left')
ya = 56
for i, (w, x) in enumerate(zip(words, xs)):
    inside = i >= 3
    rbox(ax, x, ya, 15.6, 7.5, 'white', INK if inside else LIGHT, lw=1.8 if inside else 1.4)
    T(ax, x, ya, w, fs=15, color=INK if inside else FAINT)
T(ax, xs[1], ya - 7.4, 'outside the window:', fs=14, color=ORANGE)
T(ax, xs[1], ya - 12.0, '“dogs” is never seen', fs=14, color=ORANGE)
xl, xr = xs[3] - 7.8, xs[5] + 7.8
line(ax, [xl, xl, xr, xr], [ya - 5, ya - 7.6, ya - 7.6, ya - 5], color=GREY, lw=1.8)
xm = (xl + xr) / 2
T(ax, xm, ya - 11.4, 'window of 3 words', fs=14, color=GREY)
yf = 36
rbox(ax, xm, yf, 40, 7.5, PALEGREY, GREY)
T(ax, xm, yf, 'feedforward network', fs=15)
arrow(ax, (xm, ya - 14.0), (xm, yf + 4.0))
arrow(ax, (xm + 20.5, yf), (xm + 28, yf))
T(ax, xm + 31, yf, '?', fs=22, bold=True)
# divider
line(ax, [1, W - 1], [28.5, 28.5], color='#dddddd', lw=1.2)
# ---- row B: RNN
T(ax, 1, 25, 'RNN', fs=16, bold=True, ha='left')
yc, yw = 12.5, 2.0
for i, (w, x) in enumerate(zip(words, xs)):
    rbox(ax, x, yc, 13.5, 8.0, PALEGREEN, GREEN)
    T(ax, x, yc, '$h_%d$' % (i + 1), fs=15)
    circ(ax, x, yw - 0.0, 0.01, 'white', 'white')
    arrow(ax, (x, yw + 3.3), (x, yc - 4.1), color=GREY, lw=1.6, ms=13)
    T(ax, x, yw - 0.3, w, fs=15)
    if i < 5:
        arrow(ax, (x + 6.9, yc), (xs[i + 1] - 6.9, yc), color=(ORANGE if i >= 1 else GREY), lw=(3.2 if i >= 1 else 1.8), ms=(14 if i >= 1 else 14))
xo = xs[5]
arrow(ax, (xo, yc + 4.1), (xo, yc + 9.5))
T(ax, xo, yc + 12.0, 'barking', fs=15, bold=True)
T(ax, (xs[1] + xs[4]) / 2 + 3, yc + 8.0, 'the state carries “dogs” forward', fs=14, color=ORANGE)
print(save_crop(fig, '/tmp/rfig/R1_ff_vs_rnn.png'))
