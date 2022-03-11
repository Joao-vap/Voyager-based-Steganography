import numpy as np
from src.SBS.imagemessage import ImageMessage as imagemessage
from src.SBS.key import Key as key

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
    
    def __repr__(self) -> str:
        """ Return string representation of message
               
        Returns:
            str: string representation of message
        """
        return (self.message_left.__repr__(), self.message_right.__repr__())

    def __sub__(self, other):
        """ Subtract two messages

        Args:
            other (ImageMessage): message to be subtracted
        """
        if isinstance(other, key):
            # if key is shorter than message
            if len(other) < len(self):
                # repeats key until it is the same length as message
                
                key = np.concatenate((np.tile(other.message_left, int(len(self)/len(other))), other.message_left[:len(self)%len(other)]), axis=None)
                self.message_left = self.message_left - key
                key = np.concatenate((np.tile(other.message_right, int(len(self)/len(other))), other.message_right[:len(self)%len(other)]), axis=None)
                self.message_right = self.message_right - key
                return key
            else:
                # we use a fraction of the key
                key = other.message_left[:len(self)]
                self.message_left = self.message_left - key
                key = other.message_right[:len(self)]
                self.message_right = self.message_right - key
                return key
        else:
            raise TypeError("unsupported operand type(s) for -: 'Sender' and '{}'".format(type(other)))
        
