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

set_tempoの値は四分音符の長さ(マイクロ秒)

```python
BPM = 6 * (10 ** 7) / set_tempo
```

```python
time = tick * set_tempo / (ticks_per_beat * 10 ** 6)
```

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
midoがなんか変な感じになってるので自分で構造体を作る

- Score
  - ticks_per_beat
  - list [Message]
    1. 基本的にMIDIをそのままコピーする
    2. 変更点は以下の通り
       - Message == BPMのときは現在の秒数を追加
       - ticksには累積のtick

### 構成

- Score
  - name
  - filepath
  - ticks_per_beat
  - message
    - type
    - value: dict

#### Messageについて

- message
  - type == time_signature
  - value: dict
    - numerator
    - denominator
    - clocks_per_click
    - notated_32nd_notes_per_beat
    - time

- message
  - type == key_signature
  - value: dict
    - key
    - time

- message
  - type == set_tempo
  - value: dict
    - tempo
    - time

- message
  - type == end_of_track
  - value
    - time

- message
  - type == track_name
  - value: dict
    - name
    - time

- message
  - type == note_on
  - value: dict
    - channel
    - note
    - velocity
    - time

- message
  - type == note_off
  - value: dict
    - channel
    - note
    - velocity // 通常は無視
    - tiem

- message
  - type == pitchwheel
  - value: dict
    - channel
    - pitch
    - time

- message
  - type == control_change
  - value: dict
    - channel
    - control
    - value
    - time
