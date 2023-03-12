import subprocess
import matplotlib.pyplot as plt
import cv2

#variable
img = "Inputs/Texture/input_00.png"
blocksize = 100
overlapsize = 10
scale = 3
tolerance = 0.1
cmd = "python3 texture_Synthesis/main.py --synthesis -i "+ img + " -b "+ str(blocksize) + " -o " +str(overlapsize) + " -t "+str(tolerance)+ " -s " + str(scale) 
subprocess.Popen(cmd, shell=True)

input = cv2.imread(img)
output = cv2.imread("../results/synthesis/" + img + "_b=" + str(blocksize) + "_o=" + str(overlapsize) + "_t=" + str(tolerance).replace(".", "_") + ".png")

fig = plt.figure(figsize=(16, 9))
ax1,ax2 = fig.subplots(2)
ax1.imshow(input)
ax1.set_title("original")
ax1.axis('off')
ax2.imshow(output)
ax2.set_title("Synthesis_result")
plt.show
