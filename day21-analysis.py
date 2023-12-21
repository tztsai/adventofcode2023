
# %%
import json
import numpy as np
import matplotlib.pyplot as plt

with open('day21.json') as f:
    data = json.load(f)

arrays = {}
sum_arr = []

for t, x in enumerate(data):
    s = 0
    for cell, n in x:
        a = arrays.setdefault(tuple(cell), [])
        a.append([t+1, n])
        s += n
    sum_arr.append(s)

arrays = {k: np.array(v) for k, v in arrays.items()}
sum_arr = np.array(sum_arr)

# %%
# from scipy.sparse import csr_matrix
# from matplotlib.animation import FuncAnimation

# im = None

# fig, ax = plt.subplots()

# def update(x):
#     global im
#     poses = np.array([(m*131+i, n*131+j) for (m, n), _, ps in x for i, j in ps])
#     x_lo = min(p[0]*131 for p, _, _ in x)
#     y_lo = min(p[1]*131 for p, _, _ in x)
#     m = max((p[0]+1)*131 for p, _, _ in x) - x_lo
#     n = max((p[1]+1)*131 for p, _, _ in x) - y_lo
#     poses -= np.array([x_lo, y_lo])
#     mat = csr_matrix((np.ones(len(poses), dtype=np.int64), 
#                       (poses[:, 0], poses[:, 1])), shape=(m, n))
#     if im is None:
#         im = plt.imshow(mat.toarray(), animated=True)
#     else:
#         im.set_data(mat.toarray())
#     return im,

# ani = FuncAnimation(fig, update, frames=data, blit=True)
# ani.save("animation.gif", fps=50, writer="imagemagick")

# %%
for k, v in arrays.items():
    plt.plot(v[:, 0], v[:, 1], '-', label=k)
plt.show()

# %%
hm = {p: a[-1, 1] for p, a in arrays.items()}
x_lo, x_hi = [f(p[0] for p in hm) for f in (min, max)]
y_lo, y_hi = [f(p[1] for p in hm) for f in (min, max)]
plt.imshow([[hm.get((i, j), 0) for j in range(y_lo, y_hi + 1)]
            for i in range(x_lo, x_hi + 1)])
plt.show()

# %%
t = np.arange(30, len(sum_arr) + 1)
x = sum_arr[29:]
m = 11

coefs = np.polyfit(t, x, 2)
print(coefs)
y = np.polyval(coefs, t)
plt.plot(t, x, '-', t, y, '.')
plt.show()
u = x / (2*(t//m)**2*m**2)
plt.plot(t, u, '-')
plt.show()

# %%
expand_times = np.array(sorted(set(a[0, 0] for a in arrays.values())),
                        dtype=np.int64) - 1
expand_times

# %%
t = expand_times[1::2]
x1 = sum_arr[t - 1]
coefs = np.polyfit(t, x1, 2)
y = np.polyval(coefs, t)
plt.plot(t, x1, '.', t, y, '-')
plt.show()
# u = x1 / (2*expand_times**2)
# plt.plot(expand_times[3:], u[3:], '-')
expand_times, coefs

# %%
np.polyval(coefs, 26501365)

# %%
# import pandas as pd

# dfs = [pd.DataFrame(a[:,:2], columns=['t', 'n']).set_index('t')
#        for a in arrays.values()]
# df = pd.concat(dfs, keys=arrays.keys(), names=['x', 'y'])
# df = df.reset_index().set_index('t').sort_index().sort_values('n')
# df.loc[expand_times]
