import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
import matplotlib.colors as mc
W, H = 112, 82
fig, ax = new_fig(W, H, width_in=11.5)
T(ax, 1, 79.5, 'A language model: at every step the RNN predicts the next word', fs=16, bold=True, ha='left')
rbox(ax, 3.2, 74.6, 4.4, 2.6, BLUE, BLUE, lw=1, r=0.5)
T(ax, 6.6, 74.6, 'is the word that actually comes next. All probabilities are example values.', fs=14, color=GREY, ha='left')
cols = [
    dict(x=38, inp='the', emb=[0.2, 0.8, 0.5, 0.1], h=r'$h_1$',
         bars=[('dogs', .40), ('cats', .30), ('kids', .10), ('birds', .08)], tgt=0, loss='0.92'),
    dict(x=67, inp='dogs', emb=[0.7, 0.3, 0.9, 0.4], h=r'$h_2$',
         bars=[('are', .55), ('in', .20), ('run', .06), ('bark', .05)], tgt=3, loss='3.00'),
    dict(x=96, inp='bark', emb=[0.4, 0.6, 0.2, 0.8], h=r'$h_3$',
         bars=[('loudly', .30), ('again', .25), ('all', .20), ('at', .10)], tgt=0, loss='1.20'),
]
yin, yemb, yh = 14, 24, 35
rows = [59, 55, 51, 47]
yl = 67
for c in cols:
    x = c['x']
    # input word
    rbox(ax, x, yin, 13, 6.2, 'white', GREY, lw=1.8)
    T(ax, x, yin, c['inp'], fs=15.5)
    arrow(ax, (x, yin + 3.4), (x, yemb - 2.9), color=GREY, lw=2.0, ms=14)
    # embedding cells
    for k, v in enumerate(c['emb']):
        col = tuple(np.array([1, 1, 1]) * (1 - v) + np.array(mc.to_rgb(BLUE)) * v)
        ax.add_patch(Rectangle((x - 6.4 + k * 3.3, yemb - 2.0), 3.1, 4.0, fc=col, ec=BLUE, lw=1.5, zorder=3))
    arrow(ax, (x, yemb + 2.5), (x, yh - 4.2), color=GREY, lw=2.0, ms=14)
    # hidden
    rbox(ax, x, yh, 13, 7.4, PALEGREEN, GREEN, lw=2.0)
    T(ax, x, yh, c['h'], fs=16.5)
    arrow(ax, (x, yh + 3.9), (x, rows[-1] - 3.3), color=GREY, lw=2.0, ms=14)
    # bars
    x0 = x - 6.0
    for (w, p), yy in zip(c['bars'], rows):
        is_t = (c['bars'].index((w, p)) == c['tgt'])
        T(ax, x0 - 0.9, yy, w, fs=14, ha='right', color=INK if is_t else GREY, bold=is_t)
        ax.add_patch(Rectangle((x0, yy - 1.35), max(p * 20, 0.3), 2.7, fc=BLUE if is_t else '#cfcfcf', ec='none', zorder=3))
        T(ax, x0 + p * 20 + 0.8, yy, '%.2f' % p, fs=13.5, ha='left', color=INK if is_t else GREY, bold=is_t)
    # loss
    arrow(ax, (x, 61.8), (x, yl - 3.1), color=GREY, lw=2.0, ms=14)
    rbox(ax, x, yl, 13.5, 5.8, PALEORANGE, ORANGE, lw=2.0)
    T(ax, x, yl, 'loss ' + c['loss'], fs=15, bold=True)
# h chain
for a, b in [(0, 1), (1, 2)]:
    arrow(ax, (cols[a]['x'] + 7.0, yh), (cols[b]['x'] - 7.0, yh), color=GREY, lw=2.2, ms=15)
# layer labels
def lab(y, a, b=None):
    if b is None:
        T(ax, 1, y, a, fs=15, bold=True, ha='left')
    else:
        T(ax, 1, y + 2.0, a, fs=15, bold=True, ha='left')
        T(ax, 1, y - 2.0, b, fs=13.5, color=GREY, ha='left')
lab(yin, 'Input word')
lab(yemb, 'Embedding')
lab(yh, 'Hidden state')
lab(53, 'Next-word', 'probabilities')
lab(yl, 'Loss', '−log of blue bar')
# summary
line(ax, [1, 111], [8.4, 8.4], color='#dddddd', lw=1.2)
T(ax, 1, 3.6, 'Average loss = (0.92 + 3.00 + 1.20) / 3 = 1.71', fs=15.5, bold=True, ha='left')
T(ax, 66, 3.6, 'Perplexity = exp(1.71) = 5.5', fs=15.5, bold=True, ha='left', color=ORANGE)
print(save_crop(fig, '/tmp/rfig/R8_language_model.png'))
