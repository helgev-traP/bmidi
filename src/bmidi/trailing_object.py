'''
全てができるようにしようとすると
結局BlenderAPIでやったほうが速い状況になるので、
なるべく単純な構造体にする

わざわざ構造体にしなくても関数の集まりでいいかも
-> Blenderのオブジェクトはクラスの中に作った方が安全ではある
'''

import bpy


class EndPoint():
    '''関数間の受け渡しでいい感じにレベル分けするためのもの'''
    # クラス名あとでいい感じにする

    def __init__(self,
                 frame: int,
                 location: list[float],
                 scale: list[float],
                 euler: list[float],
                 alpha: float
                 ) -> None:
        self.frame = frame
        self.location = location
        self.scale = scale
        self.euler = euler
        self.alpha = alpha
        return


class SimpleObjectClass():
    '''2点間の移動を簡単にいい感じにできる。宣言した瞬間にBlenderに焼き込んじゃう'''

    def __init__(self, name, mesh, start_from: EndPoint, end_to: EndPoint) -> None:
        # クラスの構造体を引数に取れるようにする
        self.object = bpy.data.objects.new(name, mesh)
        self.start_from = start_from
        self.end_to = end_to
        self.bake_to_blender(self.start_from, self.end_to)

    def bake_to_blender(self, start_from: EndPoint, end_to: EndPoint):
        '''Blenderに焼く'''
        self.object.data.materials[0].use_nodes = True
        # hide object
        bpy.context.scene.frame_set(start_from.frame - 1)
        self.object.hide_render = True
        self.object.hide_viewport = True
        self.object.keyframe_insert(data_path="hide_render", index=-1)
        self.object.keyframe_insert(data_path="hide_viewport", index=-1)
        # start point
        bpy.context.scene.frame_set(start_from.frame)
        self.object.location = start_from.location
        self.object.scale = start_from.scale
        self.object.rotation_euler = start_from.euler
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].default_value = start_from.alpha
        self.object.hide_render = False
        self.object.hide_viewport = False
        # Bake
        self.object.keyframe_insert(data_path="location", index=-1)
        self.object.keyframe_insert(data_path="scale", index=-1)
        self.object.keyframe_insert(data_path="rotation_euler", index=-1)
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].keyframe_insert(
            data_path="default_value", index=-1)
        self.object.keyframe_insert(data_path="hide_render", index=-1)
        self.object.keyframe_insert(data_path="hide_viewport", index=-1)
        # end point
        bpy.context.scene.frame_set(end_to.frame)
        self.object.location = end_to.location
        self.object.scale = end_to.scale
        self.object.rotation_euler = end_to.euler
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].default_value = end_to.alpha
        self.object.hide_render = True
        self.object.hide_viewport = True
        # Bake
        self.object.keyframe_insert(data_path="location", index=-1)
        self.object.keyframe_insert(data_path="scale", index=-1)
        self.object.keyframe_insert(data_path="rotation_euler", index=-1)
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].keyframe_insert(
            data_path="default_value", index=-1)
        self.object.keyframe_insert(data_path="hide_render", index=-1)
        self.object.keyframe_insert(data_path="hide_viewport", index=-1)

if __name__ == "__main__":
    print("Here is sample program. Nothing will happen in CLI!")
    sample = SimpleObjectClass(
        name="sample",
        mesh=bpy.data.meshes.new(),
        start_from=EndPoint(frame=1,
                            location=[1, 1, 1],
                            scale=[1, 1, 1],
                            euler=[0, 0, 0],
                            alpha=1.0,
                            ),
        end_to=EndPoint(frame=1,
                        location=[1, 1, 1],
                        scale=[1, 1, 1],
                        euler=[0, 0, 0],
                        alpha=1.0,
                        ),
    )
