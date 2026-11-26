import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from scipy.signal import convolve2d
from skimage import data, color, transform
RED = '#d9534f'; GREEN = '#2e9e5b'
PALEGREEN = '#dff3e6'; PALERED = '#fbe0dc'

X = np.array([[1,1,2,4],[5,6,7,8],[3,2,1,0],[1,2,3,4]], float)
def pool(a, f):
    h, w = a.shape
    return f(a.reshape(h//2, 2, w//2, 2), axis=(1, 3))
MX, AV = pool(X, np.max), pool(X, np.mean)
print(MX, AV)
assert MX[0,0] == 6 and AV[0,0] == 3.25

W, H = 147, 52
fig, ax = new_fig(W, H)
fc = [[PALEYEL, PALEBLUE], [PALEGREEN, PALERED]]
ec = [[YEL, BLUE], [GREEN, RED]]
s = 3.2
yc = 23.0
# titles
ax.text(34, H - 3.0, 'Pooling a 4 × 4 map', ha='center', va='baseline', fontsize=LBL + 1, fontweight='bold', color=INK)
ax.text(34, H - 7.4, '2 × 2 filter, stride 2', ha='center', va='baseline', fontsize=13, color=GREY)
ax.text(104, H - 3.0, 'Pooling a real feature map', ha='center', va='baseline', fontsize=LBL + 1, fontweight='bold', color=INK)
ax.text(104, H - 7.4, 'vertical edges of the cat photo, zoom on the yellow box', ha='center', va='baseline', fontsize=13, color=GREY)

# input
xi = 2.0
fills = [[fc[r//2][c//2] for c in range(4)] for r in range(4)]
grid(ax, X, xi, yc + 2*s, s, fills=fills, fs=15, ec=LIGHT, lw=0.9)
for br in range(2):
    for bc in range(2):
        ax.add_patch(Rectangle((xi + bc*2*s, yc + 2*s - (br+1)*2*s), 2*s, 2*s, fill=False, ec=ec[br][bc], lw=2.6, zorder=6))
ax.text(xi + 2*s, yc - 2*s - 3.4, 'Input', ha='center', va='baseline', fontsize=LBL, color=INK)

# outputs
xo = 31.0
so = 4.6
def out_grid(M, yc_o, fmt, fsz=14):
    fills = [[fc[r][c] for c in range(2)] for r in range(2)]
    grid(ax, M, xo, yc_o + so, so, fills=fills, fs=fsz, ec=LIGHT, lw=0.9, fmt=fmt)
    for br in range(2):
        for bc in range(2):
            ax.add_patch(Rectangle((xo + bc*so, yc_o + so - (br+1)*so), so, so, fill=False, ec=ec[br][bc], lw=2.0, zorder=6))
y_max, y_avg = yc + 10.6, yc - 10.6
out_grid(MX, y_max, lambda v: f'{v:g}')
out_grid(AV, y_avg, lambda v: f'{v:g}', 12)
for yo in (y_max, y_avg):
    ax.add_patch(FancyArrowPatch((xi + 4*s + 1.8, yc), (xo - 1.8, yo), arrowstyle='-|>', mutation_scale=20, color=GREY, lw=1.6, zorder=2))
ax.text(xo + 2*so + 2.6, y_max + 1.9, 'Max pooling', ha='left', va='baseline', fontsize=15, fontweight='bold', color=INK)
ax.text(xo + 2*so + 2.6, y_max - 1.0, 'keeps the strongest\nvalue of each block', ha='left', va='top', fontsize=13, color=GREY, linespacing=1.1)
ax.text(xo + 2*so + 2.6, y_avg + 1.9, 'Average pooling', ha='left', va='baseline', fontsize=15, fontweight='bold', color=INK)
ax.text(xo + 2*so + 2.6, y_avg - 1.0, 'keeps the mean\nof each block', ha='left', va='top', fontsize=13, color=GREY, linespacing=1.1)
# one-block working under the outputs (top-left block of the Q5 table)
ax.text(xo + 2*so + 2.6, y_max - 6.6 + 0.2, 'block 1, 1, 5, 6 gives 6', ha='left', va='top', fontsize=13, color=INK)
ax.text(xo + 2*so + 2.6, y_avg - 6.6 + 0.2, '(1 + 1 + 5 + 6) / 4 = 3.25', ha='left', va='top', fontsize=13, color=INK)

# real feature map
rgb = data.chelsea(); crop = rgb[18:274, 96:352]
g = color.rgb2gray(transform.resize(crop, (96, 96), anti_aliasing=True))
sob = np.array([[-1,0,1],[-2,0,2],[-1,0,1]], float)
fm = np.maximum(convolve2d(g, sob[::-1, ::-1], mode='same', boundary='symm'), 0)
fm = np.clip(fm / np.percentile(fm, 99.5), 0, 1)
r0, r1, c0, c1 = 22, 54, 8, 40            # zoom box (left eye)
zoom = fm[r0:r1, c0:c1]
pm, pa = pool(zoom, np.max), pool(zoom, np.mean)
xb = 72.0; size = 21.0
yb = yc - size/2
ax.imshow(fm, extent=(xb, xb + size, yb, yb + size), cmap='gray', vmin=0, vmax=1, interpolation='nearest', zorder=2)
ax.add_patch(Rectangle((xb, yb), size, size, fill=False, ec=INK, lw=1.0, zorder=3))
u = size / 96
bx0 = xb + c0*u; bx1 = xb + c1*u
by1 = yb + size - r0*u; by0 = yb + size - r1*u
ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, fill=False, ec=YEL, lw=2.4, zorder=5))
ax.text(xb + size/2, yb - 3.4, 'Feature map', ha='center', va='baseline', fontsize=LBL, color=INK)
ax.text(xb + size/2, yb - 7.4, '96 × 96', ha='center', va='baseline', fontsize=SUB, color=GREY)
xs_ = 102.0; ss = 17.0
for img, yo, nm, note in ((pm, y_max, 'Max pooling', 'edges stay bright'), (pa, y_avg, 'Average pooling', 'edges are dimmer')):
    ax.imshow(img, extent=(xs_, xs_ + ss, yo - ss/2, yo + ss/2), cmap='gray', vmin=0, vmax=1, interpolation='nearest', zorder=2)
    ax.add_patch(Rectangle((xs_, yo - ss/2), ss, ss, fill=False, ec=YEL, lw=2.4, zorder=3))
    ax.annotate('', xy=(xs_ - 1.2, yo), xytext=(bx1 + 1.0, (by0 + by1)/2 + (3.0 if yo > yc else -3.0)),
                arrowprops=dict(arrowstyle='-|>', color=GREY, lw=1.4, shrinkA=0, shrinkB=0), zorder=2)
    ax.text(xs_ + ss + 2.2, yo + 2.2, nm, ha='left', va='baseline', fontsize=15, fontweight='bold', color=INK)
    ax.text(xs_ + ss + 2.2, yo - 0.9, '16 × 16 (zoom)', ha='left', va='top', fontsize=13, color=GREY)
    ax.text(xs_ + ss + 2.2, yo - 4.4, note, ha='left', va='top', fontsize=13, color=GREY)
# divider
ax.plot([68.5, 68.5], [3, H - 9], color='#dddddd', lw=1.2, zorder=1)
print(save_crop(fig, '/tmp/figs2/Figure5_max_vs_average_pooling.png'))
