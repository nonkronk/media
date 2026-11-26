import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch
from PIL import Image
plt.rcParams['font.family'] = 'Liberation Sans'
INK = '#2b2b2b'; GREY = '#4d4d4d'; BLUE = '#1f6fd1'; LIGHT = '#bdbdbd'; YEL = '#f2b400'
PALEBLUE = '#dbe9fb'; PALEYEL = '#fff1c2'; PALEGREY = '#e6e6e6'
LBL = 16; SUB = 13.5

def new_fig(W, H, width_in=12):
    fig = plt.figure(figsize=(width_in, width_in * H / W), dpi=250)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

def save_crop(fig, path, margin=24):
    fig.savefig(path, facecolor='white')
    plt.close(fig)
    im = Image.open(path).convert('RGB')
    a = np.asarray(im)
    mask = (a < 250).any(axis=2)
    ys, xs = np.where(mask)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    y0 = max(0, y0 - margin); x0 = max(0, x0 - margin)
    y1 = min(a.shape[0], y1 + margin); x1 = min(a.shape[1], x1 + margin)
    im.crop((x0, y0, x1, y1)).save(path)
    return im.crop((x0, y0, x1, y1)).size

def grid(ax, data, x0, ytop, s, fills=None, fs=18, ec=INK, lw=1.0, bold=None, fmt=None, color=INK):
    """data[r][c]; (x0, ytop) is the top-left corner; y goes down."""
    data = np.asarray(data)
    R, C = data.shape
    for r in range(R):
        for c in range(C):
            xl, yb = x0 + c * s, ytop - (r + 1) * s
            fc = 'white' if fills is None else fills[r][c]
            ax.add_patch(Rectangle((xl, yb), s, s, fc=fc, ec=ec, lw=lw, zorder=2))
            v = data[r, c]
            t = fmt(v) if fmt else (str(int(v)) if float(v).is_integer() else f'{v:g}')
            w = 'bold' if (bold and bold[r][c]) else 'normal'
            ax.text(xl + s / 2, yb + s / 2, t, ha='center', va='center', fontsize=fs,
                    color=color, fontweight=w, zorder=3)

def label(ax, x, y, name, sub=None, ys=None):
    ax.text(x, y, name, ha='center', va='baseline', fontsize=LBL, color=INK, linespacing=1.15)
    if sub:
        ax.text(x, ys, sub, ha='center', va='baseline', fontsize=SUB, color=GREY, linespacing=1.1)
