import numpy as np
import pydub as pd
from src.VBS.audiomessage import AudioMessage as audiomessage

class Key(audiomessage):

    def __init__(self, files_path=None):
        super().__init__(files_path)

    def __add__(self, other) -> 'Key':
        """ Add two messages

        Args:
            other: message to be added

        Returns:
            Key: new message
        """
        if isinstance(other, Key):
            message = Key()
            message.message_left = np.concatenate([self.message_left, other.message_left])
            message.message_right = np.concatenate([self.message_right, other.message_right])
            return message
    
    def __repr__(self) -> str:
        """ Return string representation of message
            
        Returns:
            str: string representation of message
        """
        return (self.message_left.__repr__(), self.message_right.__repr__())