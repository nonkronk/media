import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
import matplotlib.colors as mc
W, H = 112, 70
fig, ax = new_fig(W, H, width_in=11.2)
T(ax, 1, 67.5, 'Example: classifying a movie review with an LSTM', fs=16, bold=True, ha='left')
xs = [40, 58, 76, 94]
words = ['I', 'loved', 'this', 'movie']
embs = [[0.3, 0.8, 0.2, 0.6], [0.9, 0.2, 0.7, 0.4], [0.1, 0.5, 0.8, 0.3], [0.6, 0.7, 0.1, 0.9]]
yw, ye, yl = 11, 22, 34
for i, x in enumerate(xs):
    rbox(ax, x, yw, 12, 6.0, PALEBLUE, BLUE, lw=1.9)
    T(ax, x, yw, words[i], fs=15)
    arrow(ax, (x, yw + 3.4), (x, ye - 2.9), color=GREY, lw=2.0, ms=14)
    for k, v in enumerate(embs[i]):
        col = tuple(np.array([1, 1, 1]) * (1 - v) + np.array(mc.to_rgb(BLUE)) * v)
        ax.add_patch(Rectangle((x - 6.4 + k * 3.3, ye - 2.0), 3.1, 4.0, fc=col, ec=BLUE, lw=1.5, zorder=3))
    arrow(ax, (x, ye + 2.5), (x, yl - 3.9), color=GREY, lw=2.0, ms=14)
    rbox(ax, x, yl, 12, 7.0, PALEGREEN, GREEN, lw=2.0)
    T(ax, x, yl, 'LSTM', fs=15, bold=True)
    if i < 3:
        arrow(ax, (x + 6.3, yl), (xs[i + 1] - 6.3, yl), color=GREY, lw=2.2, ms=15)
# classifier
x = xs[-1]
arrow(ax, (x, yl + 3.9), (x, 44.3), color=GREY, lw=2.2, ms=15)
T(ax, x + 2.0, 40.3, r'final state $h_n$', fs=14, color=GREY, ha='left')
rbox(ax, x, 47.5, 20, 6.2, PALEYEL, YEL, lw=2.0)
T(ax, x, 47.5, 'Dense + sigmoid', fs=14.5, bold=True)
arrow(ax, (x, 50.8), (x, 55.3), color=GREY, lw=2.2, ms=15)
rbox(ax, x, 59.5, 20, 6.2, 'white', INK, lw=2.0)
T(ax, x, 59.5, 'positive 0.94', fs=15, bold=True)
T(ax, x - 12, 59.5, 'probability that the review is positive', fs=14, color=GREY, ha='right')
T(ax, x - 12, 55.5, '(example value)', fs=13.5, color=GREY, ha='right')
# layer labels
def lab(y, a, b=None):
    if b is None:
        T(ax, 1, y, a, fs=15, bold=True, ha='left')
    else:
        T(ax, 1, y + 2.0, a, fs=15, bold=True, ha='left')
        T(ax, 1, y - 2.0, b, fs=13.5, color=GREY, ha='left')
lab(yw, 'Words')
lab(ye, 'Embedding')
lab(yl, 'LSTM', 'one step per word')
lab(47.5, 'Classifier')
line(ax, [1, 111], [4.6, 4.6], color='#dddddd', lw=1.2)
T(ax, 1, 1.4, 'Every review is cut or padded to 256 words, so the LSTM runs 256 steps (four are drawn).', fs=14, color=GREY, ha='left')
print(save_crop(fig, '/tmp/rfig/R10_imdb_pipeline.png'))
