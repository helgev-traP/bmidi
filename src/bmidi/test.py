# 開発環境のみ
import sys
sys.dont_write_bytecode = True
import __init__

#

import mido

midi = mido.MidiFile(R"C:\0_program\projects\bmidi\test_midi\test.mid")

print(midi.tracks[0])
print(midi.tracks[1])
