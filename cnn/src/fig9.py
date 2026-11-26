import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from matplotlib.patches import FancyBboxPatch, Polygon
W, H = 128, 40
fig, ax = new_fig(W, H)
yc = 17.0
CONV = ('#cfe2fa', BLUE); RELU = ('#ececec', GREY); ADD = ('#dff3e6', GREEN := '#2e9e5b')
def box(x, w, h, txt, col, fs=LBL - 1):
    ax.add_patch(FancyBboxPatch((x, yc - h/2), w, h, boxstyle='round,pad=0,rounding_size=1.0', fc=col[0], ec=col[1], lw=1.8, zorder=3))
    ax.text(x + w/2, yc, txt, ha='center', va='center', fontsize=fs, color=INK, zorder=4, linespacing=1.1)
def arrow(x0, x1, y=None, lw=1.8):
    ax.add_patch(FancyArrowPatch((x0, yc if y is None else y), (x1, yc if y is None else y), arrowstyle='-|>', mutation_scale=16, color=GREY, lw=lw, zorder=2, shrinkA=0, shrinkB=0))
def cuboid(x, h, d, cols):
    dx, dy = d * 0.85, d * 0.55
    y0 = yc - (h + dy) / 2
    fr, tp, rt = cols
    ax.add_patch(Rectangle((x, y0), h, h, fc=fr, ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Polygon([(x, y0+h), (x+h, y0+h), (x+h+dx, y0+h+dy), (x+dx, y0+h+dy)], fc=tp, ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Polygon([(x+h, y0), (x+h+dx, y0+dy), (x+h+dx, y0+h+dy), (x+h, y0+h)], fc=rt, ec=INK, lw=1.1, zorder=3))
    return x + h + dx
CC = ('#cfe2fa', '#e8f1fd', '#9fc2ee')
# x
x_end = cuboid(3, 9, 4, CC)
ax.text(3 + 4.5, yc - 9.5, 'x', ha='center', va='center', fontsize=LBL + 2, color=INK, fontweight='bold')
ax.text(3 + 4.5, yc - 13.2, 'input', ha='center', va='center', fontsize=13, color=GREY)
# main path
xs = 22.0
arrow(x_end + 1.2, xs - 0.6)
box(xs, 13, 8, 'Conv\n3 × 3', CONV); x1 = xs + 13
arrow(x1 + 0.6, x1 + 4.6); box(x1 + 5.2, 9, 8, 'ReLU', RELU); x2 = x1 + 5.2 + 9
arrow(x2 + 0.6, x2 + 4.6); box(x2 + 5.2, 13, 8, 'Conv\n3 × 3', CONV); x3 = x2 + 5.2 + 13
add_x = x3 + 10.5
arrow(x3 + 0.6, add_x - 2.6)
ax.add_patch(Circle((add_x, yc), 2.6, fc=ADD[0], ec=ADD[1], lw=2.0, zorder=3))
ax.text(add_x, yc - 0.1, '+', ha='center', va='center', fontsize=26, color=INK, zorder=4)
arrow(add_x + 2.6 + 0.6, add_x + 7.4); xr = add_x + 8.0
box(xr, 9, 8, 'ReLU', RELU); xo = xr + 9
arrow(xo + 0.6, xo + 4.6)
oend = cuboid(xo + 5.2, 9, 4, CC)
ax.text(xo + 5.2 + 4.5, yc - 9.5, 'F(x) + x', ha='center', va='center', fontsize=LBL + 1, color=INK, fontweight='bold')
ax.text(xo + 5.2 + 4.5, yc - 13.2, 'output', ha='center', va='center', fontsize=13, color=GREY)
# shortcut
ys = yc + 11.2
sx0 = x_end + 4.0
ax.plot([sx0, sx0], [yc, ys], color=BLUE, lw=2.4, zorder=2, solid_capstyle='round')
ax.plot([sx0, add_x], [ys, ys], color=BLUE, lw=2.4, zorder=2, solid_capstyle='round')
ax.add_patch(FancyArrowPatch((add_x, ys), (add_x, yc + 2.9), arrowstyle='-|>', mutation_scale=16, color=BLUE, lw=2.4, zorder=2, shrinkA=0, shrinkB=0))
ax.add_patch(Circle((sx0, yc), 0.7, fc=BLUE, ec='none', zorder=4))
ax.text((sx0 + add_x) / 2, ys + 1.6, 'shortcut: x is copied unchanged', ha='center', va='baseline', fontsize=15, color=BLUE, fontweight='bold')
# F(x) bracket
yb = yc - 6.4
bx0, bx1 = xs, x3
ax.plot([bx0, bx0, bx1, bx1], [yb + 1.3, yb, yb, yb + 1.3], color=INK, lw=1.4)
ax.text((bx0 + bx1) / 2, yb - 1.4, 'F(x): the two convolutions learn only the change', ha='center', va='top', fontsize=15, color=INK)
print(save_crop(fig, '/tmp/figs2/Figure9_residual_block.png'))
