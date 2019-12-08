from typing import List
import numpy as np
from matplotlib import pyplot as plt

Layer = List[int]


def get_layers(image: List[int], layer_size: int) -> List[Layer]:
    return np.reshape(image, (-1, layer_size)).tolist()


def layer_with_fewest_zeros(layers: List[Layer]) -> Layer:
    num_zeros = lambda l: l.count(0)
    return min(layers, key=num_zeros)


def full_image(layers: List[Layer]) -> Layer:
    combined_layer = []
    for pixels in zip(*layers):
        for pixel in pixels:
            if pixel != 2:
                combined_layer.append(pixel)
                break
    return combined_layer


TEST_IMAGE = [int(c) for c in "123456789012"]
assert get_layers(TEST_IMAGE, 3 * 2) == [[1,2,3,4,5,6],[7,8,9,0,1,2]]
assert layer_with_fewest_zeros(get_layers(TEST_IMAGE, 3 * 2)) == [1,2,3,4,5,6]

TEST_IMAGE2 = [int(c) for c in "0222112222120000"]
assert get_layers(TEST_IMAGE2, 2 * 2) == [[0,2,2,2],[1,1,2,2],[2,2,1,2],[0,0,0,0]]
assert full_image(get_layers(TEST_IMAGE2, 2 * 2)) == [0,1,1,0]

with open("input.txt") as f:
    image = [int(c) for c in f.read().strip()]
    image_layers = get_layers(image, 25 * 6)
    max_layer = layer_with_fewest_zeros(image_layers)
    print("Part 1:", max_layer.count(1) * max_layer.count(2))
    print("Part 2:")
    decoded_image = np.reshape(full_image(image_layers), (6, 25))
    plt.imshow(decoded_image)
    plt.show()
