'''
1. 譜面データの保持
2. frameまわりのデータの保持
'''

# 使うかどうかはわからない
import mido
import bpy
from attribute_access import *


class Score:
    class Message:
        def __init__(self) -> None:
            self.type

    def __init__(self) -> None:
        self.ticks_per_beat
        self.message: list
