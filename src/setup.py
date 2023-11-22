"""
メジャーバージョン:
v0:
MIDIしか扱えない
v1:
Pythonからある程度Blenderのオブジェクトが扱える
v2:
GUIで操作できるようにする。アドオン化を狙う
"""

from setuptools import setup, find_packages

setup(
    name="bmidi",
    version="1.1.0",
    packages=find_packages(),
    install_requires="mido",
)
