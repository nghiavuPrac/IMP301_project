from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse
from texture_Synthesis import textureSynthesis
#import textureTransfer
import sys


class texture_handler():
    def __init__(self,img, block_size, overlap, scale, tolerance):
        self.img = img
        self.block_size = block_size
        self.overlap = overlap

        # self.block_size = self.img.shape[0]-10
        # self.overlap = self.block_size // 3

        self.scale = scale
        self.tolerance = tolerance


    # def LoadImage(self,infilename) :
    #     img = Image.open(infilename).convert('RGB')
    #     data = np.asarray(img)
    #     return data

    # def getMask(img_path, threshold):
    #     img_bw = Image.open(img_path).convert('LA').split()[0]
    #     mask = np.asarray(img_bw) > threshold
    #     return np.stack((mask, mask, mask), axis = 2)
    
    def show_result(input,output):
        fig = plt.figure(figsize=(16, 9))
        ax1,ax2 = fig.subplots(2)
        ax1.imshow(input)
        ax1.set_title("original")
        ax1.axis('off')
        ax2.imshow(output)
        ax2.set_title("Synthesis_result")
        plt.show()

    # def save_img(self):
    #     try:
    #         img_name = self.img_path.split("/")[-1].split(".")[0]
    #         img_to_save = Image.fromarray(self.new_img.astype('uint8'), 'RGB')
    #         img_to_save.save("results/synthesis/" + img_name + "_b=" + str(self.block_size) + "_o=" + str(self.overlap) + "_t=" + str(self.tolerance).replace(".", "_") + ".png")
    #     except Exception as e:
    #         print("Error: ", e)
    #         sys.exit(1)



    def synthesis(self):
        try:
            # Get the generated texture
            new_h, new_w = int(self.scale * self.img.shape[0]), int(self.scale * self.img.shape[1])
            # print(img.shape)
            self.new_img = textureSynthesis.Construct(self.img, [self.block_size, self.block_size], self.overlap, new_h, new_w, self.tolerance)
            #show_result(img,new_img)
            # Save generated image if required
        except Exception as e:
            print("Error: ", e)
            sys.exit(1)
        
        return Image.fromarray(self.new_img.astype('uint8'), 'RGB')

# def transfer(args):
#     try:
#         texture_img = LoadImage(args.texture_img_path)
#         target_img = LoadImage(args.target_img_path)

#         new_img = textureTransfer.Construct(texture_img, target_img, [args.block_size, args.block_size], args.overlap, args.alpha, args.tolerance)

#         # If threshold is set, generate a mask for the target object & use it
#         if args.threshold:
#             target_mask = getMask(args.target_img_path, args.threshold)
#             new_img = target_mask * new_img

#         # Save generated image if required
#         texture_img_name = args.texture_img_path.split("/")[-1].split(".")[0]
#         target_img_name = args.target_img_path.split("/")[-1].split(".")[0]
#         img_to_save = Image.fromarray(new_img.astype('uint8'), 'RGB')
#         img_to_save.save("../results/transfer/" + texture_img_name + "_" + target_img_name + "_b=" + str(args.block_size) + "_o=" + str(args.overlap) + "_a=" + str(args.alpha).replace(".", "_") + "_t=" + str(args.tolerance).replace(".", "_") + ".png")
#     except Exception as e:
#         print("Error: ", e)
#         sys.exit(1)

# def objectTextureTransfer(args):
#     try:
#         texture_img = LoadImage(args.texture_img_path)
#         target_img = LoadImage(args.target_img_path)
#         target_mask = getMask(args.target_img_path, args.threshold)

#         new_img = textureTransfer.Construct(texture_img, target_img, [args.block_size, args.block_size], args.overlap, args.alpha, args.tolerance)
#         new_img = mask * new_img
## Get parser arguments
parser = argparse.ArgumentParser()
parser.add_argument("--synthesis", action="store_true", help="perform synthesis")
#parser.add_argument("--transfer", action="store_true", help="perform transfer")
#parser.add_argument("--object_transfer", action="store_true", help="perform transfer on 2 objects")
parser.add_argument("-i", "--img_path", type=str, help="path of image you want to quilt")
#parser.add_argument("-i1", "--texture_img_path", type=str, help="path of texture image")
#parser.add_argument("-i2", "--target_img_path", type=str, help="path of target image")
parser.add_argument("-b", "--block_size", type=int, default=100, help="block size in pixels")
parser.add_argument("-o", "--overlap", type=int, default=20, help="overlap size in pixels")
parser.add_argument("-s", "--scale", type=float, default=2, help="scaling w.r.t. to input image")
parser.add_argument("-t", "--tolerance", type=float, default=0.1, help="tolerance fraction")
#parser.add_argument("-a", "--alpha", type=float, default=0.1, help="weightage of target image intensity error wrt texture boundary error")
#parser.add_argument("-T", "--threshold", type=int, help="threshold for object mask generation")

args = parser.parse_args()

if __name__ == "__main__":
    # if (args.synthesis and args.transfer): # or (args.synthesis and args.object_transfer) or (args.object_transfer and args.transfer) :
    #     print("Cannot perform synthesis & transfer simultaneously")
    #     sys.exit(1)
    # elif args.synthesis:
    textureSynthesis.synthesis(args)
    # elif args.transfer:
    #     transfer(args)
    # elif args.object_transfer:
    #     objectTextureTransfer(args)


