import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from matplotlib.patches import Polygon
from skimage import data, transform

conv = lambda cin, cout: 3*3*cin*cout + cout
P = [conv(3,32), conv(32,64), conv(64,128), 8*8*128*64 + 64, 64*4 + 4]
total = sum(P); print(P, total)
assert total == 617860 and 8*8*128 == 8192

PITCH = 22.0
W, H = 2 + 5 * PITCH + 2 + 16, 82
fig, ax = new_fig(W, H)
CONV = ('#cfe2fa', '#e8f1fd', '#9fc2ee'); POOL = ('#fde9a8', '#fff4d1', '#f1d06a')
from PIL import Image
photo = np.asarray(Image.open('/tmp/leaf/lb8.jpg').convert('RGB').resize((64, 64), Image.LANCZOS)) / 255.0
rng = np.random.RandomState(3)
FS_NAME, FS_SHAPE, FS_PAR = 16, 14.5, 13.5

def stage(col, yc, kind, h, d, name, shape, par):
    cx = 2 + PITCH/2 + col * PITCH
    if kind in ('conv', 'pool', 'in'):
        dx, dy = d * 0.85, d * 0.55
        wtot = h + dx
        x = cx - wtot / 2; y0 = yc - (h + dy) / 2
        fr, tp, rt = CONV if kind == 'conv' else POOL
        if kind == 'in':
            ax.imshow(photo, extent=(x, x + h, y0, y0 + h), zorder=3, interpolation='bilinear')
            ax.add_patch(Rectangle((x, y0), h, h, fill=False, ec=INK, lw=1.1, zorder=4)); fr, tp, rt = '#e3d3b8', '#efe3cf', '#cdb890'
        else:
            ax.add_patch(Rectangle((x, y0), h, h, fc=fr, ec=INK, lw=1.1, zorder=3))
        ax.add_patch(Polygon([(x, y0+h), (x+h, y0+h), (x+h+dx, y0+h+dy), (x+dx, y0+h+dy)], fc=tp, ec=INK, lw=1.1, zorder=3))
        ax.add_patch(Polygon([(x+h, y0), (x+h+dx, y0+dy), (x+h+dx, y0+h+dy), (x+h, y0+h)], fc=rt, ec=INK, lw=1.1, zorder=3))
        half = wtot / 2
    elif kind == 'flat':
        fw, fh, n = 2.4, 22, 28
        for k in range(n):
            g = 0.35 + 0.6 * rng.rand()
            ax.add_patch(Rectangle((cx - fw/2, yc - fh/2 + k*fh/n), fw, fh/n, fc=(g,)*3, ec='none', zorder=3))
        ax.add_patch(Rectangle((cx - fw/2, yc - fh/2), fw, fh, fill=False, ec=INK, lw=1.1, zorder=4))
        half = fw / 2
    else:   # circles
        n, span = (7, 18) if kind == 'fc' else (4, 10.5)
        classes = [('Healthy', 0.03), ('Early blight', 0.23), ('Late blight', 0.64), ('Leaf mold', 0.10)]
        for k, yy in enumerate(np.linspace(yc + span/2, yc - span/2, n)):
            top = kind == 'out' and k == 2
            ax.add_patch(Circle((cx, yy), 1.45, fc=(BLUE if top else '#dff3e6'), ec=INK, lw=1.1, zorder=3))
            if kind == 'out':
                nm_, p_ = classes[k]
                fw_ = 'bold' if top else 'normal'
                ax.text(cx + 2.8, yy, nm_, ha='left', va='center', fontsize=14, color=INK, fontweight=fw_)
                ax.text(cx + 2.8 + 13.2, yy, f'{p_:.2f}', ha='left', va='center', fontsize=14, color=INK, fontweight=fw_)
        half = 1.45
    ax.text(cx, yc - 16.9, name, ha='center', va='bottom', fontsize=FS_NAME, color=INK, linespacing=1.1)
    ax.text(cx, yc - 17.6, shape, ha='center', va='top', fontsize=FS_SHAPE, color=INK, fontweight='bold')
    if par:
        ax.text(cx, yc - 20.8, f'{par:,} params', ha='center', va='top', fontsize=FS_PAR, color=GREY)
    return cx, half

def arrow(a, b, yc):
    ax.add_patch(FancyArrowPatch((a, yc), (b, yc), arrowstyle='-|>', mutation_scale=13, color=GREY, lw=1.4, zorder=2, shrinkA=0, shrinkB=0))

y1, y2 = 70.0, 30.0
row1 = [('in', 15, 1.2, 'Input\nleaf photo', '64 × 64 × 3', None), ('conv', 15, 3.6, 'Conv 1\n+ ReLU', '64 × 64 × 32', P[0]),
        ('pool', 10.5, 3.6, 'Max\npooling', '32 × 32 × 32', None), ('conv', 10.5, 6.0, 'Conv 2\n+ ReLU', '32 × 32 × 64', P[1]),
        ('pool', 7.5, 6.0, 'Max\npooling', '16 × 16 × 64', None)]
row2 = [('conv', 7.5, 9.5, 'Conv 3\n+ ReLU', '16 × 16 × 128', P[2]), ('pool', 5.2, 9.5, 'Max\npooling', '8 × 8 × 128', None),
        ('flat', 0, 0, 'Flatten', '8,192', None), ('fc', 0, 0, 'Fully connected\n+ ReLU', '64', P[3]), ('out', 0, 0, 'Output\n+ softmax', '4 classes', P[4])]
pos = []
for rown, (yc, rows) in enumerate(((y1, row1), (y2, row2))):
    prev = None
    for c, (kind, h, d, nm, sh, pr) in enumerate(rows):
        cx, half = stage(c, yc, kind, h, d, nm, sh, pr)
        if prev: arrow(prev[0] + prev[1] + 1.2, cx - half - 1.2, yc)
        prev = (cx, half); pos.append((cx, half))
    if rown == 0: end1 = prev
# elbow connector from the end of row 1 to the start of row 2
xs0 = 2 + PITCH/2
xr = end1[0] + end1[1] + 1.2
ymid = y1 - 25.0
ax.plot([xr, xr + 2.0, xr + 2.0], [y1, y1, ymid], color=GREY, lw=1.4, zorder=2)
ax.plot([xr + 2.0, 2.0 - 0.6, 2.0 - 0.6], [ymid, ymid, y2], color=GREY, lw=1.4, zorder=2)
x_first = xs0 - (7.5 + 9.5*0.85) / 2
ax.add_patch(FancyArrowPatch((2.0 - 0.6, y2), (x_first - 1.2, y2), arrowstyle='-|>', mutation_scale=13, color=GREY, lw=1.4, zorder=2, shrinkA=0, shrinkB=0))
ax.text(W/2, 4.2, f'Total: {total:,} parameters, {P[3]/total:.0%} of them in the first fully connected layer.', ha='center', va='bottom', fontsize=13.5, color=GREY)
ax.text(W/2, 0.9, 'Padding 1 keeps the height and width in each convolution; each pooling halves them.', ha='center', va='bottom', fontsize=13.5, color=GREY)
print(save_crop(fig, '/tmp/figs2/Figure6_architecture_volumes.png'))
