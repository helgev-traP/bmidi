"""
全てができるようにしようとすると
結局BlenderAPIでやったほうが速い状況になるので、
なるべく単純な構造体にする

わざわざ構造体にしなくても関数の集まりでいいかも
-> Blenderのオブジェクトはクラスの中に作った方が安全ではある
"""

import bpy
import re


# # BasicEndPoint


class BasicEndPoint:
    """関数間の受け渡しでいい感じにレベル分けするためのもの"""

    # クラス名あとでいい感じにする

    def __init__(
        self,
        frame: int,
        location: list[float],
        scale: list[float],
        euler: list[float],
        alpha: float,
    ) -> None:
        self.frame = frame
        self.location = location
        self.scale = scale
        self.euler = euler
        self.alpha = alpha
        return


# # SimpleObjectClass


class SimpleObject:
    """2点間の移動を簡単にいい感じにできる。宣言した瞬間にBlenderに焼き込んじゃう"""

    def __init__(
        self, name, mesh, start_from: BasicEndPoint, end_to: BasicEndPoint
    ) -> None:
        # クラスの構造体を引数に取れるようにする
        self.__object = bpy.data.objects.new(name, mesh)
        self.__start_from = start_from
        self.__end_to = end_to
        self.bake_to_blender(self.__start_from, self.__end_to)

    def bake_to_blender(self, start_from: BasicEndPoint, end_to: BasicEndPoint):
        """Blenderに焼く"""
        self.__object.data.materials[0].use_nodes = True
        # hide object
        bpy.context.scene.frame_set(start_from.frame - 1)
        self.__object.hide_render = True
        self.__object.hide_viewport = True
        self.__object.keyframe_insert(data_path="hide_render", index=-1)
        self.__object.keyframe_insert(data_path="hide_viewport", index=-1)
        # start point
        bpy.context.scene.frame_set(start_from.frame)
        self.__object.location = start_from.location
        self.__object.scale = start_from.scale
        self.__object.rotation_euler = start_from.euler
        self.__object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[
            21
        ].default_value = start_from.alpha
        self.__object.hide_render = False
        self.__object.hide_viewport = False
        # Bake
        self.__object.keyframe_insert(data_path="location", index=-1)
        self.__object.keyframe_insert(data_path="scale", index=-1)
        self.__object.keyframe_insert(data_path="rotation_euler", index=-1)
        self.__object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[
            21
        ].keyframe_insert(data_path="default_value", index=-1)
        self.__object.keyframe_insert(data_path="hide_render", index=-1)
        self.__object.keyframe_insert(data_path="hide_viewport", index=-1)
        # end point
        bpy.context.scene.frame_set(end_to.frame)
        self.__object.location = end_to.location
        self.__object.scale = end_to.scale
        self.__object.rotation_euler = end_to.euler
        self.__object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[
            21
        ].default_value = end_to.alpha
        self.__object.hide_render = True
        self.__object.hide_viewport = True
        # Bake
        self.__object.keyframe_insert(data_path="location", index=-1)
        self.__object.keyframe_insert(data_path="scale", index=-1)
        self.__object.keyframe_insert(data_path="rotation_euler", index=-1)
        self.__object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[
            21
        ].keyframe_insert(data_path="default_value", index=-1)
        self.__object.keyframe_insert(data_path="hide_render", index=-1)
        self.__object.keyframe_insert(data_path="hide_viewport", index=-1)


# # ExtendedObject


