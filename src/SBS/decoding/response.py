from matplotlib import pyplot as plt
import numpy as np
from src.SBS.audiomessage import AudioMessage as audiomessage
from cv2 import imread, imwrite, IMREAD_GRAYSCALE

class Response(audiomessage):

    """
    Class to represent a Response message
    which is a message subtrated a key.
    """

    def __init__(self, files_path=None):
        self.setted = False
        self.maxMagnitude, self.medMagnitude = 0, 0
        self.imageLength, self.lineLength = 0, 0
        self._partialimagees_left = np.array([])
        self._partialimagees_right = np.array([])
        super().__init__(files_path)

    def set_left_partialimage(self):

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
    
    def set_rigth_partialimage(self):

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

    def setpartialimagees(self):
        l = self.set_left_partialimage()
        r = self.set_rigth_partialimage()
        return r and l

    def __len__(self):
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
    
    def plot_from_leftChannel(self, index):
        """ Plot a partialimage from the left channel

        Args:
            index (int): index of partialimage to plot
        """
        if not self.setted:
            self.setted = self.setpartialimagees()

        plt.imshow(self._partialimagees_left[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.show()

    def plot_from_rightChannel(self, index):
        """ Plot a partialimage from the right channel

        Args:
            index (int): index of partialimage to plot
        """
        if not self.setted:
            self.setted = self.setpartialimagees()

        # set aspect to 384/2048
        plt.imshow(self._partialimagees_right[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.show()
    
    def save_from_leftChannel(self, index, path):
        """ Save a partialimage from the left channel

        Args:
            index (int): index of partialimage to save
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
         
        plt.imshow(self._partialimagees_left[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.savefig(path + str(index) + '.png')
    
    def save_from_rightChannel(self, index, path):
        """ Save a partialimage from the right channel

        Args:
            index (int): index of partialimage to save
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
        
        plt.imshow(self._partialimagees_right[index], cmap='gray', interpolation='bilinear', aspect='auto')
        plt.savefig(path + str(index) + '.png')
    
    def save_all_from_leftChannel(self, path):
        """ Save all matrices from the left channel

        Args:
            path (str): path to save to
        """
        if not self.setted:
            self.setted = self.setpartialimagees()
         
        for i in range(len(self._partialimagees_left)):
            self.save_from_leftChannel(i, path)

    def save_all_from_rightChannel(self, path):
        """ Save all matrices from the right channel

        Args:
            path (str): path to save to
        """
        if not self.setted:
            self.setpartialimagees()
            self.setted = True
         
        for i in range(len(self._partialimagees_right)):
            self.save_from_rightChannel(i, path)

    def create_colored_image(path1, path2, path3, final_path):
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
        final_img = np.dstack([b_np, g_np*2, r_np]).astype(np.uint8)

        # Save the needed multi channel image
        imwrite(final_path, final_img)