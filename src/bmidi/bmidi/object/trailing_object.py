"""
Usage:
if __name__ == "__main__": の中

todo なるべく関数に返り値がつくようにする
"""

import bpy
from ..attribute_access.attribute_access import getattr_h
from ..attribute_access.attribute_access import setattr_h

INTERPOLATIONS = [
    "CONSTANT",
    "LINEAR",
    "BEZIER",
    "SINE",
    "QUAD",
    "CUBIC",
    "QUART",
    "QUINT",
    "EXPO",
    "CIRC",
    "BACK",
    "BOUNCE",
    "ELASTIC",
]

# # BasicEndPoint


class SimpleObjectEndPoint:
    """関数間の受け渡しでいい感じにレベル分けするためのもの"""

    # クラス名あとでいい感じにする

    def __init__(
        self,
        frame: int,
        location: list[float],
        scale: list[float],
        rotation: list[float],
        alpha: float,
    ) -> None:
        self.frame = frame
        self.location = location
        self.scale = scale
        self.rotation = rotation
        self.alpha = alpha
        return


# # SimpleObjectClass


class SimpleObject:
    """2点間の移動のみ"""

    def __init__(
        self,
        name: str,
        mesh,
        start_from: SimpleObjectEndPoint,
        end_to: SimpleObjectEndPoint,
        interpolation: str = "BEZIER",
    ) -> None:
        # todo 補完モードに関して実装する
        # todo 動くかチェック
        self.object = Object(name=name, mesh=mesh)
        self.object.new_channel_material(
            name="alpha",
            material_input='data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[21]',
        )
        # 1
        # todo alphaを0に
        self.object.add_anchor(
            channel_name="alpha",
            frame=start_from.frame - 1,
            value=0.0,
        )
        # 2
        # todo alphaをalpha_1に
        self.object.add_anchor(
            channel_name="alpha",
            frame=start_from.frame,
            value=start_from.alpha,
        )
        self.object.add_anchor(
            channel_name="location",
            frame=start_from.frame,
            value=start_from.location,
        )
        self.object.add_anchor(
            channel_name="scale",
            frame=start_from.frame,
            value=start_from.scale,
        )
        self.object.add_anchor(
            channel_name="rotation",
            frame=start_from.frame,
            value=start_from.rotation,
        )
        # 3
        # todo alphaをalpha_2に
        self.object.add_anchor(
            channel_name="alpha",
            frame=end_to.frame,
            value=end_to.alpha,
        )
        self.object.add_anchor(
            channel_name="location",
            frame=end_to.frame,
            value=end_to.location,
        )
        self.object.add_anchor(
            channel_name="scale",
            frame=end_to.frame,
            value=end_to.scale,
        )
        self.object.add_anchor(
            channel_name="rotation",
            frame=end_to.frame,
            value=end_to.rotation,
        )
        # 4
        # todo alphaを0に
        self.object.add_anchor(
            channel_name="alpha",
            frame=end_to.frame + 1,
            value=0.0,
        )
        # bake
        self.object.bake2blend()


# # ExtendedObject


