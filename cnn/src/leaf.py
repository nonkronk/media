import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse
from matplotlib.backends.backend_agg import FigureCanvasAgg
SPOTS = [(0.40, 0.58, 0.060), (0.60, 0.46, 0.048), (0.47, 0.30, 0.040), (0.57, 0.70, 0.036)]   # x, y, radius (leaf coordinates 0..1)
def outline(n=200):
    t = np.linspace(0, 1, n)
    w = 0.30 * np.sin(np.pi * t) ** 0.85 * (1 - 0.35 * t)
    return t, w
def render(size=256, diseased=True, seed=0):
    rs = np.random.RandomState(seed)
    fig = plt.figure(figsize=(size/100, size/100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis('off')
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, fc='#e9e6df', ec='none'))          # light paper background
    t, w = outline()
    y = 0.10 + 0.82 * t; xc = 0.5 + 0.03 * np.sin(2 * np.pi * t)                # slightly bent leaf
    left = np.c_[xc - w, y]; right = np.c_[xc + w, y][::-1]
    ax.add_patch(Polygon(np.r_[left, right], fc='#4f9a3d', ec='#2f6a26', lw=2.0, zorder=2))
    ax.plot([0.5, 0.5], [0.0, 0.10], color='#3d7a2e', lw=4.0, zorder=1, solid_capstyle='round')
    ax.plot(xc, y, color='#9bd47a', lw=2.4, zorder=3)
    for tt in np.linspace(0.14, 0.82, 8):
        i = int(tt * (len(t) - 1)); wi = w[i]
        for s in (-1, 1):
            ax.plot([xc[i], xc[i] + s * wi * 0.92], [y[i], y[i] + 0.09], color='#8fcb6f', lw=1.2, zorder=3)
    if diseased:
        for (sx, sy, r) in SPOTS:
            ax.add_patch(Ellipse((sx, sy), r * 3.0, r * 2.5, angle=20, fc='#d6c24a', ec='none', alpha=0.85, zorder=4))
            ax.add_patch(Ellipse((sx, sy), r * 1.7, r * 1.4, angle=20, fc='#7a4a21', ec='none', zorder=5))
    canvas = FigureCanvasAgg(fig); canvas.draw()
    a = np.asarray(canvas.buffer_rgba())[..., :3].copy()
    plt.close(fig)
    return a
def heat(size=256):
    yy, xx = np.mgrid[0:size, 0:size] / (size - 1.0); yy = 1 - yy
    h = np.zeros((size, size))
    for (sx, sy, r) in SPOTS:
        h += np.exp(-((xx - sx) ** 2 + (yy - sy) ** 2) / (2 * (r * 1.6) ** 2))
    return np.clip(h / h.max(), 0, 1)
if __name__ == '__main__':
    from PIL import Image
    Image.fromarray(np.hstack([render(256, True), render(256, False)])).save('/tmp/figs2/_leaf.png')
