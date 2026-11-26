import sys; sys.path.insert(0, '/tmp/figs2')
from common import *
ORANGE = '#d9622b'
Hs = np.load('/tmp/fig8/hists_100_0.15.npy')       # runs x epochs x (ep, train loss, val loss, train acc, val acc)
H = Hs.mean(0)
ep = H[:, 0]; trl, val, tra, vaa = H[:, 1], H[:, 2], H[:, 3] * 100, H[:, 4] * 100
stop = int(ep[val.argmin()]); print('stop epoch', stop, 'val min', val.min(), 'final val', val[-1], 'train acc', tra[-1], 'val acc', vaa[-1])
fig = plt.figure(figsize=(12, 5.0), dpi=250)
axl = fig.add_axes([0.07, 0.17, 0.41, 0.68]); axr = fig.add_axes([0.58, 0.17, 0.40, 0.68])
def style(a):
    for s in ('top', 'right'): a.spines[s].set_visible(False)
    for s in ('left', 'bottom'): a.spines[s].set_color(LIGHT)
    a.tick_params(colors=GREY, labelsize=13, length=3)
    a.grid(True, color='#ececec', lw=0.8); a.set_axisbelow(True)
    a.set_xlim(0, ep[-1]); a.set_xlabel('Epoch (one pass over the training images)', fontsize=13.5, color=GREY)
style(axl); style(axr)
# ---- loss ----
axl.plot(ep, trl, color=BLUE, lw=2.6); axl.plot(ep, val, color=ORANGE, lw=2.6)
axl.set_ylim(0, 2.3); axl.set_ylabel('Loss (lower is better)', fontsize=13.5, color=GREY)
axl.axvspan(stop, ep[-1], color='#f6f6f6', zorder=0)
axl.axvline(stop, color=INK, lw=1.4, ls=(0, (4, 3)), zorder=2)
axl.plot([stop], [val[stop - 1]], 'o', color=ORANGE, ms=8, mec='white', mew=1.6, zorder=5)
axl.annotate(f'Stop training here\n(epoch {stop}, lowest validation loss)', xy=(stop, val[stop - 1]), xytext=(stop + 5, 1.78),
             fontsize=13.5, color=INK, va='center', arrowprops=dict(arrowstyle='-|>', color=GREY, lw=1.2))
axl.text(ep[-1] * 0.98, trl[-1] + 0.17, 'Training loss', ha='right', va='bottom', fontsize=13, color=BLUE, fontweight='bold')
axl.text(ep[-1] * 0.98, val[-1] + 0.06, 'Validation loss', ha='right', va='bottom', fontsize=13, color=ORANGE, fontweight='bold')
axl.text((stop + ep[-1]) / 2 + 12, 1.22, 'overfitting: the validation\nloss rises again', ha='center', va='center', fontsize=13, color=GREY)
# ---- accuracy ----
axr.plot(ep, tra, color=BLUE, lw=2.6); axr.plot(ep, vaa, color=ORANGE, lw=2.6)
axr.set_ylim(20, 104); axr.set_ylabel('Accuracy (%)', fontsize=13.5, color=GREY)
axr.axvline(stop, color=INK, lw=1.4, ls=(0, (4, 3)), zorder=2)
axr.text(ep[-1] * 0.5, tra[-1] - 5.0, 'Training accuracy', ha='center', va='top', fontsize=13, color=BLUE, fontweight='bold')
axr.text(ep[-1] * 0.5, vaa[-1] + 3.0, 'Validation accuracy', ha='center', va='bottom', fontsize=13, color=ORANGE, fontweight='bold')
xg = ep[-1] * 0.93
axr.annotate('', xy=(xg, vaa[-1] + 1), xytext=(xg, tra[-1] - 1), arrowprops=dict(arrowstyle='<|-|>', color=INK, lw=1.4, shrinkA=0, shrinkB=0))
axr.text(xg - 2, (tra[-1] + vaa[-1]) / 2, f'gap\n{tra[-1] - vaa[-1]:.0f} points', ha='right', va='center', fontsize=13.5, color=INK)
fig.text(0.07, 0.945, 'Loss', ha='left', va='center', fontsize=17, fontweight='bold', color=INK)
fig.text(0.58, 0.945, 'Accuracy', ha='left', va='center', fontsize=17, fontweight='bold', color=INK)
fig.text(0.5, 0.02, 'Example run: a small CNN on 8 × 8 digit images, 100 training images (15% of the labels wrong on purpose), 600 validation images, mean of 5 runs.',
         ha='center', va='bottom', fontsize=13, color=GREY)
fig.savefig('/tmp/figs2/Figure8_early_stopping_real_run.png', facecolor='white')
print(Image.open('/tmp/figs2/Figure8_early_stopping_real_run.png').size)
