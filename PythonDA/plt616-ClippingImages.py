import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cbook as cbook
import matplotlib.image as mpimg


# with cbook.get_sample_data('grace_hopper.png') as image_file:
#     image = plt.imread(image_file)
image = mpimg.imread('test.jpg')
fig, ax = plt.subplots()
im = ax.imshow(image)
patch = patches.Circle((2000, 2000), radius=1000, transform=ax.transData)
im.set_clip_path(patch)

ax.axis('off')
plt.show()