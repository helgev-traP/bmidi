# Score構造体

やるべきこと:

- Midiとは別に使いやすい譜面データを作る
  -

- MidiTrack()からMidiTrackを受け取る
- add_noteから新ノートを受け取る

## MIDI

### フォーマット

Cakewalkのデフォルト出力はフォーマット1
一般的に人間可読なフォーマット1が好まれる

### set_tempoについて



## midoの構造

### 外側

- track
  - filename
  - type ?
  - ticks_per_beat
  - charset ?
  - debug ?
  - clip ?
  - tracks
    - MidiTrack[0]
      - MetaMessageがたくさん
    - MidiTrack[1]
      - Messageがたくさん

### Metamessage

- set_tempo
  - tempo
  - time
- marker
  - text
  - time
- end_of_track
  - time=0

### Message

- note_on
  - channel
  - note
  - velocity
  - time
- note_off
  - channel
  - note
  - volocity 通常は無視
  - time
- control_change
  - channel
  - control
  - value
  - time

あとは気が向いたら追加する

## 譜面としてちゃんと持つ場合のデータ構造

- measures
  - measure
    - beats
    - time
    - message
      - bpms
        - beat
        - value
      - notes
        - beat
        - note
        - velocity
        - length

## add_noteをMIDIの構造に変換する場合のデータ構造

**これにしよう**

自分で構造体は用意する
MIDIと似た形で、MIDIに新しく情報を追加しながらDPで処理できるような構造にする

- Score
  - ticks_per_beat
  - list [Message]
    1. 基本的にMIDIをそのままコピーする
    2. 変更点は以下の通り
       - Message == BPMのときは現在の秒数を追加
       - ticksには累積のtick

