import numpy as np
from src.VBS.encoding.send import Send
from src.VBS.imagemessage import ImageMessage as imagemessage
from src.VBS.key import Key as k

class Sender(imagemessage):
    
    def __init__(self, images_path=None):
        super().__init__(images_path)
    
    def __add__(self, other) -> 'Sender':
        """ Add two messages
    
        Args:
            other: message to be added
    
        Returns:
            Sender: new message
        """
        if isinstance(other, Sender):
            message = Sender()
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
    
    def __repr__(self) -> str:
        """ Return string representation of message
               
        Returns:
            str: string representation of message
        """
        return (self.message_left.__repr__(), self.message_right.__repr__())

            
