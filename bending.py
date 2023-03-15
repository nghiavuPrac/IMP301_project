import cv2, time
import numpy as np
from matplotlib import pyplot as plt
from rembg import remove
from skimage import io, util
from multiprocessing import Process, Pool

class LBP:
    def __init__(self, num_process=8) -> None:
        self.workers = num_process

    def __call__(self, img):
        self.img = img
        height, width = img.shape
        self.width = width

        output = np.zeros(shape=(height-2, width-2), dtype=np.uint8)
        print(height, width)

        pool = Pool(processes=self.workers)
        results = pool.map(self.row_process, range(height-2))
        for i, row in results:
            output[i] = row

        return output

    def row_process(self, h):
        row = np.zeros(self.width-2, dtype=np.uint8)
        for w in range(self.width-2):
            row[w] = self.each_cell(self.img[h:h+3, w:w+3])
        return (h, row)

    
    def each_cell(self, img):
        result = 0
        center = img[1, 1]
        # center +=1
        if img[0, 0] >= center:      result += 1
        if img[0, 1] >= center:      result += 2
        if img[0, 2] >= center:      result += 4
        if img[1, 0] >= center:      result += 128
        if img[1, 2] >= center:      result += 8
        if img[2, 0] >= center:      result += 64
        if img[2, 1] >= center:      result += 32
        if img[2, 2] >= center:      result += 16

        return result


def blending(root_path, filter_path, k=2, alpha=1.2, beta=-20):
    
    lbp = LBP()
    lbp_img = lbp(cv2.imread(root_path, 0))
    k_size=5
    texture = cv2.blur(lbp_img, (k_size, k_size), )
    texture = cv2.convertScaleAbs(texture, alpha=alpha, beta=beta)
    height, width = texture.shape

    pattern = io.imread(filter_path)
    pattern = cv2.resize(pattern, (width, height))

    input_img = cv2.imread(root_path)[1:-1, 1:-1]
    mask  = remove(input_img)[:, :, 3]
    

    # plt.imshow(lbp_img, cmap='gray')
    # plt.show()
    # plt.imshow(texture, cmap='gray')
    # plt.show()
    # plt.imshow(mask, cmap='gray')
    # plt.show()

    texture = texture / 255
    texture = 1.2 - texture
    texture = texture * k
    texture[texture > 1] = 1
    for i in range(3):
        input_img[:, :, i] = texture * pattern[:, :, i]
        
    input_img[mask < 64 ] = 255
    return input_img
    plt.imshow(input_img)
    plt.show()

output = blending('/home/anhpn19/IMP/blend/face.jpg', '/home/anhpn19/IMP/blend/ren.jpg', k=1.5, alpha=1.2, beta=-00)
plt.imshow(output)
