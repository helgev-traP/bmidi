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

## 注意・ライセンス

現在このライブラリをOSSとして開発するかどうかは定かではありません。突然リポジトリを非公開にする可能性もあるので使いたい方は今のうちにクローンするなどしてください。

現在を含め、あなた自身によるこのライブラリの改変などを身内に配布するなどの事はグレーゾーンとして認めますが、このライブラリを改変、無改変を問わず不特定多数が触れることのできる環境下にアップロードすることは禁止とします。

さらに、このライブラリの改変についても同様のライセンスを継承することとします。

クレジット表記は任意で大丈夫ですが、していただけるとめちゃくちゃ喜びます。
