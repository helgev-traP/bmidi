'''usage example of trailing_objects.py'''

# import bmidi
from .trailing_objects import *

mesh = bpy.data.meshes['']

obj = CreateObject(name='sample', mesh=mesh, frame=1)