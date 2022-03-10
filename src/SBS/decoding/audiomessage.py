import os
import numpy as np
import pydub as pd
from abc import ABC, abstractmethod

class AudioMessage(ABC):

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
        # or list of mp3 files
        if isinstance(files_path, str):
            message_left, message_rigth = self._getMessageFromDirectory(files_path)
        elif isinstance(files_path, list):
            message_left, message_rigth = self._getMessageFromMp3s(files_path)
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
        mp3_files = self._getMp3FilesInDirectory(files_path)
        # get all messages from mp3 files
        message_left, message_rigth = self._getMessageFromMp3s(mp3_files)
        # concatenate all messages
        return message_left, message_rigth
    
    def _getMp3FilesInDirectory(self, files_path) -> list:
        """ Return mp3 files in directory

        Args:
            files_path (str): path of files

        Returns:
            list: mp3 files in directory
        """
        # get all mp3 files in directory
        mp3_files = []
        for file in os.listdir(files_path):
            # add paths of m3 files to list
            if file.endswith(".mp3"):
                mp3_files.append(files_path + '/' + file)
        return mp3_files
    
    def _getMessageFromMp3s(self, mp3_files) -> list:
        """ Return message from mp3 files
        
        Args:
            mp3_files (list): list of mp3 files

        Returns:
            list: message from mp3 files
        """
        # get all messages from mp3 files
        message_left, message_rigth = [], []
        for file in mp3_files:
            message_l, message_r = self._getMessageFromMp3(file)
            message_left.append(message_l)
            message_rigth.append(message_r)
        return message_left, message_rigth
    
    def _getMessageFromMp3(self, file) -> np.ndarray:
        """ Return message from mp3 file

        Args:
            file (str): path of mp3 file

        Returns:
            np.ndarray: message from mp3 file
        """
        # get message from mp3 file
        mp3 = pd.AudioSegment.from_mp3(f"{file}")
        left, right = mp3.split_to_mono()[0], mp3.split_to_mono()[1]
        return np.array(left.get_array_of_samples()), np.array(right.get_array_of_samples())

    def _concatenateMessages(self, messages) -> np.ndarray:
        """ Return concatenated message

        Args:
            messages (list): list of messages

        Returns:
            np.ndarray: concatenated message
        """
        # concatenate all messages
        return np.concatenate(messages)
        
