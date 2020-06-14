# -*- mode: python3 ; coding: utf-8 -*-

block_cipher = None

from kivymd import hooks_path as kivymd_hooks_path
path = os.path.abspath("app/")

a = Analysis(['app/__main__.py'],
             #pathex=['/Users/linear/Documents/pg/pythonnnnn/schreen/MacOSBuild'],
             pathex=['/Users/unkonow/Documents/pg/python/nowProject/schreen/Schreen'],
             binaries=[],
             datas=[('app/','app/'),
                    ("app/uix/","app/uix/"),
                    ("app/images/","app/images/"),
                    ("app/server/templates/","app/server/templates"),
                    ("app/server/","app/server/")],
             hiddenimports=['pkg_resources.py2_warn'],
             hookspath=[kivymd_hooks_path],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)



exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Schreen',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='Schreen.app',
             icon="app/images/icon.icns",
             info_plist={
                 'NSHighResolutionCapable': 'True', # Support Ratina Display
                 'NSRequiresAquaSystemAppearance': 'Yes', # Support DarkMode?
                 },
             bundle_identifier=None)
