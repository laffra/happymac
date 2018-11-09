# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/happymac.py'],
             pathex=['/Users/chris/dev/happymac'],
             binaries=[],
             datas=[
               ('icons', 'icons'),
             ],
             hiddenimports=['versions.v00001.main'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tkinter'],
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
          name='happymac',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )