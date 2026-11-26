import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 116, 84
fig, ax = new_fig(W, H, width_in=11.5)
oy = 17
Y = lambda y: y + oy
T(ax, 1, 81, 'An LSTM cell: three gates decide what the cell state keeps, writes and shows', fs=16, bold=True, ha='left')
# cell state line
yc = Y(55)
T(ax, 3.5, yc, r'$c_{t-1}$', fs=16, color=BLUE, bold=False)
T(ax, 111, yc, r'$c_t$', fs=16, color=BLUE)
T(ax, 64, yc + 5.2, 'cell state: the long-term memory', fs=14.5, color=BLUE, bold=True)
def op(x, y, s):
    circ(ax, x, y, 2.5, 'white', INK, lw=1.9)
    T(ax, x, y - 0.1, s, fs=16 if s == '×' else 15, bold=True)
CL = dict(color=BLUE, lw=3.6, ms=17)
arrow(ax, (7.2, yc), (20 - 2.5, yc), **CL)
arrow(ax, (20 + 2.5, yc), (45.5 - 2.5, yc), **CL)
arrow(ax, (45.5 + 2.5, yc), (107, yc), **CL)
op(20, yc, '×'); op(45.5, yc, '+')
circ(ax, 91, yc, 0.9, BLUE, BLUE, z=5)
# gates
gy = Y(24); gw, gh = 14.8, 13.0
def gate(x, act, name, role, fc, ec):
    rbox(ax, x, gy, gw, gh, fc, ec, lw=2.0)
    T(ax, x, gy + 3.9, act, fs=16, bold=True)
    T(ax, x, gy - 0.4, name, fs=14, bold=True)
    T(ax, x, gy - 4.3, role, fs=13.5, color=GREY)
gate(20, 'σ', 'forget gate', 'what to keep', PALEYEL, YEL)
gate(37, 'σ', 'input gate', 'what to write', PALEYEL, YEL)
gate(54, 'tanh', 'candidate', 'new content', PALEGREEN, GREEN)
gate(80, 'σ', 'output gate', 'what to show', PALEYEL, YEL)
top = gy + gh / 2
# bus
yb = Y(9)
line(ax, [8.5, 80], [yb, yb], color=GREY, lw=2.0)
T(ax, 3.2, yb, r'$h_{t-1}$', fs=16)
arrow(ax, (14, yb - 4.6), (14, yb), color=GREY, lw=2.0, ms=14)
T(ax, 14, yb - 6.8, r'$x_t$', fs=16)
for gx in (20, 37, 54, 80):
    circ(ax, gx, yb, 0.55, GREY, GREY, z=4)
    arrow(ax, (gx, yb), (gx, gy - gh / 2 - 0.1), color=GREY, lw=2.0, ms=14)
T(ax, 84, yb, r'Every gate reads $x_t$ and $h_{t-1}$', fs=14, color=GREY, ha='left')
# gate outputs
G = dict(color=GREY, lw=2.0, ms=14)
arrow(ax, (20, top + 0.1), (20, yc - 2.6), **G)
T(ax, 22.4, Y(42), r'$f_t$', fs=16, ha='left', bold=False)
yi = Y(41)
op(45.5, yi, '×')
line(ax, [37, 37], [top + 0.1, yi], color=GREY, lw=2.0)
arrow(ax, (37, yi), (45.5 - 2.6, yi), **G)
T(ax, 34.7, Y(35.8), r'$i_t$', fs=16, ha='right')
line(ax, [54, 54], [top + 0.1, yi], color=GREY, lw=2.0)
arrow(ax, (54, yi), (45.5 + 2.6, yi), **G)
T(ax, 56.3, Y(35.8), r'$g_t$', fs=16, ha='left')
arrow(ax, (45.5, yi + 2.6), (45.5, yc - 2.6), **G)
# output branch
op(91, Y(36), '×')
rbox(ax, 91, Y(46.5), 11, 6.0, PALEGREEN, GREEN, lw=2.0)
T(ax, 91, Y(46.5), 'tanh', fs=14.5, bold=True)
arrow(ax, (91, yc - 0.9), (91, Y(46.5) + 3.1), color=BLUE, lw=2.6, ms=14)
arrow(ax, (91, Y(46.5) - 3.1), (91, Y(36) + 2.6), color=GREY, lw=2.0, ms=14)
line(ax, [80, 80], [top + 0.1, Y(36)], color=GREY, lw=2.0)
arrow(ax, (80, Y(36)), (91 - 2.6, Y(36)), **G)
T(ax, 82.3, Y(33.2), r'$o_t$', fs=16, ha='left')
arrow(ax, (91 + 2.6, Y(36)), (107, Y(36)), **G)
T(ax, 111, Y(36), r'$h_t$', fs=16)
T(ax, 111, Y(36) - 4.4, 'hidden', fs=13.5, color=GREY)
T(ax, 111, Y(36) - 7.2, 'state', fs=13.5, color=GREY)
# gate example
line(ax, [1, 115], [Y(-3.5), Y(-3.5)], color='#dddddd', lw=1.2)
T(ax, 1, 11.8, 'A gate scales each value by a number from 0 to 1', fs=15, bold=True, ha='left')
def trip(x0, vals, kind):
    for k, v in enumerate(vals):
        x = x0 + 4.25 + k * 9.3
        if kind == 'gate':
            m = min(max(v, 0), 1)
            c = tuple(np.array([1, 1, 1]) * (1 - m) + np.array(matplotlib.colors.to_rgb(YEL)) * m)
            fc, ec = c, YEL
        elif kind == 'res':
            fc, ec = PALEGREEN, GREEN
        else:
            fc, ec = PALEBLUE, BLUE
        rbox(ax, x, 6.2, 8.5, 5.0, fc, ec, lw=1.8, r=0.8)
        T(ax, x, 6.2, (('%.2f' % v).rstrip('0').rstrip('.') if v not in (1.0, 0.0) else ('%.1f' % v)).replace('-', '−'), fs=14.5)
    T(ax, x0 + 13.6, 1.3, {'gate': 'gate', 'res': 'result', 'data': 'data'}[kind], fs=13.5, color=GREY)
import matplotlib.colors
trip(1, [0.8, -0.5, 0.3], 'data')
T(ax, 32.2, 6.2, '×', fs=18, bold=True)
trip(36, [1.0, 0.0, 0.5], 'gate')
T(ax, 67.2, 6.2, '=', fs=18, bold=True)
trip(71, [0.8, 0.0, 0.15], 'res')
T(ax, 101, 8.4, '1 keeps it', fs=14, color=GREY, ha='left')
T(ax, 101, 4.2, '0 blocks it', fs=14, color=GREY, ha='left')
print(save_crop(fig, '/tmp/rfig/R7_lstm_cell.png'))
