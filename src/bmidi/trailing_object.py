'''
全てができるようにしようとすると
結局BlenderAPIでやったほうが速い状況になるので、
なるべく単純な構造体にする

わざわざ構造体にしなくても関数の集まりでいいかも
-> Blenderのオブジェクトはクラスの中に作った方が安全ではある
'''

import bpy

class SimpleObject():
    '''2点間の移動を簡単にいい感じにできる。宣言した瞬間にBlenderに焼き込んじゃう'''
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

    def __init__(self, name, mesh, start_from: EndPoint, end_to:EndPoint) -> None:
        # クラスの構造体を引数に取れるようにする
        self.object = bpy.data.objects.new(name, mesh)
        self.start_from = start_from
        self.end_to = end_to
        self.bake_to_blender(self.start_from,self.end_to)

    def end_point(self, frame, location, scale, euler, alpha):
        '''関数間の受け渡しでいい感じにレベル分けするためのもの'''
        point = self.EndPoint(frame, location, scale, euler, alpha)
        return point

    def bake_to_blender(self, start_from: EndPoint, end_to:EndPoint):
        '''Blenderに焼く'''
        self.object.data.materials[0].use_nodes = True
        # start point
        bpy.context.scene.frame_set(start_from.frame)
        self.object.location = start_from.location
        self.object.scale = start_from.scale
        self.object.rotation_euler = start_from.euler
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].default_value = start_from.alpha
        # Bake
        self.object.keyframe_insert(data_path="location", index=-1)
        self.object.keyframe_insert(data_path="scale", index=-1)
        self.object.keyframe_insert(data_path="rotation_euler", index=-1)
        self.object.data.materials[0].node_tree.nodes["Principled BSDF"].inputs[21].keyframe_insert(data_path="default_value", index=-1)
