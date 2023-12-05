import sys
import os

block_cipher = None

def get_pulp_path():
    import pulp
    return pulp.__path__[0]

path_main = os.path.dirname(os.path.abspath("app.py"))

a = Analysis(['app.py'],
             pathex=[path_main],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += Tree(get_pulp_path(), prefix='pulp', excludes=["*.pyc"])

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz, a.scripts, exclude_binaries=True, name='School Harmony', debug=False, strip=False, upx=True, console=False)
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=True, name='School Harmony')
