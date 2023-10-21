import bpy
import re

"""
方針:
スクリプトで作成したオブジェクトは全て一意な名前をつけて管理
カット毎に添え字を変える
    オブジェクト命名
        PREFIX-Cut_{No.}-obj_{No.}

コレクションも変えておく？(あとまわし)

外部ファイル(json？)を読み込んでオブジェクトの動きをBlenderに伝える

"""

PREFIX = "bmidi"


def get_meshes_name() -> list:
    return [mesh.name for mesh in bpy.data.meshes]


def get_objects_name() -> list:
    return [obj.name for obj in bpy.data.objects]


def get_material_name() -> list:
    return [material.name for material in bpy.data.materials]


class MotionCut:
    def __init__(self) -> None:
        self.meshes = []
        self.material = []
        self.objects = []

    def search_previous():
        """search for exist MotionCut return listed name"""
        exist_MotionCuts = []
        for i in bpy.data.objects:
            if re.match(PREFIX + "-Cut_[0-9]+-obj_[0-9]+", i.name) != None:
                if (re.findall("Cut_[0-9]+", i.name)[0] in exist_MotionCuts) == False:
                    exist_MotionCuts.append((re.findall("Cut_[0-9]+", i.name))[0])
        return exist_MotionCuts

