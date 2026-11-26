import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Liberation Sans'
plt.rcParams['mathtext.it'] = 'Liberation Sans:italic'
plt.rcParams['mathtext.bf'] = 'Liberation Sans:bold'
plt.rcParams['mathtext.default'] = 'it'
GREEN = '#2e9e5b'; PALEGREEN = '#dff3e6'; RED = '#d9534f'; PALERED = '#fbe0dc'
ORANGE = '#d9622b'; PALEORANGE = '#fbe3d6'; FAINT = '#a8a8a8'

def rbox(ax, cx, cy, w, h, fc, ec, lw=1.8, r=1.2, z=3, ls='-'):
    p = FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                       fc=fc, ec=ec, lw=lw, zorder=z, linestyle=ls)
    ax.add_patch(p); return p

def circ(ax, cx, cy, r, fc, ec, lw=1.8, z=3, ls='-'):
    ax.add_patch(Circle((cx, cy), r, fc=fc, ec=ec, lw=lw, zorder=z, linestyle=ls))

def T(ax, x, y, s, fs=15, color=INK, ha='center', va='center', bold=False, z=6, **kw):
    return ax.text(x, y, s, ha=ha, va=va, fontsize=fs, color=color, fontweight=('bold' if bold else 'normal'), zorder=z, **kw)

def arrow(ax, p0, p1, color=GREY, lw=1.8, ms=15, ls='-', rad=0.0, z=2, style='-|>'):
    a = FancyArrowPatch(p0, p1, arrowstyle=style, mutation_scale=ms, color=color, lw=lw, linestyle=ls,
                        connectionstyle=f'arc3,rad={rad}', shrinkA=0, shrinkB=0, zorder=z)
    ax.add_patch(a); return a

def line(ax, xs, ys, color=GREY, lw=1.8, ls='-', z=2):
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle='butt')
