from audioop import tostereo
from src.SBS.decoding.response import Response
from src.SBS.key import Key
from src.SBS.encoding.send import Send
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
# resp = Send(images_path=['./image/circle.png', './image/circle.png'])
# mp3_path = resp.create_mp3_file(path='./audio/message_toSend.mp3', sample_width=1)

mp3 = pd.AudioSegment.from_mp3('./audio/message_toSend.mp3')
left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
print(len(np.array(left.get_array_of_samples())))
left = np.split(np.array(left.get_array_of_samples()[:-81]), 386)
right = np.split(np.array(right.get_array_of_samples()[:-81]), 386)

plt.imshow(left, cmap = 'Greys', interpolation='nearest')
plt.show()

# # decode
# message = Response(files_path=['./audio/message_toSend.mp3'])
# # message.plot_from_leftChannel(1)
# message.plot_from_leftChannel(0)