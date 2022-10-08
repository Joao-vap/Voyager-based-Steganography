import os
import numpy as np
import pydub as pd
from abc import ABC, abstractmethod
from src.SBS.messenger import Messenger as messenger

class AudioMessage(messenger, ABC):

    """ Abstract methods """

    def __init__(self, files_path=None):
        super().__init__(files_path)

    @abstractmethod    
    def __add__(self, other):
        """ Add two messages

        Args:
            other (AudioMessage): message to be added
        """
        pass

    @abstractmethod
    def __repr__(self):
        """ Return string representation of message
        """
        pass

    def _getMessageFromFiles(self, files) -> list:
        """
        Return message from mp3 files,
        divide calls beetween left and right

        Args:
            files (list): paths of mp3 files
        
        Returns:
            message left and right: list of messages
        """
        # get all messages from files
        message_left, message_rigth = [], []
        
        for file in files:
            message_l, message_r = self._getMessageFromFile(file)
            message_left.append(message_l)
            message_rigth.append(message_r)

        return [message_left, message_rigth]

    def _getMessageFromFile(self, file) -> list:
        """ Return message from mp3 file

        Args:
            file (str): path of mp3 file

        Returns:
            np.ndarray: message from mp3 file
        """
        # get message from mp3 file
        mp3 = pd.AudioSegment.from_mp3(f"{file}")
        left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
        left = np.array(left.get_array_of_samples())
        right = np.array(right.get_array_of_samples())
        return [left, right]