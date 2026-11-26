import sys; sys.path.insert(0, '/tmp/rfig')
from rc import *
W, H = 104, 66
fig, ax = new_fig(W, H, width_in=10.5)
o = 8
def Y(y): return y + o
# previous state
rbox(ax, 9, Y(30), 15, 9, PALEGREEN, GREEN); T(ax, 9, Y(30), '$h_{t-1}$', fs=17)
T(ax, 9, Y(37.5), 'previous state', fs=13.5, color=GREY)
# W
rbox(ax, 28, Y(30), 9, 8, PALEGREY, GREY); T(ax, 28, Y(30), 'W', fs=17, bold=True)
T(ax, 28, Y(37.5), 'recurrent weights', fs=13.5, color=GREY)
arrow(ax, (16.9, Y(30)), (23.3, Y(30)))
# input path
rbox(ax, 9, Y(8), 15, 8, PALEBLUE, BLUE); T(ax, 9, Y(8), '$x_t$', fs=17)
T(ax, 9, Y(1.6), 'input', fs=13.5, color=GREY)
rbox(ax, 28, Y(8), 9, 8, PALEGREY, GREY); T(ax, 28, Y(8), 'U', fs=17, bold=True)
T(ax, 28, Y(1.6), 'input weights', fs=13.5, color=GREY)
arrow(ax, (16.9, Y(8)), (23.3, Y(8)))
line(ax, [32.8, 49], [Y(8), Y(8)])
arrow(ax, (49, Y(8)), (49, Y(27.2)))
# sum node
circ(ax, 49, Y(30), 2.9, 'white', INK); T(ax, 49, Y(30), '+', fs=20)
arrow(ax, (32.8, Y(30)), (46.0, Y(30)))
T(ax, 39.5, Y(33.4), '$W\\,h_{t-1}$', fs=14.5)
T(ax, 39.5, Y(11.6), '$U\\,x_t$', fs=14.5)
# bias
rbox(ax, 49, Y(48), 8, 7, PALEGREY, GREY); T(ax, 49, Y(48), 'b', fs=17, bold=True)
T(ax, 54.6, Y(48), 'bias', fs=13.5, color=GREY, ha='left')
arrow(ax, (49, Y(44.5)), (49, Y(33.0)))
# tanh
arrow(ax, (52.0, Y(30)), (62.3, Y(30)))
rbox(ax, 68, Y(30), 11, 8, PALEYEL, YEL); T(ax, 68, Y(30), 'tanh', fs=16, bold=True)
T(ax, 68, Y(22.6), 'keeps each value', fs=13.5, color=GREY)
T(ax, 68, Y(18.8), 'between −1 and 1', fs=13.5, color=GREY)
# new state
arrow(ax, (73.6, Y(30)), (79.3, Y(30)))
rbox(ax, 87, Y(30), 15, 9, PALEGREEN, GREEN); T(ax, 87, Y(30), '$h_t$', fs=17)
T(ax, 87, Y(22.8), 'new state', fs=13.5, color=GREY)
# output
arrow(ax, (87, Y(34.5)), (87, Y(43.2)))
circ(ax, 87, Y(47), 3.8, PALEYEL, YEL); T(ax, 87, Y(47), '$y_t$', fs=16)
T(ax, 92.4, Y(47), 'output', fs=13.5, color=GREY, ha='left')
# next step
arrow(ax, (94.5, Y(30)), (103, Y(30)))
T(ax, 98.7, Y(34.2), 'next step', fs=13.5, color=GREY)
T(ax, 1, Y(55.5), 'The same W, U and b are used at every step.', fs=14.5, color=INK, ha='left')
T(ax, 52, 2.5, '$h_t = \\tanh(W\\,h_{t-1} + U\\,x_t + b)$', fs=19, color=INK)
print(save_crop(fig, '/tmp/rfig/R2_rnn_cell.png'))
