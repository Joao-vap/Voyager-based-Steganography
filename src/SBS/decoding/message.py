import numpy as np
from audiomessage import AudioMessage as audiomessage
from key import Key as k
from response import Response as response

class Message(audiomessage):
    
    def __init__(self, files_path=None):
        super().__init__(files_path)

    def __add__(self, other) -> 'Message':
        """ Add two messages

        Args:
            other (Message): message to be added

        Returns:
            Message: new message
        """
        if isinstance(other, Message):
            message = Message()
            message.message_left = np.concatenate([self.message_left, other.message_left])
            message.message_right = np.concatenate([self.message_right, other.message_right])
            return message

    def __sub__(self, other) -> response:
        """ Subtract key from message
        
        Args:
            other (Key): key to be subtracted

        Returns:
            response: response
        """
        if isinstance(other, k):
            res = response()
            # if key is shorter than message
            if len(other) < len(self):
                # repeats key until it is the same length as message
                key = np.concatenate((np.tile(other.message_left, int(len(self)/len(other))), other.message_left[:len(self)%len(other)]), axis=None)
                res.message_left = self.message_left - key
                key = np.concatenate((np.tile(other.message_right, int(len(self)/len(other))), other.message_right[:len(self)%len(other)]), axis=None)
                res.message_right = self.message_right - key
            else:
                # we use a fraction of the key
                key = other.message_left[:len(self)]
                res.message_left = self.message_left - key
                key = other.message_right[:len(self)]
                res.message_right = self.message_right - key

            print(res.message_left.shape)
            print(res.message_right.shape)
            return res

    def __repr__(self) -> str:
        """ Return string representation of message
            
        Returns:
            str: string representation of message
        """
        return (self.message_left.__repr__(), self.message_right.__repr__())
