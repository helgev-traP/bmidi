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
    # # datas

    class ChannelObject:
        """これは__init__でプロパティ分作られる"""

        class Anchor:
            def __init__(self, frame, value) -> None:
                self.frame
                self.value

        def __init__(self, base_entity, value_entity, data_path: str) -> None:
            self.base_entity = base_entity
            self.value_entity = value_entity
            self.data_path = data_path
            self.anchors = []

        def add_anchor(self, frame, value):
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    print("At channel of", self.value_entity)
                    print("There is a anchor already")
                    return
                if frame < anchor.frame:
                    self.anchors.insert(i, self.Anchor(frame=frame, value=value))
                    return
            self.anchors.append(self.Anchor(frame=frame, value=value))


    class ChannelMaterial:
        pass

    class ChannelModifier:
        pass

    class channelMatrix:
        pass

    # # main

    def __init__(self, name, mesh, location=None, scale=None, rotation=None) -> None:
        self.__object = bpy.data.objects.new(name=name, object_data=mesh)
        self.channels = dict()
        # ## ChannelObjectの規定値を入れておく
        self.channels["location"] = self.ChannelObject(
            property_type="location", data_path="location"
        )

    # ## getters

    def get_channel_names(self):
        pass

    def get_channel_properties(self):
        pass

    # ## channel | anchor

    def new_channel(self):
        pass

    def del_channel(self):
        pass

    def add_anchor(self):
        pass

    def del_anchor(self):
        pass

    # # bake2blend

    def bake2blend(self):
        # todo memo シーンにリンクする
        pass

    # # Utilities

    def set_individual_material(self):
        pass

    def add_modifier(self):
        pass


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
