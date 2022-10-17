import numpy as np
import pydub as pd
from src.VBS.messenger import Messenger as messenger
from abc import ABC, abstractmethod
from PIL import Image

class ImageMessage(messenger, ABC):

    """ Base class for image message
    
    Args:
        messenger (ABC): abstract class for message

    Properties:
        image_divider (np.ndarray): divider for message
        line_separator (np.ndarray): separator for message
        message_left (np.ndarray): message from left channel
        message_right (np.ndarray): message from right channel

    Methods:
        _make_divider (np.ndarray): return divider for message
        _make_separator (np.ndarray): return separator for message
        _getMessageFromFiles (list): return message from image files
        _getMessageFromFile (np.ndarray): return message from image file

    """

    def __init__(self, images_path=None):
        self.image_divider = self._make_divider()
        self.line_separator = self._make_separator()
        super().__init__(images_path)

    def _make_divider(self) -> np.ndarray:
        """ Return divider for message,
        this is inspired in voyager divider and
        consists in an zig-zag pattern
        """
        divider = np.array([])
        for i in range(0, 512):
            if i % 2 == 0:
                divider = np.append(divider, 100)
            else:
                divider = np.append(divider, -100)
        return divider
    
    def _make_separator(self) -> np.ndarray:
        """ Return message with line separator that is
        a peak and a fall
        """
        separator = np.array([])
        separator = np.append(separator, 75)
        separator = np.append(separator, -75)
        return separator
        
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

    def _getMessageFromFiles(self, files) -> list:
        """ Return message from image files,
        divide calls beetween left and right

        Args:
            files (list): paths of image files

        Returns:
            list: messages from image files
        """
        message_left, message_right = [], []
        qtdLeft, qtdRight = 0, 0
        for index in range(len(files)):
            if qtdLeft <= qtdRight:
                message_to_add, qtdaux = self._getMessageFromFile(files[index])
                message_left.append(message_to_add)
                qtdLeft += qtdaux
            else:
                message_to_add, qtdaux = self._getMessageFromFile(files[index])
                message_right.append(message_to_add)
                qtdRight += qtdaux

        return [message_left, message_right]
    
    def _getMessageFromFile(self, file) -> np.ndarray:
        """ Return message from image file. This method
        is responsible for convert image to message for 
        both rgb and grayscale images.

        Args:
            file (str): path of image file

        Returns:
            np.ndarray: message from image file
        """
        image = Image.open(file)
        image = image.resize((512, 384), Image.ANTIALIAS)
        image.save(f'{file[:-4]}_resized.png')
        image = Image.open(f'{file[:-4]}_resized.png')
        arr = np.array(image) 
        scale = np.frompyfunc(lambda x, xmax, xmin: ((x-xmin)*100/(xmax-xmin))-50, 3, 1)
        # check if image is in grayscale
        if len(arr.shape) == 3:
            arr_r = arr[:, :, 0].flatten()
            arr_r = scale(arr_r, 255, 0)
            arr_g = arr[:, :, 1].flatten()
            arr_g = scale(arr_g, 255, 0)
            arr_b = arr[:, :, 2].flatten()      
            arr_b = scale(arr_b, 255, 0)
            # put line separator every 512 points in each of arrays
            for i in range(0, 384):
                ind = (i+1)*512+(i)*2
                arr_r = np.concatenate([arr_r[0:ind],self.line_separator,arr_r[ind:(384*512)+i*2]])
                arr_g = np.concatenate([arr_g[0:ind],self.line_separator,arr_g[ind:(384*512)+i*2]])
                arr_b = np.concatenate([arr_b[0:ind],self.line_separator,arr_b[ind:(384*512)+i*2]])

            return np.concatenate([
            self.image_divider, np.array(arr_r),
            self.image_divider, np.array(arr_g),
            self.image_divider, np.array(arr_b)
            ]), 3
        else:
            arr = arr.flatten()
            arr = scale(arr, 255, 0)
            # put line separator every 512 points in array
            for i in range(0, 384):
                ind = (i+1)*512+(i)*2
                arr = np.concatenate([arr[0:ind],self.line_separator,arr[ind:(384*512)+i*2]])
            return np.concatenate([self.image_divider, np.array(arr)]), 1
