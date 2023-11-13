# 開発環境のみ
import sys

sys.dont_write_bytecode = True
import __init__ as bmidi

#

import mido

midi_1 = mido.MidiFile(R"C:\0_program\projects\bmidi\test_midi\test_format_1.mid")

midi_1_one_track = mido.merge_tracks(midi_1.tracks)

print(midi_1_one_track)

print("---")

test = bmidi.Score(
    name="test", filepath=R"C:\0_program\projects\bmidi\test_midi\test_format_1.mid"
)

for i in test.messages:
    print(i.__dict__)
