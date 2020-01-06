import numpy as np

with open('input') as fh:
    image = np.fromiter(map(int, fh.readline().rstrip()), dtype=np.uint8).reshape(-1, 6, 25)

layer = np.argmin((image == 0).sum(axis=(1, 2)))
print('Part 1:', np.sum(image[layer] == 1) * np.sum(image[layer] == 2))


import matplotlib.pyplot as plt

decoded = np.frompyfunc((lambda x, y: y if x == 2 else x), 2, 1).reduce(image, axis=0).astype(np.uint8)
plt.imshow(255. * decoded)
plt.show()
