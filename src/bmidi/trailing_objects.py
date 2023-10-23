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
        Noneはアンカーを置かないとする情報
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

全ての関数にBlenderに入力する機能を持たせる(Bake=True)で入力


futures:
    - 物理演算もいい感じに扱えるようにする
"""

import traceback
import bpy


class CreateObject:
    '''オブジェクトのデータを保持するクラス'''
    # # classes
    # * 変数がNoneの時はBlenderにその変数のアンカーを置かない
    class ModifierAnchor:
        '''モディファイアのアンカーオブジェクト'''
        def __init__(self) -> None:
            pass

    class MaterialAnchor:
        '''マテリアルのアンカーオブジェクト'''
        def __init__(self) -> None:
            pass

    class __AnimationAnchor:
        '''オブジェクト情報に関するアンカーオブジェクト'''
        def __init__(self, frm, lct, scl, eul, alp) -> None:
            self.frame = frm
            self.location = lct
            self.scale = scl
            self.euler = eul
            self.alpha = alp

        def edit(self, lct, scl, eul, alp):
            """frameは関数で編集しない"""
            self.location = self.location if lct == None else lct
            self.scale = self.scale if scl == None else scl
            self.euler = self.euler if eul == None else eul
            self.alpha = self.alpha if alp == None else alp

    # # __init__
    def __init__(self, name, mesh, frame, location=None, scale=None, euler=None, alpha=None) -> None:
        self.__object = bpy.data.objects.new(name, mesh)
        self.name = name
        self.__modifier_anchors = self.ModifierAnchor()
        self.__material_anchors = self.MaterialAnchor()
        self.__animation_anchors = [
            self.__AnimationAnchor(
                frm=frame,
                lct=location,
                scl=scale,
                eul=euler,
                alp=alpha,
            )
        ]

    # # geter
    def get_anchor_number(self):
        return len(self.__animation_anchors)

    def get_mesh(self):
        return self.__object.data

    def get_material(self):
        return [i for i in self.__object.data.materials]

    def get_modifier(self):
        return [i for i in self.__object.modifiers]

    # # trailing anchor
    def new_anchor(self, frm, lct=None, scl=None, eul=None, alp=None):
        try:
            for i in range(len(self.__animation_anchors)):
                if frm == self.__animation_anchors[i].frame:
                    raise ValueError("An anchor aleady there.")
                if frm < self.__animation_anchors[i].frame:
                    self.__animation_anchors.insert(
                        i, self.__AnimationAnchor(frm, lct, scl, eul, alp)
                    )
                    return
            self.__animation_anchors.append(
                self.__AnimationAnchor(frm, lct, scl, eul, alp)
            )
        except:
            traceback.print_exc()

    def edit_anchor(
        self, anchor_no, frm="None", lct="None", scl="None", eul="None", alp="None"
    ):
        if frm == "None" or frm == self.__animation_anchors[anchor_no].frame:
            self.__animation_anchors[anchor_no].edit(
                lct=self.__animation_anchors[anchor_no].location
                if lct == "None"
                else lct,
                scl=self.__animation_anchors[anchor_no].scale if scl == "None" else scl,
                eul=self.__animation_anchors[anchor_no].euler if eul == "None" else eul,
                alp=self.__animation_anchors[anchor_no].alpha if alp == "None" else alp,
            )
        else:
            poped = self.__animation_anchors.pop(anchor_no)
            self.new_anchor(
                frm=frm,
                lct=poped.location if lct == "None" else lct,
                scl=poped.scale if scl == "None" else scl,
                eul=poped.euler if eul == "None" else eul,
                alp=poped.alpha if alp == "None" else alp,
            )

    # # for modifier and material

    def add_anchor_type():
        # todo 使うかどうかはわからない
        pass

    # # modifier

    def add_modifier(self, modifier_name, modifier_type):
        self.__object.modifiers.new(name=modifier_name, type=modifier_type)
        # todo ここにModifier追加したときのアンカーの挙動を書く
        pass

    # # material

    def set_material():
        pass

    # # Bake to Blender
    def bake_to_blender(self):
        pass
