import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from skimage import data, transform
A = np.load('/tmp/vgg/acts.npz')
groups = [
  ('Early layer', 'conv 2 of 13 · maps of 224 × 224', 'edges and fur lines', 'block1_conv2', [42, 17, 13, 26]),
  ('Middle layer', 'conv 10 of 13 · maps of 28 × 28', 'eyes, nose and ear outlines', 'block4_conv3', [309, 149, 44, 491]),
  ('Deep layer', 'conv 13 of 13 · maps of 14 × 14', 'large, coarse regions of the face', 'block5_conv3', [286, 183, 450, 355]),
]
W, H = 142, 50
fig, ax = new_fig(W, H)
yc = 27.0
S = 11.6; g = 1.0
img = transform.resize(data.chelsea()[18:274, 96:352], (224, 224), anti_aliasing=True)
isz = 23.0
x = 2.0
ax.imshow(img, extent=(x, x + isz, yc - isz/2, yc + isz/2), zorder=2, interpolation='bilinear')
ax.add_patch(Rectangle((x, yc - isz/2), isz, isz, fill=False, ec=INK, lw=1.0, zorder=3))
yl = yc - 12.8 - 3.2
ax.text(x + isz/2, yl, 'Input image', ha='center', va='baseline', fontsize=LBL, color=INK)
ax.text(x + isz/2, yl - 3.6, '224 × 224 pixels', ha='center', va='baseline', fontsize=13, color=GREY)
ax.text(x + isz/2, yl - 7.0, ' ', ha='center', va='baseline', fontsize=13, color=GREY)
x += isz + 11.5
ax.add_patch(FancyArrowPatch((x - 9.0, yc), (x - 2.2, yc), arrowstyle='-|>', mutation_scale=16, color=GREY, lw=1.6, zorder=2))
gw = 2 * S + g
for gi, (name, sub, note, layer, chans) in enumerate(groups):
    gx = x
    for j, k in enumerate(chans):
        r, c = divmod(j, 2)
        m = A[layer][:, :, k]; m = np.clip(m / (np.percentile(m, 99.5) + 1e-9), 0, 1)
        xl = gx + c * (S + g); yb = yc + gw/2 - (r + 1) * S - r * g
        ax.imshow(m, extent=(xl, xl + S, yb, yb + S), cmap='gray', vmin=0, vmax=1, interpolation='bilinear', zorder=2)
        ax.add_patch(Rectangle((xl, yb), S, S, fill=False, ec=INK, lw=0.9, zorder=3))
    cx = gx + gw / 2
    ax.text(cx, yl, name, ha='center', va='baseline', fontsize=LBL, color=INK, fontweight='bold')
    ax.text(cx, yl - 3.6, sub, ha='center', va='baseline', fontsize=13, color=GREY)
    ax.text(cx, yl - 7.0, note, ha='center', va='baseline', fontsize=13, color=INK)
    x = gx + gw + 11.5
    if gi < len(groups) - 1:
        ax.add_patch(FancyArrowPatch((x - 9.0, yc), (x - 2.2, yc), arrowstyle='-|>', mutation_scale=16, color=GREY, lw=1.6, zorder=2))
# top caption
ax.text(W/2 + 3, H - 3.4, 'Feature maps of a trained VGG16 network (bright = the filter found its pattern)', ha='center', va='baseline',
        fontsize=LBL, fontweight='bold', color=INK)
x0 = 2.0 + isz + 4.0; x1 = x - 11.5
ax.add_patch(FancyArrowPatch((x0, H - 8.6), (x1, H - 8.6), arrowstyle='-|>', mutation_scale=16, color=GREY, lw=1.4, zorder=2))
ax.text((x0 + x1)/2, H - 8.6, 'deeper in the network', ha='center', va='center', fontsize=13, color=GREY,
        bbox=dict(fc='white', ec='none', pad=3.0), zorder=3)
print(save_crop(fig, '/tmp/figs2/Figure7_vgg16_feature_maps.png'))
