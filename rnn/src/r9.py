import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 114, 95
fig, ax = new_fig(W, H, width_in=11.2)
xs = [50, 68, 86, 104]
rows = [
    dict(yc=79, title='Text classification', sub='many words, one label',
         inp=['I', 'love', 'this', 'class'], out=[None, None, None, 'positive'], fb=False),
    dict(yc=48, title='Text generation', sub='one word, many words',
         inp=['The', 'dogs', 'bark', 'loudly'], out=['dogs', 'bark', 'loudly', '<end>'], fb=True),
    dict(yc=17, title='Sequence tagging', sub='one label per word',
         inp=['John', 'lives', 'in', 'Paris'], out=['PER', 'O', 'O', 'LOC'], fb=False),
]
for ri, r in enumerate(rows):
    yc = r['yc']
    T(ax, 1, yc + 2.4, r['title'], fs=16, bold=True, ha='left')
    T(ax, 1, yc - 2.2, r['sub'], fs=14, color=GREY, ha='left')
    for i, x in enumerate(xs):
        rbox(ax, x, yc, 9.5, 6.4, PALEGREEN, GREEN, lw=2.0)
        T(ax, x, yc, 'RNN', fs=14.5, bold=True)
        dashed = r['fb'] and i > 0
        rbox(ax, x, yc - 10.6, 12, 6.0, 'white' if dashed else PALEBLUE, BLUE, lw=1.9, ls=(0, (3, 2)) if dashed else '-')
        T(ax, x, yc - 10.6, r['inp'][i], fs=14.5)
        arrow(ax, (x, yc - 7.4), (x, yc - 3.6), color=GREY, lw=2.0, ms=14)
        o = r['out'][i]
        if o:
            w = max(12, 1.0 * len(o) + 4.5)
            rbox(ax, x, yc + 10.6, w, 6.0, PALEYEL, YEL, lw=1.9)
            T(ax, x, yc + 10.6, o, fs=14.5, bold=True)
            arrow(ax, (x, yc + 3.6), (x, yc + 7.4), color=GREY, lw=2.0, ms=14)
        if i < 3:
            arrow(ax, (x + 5.0, yc), (xs[i + 1] - 5.0, yc), color=GREY, lw=2.2, ms=15)
            if r['fb']:
                arrow(ax, (x + 6.2, yc + 8.2), (xs[i + 1] - 6.2, yc - 8.2), color=ORANGE, lw=2.0, ms=13, z=5)
    if ri < 2:
        line(ax, [1, 113], [yc - 15.6, yc - 15.6], color='#dddddd', lw=1.2)
# note for generation
T(ax, 1, 48 - 6.6, 'orange: output used as next input', fs=13.5, color=ORANGE, ha='left')
print(save_crop(fig, '/tmp/rfig/R9_input_output_types.png'))
