from sklearn.datasets import fetch_olivetti_faces
import numpy as np
import matplotlib.pyplot as plt

faces = fetch_olivetti_faces().images
fig, ax = plt.subplots(5, 5, figsize=(5, 5))
fig.subplots_adjust(hspace=0, wspace=0)
for i in range(5):
    for j in range(5):
        ax[i, j].xaxis.set_major_locator(plt.NullLocator())
        ax[i, j].yaxis.set_major_locator(plt.NullLocator())
        ax[i, j].imshow(faces[10*i+j], cmap='bone')
plt.show()