class Object:
    # # datas
    class Channel:
        class Anchor:
            def __init__(self, frame: int, value) -> None:
                self.frame = frame
                self.value = value
                self.interpolation = None

            def set_interpolation(self, interpolation):
                self.interpolation = interpolation

        def __init__(
            self,
            base_entity: str,
            value_entity: str,
            data_path: str,
        ) -> None:
            self.base_entity: str = base_entity
            self.value_entity: str = value_entity
            self.data_path: str = data_path
            self.anchors = []
            self.default_interpolation = True
            self.channel_interpolation_enable = True
            self.channel_interpolation = "BEZIER"

        def add_anchor(self, frame: int, value):
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    print("At channel of", self.value_entity)
                    print("There is a anchor already")
                    return
                if frame < anchor.frame:
                    self.anchors.insert(i, self.Anchor(frame=frame, value=value))
                    return
            self.anchors.append(self.Anchor(frame=frame, value=value))
            return

        def del_anchor(
            self,
            frame: int | None = None,
            index: int | None = None,
        ):
            if (frame == None) ^ (index == None):
                print("At channel of", self.value_entity)
                print("Specify frame OR index.")
                return
            if index != None:
                try:
                    self.anchors.pop(index)
                except IndexError:
                    print("At channel of", self.value_entity)
                    print("Index out of range.")
                return
            for i, anchor in enumerate(self.anchors):
                if frame == anchor.frame:
                    self.anchors.pop(i)
                    return
            print("At channel of", self.value_entity)
            print("No anchor at frame", frame)
            return

        def move_anchor(self, index: str, frame: str):
            val = self.anchors[index].value
            self.del_anchor(index=index)
            self.add_anchor(frame=frame, value=val)

        def set_channel_interpolation(self, interpolation: str):
            if interpolation not in INTERPOLATIONS:
                print("invalid interpolation name.")
                return False
            elif self.base_entity != "":
                # ! オブジェクト直下のプロパティのみ編集可能
                print("changing interpolation is now only enable at object properties.")
                return False
            else:
                self.default_interpolation = False
                self.channel_interpolation = interpolation
                self.channel_interpolation_enable = True
                for i in self.anchors:
                    i.set_interpolation(interpolation)
                return True

        def set_interpolation(self, interpolation: str, index):
            if interpolation not in INTERPOLATIONS:
                print("invalid interpolation name.")
                return False
            elif self.base_entity != "":
                # ! オブジェクト直下のプロパティのみ編集可能
                print("changing interpolation is now only enable at object properties.")
                return False
            else:
                self.default_interpolation = False
                self.channel_interpolation_enable = False
                self.anchors[index].set_interpolation(interpolation)

        def get_channel_interpolation_enable(self):
            return self.channel_interpolation_enable

        def get_channel_interpolation(self):
            if self.channel_interpolation_enable:
                return self.channel_interpolation
            else:
                return None

    # # main

    def __init__(
        self,
        name: str,
        mesh,
        location: list[float] = None,
        scale: list[float] = None,
        rotation: list[float] = None,
    ) -> None:
        self.__object = bpy.data.objects.new(name=name, object_data=mesh)
        self.channels = dict()
        # ## location, scale, rotationの3つは規定値として入れておく。アンカーは入れない。
        self.new_channel(
            name="location",
            base_entity="",
            value_entity="location",
            data_path="location",
        )
        self.new_channel(
            name="scale",
            base_entity="",
            value_entity="scale",
            data_path="scale",
        )
        self.new_channel(
            name="rotation",
            base_entity="",
            value_entity="rotation_euler",
            data_path="rotation_euler",
        )
        # ## Blender側にオブジェクトプロパティだけ伝えておく
        setattr_h(
            instance=self.__object,
            attribute_path="location",
            value=location if location != None else (0, 0, 0),
        )
        setattr_h(
            instance=self.__object,
            attribute_path="scale",
            value=scale if scale != None else (1, 1, 1),
        )
        setattr_h(
            instance=self.__object,
            attribute_path="rotation_euler",
            value=rotation if rotation != None else (0, 0, 0),
        )

    # ## getters

    def get_channel_names(self):
        """get channels' key"""
        return self.channels.keys()

    def get_channel_properties(self):
        """get channel' property"""
        return [i.value_entity for i in self.channels.values()]

    # ## channel | anchor

    def new_channel(
        self, name: str, base_entity: str, value_entity: str, data_path: str
    ):
        """"""
        # todo ここの衝突回避が生きているかチェック
        # check name
        if name in self.get_channel_names():
            print("name:", name, "is already be used.")
            return
        # check property
        if value_entity in self.get_channel_properties():
            print("channel of property", value_entity, "is already exist.")
            return
        # add
        self.channels[name] = self.Channel(
            base_entity=base_entity,
            value_entity=value_entity,
            data_path=data_path,
        )
        return

    def rename_channel(self, name: str, new_name: str):
        channel = self.channels.pop(name, None)
        if channel == None:
            print("No channel has such name:", name)
            return
        self.channels[new_name] = channel

    def del_channel(self, channel_name: str):
        if self.channels.pop(channel_name, None) == None:
            print("No channel has such name:", channel_name)

    def add_anchor(
        self,
        channel_name: str,
        frame: int,
        value: int | float | list,
    ):
        self.channels[channel_name].add_anchor(frame=frame, value=value)

    def del_anchor(
        self,
        channel_name: str,
        frame: int | None = None,
        index: int | None = None,
    ):
        self.channels[channel_name].del_anchor(frame=frame, index=index)

    # ## wrapping new_channel

    def new_channel_object(self, name, object_property):
        self.new_channel(
            name=name,
            base_entity="",
            value_entity=object_property,
            data_path=object_property,
        )

    def new_channel_material(self, name, material_input):
        self.new_channel(
            name=name,
            base_entity=material_input,
            value_entity=material_input + "default_value",
            data_path="default_value",
        )

    def new_channel_modifier(self, name, modifier_entity, modifier_property):
        self.new_channel(
            name=name,
            base_entity=modifier_entity,
            value_entity=modifier_entity + modifier_property,
            data_path=modifier_property,
        )

    # ## interpolation

    def set_global_interpolation(self, interpolation: str):
        if interpolation not in INTERPOLATIONS:
            return False
        else:
            for channel in self.channels:
                channel.set_channel_interpolation(interpolation)

    def set_channel_interpolation(self, channel: str, interpolation: str):
        if interpolation not in INTERPOLATIONS:
            return False
        else:
            self.channels[channel].set_channel_interpolation(interpolation)

    def set_interpolation(self, channel: str, index: int, interpolation: str):
        if interpolation not in INTERPOLATIONS:
            return False
        else:
            self.channels[channel].set_interpolation(
                interpolation=interpolation, index=index
            )

    # # Blender Utilities

    def set_individual_material(self):
        pass

    def add_modifier(self):
        pass

    # # bake2blend

    def bake2blend(self):
        action = bpy.data.actions[self.__object.animation_data.action.name]
        for channel in self.channels.values():
            for anchor in channel.anchors:
                bpy.context.scene.frame_set(anchor.frame)
                # channel.value_entity = anchor.value
                setattr_h(
                    instance=self.__object,
                    attribute_path=channel.value_entity,
                    value=anchor.value,
                )
                # channel.base_entity.keyframe_insert(
                #     data_path=channel.data_path, index=-1
                # )
                getattr_h(
                    instance=self.__object,
                    attribute_path=channel.base_entity + "keyframe_insert",
                )(data_path=channel.data_path, index=-1)

            # ! オブジェクト直下のプロパティのみ編集可能
            if channel.base_entity == "" and channel.default_interpolation == False:
                for i, anchor in enumerate(channel.anchors):
                    if anchor.interpolation != None:
                        action.fcurves.find(
                            channel.data_path, index=-1
                        ).keyframe_points[i].interpolation = anchor.interpolation

        # link
        bpy.context.scene.collection.objects.link(self.__object)


