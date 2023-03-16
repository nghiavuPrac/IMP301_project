import time
import matplotlib.pyplot as plt
import cv2
import multiprocessing
import texture_Synthesis.main as np_main 
import texture_Synthesis_Cupy.main as torch_main
#variable



img = "Inputs/Texture/t4.jpg"
blocksize = 50
overlapsize = 5
scale = 2
tolerance = 0.1

input  = cv2.imread(img)

# img_name = img.split("/")[-1].split(".")[0]
# input = cv2.imread(img)
# output = cv2.imread("results/synthesis/" + img_name + "_b=" + str(blocksize) + "_o=" + str(overlapsize) + "_t=" + str(tolerance).replace(".", "_") + ".png")

def torch_process():
    start = time.time()
    handle = torch_main.texture_handler(img,blocksize,overlapsize,scale,tolerance)
    output = handle.synthesis()
    end = time.time()
    handle.save_img()
    print(f'torch finished in {round(end-start, 2)} second(s)')
    # fig,ax = plt.subplots(1,2)
    # ax[0].axis('off')
    # ax[0].imshow(input)
    # ax[0].set_title("original")
    # ax[1].axis('off')
    # ax[1].imshow(output)
    # ax[1].set_title("Synthesis_result")
    # plt.show()




def np_process():
    start = time.time()
    handle = np_main.texture_handler(img,blocksize,overlapsize,scale,tolerance)
    output = handle.synthesis()
    end = time.time()
    handle.save_img()
    print(f'numpy finished in {round(end-start, 2)} second(s)')

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    #plt.rcParams["figure.autolayout"] = True
    fig,ax = plt.subplots(1,2)
    #ax[0].axis('off')
    ax[0].imshow(input)
    ax[0].set_title("original")
    ax[0].set_xlim(output.shape[0])
    ax[0].set_xlim(output.shape[1])
    #ax[1].axis('off')
    ax[1].imshow(output)
    ax[1].set_title("Synthesis_result")
    ax[1].set_xlim(output.shape[0])
    ax[1].set_xlim(output.shape[1])
    plt.show()

process1 = multiprocessing.Process(target= np_process)
#process2 = multiprocessing.Process(target = torch_process)

process1.start()
#process2.start()
process1.join()
#process2.join()
