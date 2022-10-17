import pydub as pd
import numpy as np
from src.VBS.imagemessage import ImageMessage as imagemessage
from src.VBS.key import Key as k

class Send(imagemessage):

    """
    Class for message to be sent, that is, the message
    that will be encoded in the audio file.

    Properties:
        message_left (np.ndarray): message from left channel
        message_right (np.ndarray): message from right channel

    Methods:
        __len__ (int): return the length of the message
        __add__ (Send): add two messages
        __repr__ (str): return string representation of message
    """

    def __init__(self, images_path=None):
        super().__init__(images_path)

    def __len__(self):
        """ Return the length of the message

        Returns:
            int: length of message
        """
        return self.message_left.shape[0]

    def __add__(self, other) -> 'Send':
        """ Add two messages

        Args:
            other (Send): message to be added

        Returns:
            Send: new message
        """
        if isinstance(other, Send):
            message = Send()
            message.message_left = np.concatenate([self.message_left, other.message_left])
            message.message_right = np.concatenate([self.message_right, other.message_right])
            return message

        if isinstance(other, k):
            if len(other) > len(self):
                message = Send()
                key = other.message_left
                message.message_left = imagemessage.sum_difsize_lists(self.message_left, key)
                key = other.message_right
                message.message_right = imagemessage.sum_difsize_lists(self.message_right, key)
                return message
            elif len(other) < len(self):
                #repeat the key until it is the same length as the message
                message = Send()
                key = np.concatenate((np.tile(other.message_left, int(len(self)/len(other))), other.message_left[:len(self)%len(other)]), axis=None)
                message.message_left = imagemessage.sum_difsize_lists(self.message_left, key)
                key = np.concatenate((np.tile(other.message_right, int(len(self)/len(other))), other.message_right[:len(self)%len(other)]), axis=None)
                message.message_right = imagemessage.sum_difsize_lists(self.message_right, key)
                return message   
        
        return Send()

    def __repr__(self) -> str:
        """ Return string representation of message
        
        Returns:
            str: string representation of message
        """
        return f'{self.message_left.__repr__()} ({len(self.message_left)}),  {self.message_right.__repr__()} ({len(self.message_right)})'

