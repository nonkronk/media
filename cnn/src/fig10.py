import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
from matplotlib.patches import Polygon
from skimage import transform
import matplotlib.cm as cm
import leaf
leafimg = leaf.render(256, True) / 255.0
H_ = leaf.heat(256)
W, H = 182, 50
fig, ax = new_fig(W, H)
yc = 28.0
def show(img, x, y, s, lw=1.0):
    ax.imshow(img, extent=(x, x + s, y, y + s), zorder=2, interpolation='bilinear')
    ax.add_patch(Rectangle((x, y), s, s, fill=False, ec=INK, lw=lw, zorder=3))
def arrow(x0, x1):
    ax.add_patch(FancyArrowPatch((x0, yc), (x1, yc), arrowstyle='-|>', mutation_scale=16, color=GREY, lw=1.6, zorder=2, shrinkA=0, shrinkB=0))
yl = yc - 14.5
def lab(cx, name, sub):
    ax.text(cx, yl, name, ha='center', va='baseline', fontsize=15, color=INK, fontweight='bold', linespacing=1.1)
    ax.text(cx, yl - 3.4, sub, ha='center', va='top', fontsize=13, color=GREY, linespacing=1.2)
S = 21.0
# 1 photo
x1 = 8.0
show(leafimg, x1, yc - S/2, S)
lab(x1 + S/2, 'Leaf photo', '54,000 images\n38 classes')
# 2 preprocess (real transforms of the drawn image)
x2 = x1 + S + 9
aug = [transform.resize(leafimg, (224, 224), anti_aliasing=True), leafimg[:, ::-1], transform.rotate(leafimg, 20, mode='edge'), np.clip(leafimg * 1.28, 0, 1)]
t = 10.0; gp = 1.0
for j, im in enumerate(aug):
    r, c = divmod(j, 2)
    show(im, x2 + c * (t + gp), yc + S/2 - (r + 1) * t - r * gp, t, 0.9)
lab(x2 + S/2, 'Preprocess', 'resize to 224 × 224,\nnormalise, augment')
# 3 ResNet18
x3 = x2 + S + 9
CC = [('#cfe2fa', '#e8f1fd', '#9fc2ee')] * 3
xx = x3 + 0.5
for h, d in ((9.5, 2.2), (6.8, 3.6), (4.6, 5.6)):
    dx, dy = d * 0.85, d * 0.55
    y0 = yc - (h + dy) / 2
    fr, tp, rt = CC[0]
    ax.add_patch(Rectangle((xx, y0), h, h, fc=fr, ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Polygon([(xx, y0+h), (xx+h, y0+h), (xx+h+dx, y0+h+dy), (xx+dx, y0+h+dy)], fc=tp, ec=INK, lw=1.1, zorder=3))
    ax.add_patch(Polygon([(xx+h, y0), (xx+h+dx, y0+dy), (xx+h+dx, y0+h+dy), (xx+h, y0+h)], fc=rt, ec=INK, lw=1.1, zorder=3))
    xx += h + dx + 1.6
w3 = xx - x3 - 1.6
lab(x3 + w3/2, 'ResNet18', 'pretrained on ImageNet,\nfine-tuned on leaves')
# 4 prediction
x4 = x3 + w3 + 9.5
classes = [('Tomato healthy', 0.12), ('Tomato early blight', 0.22), ('Tomato late blight', 1.0), ('Tomato leaf mold', 0.16)]
bh = 3.3; gpb = 2.6; bw = 15.0
ytop = yc + (4 * bh + 3 * gpb) / 2
for i, (nm, v) in enumerate(classes):
    y = ytop - (i + 1) * bh - i * gpb
    top = (i == 2)
    ax.add_patch(Rectangle((x4, y), max(bw * v, 0.5), bh, fc=BLUE if top else LIGHT, ec='none', zorder=3))
    ax.text(x4 + max(bw * v, 0.5) + 1.2, y + bh/2, nm, ha='left', va='center', fontsize=13, color=INK, fontweight='bold' if top else 'normal')
w4 = bw + 22
lab(x4 + w4/2 - 3, 'Prediction', 'softmax: one probability\nper class')
# 5 Grad-CAM
x5 = x4 + w4 + 7
a = np.clip(1.25 * H_ ** 0.8, 0, 1)[..., None] * 0.62
over = (1 - a) * leafimg + a * cm.jet(H_)[..., :3]
show(over, x5, yc - S/2, S)
lab(x5 + S/2, 'Grad-CAM check', 'do the red areas sit on\nthe lesions?')
# arrows
arrow(x1 + S + 1.5, x2 - 1.5); arrow(x2 + S + 1.5, x3 - 1.5); arrow(x3 + w3 + 1.5, x4 - 1.5); arrow(x4 + w4 - 4.5, x5 - 1.5)
ax.text(W/2, 0.0, 'Schematic: the leaf, the bars and the heat map are drawn for illustration.', ha='center', va='bottom', fontsize=13, color=GREY)
print(save_crop(fig, '/tmp/figs2/Figure10_plant_disease_pipeline.png'))
