import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from scipy.signal import convolve2d
from skimage import data, color, transform

rgb = data.chelsea()
crop = rgb[18:274, 96:352]
g = color.rgb2gray(transform.resize(crop, (200, 200), anti_aliasing=True))

kernels = [
    ('Original',     [[0,0,0],[0,1,0],[0,0,0]], 'same'),
    ('Blur',         np.ones((3,3))/9,           'blur'),
    ('Sharpen',      [[0,-1,0],[-1,5,-1],[0,-1,0]], 'same'),
    ('Edge detect',  [[0,1,0],[1,-4,1],[0,1,0]],  'abs'),
    ('Vertical edges', [[-1,0,1],[-2,0,2],[-1,0,1]], 'abs'),
]
def run(k, mode):
    k = np.array(k, float)
    out = convolve2d(g, k[::-1, ::-1], mode='same', boundary='symm')
    if mode == 'abs':
        out = np.abs(out); out = np.clip(out / np.percentile(out, 99.8), 0, 1)
    else:
        out = np.clip(out, 0, 1)
    return out

n = len(kernels)
pw, gap = 20, 4.5
W = n * pw + (n - 1) * gap + 4
H = 20 + 25
fig, ax = new_fig(W, H)
y_img_top = H - 2
for i, (name, k, mode) in enumerate(kernels):
    x0 = 2 + i * (pw + gap)
    out = run(k, mode)
    ax.imshow(out, extent=(x0, x0 + pw, y_img_top - pw, y_img_top), cmap='gray', vmin=0, vmax=1,
              interpolation='bilinear', zorder=2)
    ax.add_patch(Rectangle((x0, y_img_top - pw), pw, pw, fill=False, ec=INK, lw=1.0, zorder=3))
    # name
    ax.text(x0 + pw/2, y_img_top - pw - 3.6, name, ha='center', va='baseline', fontsize=LBL, color=INK)
    # kernel grid
    kk = np.array(k)
    s = 2.7
    kx = x0 + pw/2 - 1.5 * s
    ktop = y_img_top - pw - 6.4
    fmt = (lambda v: f'1/9') if i == 1 else None
    fills = [[PALEBLUE]*3 for _ in range(3)]
    grid(ax, np.round(kk * (9 if i == 1 else 1)).astype(int) if i == 1 else kk.astype(int), kx, ktop, s,
         fills=fills, fs=13, ec=BLUE, lw=1.2, fmt=(lambda v: '1') if i == 1 else None)
    if i == 1:
        ax.text(x0 + pw/2, ktop - 3*s - 2.2, 'each weight is 1/9', ha='center', va='baseline', fontsize=13, color=GREY)
print(save_crop(fig, '/tmp/figs2/Figure2_kernel_effects.png'))