class CreateObject:
    """
    データ構造について:

    メモ1:
    各パラメータのデータタイプについて
    オブジェクトプロパティ
        オブジェクトから直接生えている
        <class 'Vector'>
    マテリアルプロパティ
        ノード.inputs[].default_value
        <class 'bpy.types.NodeSocket{パラメータ名}'>
    モディファイアプロパティ
        モディファイアから直接生えている
        <class 'bpy.types.{モディファイア名}Modifier'>
    全部全体マッチでいける

    メモ2:
    クラスの型については、type()で
    <class '__main__.C.CC'>
    みたいに出力される
    """

    # todo オブジェクトプロパティとモディファイアプロパティはdefault_valueで管理されていないのでそれ用のものを作る
    # ## Channels
    class ChannelObject:
        """channel of object"""

        class Anchor:
            """anchor"""

            def __init__(self, frame, value) -> None:
                self.frame = frame
                self.value = value

        def __init__(self, data_path) -> None:
            """なるべく汎用にする"""
            self.data_path = data_path
            self.anchors: list = []

        def add_anchor(self, frame, value):
            """add anchor"""
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    print("This frame already exists a anchor of", self.data_path)
                    return
                if frame < anchor.frame:
                    self.anchors.insert(i, self.Anchor(frame=frame, value=value))
                    return
            self.anchors.append(self.Anchor(frame=frame, value=value))

    class ChannelMaterial:
        """channel of material"""

        class Anchor:
            """anchor"""

            def __init__(self, frame, value) -> None:
                self.frame = frame
                self.value = value

        def __init__(self, obj_property) -> None:
            """なるべく汎用にする"""
            self.obj_property = obj_property
            self.anchors: list = []

        def add_anchor(self, frame, value):
            """add anchor"""
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    print("This frame already exists a anchor of", self.obj_property)
                    return
                if frame < anchor.frame:
                    self.anchors.insert(i, self.Anchor(frame=frame, value=value))
                    return
            self.anchors.append(self.Anchor(frame=frame, value=value))

    class ChannelModifier:
        """channel of material"""

        class Anchor:
            """anchor"""

            def __init__(self, frame, value) -> None:
                self.frame = frame
                self.value = value

        def __init__(self, modifier, data_path) -> None:
            """なるべく汎用にする"""
            self.modifier = modifier
            self.data_path = data_path
            self.anchors: list = []

        def add_anchor(self, frame, value):
            """add anchor"""
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    print("This frame already exists a anchor.")
                    return
                if frame < anchor.frame:
                    self.anchors.insert(i, self.Anchor(frame=frame, value=value))
                    return
            self.anchors.append(self.Anchor(frame=frame, value=value))

    # ## matrix
    class ChannelMatrix:
        '''チャンネル名とそのtype、data_pathとかをマトリクスにしたもの'''

    # ## main
    def __init__(self, name, mesh) -> None:
        """オブジェクトとアンカーのみを持つ"""
        self.__object = bpy.data.meshes.new(name, mesh)
        self.channels = dict()

    # ## geters
    def get_channel_names(self):
        """get channels' key"""
        return self.channels.keys()

    def get_channel_properties(self):
        """get channel' property"""
        return [i.obj_property for i in self.channels.items()]

    # ## channels
    def new_channel(self, name, channel_type, channel_object, data_path=None):
        """プロパティ本体をchannel構造体に持たせる"""
        # 衝突のチェック
        if name in self.get_channel_names():
            print("name:", name, "is already be used.")
            return
        # todo プロパティごとの衝突のチェックが抜けるのでどうにかする
        # 各タイプで作業
        if channel_type == "object":
            # ## object
            self.channels[name] = self.ChannelObject(
                data_path=data_path,
            )
        elif channel_type == "material":
            # ## Material
            if channel_object in self.get_channel_properties():
                print("property:", channel_object, "already exist")
                return
            self.channels[name] = self.ChannelMaterial(
                obj_property=channel_object,
            )
        elif channel_type == "modifier":
            # ## Modifier
            self.channels[name] = self.ChannelModifier(modifier=channel_object)
            pass
        else:
            print("property:", obj_property, "is not supported.")

    def add_anchor(self, name, frame, value):
        """channel の中の add_anchor に繋げる"""
        self.channels[name].add_anchor(frame=frame, value=value)

    def bake2blend(self):
        """Bake all anchors to Blender
        old:
        for channel in self.channels.items():
            obj_property = channel.obj_property
            anchors = channel.anchors
            data_type = str(type(obj_property))
            # todo ここはデータ構造の変更に伴って改築する
            if re.fullmatch("<class 'Vector'>", data_type) is not None:
                # object
                pass
            elif (
                re.fullmatch("<class 'bpy.types.NodeSocket[a-zA-Z]*'>", data_type)
                is not None
            ):
                # Material
                for anchor in anchors:
                    bpy.context.scene.frame_set(anchor.frame)
                    obj_property.default_value = anchor.value
                    obj_property.keyframe_insert(data_path="default_value", index=-1)
            elif (
                re.fullmatch("<class 'bpy.types.[a-zA-Z]*Modifier'>", data_type)
                is not None
            ):
                # Modifier
                for anchor in anchors:
                    bpy.context.scene.frame_set(anchor.frame)
                    obj_property = anchor.value
                    obj_property.keyframe_insert(data_path="?", index=-1)
            else:
                print("property:", obj_property, "is not supported.")
                pass
        """


# # Usage Example

if __name__ == "__main__":
    print("Here is sample program. Nothing will happen in CLI!")
    sample = SimpleObject(
        name="sample",
        mesh=bpy.data.meshes.new(),
        start_from=BasicEndPoint(
            frame=1,
            location=[1, 1, 1],
            scale=[1, 1, 1],
            euler=[0, 0, 0],
            alpha=1.0,
        ),
        end_to=BasicEndPoint(
            frame=1,
            location=[1, 1, 1],
            scale=[1, 1, 1],
            euler=[0, 0, 0],
            alpha=1.0,
        ),
    )
