# Trailing Object

## Blender側のデータ構造

### オブジェクト

- object
  - <keyframe_insert>
  - location
    - 値
  - scale
    - 値
  - rotation_euler
    - 値

| keyframe insert to | data_path |
| the object         | "{path}"  |

### マテリアル

- object.data
  - materials["{マテリアル名}"]
    - node_tree
      - nodes["ノード名"]
        - inputs[{入力番号}]
          - <keyframe_insert>
          - default_value
            - 値

| keyframe insert to | data_path       |
| inputs[x]          | "default_value" |

### モディファイア

- object
  - modifiers["{モディファイア名}"]
    - <keyframe_insert>
    - {データ}
      - 値

| keyframe insert to | data_path |
| the modifier       | "{path}"  |

## CreateObject

keyframe_insert先を "base_entity" と呼ぶ

値の格納場所を "value_entity" と呼ぶ

data_path はそのまま呼ぶ

各タイプの違いはオブジェクト直下のメソッドで吸収出来れば吸収する

### データ構造

- CreateObject
  - __object
  - channels
    - type: ChannelObject
      - // このチャンネルはオブジェクトを作ったときに自動生成される
      - base_entity
      - value_entity
      - data_path
      - anchors
        - frame
        - value
    - type: ChannelMaterial
      - base_entity
      - value_entity = base_entity.default_value
      - data_path = default_value
      - anchors
        - frame
        - value
    - type: ChannelModifier
      - base_entity
      - value_entity
      - data_path
      - anchors
        - frame
        - value
  - matrix: dict
    - name(dict)
    - type
    - data_path
    - channel_object

### メソッド
