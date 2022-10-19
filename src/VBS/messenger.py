import os
import numpy as np
import pydub as pd
from abc import ABC, abstractmethod

class Messenger(ABC):

    """
    Base class for all messengers, audio or image
    
    Attributes:
        message_left (np.ndarray): message from left channel
        message_right (np.ndarray): message from right channel    
        
    Methods:
        __init__(self, files_path=None)
            Initialize class
        __len__(self) -> 'int'
            Return length of message
        __getitem__(self, key) -> 'list[int]'
            Return item at index
        __iter__(self) -> 'list[np.ndarray]'
            Return iterator of message
        __next__(self) -> int
            Return next item in message
        _getMessage(self, files_path) -> 'list[np.ndarray]'
            Return message from files
        _getMessageFromDirectory(self, files_path) -> 'list[np.ndarray]'
            Return message from files in directory
        _getFilesinDirectory(self, files_path) -> list
            Return files in directory
        _concatenateMessages(self, messages) -> np.ndarray
            Return concatenated message
        create_mp3_file(self) -> string
            Return path of MP3 file generated
    
    """

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

    def create_mp3_file(self, path, sample_width=1, fr=44100, channels = 2) -> str:
        """ Create mp3 file from message

        Args:
            path (str): path to save mp3 file
            sr (int): sampling rate
        """
        # if len(self.message_left) > len(self.message_right):
        #     diff = len(self.message_left) - len(self.message_right)
        #     self.message_right = np.concatenate([self.message_right, np.zeros(diff)])

        if channels == 2:
            left = pd.AudioSegment(self.message_left.astype(np.int32).tobytes(), frame_rate=fr, sample_width=sample_width, channels = 1)
            right = pd.AudioSegment(self.message_right.astype(np.int32).tobytes(), frame_rate=fr, sample_width=sample_width, channels = 1)
            song = pd.AudioSegment.from_mono_audiosegments(left, right)
        else:
            x = np.concatenate([self.message_left, self.message_right])
            song = pd.AudioSegment(x.astype(np.int32).tobytes(), frame_rate=fr, sample_width=sample_width, channels=channels)
        
        # song = pd.AudioSegment(np.int16(x), frame_rate=fr, sample_width=sample_width, channels=channels)
        song.export(path, format="mp3", bitrate="320k")
        return path