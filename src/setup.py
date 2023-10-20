from setuptools import setup, find_packages

'''
メジャーバージョン:
v0:
MIDIしか扱えない
v1:
Pythonからある程度Blenderのオブジェクトが扱える
v2:
GUIで操作できるようにする。アドオン化を狙う
'''

setup(
    name='bmidi',
    version='0.1.2',
    packages=find_packages(),
    install_requires="mido",
)