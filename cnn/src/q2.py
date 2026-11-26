import sys; sys.path.insert(0, '/tmp/figs2')
from common import *

X = np.array([[0,0,0,0,0,0,0],
              [0,1,0,0,0,1,0],
              [0,0,0,0,0,0,0],
              [0,0,0,1,0,0,0],
              [0,1,0,0,0,1,0],
              [0,0,1,1,1,0,0],
              [0,0,0,0,0,0,0]])
K = np.array([[0,0,1],[1,0,0],[0,1,1]])
F = np.zeros((5,5), int)
for i in range(5):
    for j in range(5):
        F[i,j] = (X[i:i+3, j:j+3] * K).sum()
print(F)
assert (F == np.array([[0,1,0,0,0],[0,1,1,1,0],[1,0,0,2,1],[1,4,2,1,0],[0,0,1,2,1]])).all()
wi, wj = 3, 1                      # window at row 3, column 1 -> value 4
win = X[wi:wi+3, wj:wj+3]
P = win * K

s = 3.0
W, H = 100, 44
fig, ax = new_fig(W, H)
yc = 27.0
def top(n): return yc + n * s / 2

# input
x_in = 2
grid(ax, X, x_in, top(7), s, fills=[[PALEGREY if v else 'white' for v in r] for r in X])
ax.add_patch(Rectangle((x_in + wj*s, top(7) - (wi+3)*s), 3*s, 3*s, fill=False, ec=YEL, lw=3.4, zorder=6))
# kernel
x_k = x_in + 7*s + 9
grid(ax, K, x_k, top(3), s, fills=[[PALEBLUE if v else 'white' for v in r] for r in K], ec=BLUE, lw=1.4)
# products
x_p = x_k + 3*s + 9
grid(ax, P, x_p, top(3), s, fills=[[PALEYEL if v else 'white' for v in r] for r in P], ec=YEL, lw=1.4)
# feature map
x_f = x_p + 3*s + 11
grid(ax, F, x_f, top(5), s,
     fills=[[(lambda t: (1-0.55*t, 1-0.35*t, 1-0.02*t))(F[i,j]/4) for j in range(5)] for i in range(5)])
ax.add_patch(Rectangle((x_f + wj*s, top(5) - (wi+1)*s), s, s, fill=False, ec=YEL, lw=3.4, zorder=6))
ax.text(x_f + wj*s + s/2, top(5) - (wi+1)*s + s/2, '4', ha='center', va='center', fontsize=18,
        fontweight='bold', color=INK, zorder=7)

# operators
def op(x, t, fs=30): ax.text(x, yc, t, ha='center', va='center', fontsize=fs, color=GREY)
op(x_in + 7*s + 4.5, '×')
op(x_k + 3*s + 4.5, '=')
ax.add_patch(FancyArrowPatch((x_p + 3*s + 1.6, yc), (x_f - 1.6, yc), arrowstyle='-|>', mutation_scale=22,
                             color=GREY, lw=1.8, zorder=2))
ax.text((x_p + 3*s + x_f)/2, yc + 3.2, 'add up', ha='center', va='center', fontsize=SUB, color=GREY)

# labels (names on one line, sub-labels on one line)
yl = yc - 7*s/2 - 4.4
ys = yl - 4.6
label(ax, x_in + 7*s/2, yl, 'Input image', '7 × 7 pixels', ys)
label(ax, x_k + 3*s/2, yl, 'Kernel', '3 × 3 weights', ys)
label(ax, x_p + 3*s/2, yl, 'Window × kernel', '0+0+1+1+0+0+0+1+1 = 4', ys)
label(ax, x_f + 5*s/2, yl, 'Feature map', '5 × 5 values', ys)
print(save_crop(fig, '/tmp/figs2/Q2_convolution_example.png'))