# # Usage Example

# todo 以下の内容を__init__.pyか他のチュートリアルのモジュールに置く

if __name__ == "__main__":
    print("Here is sample program. Nothing will happen in CLI!")
    if False:
        sample = SimpleObject(
            name="sample",
            mesh=bpy.data.meshes.new(),
            start_from=SimpleObjectEndPoint(
                frame=1,
                location=[1, 1, 1],
                scale=[1, 1, 1],
                rotation=[0, 0, 0],
                alpha=1.0,
            ),
            end_to=SimpleObjectEndPoint(
                frame=1,
                location=[1, 1, 1],
                scale=[1, 1, 1],
                rotation=[0, 0, 0],
                alpha=1.0,
            ),
        )
    if True:
        test_cube = Object(
            name="test_cube",
            mesh=bpy.data.meshes["Cube"],
            location=(0, 0, 0),  # default value is (0,0,0)
            scale=(1, 1, 1),  # default value is (1,1,1)
            rotation=(0, 0, 0),  # default value is (0,0,0)
        )

        test_cube.add_anchor(
            channel_name="location",
            frame=1,
            value=(0, 0, 0),
        )
        test_cube.add_anchor(
            channel_name="location",
            frame=150,
            value=(5, 5, 0),
        )

        test_cube.bake2blend()
    print("Finish!")
