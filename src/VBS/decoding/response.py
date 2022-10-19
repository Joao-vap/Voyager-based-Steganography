from matplotlib import pyplot as plt
import numpy as np
from src.VBS.audiomessage import AudioMessage as audiomessage
from cv2 import imread, imwrite, IMREAD_GRAYSCALE
import os

class Response(audiomessage):

    """
    Class to represent a Response message
    which is a message subtrated a key.

    Attributes:
        message_left (np.array): left channel of message
        message_right (np.array): right channel of message
        maxMagnitude (int): max value of message
        medMagnitude (int): median value of message
        imageLength (int): length of image
        lineLength (int): length of line
        _partialimagees_left (np.array): left channel of partialimagees
        _partialimagees_right (np.array): right channel of partialimagees

    Methods:
        set_left_partialimage (bool): set partialimagees left channel
        set_rigth_partialimage (bool): set partialimagees right channel
        setpartialimagees (bool): set partialimagees
        __len__ (int): return length of message
        __getitem__ (np.array): return partialimage
        __setitem__ (bool): set partialimage
        __delitem__ (bool): delete partialimage
        __iter__ (np.array): return iterator of partialimagees
        __add__ (Response): add two messages
        __repr__ (str): return string representation of message
        plot_from_leftChannel (None): plot a partialimage from left channel
        plot_from_rigthChannel (None): plot a partialimage from right channel
        save_from_leftChannel (None): save a partialimage from left channel
        save_from_rigthChannel (None): save a partialimage from right channel
        save_all_from_leftChannel (None): save all partialimagees from left channel
        save_all_from_rigthChannel (None): save all partialimagees from right channel
        save_all (None): save all partialimagees
        create_colored_image (None): Creates colored image with 3 paths RGB

    """

    def __init__(self, files_path=None):
        self.setted = False
        self.maxMagnitude, self.medMagnitude = 0, 0
        self.imageLength, self.lineLength = 0, 0
        self._partialimagees_left = np.array([])
        self._partialimagees_right = np.array([])
        super().__init__(files_path)

    def set_left_partialimage(self) -> bool:

        '''
        Method to set partialimagees for left channel

        Returns:
            bool: True if partialimagees are setted
        '''

        # if theres no data, return True
        if self.message_left.size == 0:
            return True

        # search for max value (divisor of images) at beggining
        if self.maxMagnitude == 0:
            self.maxMagnitude = np.amax(self.message_left[:1500])
        
        # find next max zig zag peaks and repeat append of partialimage
        # until end of message
        ImageNumber = 0
        i = 0
        while len(self.message_left)-self.imageLength*ImageNumber >= self.imageLength:

            partialimage = np.array([], dtype='float')

            # search for first point of image line (end of zig zag)
            while abs(np.amax(self.message_left[i:i+10]) - self.maxMagnitude) < 3000:
                i += 8

            # look for medMagnitude
            if self.medMagnitude == 0:
                self.medMagnitude = np.amax(self.message_left[i:i+3000])
            
            j = np.argmax(self.message_left[i:i+3000]) + i

            if self.lineLength == 0:
                self.lineLength = j - i + 8

            #put lines in partialimage
            for _ in range(0, 384):
                partialimage = np.append(partialimage, self.message_left[i:i+self.lineLength])
                i = i + self.lineLength

            scale = np.frompyfunc(lambda x, xmax, xmin: ((x-xmin)*255/(xmax-xmin)), 3, 1)
            partialimage = np.array([scale(partialimage, np.amax(partialimage), np.min(partialimage))], dtype='float')
                
            partialimage = partialimage.reshape(384, self.lineLength)

            self.imageLength = 384*self.lineLength

            self._partialimagees_left = np.append(self._partialimagees_left, partialimage)

            ImageNumber += 1

        self._partialimagees_left = self._partialimagees_left.reshape((ImageNumber, 384, self.lineLength))

        return True
    
    def set_rigth_partialimage(self) -> bool:

        '''
        Method to set partialimagees for right channel

        Returns:
            bool: True if partialimagees are setted
        '''

        # if theres no data, return True
        if self.message_right.size == 0:
            return True

        # search for max value (divisor of images) at beggining
        if self.maxMagnitude == 0:
            self.maxMagnitude = np.amax(self.message_right[:1500])
        
        # find next max zig zag peaks and repeat append of partialimage
        # until end of message
        ImageNumber = 0
        i = 0
        while len(self.message_right)-self.imageLength*ImageNumber >= self.imageLength:

            partialimage = np.array([], dtype='float')

            # search for first point of image line (end of zig zag)
            while abs(np.amax(self.message_right[i:i+10]) - self.maxMagnitude) < 3000:
                i += 8

            # look for medMagnitude
            if self.medMagnitude == 0:
                self.medMagnitude = np.amax(self.message_right[i:i+3000])
            
            j = np.argmax(self.message_right[i:i+3000]) + i

            if self.lineLength == 0:
                self.lineLength = j - i + 8

            #put lines in partialimage
            for _ in range(0, 384):
                partialimage = np.append(partialimage, self.message_right[i:i+self.lineLength])
                i = i + self.lineLength

            scale = np.frompyfunc(lambda x, xmax, xmin: ((x-xmin)*255/(xmax-xmin)), 3, 1)
            partialimage = np.array([scale(partialimage, np.amax(partialimage), np.min(partialimage))], dtype='float')
                
            partialimage = partialimage.reshape(384, self.lineLength)

            self.imageLength = 384*self.lineLength

            self._partialimagees_right = np.append(self._partialimagees_right, partialimage)

            ImageNumber += 1

        self._partialimagees_right = self._partialimagees_right.reshape((ImageNumber, 384, self.lineLength))

        return True

    def setpartialimagees(self) -> bool:

        '''
        Method to set partialimagees for both channels

        Returns:
            bool: True if partialimagees are setted
        '''
        l = self.set_left_partialimage()
        r = self.set_rigth_partialimage()
        return r and l

    def __len__(self) -> int:
        """ Return the length of the message

        Returns:
            int: length of message
        """
        return self._partialimagees_left.shape[1]

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
    
    def plot_from_leftChannel(self, index) -> None:
        """ Plot a partialimage from the left channel

        Args:
            index (int): index of partialimage to plot
        """
        if not self.setted:
            self.setted = self.setpartialimagees()

        plt.imshow(self._partialimagees_left[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.show()

    def plot_from_rightChannel(self, index) -> None:
        """ Plot a partialimage from the right channel

        Args:
            index (int): index of partialimage to plot
        """
        if not self.setted:
            self.setted = self.setpartialimagees()

        # set aspect to 384/2048
        plt.imshow(self._partialimagees_right[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.show()
    
    def save_from_leftChannel(self, index, path) -> None:
        """ Save a partialimage from the left channel

        Args:
            index (int): index of partialimage to save
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
         
        plt.imshow(self._partialimagees_left[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.savefig(path + str(index) + '.png')
    
    def save_from_rightChannel(self, index, path) -> None:
        """ Save a partialimage from the right channel

        Args:
            index (int): index of partialimage to save
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
        
        plt.imshow(self._partialimagees_right[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.savefig(path + str(index) + '.png')
    
    def save_all_from_leftChannel(self, path) -> None:
        """ Save all matrices from the left channel

        Args:
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
         
        for i in range(len(self._partialimagees_left)):
            self.save_from_leftChannel(i, path)

    def save_all_from_rightChannel(self, path) -> None:
        """ Save all matrices from the right channel

        Args:
            path (str): path to save to
        """
        if not self.setted:
            self.setpartialimagees()
            self.setted = True
         
        for i in range(len(self._partialimagees_right)):
            self.save_from_rightChannel(i, path)

    def save_all(self, path) -> None:
        """ Save all matrices

        Args:
            path (str): path to save to
        """
        # check if 1 or 2 channels
        if self._partialimagees_right.shape[0] == 0:
            self.save_all_from_leftChannel(path)
        else:
            # create folder for both channels
            path_left = path + 'left/'
            path_right = path + 'right/'
            os.mkdir(path_left)
            os.mkdir(path_right)
            self.save_all_from_leftChannel(path_left)
            self.save_all_from_rightChannel(path_right)

    def create_colored_image(self, path1, path2, path3, final_path) -> None:
        """ Create a colored image from three grayscale images

        Args:
            path1 (str): path to first image
            path2 (str): path to second image
            path3 (str): path to third image
            final_path (str): path to save to
        """
        r_np = imread(path1, IMREAD_GRAYSCALE)
        g_np = imread(path2, IMREAD_GRAYSCALE)
        b_np = imread(path3, IMREAD_GRAYSCALE)

        # Add the channels to the final image
        img = np.dstack([b_np, g_np, r_np]).astype(np.uint8)

        # Save the needed multi channel image, without border and scale
        imwrite(final_path, img)