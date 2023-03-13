import subprocess
import time
import matplotlib.pyplot as plt
import cv2
from skimage import io, util
from texture_Synthesis import main

#variable
img = "Inputs/Texture/t4.jpg"
blocksize = 10
overlapsize = 2
scale = 2
tolerance = 0.1
# cmd = "python3 texture_Synthesis/main.py --synthesis -i "+ img + " -b "+ str(blocksize) + " -o " +str(overlapsize) + " -t "+str(tolerance)+ " -s " + str(scale) 
# subprocess.Popen(cmd, shell=True)


# img_name = img.split("/")[-1].split(".")[0]
# input = cv2.imread(img)
# output = cv2.imread("results/synthesis/" + img_name + "_b=" + str(blocksize) + "_o=" + str(overlapsize) + "_t=" + str(tolerance).replace(".", "_") + ".png")

input  = cv2.imread(img)
handle = main.texture_handler(img,blocksize,overlapsize,scale,tolerance)
start = time.time()
output = handle.synthesis()
end = time.time()
handle.save_img()
print('Execution time:', (end - start) , 'seconds')



fig,ax = plt.subplots(1,2)
ax[0].axis('off')
ax[0].imshow(input)
ax[0].set_title("original")
ax[1].axis('off')
ax[1].imshow(output)
ax[1].set_title("Synthesis_result")

plt.show()


# texture = io.imread(img)
# output = io.imread("results/synthesis/" + img_name + "_b=" + str(blocksize) + "_o=" + str(overlapsize) + "_t=" + str(tolerance).replace(".", "_") + ".png")
# io.imshow(texture)
# io.show()

# io.imshow(output)
# io.imshow()