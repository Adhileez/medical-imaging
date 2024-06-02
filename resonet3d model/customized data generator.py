import os
import numpy as np
import multiprocessing
from skimage.transform import rotate
from scipy.ndimage import map_coordinates, gaussian_filter
import random

def random_rotate(image, mask):
    # Random rotation for 3D volumes
    angle = np.random.randint(0, 360)
    rotated_image = rotate(image, angle, axes=(0, 1), reshape=False)
    rotated_mask = rotate(mask, angle, axes=(0, 1), reshape=False)
    return rotated_image, rotated_mask

def random_flip(image, mask):
    # Random flip for 3D volumes
    if np.random.rand() < 0.5:
        axis = np.random.choice([0, 1])  # 0: up-down, 1: left-right
        image = np.flip(image, axis=axis)
        mask = np.flip(mask, axis=axis)
    return image, mask

def elastic_deform(image, mask, alpha=720, sigma=24):
    # Elastic deformation for 3D volumes
    random_state = np.random.RandomState(None)
    shape = image.shape[:3]  # assuming image is of shape (depth, height, width, channels)

    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha

    dz = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma, mode="constant", cval=0) * alpha
    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]), indexing="ij")
    indices = (x + dx).flatten(), (y + dy).flatten(), (z + dz).flatten()

    distorted_image = map_coordinates(image, indices, order=1, mode='reflect').reshape(image.shape)
    distorted_mask = map_coordinates(mask, indices, order=1, mode='reflect').reshape(mask.shape)
    return distorted_image, distorted_mask

def load_img(file_path):
    # Load a single .npy file
    return np.load(file_path)

def batch_generator(img_dir, img_list, mask_dir, mask_list, batch_size, augment=True):
    # Generator to yield batches
    L = len(img_list)
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    try:
        while True:
            for start in range(0, L, batch_size):
                end = min(start + batch_size, L)
                img_paths = [os.path.join(img_dir, fname) for fname in img_list[start:end]]
                mask_paths = [os.path.join(mask_dir, fname) for fname in mask_list[start:end]]

                imgs = pool.map(load_img, img_paths)
                masks = pool.map(load_img, mask_paths)

                imgs = np.array(imgs)
                masks = np.array(masks)

                if augment:
                    for i in range(len(imgs)):
                        imgs[i], masks[i] = random_rotate(imgs[i], masks[i])
                        imgs[i], masks[i] = random_flip(imgs[i], masks[i])
                        if np.random.rand() > 0.7:
                            imgs[i], masks[i] = elastic_deform(imgs[i], masks[i])

                yield imgs, masks
    finally:
        pool.close()
        pool.join()

