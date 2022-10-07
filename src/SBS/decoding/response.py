from matplotlib import pyplot as plt
import numpy as np
from src.SBS.audiomessage import AudioMessage as audiomessage

class Response(audiomessage):

    """
    Class to represent a Response message
    which is a message subtrated a key.
    """

    def __init__(self, files_path=None):
        super().__init__(files_path)
    
    @property
    def message_left(self):
        return self._message_left

    @message_left.setter
    def message_left(self, message_left):
        self._message_left = message_left[:len(message_left)//(512*384)*512*384]
        self._matrixes_left = self._message_left.reshape(len(self._message_left)//(512*384), 512, 384)

    @property
    def message_right(self):
        return self._message_right

    @message_right.setter
    def message_right(self, message_right):
        self._message_right = message_right[:len(message_right)//(512*384)*512*384]
        self._matrixes_right = self._message_right.reshape(len(self._message_right)//(512*384), 512, 384)

    @property
    def matrixes_left(self):
        return self._matrixes_left
    
    @property
    def matrixes_right(self):
        return self._matrixes_right

    def __len__(self):
        """ Return the length of the message

        Returns:
            int: length of message
        """
        return self.matrixes_left.shape[1]

    def __add__(self, other) -> 'Response':
        """ Add two messages

        Args:
            other (Response): message to be added

        Returns:
            Response: new message
        """
        if isinstance(other, Response):
            message = Response()
            message.message_left = np.concatenate([self.message_left, other.message_left])
            message.message_right = np.concatenate([self.message_right, other.message_right])
            return message

    def __repr__(self) -> str:
        """ Return string representation of message
        
        Returns:
            str: string representation of message
        """
        return (self.message_left.__repr__(), self.message_right.__repr__())
    
    def plot_from_leftChannel(self, index):
        """ Plot a matrix from the left channel

        Args:
            index (int): index of matrix to plot
        """
        plt.imshow(self.matrixes_left[index], cmap='gray', interpolation='nearest')
        plt.show()

    def plot_from_rightChannel(self, index):
        """ Plot a matrix from the right channel

        Args:
            index (int): index of matrix to plot
        """
        plt.imshow(self.matrixes_right[index], cmap='gray', interpolation='nearest')
        plt.show()
    
    def save_from_leftChannel(self, index, filename):
        """ Save a matrix from the left channel

        Args:
            index (int): index of matrix to save
            filename (str): filename to save to
        """
        plt.imshow(self.matrixes_left[index], cmap='gray', interpolation='nearest')
        plt.savefig(filename)
    
    def save_from_rightChannel(self, index, filename):
        """ Save a matrix from the right channel

        Args:
            index (int): index of matrix to save
            filename (str): filename to save to
        """
        plt.imshow(self.matrixes_right[index], cmap='gray', interpolation='nearest')
        plt.savefig(filename)
    
    def save_all_from_leftChannel(self, filename):
        """ Save all matrices from the left channel

        Args:
            filename (str): filename to save to
        """
        for i in range(len(self.matrixes_left)):
            self.save_from_leftChannel(i, filename + str(i) + '.png')

    def save_all_from_rightChannel(self, filename):
        """ Save all matrices from the right channel

        Args:
            filename (str): filename to save to
        """
        for i in range(len(self.matrixes_right)):
            self.save_from_rightChannel(i, filename + str(i) + '.png')

    
    