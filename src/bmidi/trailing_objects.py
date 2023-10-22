import bpy
import traceback

"""
1つのオブジェクトについて色々とまとめる
持つべき変数:
    - オブジェクトそのもの(bpy)
    - オブジェクト名
    - アニメーション情報
        info: アンカーと同様の処理を行う。
        - フレーム位置
        - ロケーション
        - スケール
        - オイラー角
        - アルファ
    - get関数で取ってこれるようにするもの
        - アニメーションアンカー数
        - メッシュ本体
        - マテリアル(これはオブジェクト毎に作る)本体
        - モディファイア本体

持つべき関数:
    - __init__でメッシュをもらってオブジェクトを生成する
    - アンカー追加
    - アンカーの中身を変更
    - 各種get関数
    - モディファイア・マテリアル操作を簡便にする関数

futures:
    - 物理演算もいい感じに扱えるようにする
"""


class CreateObject:
    class __AnimationAnker:
        def __init__(self, frm, lct, scl, eul, alp) -> None:
            self.frame = frm
            self.location = [0.0, 0.0, 0.0] if lct == None else lct
            self.scale = [0.0, 0.0, 0.0] if scl == None else scl
            self.euler = [0.0, 0.0, 0.0] if eul == None else eul
            self.alpha = alp

    def __init__(self, name, mesh, frm, lct=None, scl=None, eul=None, alp=1) -> None:
        self.__object = bpy.data.objects.new(name, mesh)
        self.name = name
        self.__animation_ankers = [self.__AnimationAnker(frm, lct, scl, eul, alp)]

    def get_anker_number(self):
        return len(self.animation_ankers)

    def get_mesh(self):
        return self.data

    def get_material(self):
        return [i for i in self.__object.data.materials]

    def get_modifier(self):
        return [i for i in self.__object.modifiers]

    def new_anker(self, frm, lct=None, scl=None, eul=None, alp=1.0):
        try:
            for i in range(len(self.__animation_ankers)):
                if frm == self.__animation_ankers[i].frame:
                    raise ValueError("An anker aleady there.")
                if frm < self.__animation_ankers[i].frame:
                    self.__animation_ankers.insert(
                        i, self.__AnimationAnker(frm, lct, scl, eul, alp)
                    )
                    return
            self.__animation_ankers.append(
                self.__AnimationAnker(frm, lct, scl, eul, alp)
            )
        except:
            traceback.print_exc()

    def edit_anker(self, anker_no, frm=None, lct=None, scl=None, eul=None, alp=None):
        
