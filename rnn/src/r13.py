import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 124, 64
fig, ax = new_fig(W, H, width_in=11.5)
def cell(x, y, fc, ec, s='', w=8.4, h=6.4):
    rbox(ax, x, y, w, h, fc, ec, lw=1.7, r=1.0); 
    if s: T(ax, x, y, s, fs=14)
# ---------- left: bidirectional
words = ['the', 'movie', 'was', 'terribly', 'exciting']
xs = [6 + 11.2*i for i in range(5)]
T(ax, 29, 61.5, 'Bidirectional RNN', fs=17, bold=True)
T(ax, 29, 56.5, 'the state for “terribly” sees both sides', fs=13.5, color=GREY)
for i, (x, w) in enumerate(zip(xs, words)):
    foc = (w == 'terribly')
    T(ax, x, 3.5, w, fs=14.5, bold=foc)
    arrow(ax, (x, 6.6), (x, 11.2))
    cell(x, 14.5, PALEBLUE, BLUE, '', w=9, h=6.4)
    cell(x, 27.5, PALEORANGE, ORANGE, '', w=9, h=6.4)
    arrow(ax, (x - 1.5, 17.8), (x - 1.5, 24.2), color=BLUE, lw=1.4, ms=12)
    arrow(ax, (x + 1.5, 17.8), (x + 1.5, 24.2), color=ORANGE, lw=1.4, ms=12)
    cell(x, 41, PALEGREEN, GREEN, '', w=9, h=6.4)
    arrow(ax, (x - 1.5, 30.7), (x - 1.5, 37.8), color=BLUE, lw=1.4, ms=12)
    arrow(ax, (x + 1.5, 30.7), (x + 1.5, 37.8), color=ORANGE, lw=1.4, ms=12)
    if i < 4:
        arrow(ax, (x + 4.5, 14.5), (xs[i+1] - 4.5, 14.5), color=BLUE, lw=2.0)
        arrow(ax, (xs[i+1] - 4.5, 27.5), (x + 4.5, 27.5), color=ORANGE, lw=2.0)
T(ax, xs[0] - 5.2, 14.5, 'forward', fs=13, color=BLUE, ha='right') if False else None
T(ax, 1, 21.0, '', fs=1)
T(ax, xs[4] + 7.2, 14.5, 'forward\n(past)', fs=13, color=BLUE, ha='left')
T(ax, xs[4] + 7.2, 27.5, 'backward\n(future)', fs=13, color=ORANGE, ha='left')
T(ax, xs[4] + 7.2, 41, 'joined\nstate, 2d', fs=13, color=GREEN, ha='left')
for x in xs:
    arrow(ax, (x, 44.4), (x, 48.6))
    T(ax, x, 51.2, '$y$', fs=14.5, color=GREY)
# highlight terribly
rbox(ax, xs[3], 28, 12, 33.5, 'none', GREY, lw=1.4, r=1.5, ls='--', z=1)
# ---------- right: stacked
ox = 82
T(ax, ox + 20, 61.5, '2-layer stacked RNN', fs=17, bold=True)
T(ax, ox + 20, 56.5, 'layer 2 reads the states of layer 1', fs=13.5, color=GREY)
sx = [ox + 4 + 11*i for i in range(4)]
for i, x in enumerate(sx):
    T(ax, x, 3.5, f'$x_{i+1}$', fs=14.5)
    arrow(ax, (x, 6.6), (x, 11.2))
    cell(x, 14.5, PALEBLUE, BLUE, f'$h^1_{i+1}$', w=7.8)
    arrow(ax, (x, 17.9), (x, 31.0))
    cell(x, 34.2, PALEGREEN, GREEN, f'$h^2_{i+1}$', w=7.8)
    arrow(ax, (x, 37.6), (x, 44.6))
    T(ax, x, 47.6, f'$y_{i+1}$', fs=14.5, color=GREY)
    if i < 3:
        arrow(ax, (x + 3.9, 14.5), (sx[i+1] - 3.9, 14.5), color=BLUE, lw=2.0)
        arrow(ax, (x + 3.9, 34.2), (sx[i+1] - 3.9, 34.2), color=GREEN, lw=2.0)
T(ax, ox - 1.5, 14.5, '', fs=1)
T(ax, ox + 31, 14.5, 'layer 1', fs=13, color=BLUE, ha='left') if False else None
print(save_crop(fig, '/tmp/rfig/R13_bi_stacked.png'))
