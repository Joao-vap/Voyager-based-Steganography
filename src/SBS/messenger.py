import os
import numpy as np
import pydub as pd
from abc import ABC, abstractmethod

class Messenger(ABC):

    """ Abstract methods """

    def __init__(self, files_path=None):
        if files_path is None:
            self.message_left, self.message_right = np.array([]), np.array([])
        else:
            self.message_left, self.message_right = self._getMessage(files_path)

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

    def __len__(self) -> 'int':
        """ Return length of message

        Returns:
            int: left length of message
        """
        return self.message_left.shape[0]

    def __getitem__(self, key) -> 'list[int]':
        """ Return item at index

        Args:
            key (int): index

        Returns:
            int: item at index
        """
        return (self.message_left[key], self.message_right[key])

    def __iter__(self) -> 'list[np.ndarray]':
        """ Return iterator of message

        Returns:
            np.ndarray: iterator of message
        """
        return (self.message_left.__iter__(), self.message_right.__iter__())

    def __next__(self) -> int:
        """ Return next item in message

        Returns:
            int: next item in message
        """
        return (self.message_left.__next__(), self.message_right.__next__())

    def _getMessage(self, files_path) -> 'list[np.ndarray]':
        """ Return message from files

        Args:
            files_path (str): path of files

        Raises:
            TypeError: if files_path is not str or list

        Returns:
            list[np.ndarray]: message from files, left and right channel
        """
        # check if is string with path to directory
        # or list of files
        if isinstance(files_path, str):
            message_left, message_rigth = self._getMessageFromDirectory(files_path)
        elif isinstance(files_path, list):
            message_left, message_rigth = self._getMessageFromFiles(files_path)
        else:
            raise TypeError("files_path must be string or list")
        return self._concatenateMessages(message_left), self._concatenateMessages(message_rigth)

    def _getMessageFromDirectory(self, files_path) -> 'list[np.ndarray]':
        """ Return message from files in directory

        Args:
            files_path (str): path of files

        Returns:
            list[np.ndarray]: message from files
        """
        # get all mp3 files in directory
        files = self._getFilesinDirectory(files_path)
        # get all messages from mp3 files
        message_left, message_rigth = self._getMessageFromFiles(files)
        # concatenate all messages
        return message_left, message_rigth
    
    def _getFilesinDirectory(self, files_path) -> list:
        """ Return files in directory

        Args:
            files_path (str): path of files

        Returns:
            list: files in directory
        """
        # get all mp3 files in directory
        files = []
        for file in os.listdir(files_path):
            # add paths of files to list
            files.append(files_path + '/' + file)
        return files
    
    @abstractmethod
    def _getMessageFromFiles(self, files) -> list:
        """ Return message from files
        
        Args:
            files (list): list of files

        Returns:
            list: message from files
        """
        pass
    
    @abstractmethod
    def _getMessageFromFile(self, file) -> np.ndarray:
        pass

    def _concatenateMessages(self, messages) -> np.ndarray:
        """ Return concatenated message

        Args:
            messages (list): list of messages

        Returns:
            np.ndarray: concatenated message
        """
        # concatenate all messages
        if len(messages) == 0:
            return np.array([])
        else:
            return np.concatenate(messages)
    
    def sum_difsize_lists(list1, list2):
        """ Return sum of two lists with different size
        
        Args:
            list1 (list): list 1
            list2 (list): list 2
        
        Returns:
            list: sum of two lists
        """
        # get size of list 1
        size1 = len(list1)
        # get size of list 2
        size2 = len(list2)
        # set maxlist
        if size1 > size2:
            listmax = list1
        else:
            listmax = list2
        # get size of bigger list
        size = min(size1, size2)
        # get sum of two lists
        sum_list = [list1[i] + list2[i] for i in range(size)]
        for i in range(size, len(listmax)):
            sum_list.append(listmax[i])
        return sum_list

    def create_mp3_file(self, path, sample_width=1, sr=44100) -> str:
        """ Create mp3 file from message

        Args:
            path (str): path to save mp3 file
            sr (int): sampling rate
        """
        x = np.array([self.message_left,self.message_right])
        print(x)
        channels = 2 if (x.ndim == 2 and x.shape[0] == 2) else 1
        song = pd.AudioSegment(np.int16(x), frame_rate=sr, sample_width=sample_width, channels=channels)
        song.export(path, format="mp3", bitrate="320k")