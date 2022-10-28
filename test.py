from audioop import tostereo
from email import message
from email.mime import audio
from src.VBS.decoding.response import Response
from src.VBS.key import Key
from src.VBS.encoding.send import Send
import os
import numpy as np
from matplotlib import pyplot as plt
import pydub as pd
import cv2

# # receive messages
# mymessage2 = Received(files_path='./audio')

# instatiate Key
# key = Key(files_path=['./audio/HeartlessBastards.mp3'])

# # add messages if different sources
# mymessage3 = mymessage1 + mymessage2

# # Create response object by stracting key from message
# res = mymessage3 - key

# # plot results (list of matrixes with possible images)
# res.plot_from_leftChannel(6)

####################### make the inverse process #############################

# resp = Send(images_path=['./image/balsa3.jpg','./image/Template-Needs.png', './image/LogoName.jpg', './image/balsa3.jpg'])
# # key = Key(files_path=['./audio/HeartlessBastards.mp3'])
# resp = Send(images_path=['./image/Template-Needs.png', './image/LogoName.jpg'])

# # print(resp.message_left.shape)
# # print(resp.message_right.shape)
# # print(key.message_left.shape)
# # print(key.message_right.shape)

# # toSend = resp + key

# # toSend.add_sep_and_div()
# mp3_path = resp.create_mp3_file(path='./audio/message_toSend.mp3', sample_width=1)
# mp3_path = key.create_mp3_file(path='./audio/key_toSend.mp3', sample_width=1)

#received = Received(files_path=['./audio/audio_toSend.mp3'])

# message = received - key

# mp3_path = message.create_mp3_file(path='./audio/message_received.mp3')

# print(resp.message_left)
# print(resp.message_right)
# print(key.message_left.shape)
# print(key.message_right.shape)





########################################################################

# # codify
# resp = Send(images_path=['./image/1.png.jpg', './image/2.png.jpg', './image/3.png.jpg', './image/4.png.jpg', './image/5.png.jpg', './image/6.png.jpeg', './image/7.png.jpg', './image/8.png.jpg'])
# resp = Send(images_path=['./image/circle.png'])
# mp3_path = resp.create_mp3_file(path='./audio/circle.mp3', sample_width=1, channels=1)

# mp3 = pd.AudioSegment.from_mp3('./audio/message_toSend.mp3')
# left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
# print(len(np.array(left.get_array_of_samples())))
# left = np.split(np.array(left.get_array_of_samples()[:-81]), 386)
# right = np.split(np.array(right.get_array_of_samples()[:-81]), 386)

# plt.imshow(left, cmap = 'Greys', interpolation='nearest')
# plt.show()

# # # decode
# message = Response(files_path=['./audio/message_toSend.mp3'])
# # message.plot_from_leftChannel(0)
# message.save_all('./image/')

# # # message = Response(files_path=['./audio/circle.mp3'])
# # # message.save_all('./image/')

# # # # use openCV to read the images
# # # import cv2
# # # r_np = cv2.imread('./image/decoded/right/0.png', cv2.IMREAD_GRAYSCALE)
# # # g_np = cv2.imread('./image/decoded/right/1.png', cv2.IMREAD_GRAYSCALE)
# # # b_np = cv2.imread('./image/decoded/right/2.png', cv2.IMREAD_GRAYSCALE)

# # # # # Add the channels to the final image
# # # # final_img = np.dstack([b_np, g_np, r_np]).astype(np.uint8)

# # # # # Save the needed multi channel image
# # # # cv2.imwrite('./image/decoded/img.png', final_img)


# # # # #######################################################################

# # list of 10 images of interest

# images = ['./pp/imgs/0.png', './pp/imgs/5.jpg', './pp/imgs/1.png',  './pp/imgs/6.jpg', './pp/imgs/2.png', './pp/imgs/7.jpg', './pp/imgs/3.jpg', './pp/imgs/8.jpg', './pp/imgs/4.jpg' , './pp/imgs/9.jpg']

# # for images 2-10 we make a greyscale image

# if not os.path.exists('./pp/imgs/grey'):
#     os.mkdir('./pp/imgs/grey')

# for i in range(0, 9):
#     img = cv2.imread(images[i], cv2.IMREAD_GRAYSCALE)
#     cv2.imwrite('./pp/imgs/grey/'+str(i)+'.png', img)
#     images[i] = './pp/imgs/grey/'+str(i)+'.png'

# # we now create the message to be sent

# resp = Send(images_path=images)

# # we now create the mp3 file

# if not os.path.exists('./pp/audio'):
#     os.mkdir('./pp/audio')

audio_path = './pp/audio/coded_message.mp3'

# mp3_path = resp.create_mp3_file(path=audio_path, sample_width=1, channels=1)

# we now test the decoding of the message

message = Response(files_path=[audio_path])

# we now save the images

if not os.path.exists('./pp/decoded'):
    os.mkdir('./pp/decoded/')

message.save_all('./pp/decoded/')

message.create_colored_image('./pp/decoded/9.png', './pp/decoded/10.png', './pp/decoded/11.png', './pp/decoded/img.png')

#########################################################################

# upload image

# from PIL import Image

# file = './image/1.png.jpg'
# image = Image.open(file)
# image = image.resize((512, 384), Image.ANTIALIAS)
# image.save(f'{file[:-4]}_resized.png')
# image = Image.open(f'{file[:-4]}_resized.png')
# print(image.size)
# arr = np.array(image) 
# scale = np.frompyfunc(lambda x, xmax, xmin: ((x-xmin)*100/(xmax-xmin))-50, 3, 1)
# # check if image is in grayscale
# if len(arr.shape) == 3:
#     print('color')
#     arr_r = arr[:, :, 2].flatten()
#     arr_r = scale(arr_r, 255, 0)
#     arr_g = arr[:, :, 1].flatten()
#     arr_g = scale(arr_g, 255, 0)
#     arr_b = arr[:, :, 0].flatten()      
#     arr_b = scale(arr_b, 255, 0)
#     arr = np.dstack([arr_r, arr_g, arr_b]).astype(np.uint8)
# else:
#     print('grayscale')
#     arr = arr.flatten()
#     arr = scale(arr, 255, 0)

# plt.imshow(arr, cmap = ', interpolation='nearest')
# plt.show()




