from src.SBS.decoding.received import Received
from src.SBS.key import Key
from src.SBS.encoding.sender import Sender

# receive messages
mymessage1 = Received(files_path=['./audio/audio_1.mp3', './audio/audio_0.mp3'])
mymessage2 = Received(files_path='./audio')

# instatiate Key
key = Key(files_path=['./audio/audio_1.mp3'])

# add messages if different sources
mymessage3 = mymessage1 + mymessage2

# Create response object by stracting key from message
res = mymessage3 - key

# plot results (list of matrixes with possible images)
res.plot_from_leftChannel(6)

####################### make the inverse process #############################

resp = Sender(images_path=['./audio/audio_1.mp3'])