from email import message
from tokenize import String
from matplotlib import pyplot as plt
import pydub as pd
import numpy as np
from src.SBS.imagemessage import ImageMessage as imagemessage
from src.SBS.key import Key as k

class Send(imagemessage):

    def __init__(self, images_path=None):
        super().__init__(images_path)
    
    @property
    def message_left(self):
        return self._message_left

    @message_left.setter
    def message_left(self, message_left):
        self._message_left = message_left[:len(message_left)//(512*384)*512*384] 

    @property
    def message_right(self):
        return self._message_right

    @message_right.setter
    def message_right(self, message_right):
        self._message_right = message_right[:len(message_right)//(512*384)*512*384]

    def __len__(self):
        """ Return the length of the message

        Returns:
            int: length of message
        """
        return self.message_left.shape[0]

    def __add__(self, other) -> 'Send':
        """ Add two messages

        Args:
            other (Send): message to be added

        Returns:
            Send: new message
        """
        if isinstance(other, Send):
            message = Send()
            message.message_left = np.concatenate([self.message_left, other.message_left])
            message.message_right = np.concatenate([self.message_right, other.message_right])
            return message

        if isinstance(other, k):
            if len(other) > len(self):
                message = Send()
                key = other.message_left
                message.message_left = imagemessage.sum_difsize_lists(self.message_left, key)
                key = other.message_right
                message.message_right = imagemessage.sum_difsize_lists(self.message_right, key)
                return message
            elif len(other) < len(self):
                #repeat the key until it is the same length as the message
                message = Send()
                key = np.concatenate((np.tile(other.message_left, int(len(self)/len(other))), other.message_left[:len(self)%len(other)]), axis=None)
                message.message_left = imagemessage.sum_difsize_lists(self.message_left, key)
                key = np.concatenate((np.tile(other.message_right, int(len(self)/len(other))), other.message_right[:len(self)%len(other)]), axis=None)
                message.message_right = imagemessage.sum_difsize_lists(self.message_right, key)
                return message   
        
        return Send()

    def __repr__(self) -> str:
        """ Return string representation of message
        
        Returns:
            str: string representation of message
        """
        return f'{self.message_left.__repr__()} ({len(self.message_left)}),  {self.message_right.__repr__()} ({len(self.message_right)})'

    def add_sep_and_div(self):
        """ Add separator and divider to message
        """
        self._add_separator()
        self._add_divider()

    def _add_separator(self):
        """ Add separator to message (beetween lines)

        Args:
            divider (int): divider to add
        """
        aux_esq = []
        aux_dir = []
        for i in range(512, len(self.message_left), 512):
            aux_esq.append(imagemessage.sum_difsize_lists(self.message_left[i-512:i], self.line_separator))
        for i in range(512, len(self.message_right), 512):
            aux_dir.append(imagemessage.sum_difsize_lists(self.message_right[i-512:i], self.line_separator))
        self.message_left = np.concatenate(aux_esq)
        self.message_right = np.concatenate(aux_dir)

    def _add_divider(self):
        """ Add divider to message (beetween images)
        """
        # add divider inbeetween messages, every 384*(512+len(separator)) samples
        aux_esq = []
        aux_dir = []
        for i in range(512+len(self.line_separator), len(self.message_left), 512+len(self.line_separator)):
            aux_esq.append(imagemessage.sum_difsize_lists(self.message_left[i-512-len(self.line_separator):i], self.image_divider))
        for i in range(512+len(self.line_separator), len(self.message_right), 512+len(self.line_separator)):
            aux_dir.append(imagemessage.sum_difsize_lists(self.message_right[i-512-len(self.line_separator):i], self.image_divider))
        self.message_left = np.concatenate(aux_esq)
        self.message_right = np.concatenate(aux_dir)
