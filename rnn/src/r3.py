import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
Wm, Um, b = 0.5, 1.0, 0.0
x = [1.0, 0.0, 0.0]
h = [0.0]
for xt in x: h.append(float(np.tanh(Wm * h[-1] + Um * xt + b)))
print(h)
assert round(h[1], 2) == 0.76 and round(h[2], 2) == 0.36 and round(h[3], 2) == 0.18
W, H = 104, 66
fig, ax = new_fig(W, H, width_in=10.5)
o = 14
xs = [11, 37, 63, 89]
def mix(v):
    t = min(1.0, abs(v)) * 0.85
    c0 = np.array([1, 1, 1]); c1 = np.array(matplotlib.colors.to_rgb(GREEN))
    return tuple(c0 * (1 - t) + c1 * t)
yh = 24 + o
for i, (xx, hv) in enumerate(zip(xs, h)):
    circ(ax, xx, yh, 7.0, mix(hv), GREEN)
    T(ax, xx, yh, f'{hv:.2f}' if i else '0', fs=18, bold=True)
    T(ax, xx, yh + 10.8, f'$h_{i}$', fs=17)
T(ax, xs[0], yh - 10.4, 'start: zeros', fs=13.5, color=GREY)
for i in range(3):
    arrow(ax, (xs[i] + 7.7, yh), (xs[i + 1] - 7.7, yh))
    T(ax, (xs[i] + xs[i + 1]) / 2, yh + 3.4, 'W, tanh', fs=13.5, color=GREY)
    # input
    xi = xs[i + 1]
    circ(ax, xi, o, 4.3, PALEBLUE, BLUE, z=3)
    T(ax, xi, o, f'{x[i]:g}', fs=17, bold=True)
    T(ax, xi, o - 7.4, f'$x_{i+1}$', fs=16)
    arrow(ax, (xi, o + 4.9), (xi, yh - 7.7))
    T(ax, xi + 4.6, o + 8.0, 'U', fs=14, color=GREY)
# bracket on effect of x1
yb = yh + 17.0
line(ax, [xs[1], xs[1], xs[3], xs[3]], [yb - 1.2, yb, yb, yb - 1.2], color=ORANGE, lw=2.2)
T(ax, (xs[1] + xs[3]) / 2, yb + 3.6, 'the effect of $x_1$ gets smaller at every step', fs=15, color=ORANGE)
T(ax, 52, 1.8, 'Example with one number per state:  W = 0.5,  U = 1,  b = 0,  inputs 1, 0, 0.', fs=14, color=GREY)
print(save_crop(fig, '/tmp/rfig/R3_unrolled_three_steps.png'))
