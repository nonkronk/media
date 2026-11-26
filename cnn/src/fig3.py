import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
GREEN = '#2e9e5b'
W, H = 128, 51
fig, ax = new_fig(W, H)
TT = 15.5      # panel title size
def title(x, t, sub):
    ax.text(x, H - 3.2, t, ha='center', va='baseline', fontsize=LBL + 1, color=INK, fontweight='bold')
    ax.text(x, H - 7.6, sub, ha='center', va='baseline', fontsize=13, color=GREY)

PW = 30.5
xs = [2 + PW/2 + i * (PW + 1.2) for i in range(4)]
gtop = H - 12

# ---------- 1. kernel size ----------
c = 2.7
x0 = xs[0] - 7 * c / 2
title(xs[0], 'Kernel size', 'stride 1, no padding')
for r in range(7):
    for k in range(7):
        ax.add_patch(Rectangle((x0 + k*c, gtop - (r+1)*c), c, c, fc='white', ec=LIGHT, lw=0.8, zorder=1))
for n, col, lw in ((7, GREY, 2.4), (5, BLUE, 2.8), (3, YEL, 3.4)):
    ax.add_patch(Rectangle((x0, gtop - n*c), n*c, n*c, fill=False, ec=col, lw=lw, zorder=5 + (8 - n)))
rows = [('3 × 3 kernel', 'output 5 × 5', YEL), ('5 × 5 kernel', 'output 3 × 3', BLUE), ('7 × 7 kernel', 'output 1 × 1', GREY)]
for i, (a, b, col) in enumerate(rows):
    y = gtop - 7*c - 3.6 - i * 3.6
    ax.add_patch(Rectangle((xs[0] - 13.5, y - 0.7), 1.6, 1.6, fc=col, ec='none'))
    ax.text(xs[0] - 11, y, a, ha='left', va='center', fontsize=13, color=INK)
    ax.text(xs[0] + 14.5, y, b, ha='right', va='center', fontsize=13, color=INK, fontweight='bold')

# ---------- 2. stride ----------
x0 = xs[1] - 7 * c / 2
title(xs[1], 'Stride', 'kernel 3, no padding (one row shown)')
yrow = gtop - 2.2
for k in range(7):
    ax.add_patch(Rectangle((x0 + k*c, yrow - c), c, c, fc='white', ec=INK, lw=1.0, zorder=2))
    ax.text(x0 + k*c + c/2, yrow - c/2, str(k + 1), ha='center', va='center', fontsize=12, color=GREY, zorder=3)
def windows(cap, stride, ytop, col):
    n = (7 - 3) // stride + 1
    ax.text(x0, ytop, cap, ha='left', va='center', fontsize=13, color=INK, fontweight='bold')
    ytop -= 2.2
    for i in range(n):
        yy = ytop - 1.7 * i
        ax.add_patch(Rectangle((x0 + i*stride*c + 0.15, yy - 1.3), 3*c - 0.3, 1.3, fc=col, ec='none', zorder=3))
    ax.text(x0 + 7*c + 0.8, ytop - 0.85 * (n - 1) - 0.65, f'{n} outputs', ha='left', va='center', fontsize=13, color=GREY)
    return ytop - 1.7 * n
yb = windows('Stride 1: moves 1 cell', 1, yrow - c - 2.0, BLUE)
yb2 = windows('Stride 2: moves 2 cells', 2, yb - 2.6, YEL)

# ---------- 3. padding ----------
c3 = 2.2
x0 = xs[2] - 9 * c3 / 2
title(xs[2], 'Padding', 'kernel 3, stride 1')
for r in range(9):
    for k in range(9):
        pad = r in (0, 8) or k in (0, 8)
        ax.add_patch(Rectangle((x0 + k*c3, gtop + 0.5 - (r+1)*c3), c3, c3, fc=(PALEGREY if pad else 'white'),
                               ec=LIGHT, lw=0.7, zorder=1))
        if pad:
            ax.text(x0 + k*c3 + c3/2, gtop + 0.5 - r*c3 - c3/2, '0', ha='center', va='center', fontsize=9, color=GREY)
ax.add_patch(Rectangle((x0, gtop + 0.5 - 3*c3), 3*c3, 3*c3, fill=False, ec=YEL, lw=3.4, zorder=6))
ytx = gtop + 0.5 - 9*c3 - 3.2
ax.text(xs[2], ytx, 'Padding 1: output 7 × 7', ha='center', va='center', fontsize=13, color=INK, fontweight='bold')
ax.text(xs[2], ytx - 3.4, 'same size as the input', ha='center', va='center', fontsize=13, color=GREY)
ax.text(xs[2], ytx - 6.8, 'No padding: output 5 × 5', ha='center', va='center', fontsize=13, color=GREY)

# ---------- 4. receptive field ----------
title(xs[3], 'Receptive field', 'two 3-wide layers (one row shown)')
cw = 3.6
def row(n, ymid, label, active=None):
    xl = xs[3] - n * cw / 2
    cells = []
    for k in range(n):
        on = active is None or k in active
        ax.add_patch(Rectangle((xl + k*cw, ymid - cw/2), cw, cw, fc=(PALEYEL if (active is not None and on) else 'white'),
                               ec=(INK), lw=1.1, zorder=3))
        cells.append((xl + k*cw + cw/2, ymid))
    ax.text(xl - 1.2, ymid, label, ha='right', va='center', fontsize=13, color=GREY)
    return cells
y_in, y_l1, y_l2 = gtop - 17.5, gtop - 8.5, gtop - 0.5
l2 = row(1, y_l2, 'Layer 2')
l1 = row(3, y_l1, 'Layer 1')
inp = row(5, y_in, 'Input')
# colour the cells
def fill(cells, col):
    for (x, y) in cells:
        ax.add_patch(Rectangle((x - cw/2, y - cw/2), cw, cw, fc=col, ec=INK, lw=1.1, zorder=3.5))
fill(l2, YEL); fill(l1, PALEYEL); fill(inp, PALEYEL)
for k, (x, y) in enumerate(l2 + l1 + inp):
    pass
# links
for (x2, y2) in l2:
    for (x1, y1) in l1:
        ax.plot([x2, x1], [y2 - cw/2, y1 + cw/2], color=GREY, lw=1.0, zorder=2)
for i, (x1, y1) in enumerate(l1):
    for j in range(3):
        xi, yi = inp[i + j]
        ax.plot([x1, xi], [y1 - cw/2, yi + cw/2], color=GREY, lw=1.0, zorder=2)
ax.text(xs[3], y_in - cw/2 - 3.2, 'One output cell sees 5 input cells', ha='center', va='center', fontsize=13, color=INK, fontweight='bold')
ax.text(xs[3], y_in - cw/2 - 6.6, 'In 2-D: a 5 × 5 area, the same as', ha='center', va='center', fontsize=13, color=GREY)
ax.text(xs[3], y_in - cw/2 - 9.6, 'one 5 × 5 kernel, with fewer weights', ha='center', va='center', fontsize=13, color=GREY)

# formula line
ax.text(W/2, 1.6, 'Output size = (N − F + 2P) / S + 1      N input size, F kernel size, P padding, S stride',
        ha='center', va='center', fontsize=SUB, color=INK)
print(save_crop(fig, '/tmp/figs2/Figure3_kernel_stride_padding.png'))
