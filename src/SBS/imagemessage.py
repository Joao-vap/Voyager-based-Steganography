import os
import numpy as np
import pydub as pd
from src.SBS.messenger import Messenger as messenger
from abc import ABC, abstractmethod

class ImageMessage(messenger, ABC):

    """ Abstract methods """

    def __init__(self, images_path=None):
        super().__init__(images_path)

    @abstractmethod    
    def __add__(self, other):
        """ Add two messages

        Args:
            other (ImageMessage): message to be added
        """
        pass
    
    @abstractmethod
    def __repr__(self):
        """ Return string representation of message
        """
        pass
    
    def _getMessageFromFile(self, file) -> np.ndarray:
        """ Return message from mp3 file

        Args:
            file (str): path of mp3 file

        Returns:
            np.ndarray: message from mp3 file
        """
        # get message from mp3 file
        # mp3 = pd.AudioSegment.from_mp3(f"{file}")
        # left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
        left = np.array([])
        right = np.array([])
        return np.array(left.get_array_of_samples()), np.array(right.get_array_of_samples())

        
