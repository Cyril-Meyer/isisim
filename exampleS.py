import time
import numpy as np
import skimage.draw
import matplotlib.pyplot as plt

import utils
import generatorS


def example_2d(export=False):
    dense_label_2d = img = np.zeros((256, 256), dtype=np.uint8)
    dense_label_2d[skimage.draw.disk((128, 128), 64)] = 1
    print(dense_label_2d.shape, dense_label_2d.min(), dense_label_2d.max(), dense_label_2d.dtype)
    # plt.imshow(dense_label_2d, cmap="gray")
    # plt.show()

    gen_pos = generatorS.gen_click_random_uniform_advanced(dense_label_2d, click=5)
    gen_neg = generatorS.gen_click_around_border(np.abs(1 - dense_label_2d), click=5)

    pos_click_map, _ = next(gen_pos)
    neg_click_map, _ = next(gen_neg)

    print(pos_click_map.shape, pos_click_map.min(), pos_click_map.max(), pos_click_map.dtype)
    print(neg_click_map.shape, neg_click_map.min(), neg_click_map.max(), neg_click_map.dtype)

    plt.imshow(utils.combine_image_and_maps(dense_label_2d, pos_click_map, neg_click_map))
    if export:
        plt.savefig('media/example_2d.png')
    plt.show()


def example_3d(export=False):
    dense_label_3d = skimage.draw.ellipsoid(64, 64, 64)
    print(dense_label_3d.shape, dense_label_3d.min(), dense_label_3d.max(), dense_label_3d.dtype)
    # utils.show_stack(dense_label_3d, cmap="gray")

    gen_pos = generatorS.gen_click_random_uniform_advanced(dense_label_3d, click=5)
    gen_neg = generatorS.gen_click_around_border(np.abs(1 - dense_label_3d), click=8)

    pos_click_map, _ = next(gen_pos)
    neg_click_map, _ = next(gen_neg)

    print(pos_click_map.shape, pos_click_map.min(), pos_click_map.max(), pos_click_map.dtype)
    print(neg_click_map.shape, neg_click_map.min(), neg_click_map.max(), neg_click_map.dtype)

    save_filename = None
    if export:
        save_filename = 'media/example_3d.gif'
    utils.show_stack(utils.combine_image_and_maps(dense_label_3d, pos_click_map, neg_click_map), save_filename=save_filename)


def benchmark_3d():
    dense_label_3d = skimage.draw.ellipsoid(128, 128, 128)
    dense_label_3d = np.pad(dense_label_3d, ((100, 25), (100, 25), (100, 25)))
    print(dense_label_3d.shape, dense_label_3d.min(), dense_label_3d.max(), dense_label_3d.dtype)

    gen_pos = generatorS.gen_click_random_uniform(dense_label_3d, click=10)
    gen_pos_adv = generatorS.gen_click_random_uniform_advanced(dense_label_3d, click=10)
    gen_neg = generatorS.gen_click_around_border(np.abs(1 - dense_label_3d), click=10)

    t0 = time.time()
    for _ in range(8):
        _, _ = next(gen_pos)
    t1 = time.time()
    print(t1 - t0)

    t0 = time.time()
    for _ in range(8):
        _, _ = next(gen_pos_adv)
    t1 = time.time()
    print(t1 - t0)

    t0 = time.time()
    for _ in range(8):
        _, _ = next(gen_neg)
    t1 = time.time()
    print(t1 - t0)


if __name__ == "__main__":
    # example_2d(export=False)
    # example_3d(export=False)
    benchmark_3d()
    exit(0)