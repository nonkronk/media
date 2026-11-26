import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 120, 68
fig, ax = new_fig(W, H, width_in=11.5)
PW = 37.5
def panel(ox, title, sub):
    rbox(ax, ox + PW/2, 33, PW, 66, 'white', FAINT, lw=1.4, r=1.5, z=1)
    T(ax, ox + PW/2, 61.5, title, fs=17, bold=True)
    T(ax, ox + PW/2, 56.3, sub, fs=13.5, color=GREY)
def chip(x, y, s, fc, ec, w=9.6, h=7.4, fs=13):
    rbox(ax, x, y, w, h, fc, ec, lw=1.6, r=1.0); T(ax, x, y, s, fs=fs)
def node(x, y, s):
    circ(ax, x, y, 2.4, 'white', INK, lw=1.6); T(ax, x, y - 0.1, s, fs=16)
def state(x, y, s, fc=PALEGREEN, ec=GREEN):
    rbox(ax, x, y, 7.6, 6.6, fc, ec, lw=1.6, r=1.0); T(ax, x, y, s, fs=14.5)
def foot(ox, mem, par):
    T(ax, ox + PW/2, 8.6, mem, fs=13.5, color=GREY)
    T(ax, ox + PW/2, 3.9, par, fs=14, bold=True)

# ---- Simple RNN
o = 0.5
panel(o, 'Simple RNN', 'no gates')
state(o + 5, 42, '$h_{t-1}$'); state(o + 5, 24, '$x_t$', PALEBLUE, BLUE)
rbox(ax, o + 21, 33, 11, 8, PALEYEL, YEL); T(ax, o + 21, 33, 'tanh', fs=15, bold=True)
arrow(ax, (o + 9, 42), (o + 15.5, 35.2)); arrow(ax, (o + 9, 24), (o + 15.5, 30.8))
state(o + 31.5, 33, '$h_t$'); arrow(ax, (o + 26.5, 33), (o + 28, 33))
T(ax, o + PW/2, 15.5, '$h_t=\\tanh(Wh_{t-1}+Ux_t+b)$', fs=13)
foot(o, 'memory: h only', '4,672 parameters')

# ---- LSTM
o = 0.5 + PW + 3.5
panel(o, 'LSTM', 'three gates + cell state')
state(o + 4.5, 46, '$c_{t-1}$'); arrow(ax, (o + 8.4, 46), (o + 11.6, 46))
node(o + 13.5, 46, '×'); arrow(ax, (o + 15.9, 46), (o + 21.1, 46)); node(o + 23.5, 46, '+')
arrow(ax, (o + 25.9, 46), (o + 27.7, 46)); state(o + 31.5, 46, '$c_t$')
chip(o + 13.5, 34, 'forget\ngate $f$', PALEYEL, YEL); arrow(ax, (o + 13.5, 37.7), (o + 13.5, 43.6))
chip(o + 23.5, 34, 'new\n$i \\times g$', PALEYEL, YEL); arrow(ax, (o + 23.5, 37.7), (o + 23.5, 43.6))
chip(o + 31.5, 24, 'output\ngate $o$', PALEYEL, YEL); arrow(ax, (o + 31.5, 43.0), (o + 31.5, 27.9), color=GREEN, ls='--')
state(o + 31.5, 14.5, '$h_t$'); arrow(ax, (o + 31.5, 20.3), (o + 31.5, 17.9))
T(ax, o + 12, 24, '$f,i,o$ use\n$h_{t-1}$ and $x_t$', fs=12.5, color=GREY)
foot(o, 'memory: h and c', '18,688 parameters')

# ---- GRU
o = 0.5 + 2*(PW + 3.5)
panel(o, 'GRU', 'two gates, no cell state')
state(o + 4.5, 46, '$h_{t-1}$'); arrow(ax, (o + 8.4, 46), (o + 11.6, 46))
node(o + 13.5, 46, '×'); arrow(ax, (o + 15.9, 46), (o + 21.1, 46)); node(o + 23.5, 46, '+')
arrow(ax, (o + 25.9, 46), (o + 27.7, 46)); state(o + 31.5, 46, '$h_t$')
chip(o + 13.5, 34, 'update\ngate $z$', PALEYEL, YEL); arrow(ax, (o + 13.5, 37.7), (o + 13.5, 43.6))
chip(o + 23.5, 34, 'new\ncontent', PALEBLUE, BLUE); arrow(ax, (o + 23.5, 37.7), (o + 23.5, 43.6))
chip(o + 23.5, 22, 'reset\ngate $r$', PALEYEL, YEL); arrow(ax, (o + 23.5, 25.7), (o + 23.5, 30.3))
T(ax, o + 10, 23, '$z$ keeps the old,\n$1-z$ writes new', fs=12.5, color=GREY)
foot(o, 'memory: h only', '14,016 parameters')
print(save_crop(fig, '/tmp/rfig/R12_rnn_lstm_gru.png'))
