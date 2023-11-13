"""
必要な物:
- MIDIファイルのパス
- MIDIを格納する本体
- BPM
- TICKS_PER_BEAT
- FPS
"""

import mido


class MidiTrack:
    def __init__(self, path, fix=False) -> None:
        self.path = path
        self.messages = []
        self.bpm = -1
        self.ticks_per_beat = -1
        self.fps = -1
        self.fix_midi_for_cakewalk = fix

    def set_bpm(self, bpm) -> None:
        self.bpm = bpm

    def set_tick_per_beat(self, ticks_per_beat) -> None:
        self.ticks_per_beat = ticks_per_beat

    def set_fps(self, fps) -> None:
        self.fps = fps

    def convert(self, focus_on=[]) -> None:
        # self.Messages を空にする

        self.messages.clear()

        #

        focus_all = (lambda focus_list: True if len(focus_list) == 0 else False)(
            focus_on
        )

        # midi読み込み
        midi_meta_raw = (mido.MidiFile(self.path)).tracks[0]
        midi_track_raw = (mido.MidiFile(self.path)).tracks[1]

        # read bpm

        # todo ソフランに対応してないので、V0.2で直す
        if self.bpm == -1:
            for i in range(len(midi_meta_raw)):
                if midi_meta_raw[i].type == "set_tempo":
                    self.bpm = midi_meta_raw[i].tempo
                    break

        # read ticks per beat
        if self.ticks_per_beat == -1:
            self.ticks_per_beat = (mido.MidiFile(self.path)).ticks_per_beat

        # fix for cakewalk bug

        if self.fix_midi_for_cakewalk == True:
            for i in range(len(midi_track_raw)):
                if midi_track_raw[i].type == "note_on":
                    if midi_track_raw[i].velocity == 0:
                        fix_note = midi_track_raw[i].note
                        fix_time = midi_track_raw[i].time
                        midi_track_raw[i] = mido.Message(
                            "note_off", note=fix_note, time=fix_time
                        )

        # work on the data

        accumulate_ticks = 0

        for i in range(len(midi_track_raw)):
            if midi_track_raw[i].type in focus_on or focus_all:
                if midi_track_raw[i].type in ["note_on", "note_off"]:
                    # ## note_on/off
                    self.messages.append(
                        {
                            "type": midi_track_raw[i].type,
                            "note": midi_track_raw[i].note,
                            "velocity": midi_track_raw[i].velocity,
                            "frame": accumulate_ticks
                            * 60
                            * self.fps
                            // (self.bpm * self.ticks_per_beat),
                        }
                    )
                elif midi_track_raw[i].type in ["control_change"]:
                    # ## control change
                    self.messages.append(
                        {
                            "type": midi_track_raw[i].type,
                            "control": midi_track_raw[i].control,
                            "value": midi_track_raw[i].value,
                            "frame": accumulate_ticks
                            * 60
                            * self.fps
                            // (self.bpm * self.ticks_per_beat),
                        }
                    )
                else:
                    # ## else
                    self.messages.append(
                        {
                            "type": "else",
                            "frame": accumulate_ticks
                            * 60
                            * self.fps
                            // (self.bpm * self.ticks_per_beat),
                        }
                    )
            accumulate_ticks += midi_track_raw[i].time
