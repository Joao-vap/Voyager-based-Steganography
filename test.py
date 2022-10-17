from audioop import tostereo
from src.VBS.decoding.response import Response
from src.VBS.key import Key
from src.VBS.encoding.send import Send
import os
import numpy as np
from matplotlib import pyplot as plt
import pydub as pd

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
resp = Send(images_path=['./image/1.png.jpg', './image/2.png.jpg', './image/3.png.jpg', './image/4.png.jpg', './image/5.png.jpg', './image/6.png.jpeg', './image/7.png.jpg', './image/8.png.jpg'])
mp3_path = resp.create_mp3_file(path='./audio/message_toSend.mp3', sample_width=1)

# mp3 = pd.AudioSegment.from_mp3('./audio/message_toSend.mp3')
# left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
# print(len(np.array(left.get_array_of_samples())))
# left = np.split(np.array(left.get_array_of_samples()[:-81]), 386)
# right = np.split(np.array(right.get_array_of_samples()[:-81]), 386)

# plt.imshow(left, cmap = 'Greys', interpolation='nearest')
# plt.show()

# # decode
message = Response(files_path=['./audio/message_toSend.mp3'])
# message.plot_from_leftChannel(0)
message.save_all_from_rightChannel(path='./image/decoded/right/')
message.save_all_from_leftChannel(path='./image/decoded/left/')

# use openCV to read the images
import cv2
r_np = cv2.imread('./image/decoded/right/0.png', cv2.IMREAD_GRAYSCALE)
g_np = cv2.imread('./image/decoded/right/1.png', cv2.IMREAD_GRAYSCALE)
b_np = cv2.imread('./image/decoded/right/2.png', cv2.IMREAD_GRAYSCALE)

# Add the channels to the final image
final_img = np.dstack([b_np, g_np, r_np]).astype(np.uint8)

# Save the needed multi channel image
cv2.imwrite('./image/decoded/img.png', final_img)