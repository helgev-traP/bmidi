# bmidi

BlenderでMIDIとアニメーションを楽に扱えるようにするためのライブラリ。

フレーム移動してプロパティの値変えてキーフレームを差し込んで、、、、、、の作業をラッピングして自動化している。

MIDIも扱える。

## Blenderで使えるようにするには

BlenderのPythonはBlenderで専用のものを持ってる。(中身は```bpy```とか```numpy```とかがデフォルトで入ってる以外普通のPythonと同じだったはず)

BlenderのPythonが入ってるフォルダに行く。

普通は```C:\Program Files\Blender Foundation\Blender 3.x\3.x\python\bin```みたいなところにある。

そこで、

```
./python.exe -m pip install {bmidiのsetup.pyがあるディレクトリのパス}
```

をやればBlenderのPythonに入る。

するとBlender内でimportとかできるようになる。

## 使い方

ライブラリを作っている最中なのでここには書かない。
Pythonを読んでくれ。
