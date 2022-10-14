from turtle import shape
from matplotlib import pyplot as plt
import numpy as np
from src.SBS.audiomessage import AudioMessage as audiomessage

class Response(audiomessage):

    """
    Class to represent a Response message
    which is a message subtrated a key.
    """

    def __init__(self, files_path=None):
        self.setted = False
        self.n_max, self.n_med = 0, 0
        self.max_dist, self.med_dist = 0, 0
        self._matrixes_left = np.array([])
        self._matrixes_right = np.array([])
        super().__init__(files_path)

    # @property
    # def matrixes_left(self):
    #     return self._matrixes_left

    # @matrixes_left.setter
    def set_left_matrix(self):
        # search for max value (divisor of images) at beggining
        if self.n_max == 0:
            self.n_max = np.amax(self.message_left[:1500])
        
        # find next max zig zag peaks and repeat append of matrix
        # until end of message
        times = 0
        while len(self.message_left)-self.max_dist*times > self.max_dist:

            matrix = np.array([])

            print(times, self.max_dist, self.med_dist, self.n_med, self.n_max, len(self.message_left)-self.max_dist*times, 'beggin')

            # searh for end of zig-zag pattern in image divider
            ind_max = np.argmax(self.message_left[:1500])
            # search for first point of image line (end of zig zag)
            i = ind_max
            
            while abs(np.amax(self.message_left[i:i+10]) % self.n_max) < 0.1:
                i += 10

            # look for n_med
            if self.n_med == 0:
                self.n_med = np.amax(self.message_left[i:i+3000])
                j = np.argmax(self.message_left[i:i+3000])

            if self.med_dist == 0:
                self.med_dist = j - i

            #put lines in matrix
            for _ in range(0, 384):
                matrix = np.append(matrix, self.message_left[i:i+self.med_dist])
                i = i + self.med_dist

            print(self._matrixes_left.shape)
            print(matrix.shape)
                
            matrix = matrix.reshape(384, self.med_dist)

            self.max_dist = 384*self.med_dist

            self._matrixes_left = np.append(self._matrixes_left, matrix)

            print(times, self.max_dist, self.med_dist, self.n_med, self.n_max, len(self.message_left)-self.max_dist*times)
            print()

            times += 1
        
        self._matrixes_left = self._matrixes_left.reshape((times, 384, self.med_dist))

        return True
    
    # @property
    # def matrixes_right(self):
    #     return self._matrixes_right

    # @matrixes_right.setter
    def set_rigth_matrix(self):
        # search for max value (divisor of images) at beggining
        if self.n_max == 0:
            self.n_max = np.amax(self.message_right[:1500])
        
        # find next max zig zag peaks and repeat append of matrix
        # until end of message
        times = 0
        while len(self.message_right)-self.max_dist*times > self.max_dist:

            matrix = np.array([])

            print(times, self.max_dist, self.med_dist, self.n_med, self.n_max, len(self.message_right)-self.max_dist*times, 'beggin')

            # searh for end of zig-zag pattern in image divider
            ind_max = np.argmax(self.message_right[:1500])
            # search for first point of image line (end of zig zag)
            i = ind_max
            
            while abs(np.amax(self.message_right[i:i+10]) % self.n_max) < 0.1:
                i += 10

            # look for n_med
            if self.n_med == 0:
                self.n_med = np.amax(self.message_right[i:i+3000])
                j = np.argmax(self.message_right[i:i+3000])

            if self.med_dist == 0:
                self.med_dist = j - i

            #put lines in matrix
            for _ in range(0, 384):
                matrix = np.append(matrix, self.message_right[i:i+self.med_dist])
                i = i + self.med_dist

            print(self._matrixes_right.shape)
            print(matrix.shape)
                
            matrix = matrix.reshape(384, self.med_dist)

            print(matrix)
            print(self._matrixes_right)

            self.max_dist = 384*self.med_dist

            self._matrixes_right = np.append(self._matrixes_right, matrix)

            print(times, self.max_dist, self.med_dist, self.n_med, self.n_max, len(self.message_right)-self.max_dist*times)
            print()

            times += 1

        self._matrixes_right = self._matrixes_right.reshape((times, 384, self.med_dist))

        return True

    def setmatrixes(self):
        r = self.set_rigth_matrix()
        l = self.set_left_matrix()
        return r and l

    def __len__(self):
        """ Return the length of the message

        Returns:
            int: length of message
        """
        return self._matrixes_left.shape[1]

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
        if not self.setted:
            self.setted = self.setmatrixes()

        plt.imshow(self._matrixes_left[index], cmap='gray', interpolation='nearest')
        plt.show()

    def plot_from_rightChannel(self, index):
        """ Plot a matrix from the right channel

        Args:
            index (int): index of matrix to plot
        """
        if not self.setted:
            self.setted = self.setmatrixes()

        plt.imshow(self._matrixes_right[index], cmap='gray', interpolation='nearest')
        plt.show()
    
    def save_from_leftChannel(self, index, filename):
        """ Save a matrix from the left channel

        Args:
            index (int): index of matrix to save
            filename (str): filename to save to
        """
        if not self.setted:
            self.setted = self.setmatrixes()
         
        plt.imshow(self._matrixes_left[index], cmap='gray', interpolation='nearest', aspect='auto')
        plt.savefig(filename)
    
    def save_from_rightChannel(self, index, filename):
        """ Save a matrix from the right channel

        Args:
            index (int): index of matrix to save
            filename (str): filename to save to
        """
        if not self.setted:
            self.setted = self.setmatrixes()
        
        plt.imshow(self._matrixes_right[index], cmap='gray', interpolation='nearest', aspect='auto')
        plt.savefig(filename)
    
    def save_all_from_leftChannel(self, filename):
        """ Save all matrices from the left channel

        Args:
            filename (str): filename to save to
        """
        if not self.setted:
            self.setted = self.setmatrixes()
         
        for i in range(len(self._matrixes_left)):
            self.save_from_leftChannel(i, filename + str(i) + '.png')

    def save_all_from_rightChannel(self, filename):
        """ Save all matrices from the right channel

        Args:
            filename (str): filename to save to
        """
        if not self.setted:
            self.setmatrixes()
            self.setted = True
         
        for i in range(len(self._matrixes_right)):
            self.save_from_rightChannel(i, filename + str(i) + '.png')

    
    