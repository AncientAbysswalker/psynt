# -*- mode: python -*-

block_cipher = None


a = Analysis(['cst_frame.py'],
             binaries=[],
             datas=[('questions_demo.txt', '.'),
             ('convert_key_demo.yaml', '.'),
             ('img\\r_arr.png', '.\\img'),
             ('img\\cover.jpg', '.\\img'),
             ('config.yaml', '.')],
             hiddenimports=[],
             hookspath=[],
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
          name='cst_frame',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
