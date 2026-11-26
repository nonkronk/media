import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
ORANGE = '#d9622b'
x = np.linspace(-5, 5, 1001)
sig = 1/(1+np.exp(-x))
fs = [
 ('Sigmoid',    r'$f(x)=1\,/\,(1+e^{-x})$', sig,            sig*(1-sig),            (-0.12, 1.12), (-0.02, 0.32)),
 ('Tanh',       r'$f(x)=\tanh(x)$',            np.tanh(x),     1-np.tanh(x)**2,        (-1.2, 1.2),   (-0.05, 1.15)),
 ('ReLU',       r'$f(x)=\max(0,\,x)$',         np.maximum(0,x),(x>0).astype(float),    (-0.6, 5.3),   (-0.08, 1.2)),
 ('Leaky ReLU', r'$f(x)=\max(0.01x,\,x)$',    np.where(x>0,x,0.01*x), np.where(x>0,1.0,0.01), (-0.6, 5.3), (-0.08, 1.2)),
]
fig = plt.figure(figsize=(12, 5.9), dpi=250)
L, R = 0.105, 0.995
pw = (R - L) / 4
def style(a):
    for s in ('top', 'right'): a.spines[s].set_visible(False)
    for s in ('left', 'bottom'): a.spines[s].set_color(LIGHT)
    a.tick_params(colors=GREY, labelsize=12.5, length=3)
    a.grid(True, color='#ececec', lw=0.8); a.set_axisbelow(True)
    a.axhline(0, color=LIGHT, lw=0.9, zorder=1); a.axvline(0, color=LIGHT, lw=0.9, zorder=1)
axs = []
for i, (name, tex, f, df, yl1, yl2) in enumerate(fs):
    x0 = L + i * pw + 0.028
    a1 = fig.add_axes([x0, 0.56, pw - 0.058, 0.29])
    a2 = fig.add_axes([x0, 0.12, pw - 0.058, 0.29])
    for a, y, col, yl in ((a1, f, BLUE, yl1), (a2, df, ORANGE, yl2)):
        style(a); a.set_xlim(-5, 5); a.set_ylim(*yl)
        a.plot(x, y, color=col, lw=2.6, zorder=3, solid_capstyle='round')
        a.set_xticks([-4, -2, 0, 2, 4])
    fig.text(x0 + (pw - 0.058) / 2, 0.955, name, ha='center', va='center', fontsize=17, fontweight='bold', color=INK)
    fig.text(x0 + (pw - 0.058) / 2, 0.885, tex, ha='center', va='center', fontsize=14, color=GREY)
    axs.append((a1, a2))

# annotations on the gradient row (the point of the figure)
a = axs[0][1]; a.annotate('peak 0.25', xy=(0, 0.25), xytext=(0.8, 0.285), fontsize=13, color=INK, va='center',
                          arrowprops=dict(arrowstyle='-', color=GREY, lw=1.0))
a.text(0, 0.045, '', fontsize=1)
a.text(3.2, 0.205, 'near 0 at\nthe ends', ha='center', va='center', fontsize=13, color=GREY)
a = axs[1][1]; a.text(3.5, 0.5, 'near 0 at\nthe ends', ha='center', va='center', fontsize=13, color=GREY)
a.annotate('peak 1', xy=(0, 1.0), xytext=(0.8, 1.06), fontsize=13, color=INK, va='center', arrowprops=dict(arrowstyle='-', color=GREY, lw=1.0))
a = axs[2][1]; a.text(-2.5, 0.38, '0:\nno signal\nfor x < 0', ha='center', va='center', fontsize=13, color=INK)
a.text(2.8, 0.62, '1: passes\nback as is', ha='center', va='center', fontsize=13, color=INK)
a = axs[3][1]; a.annotate('0.01:\nsmall,\nnot zero', xy=(-2.5, 0.02), xytext=(-2.5, 0.50), fontsize=13, color=INK, ha='center', va='center',
                          arrowprops=dict(arrowstyle='-|>', color=GREY, lw=1.0))
a.text(2.5, 0.62, '1 for x > 0', ha='center', va='center', fontsize=13, color=INK)
# row labels
fig.text(0.004, 0.705, 'Output\nf(x)', ha='left', va='center', fontsize=14, color=BLUE, fontweight='bold', linespacing=1.15)
fig.text(0.004, 0.265, 'Gradient\nf′(x)', ha='left', va='center', fontsize=14, color=ORANGE, fontweight='bold', linespacing=1.15)
fig.text(0.5, 0.012, 'x (input to the activation)', ha='center', va='bottom', fontsize=13, color=GREY)
fig.savefig('/tmp/figs2/Figure4_activation_functions.png', facecolor='white')
im = Image.open('/tmp/figs2/Figure4_activation_functions.png'); print(im.size)
