"""
1. 譜面データの保持
2. frameまわりのデータの保持
"""

# 使うかどうかはわからない
import mido
import bpy
from attribute_access import *

# todo refactoring

class Score:
    '''
    インスタンス変数
    - name              : str
    - filepath          : str
    - ignore            : list
    - read              : list
    - midi_format_type  : int
    - ticks_per_beat    : int
    - Message           : list
      - type            : str
      - else            :
    '''
    def __init__(
        self,
        name,
        filepath=None,
        ignore: None | list = None,
        read: None | list = None,
    ) -> bool:
        self.name: str = name
        self.filepath: str = filepath
        self.Message = type("Message", (), {})

        midi_file = mido.MidiFile(self.filepath)

        # # set read, ignore
        if read != None:
            ignore = None

        if read is None:
            read = []
        if ignore is None:
            ignore = []

        # # reject format 2
        if midi_file.type not in [0, 1]:
            print(f'At socre "{self.name}", midi file format is not 0 or 1.')
            return False

        # # read meta
        self.midi_format_type = midi_file.type
        self.ticks_per_beat = midi_file.ticks_per_beat

        # # merge tracks
        if self.midi_format_type == 1:
            midi_track = mido.merge_tracks(midi_file.tracks)
        if self.midi_format_type == 0:
            midi_track = midi_file.tracks

        # # read message
        self.messages = []
        accumulate_ticks = 0
        last_set_tempo = -1

        if ignore == None:

            def read_or_not(message_type):
                if (
                    (message_type in read)
                    or (message_type == "set_tempo")
                ):
                    return True
                else:
                    return False

        else:

            def read_or_not(message_type):
                if (message_type not in ignore) or (message_type == "set_tempo"):
                    return True
                else:
                    return False

        for mido_message in midi_track:
            if read_or_not(mido_message.type):
                new_message = self.Message()
                new_message.__dict__ = mido_message.__dict__
                # append
                self.messages.append(new_message)
                # tick
                setattr(new_message, "tick", accumulate_ticks)
                # delete time
                time = self.messages[-1].__dict__.pop("time", None)
                # いろいろとメッセージごとに処理する
                if new_message.type == "set_tempo":
                    if last_set_tempo == -1:
                        setattr(
                            new_message,
                            "second",
                            0.0,
                        )
                    else:
                        setattr(
                            new_message,
                            "second",
                            self.messages[last_set_tempo].second
                            + (self.messages[-1].tick - self.messages[last_set_tempo].tick)
                            * self.messages[last_set_tempo].tempo
                            / (self.ticks_per_beat * (10**6)),
                        )
                    last_set_tempo = len(self.messages) - 1
                # ---
                accumulate_ticks += time
            else:
                accumulate_ticks += mido_message.time

    def _(self):
        pass
