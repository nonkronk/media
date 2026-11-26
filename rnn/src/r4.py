import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 110, 92
fig, ax = new_fig(W, H, width_in=11)
xs = [13 + 17 * i for i in range(6)]
def panel(oy, title, truncated):
    T(ax, 1, oy + 30.0, title, fs=16, bold=True, ha='left')
    yx, yh, yl = oy + 0.0, oy + 10.5, oy + 21.0
    for i, xx in enumerate(xs):
        circ(ax, xx, yx, 3.4, PALEBLUE, BLUE); T(ax, xx, yx, f'$x_{i+1}$', fs=14.5)
        rbox(ax, xx, yh, 11.5, 7.5, PALEGREEN, GREEN); T(ax, xx, yh, f'$h_{i+1}$', fs=15)
        circ(ax, xx, yl, 3.6, PALERED, RED); T(ax, xx, yl, f'$L_{i+1}$', fs=14.5)
        arrow(ax, (xx - 1.2, yx + 3.6), (xx - 1.2, yh - 3.9), ms=12)
        arrow(ax, (xx - 1.2, yh + 3.9), (xx - 1.2, yl - 3.8), ms=12)
        arrow(ax, (xx + 1.4, yl - 3.8), (xx + 1.4, yh + 3.9), color=ORANGE, lw=2.2, ms=12)
        if i < 5:
            arrow(ax, (xx + 5.9, yh + 1.5), (xs[i + 1] - 5.9, yh + 1.5), ms=12)
            blocked = truncated and i == 2
            if not blocked:
                arrow(ax, (xs[i + 1] - 5.9, yh - 1.5), (xx + 5.9, yh - 1.5), color=ORANGE, lw=2.2, ms=12)
            else:
                xm = (xx + xs[i + 1]) / 2
                line(ax, [xm - 2.6, xm + 2.6], [yh - 1.5, yh - 1.5], color=ORANGE, lw=2.2, ls=(0, (2, 1.5)))
                T(ax, xm, yh - 1.4, '×', fs=20, color=ORANGE, bold=True, z=7)
    if truncated:
        for a, b_ in ((0, 2), (3, 5)):
            xl, xr = xs[a] - 7.0, xs[b_] + 7.0
            ax.add_patch(FancyBboxPatch((xl, yx - 5.0), xr - xl, yl - yx + 9.6, boxstyle='round,pad=0,rounding_size=1.5',
                         fc='none', ec=FAINT, lw=1.6, ls=(0, (4, 3)), zorder=1))
            T(ax, (xl + xr) / 2, yx - 8.4, f'chunk {1 if a == 0 else 2}  (k = 3)', fs=13.5, color=GREY)
panel(58, 'Standard BPTT: the error goes back through all 6 steps', False)
T(ax, 55, 52.0, 'The gradient of W is the sum of the gradients from every step.', fs=14, color=ORANGE)
panel(18, 'Truncated BPTT: the error goes back only inside a chunk', True)
T(ax, 55, 3.6, 'The state is still passed forward, but no gradient crosses the chunk boundary.', fs=14, color=ORANGE)
print(save_crop(fig, '/tmp/rfig/R4_bptt.png'))
