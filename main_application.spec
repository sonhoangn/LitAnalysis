# -*- mode: python -*-

block_cipher = None

added_files = [
    ('programs/assets', 'assets'),          # Assets folder
    ('programs/main.py', '.'),       # Main functions script
]

a = Analysis(['programs\\gui_2.py'],  # Main script
             pathex=[],
             binaries=[],
             datas=added_files,
             hiddenimports=[
                 'aiohappyeyeballs',
                 'aiohttp',
                 'aiosignal',
                 'altair',
                 'altgraph',
                 'annotated_types',
                 'anyio',
                 'asttokens',
                 'attrs',
                 'cachetools',
                 'certifi',
                 'charset_normalizer',
                 'click',
                 'colorama',
                 'comm',
                 'contourpy',
                 'cycler',
                 'debugpy',
                 'decorator',
                 'et_xmlfile',
                 'executing',
                 'fastjsonschema',
                 'filelock', # Added
                 'fonttools', # Added
                 'frozenlist',
                 'google_ai_generativelanguage',
                 'google_api_core',
                 'google_api_python_client',
                 'google_auth',
                 'google_auth_httplib2',
                 'google_generativeai',
                 'googleapis_common_protos',
                 'grpcio',
                 'grpcio_status',
                 'h11', # Added
                 'httplib2',
                 'humanize', # Added
                 'idna',
                 'ipykernel', # Added (often needed for interactive components)
                 'ipython',
                 'ipyvue', # Added
                 'ipyvuetify', # Added
                 'ipywidgets', # Added
                 'jedi',
                 'Jinja2', # Added
                 'jsonschema', # Added
                 'jsonschema_specifications', # Added
                 'jupyter_client', # Added
                 'jupyter_core', # Added
                 'jupyterlab_widgets', # Added
                 'kiwisolver', # Added
                 'Markdown', # Added
                 'markdown_it_py', # Added
                 'MarkupSafe', # Added
                 'matplotlib', # Added
                 'matplotlib_inline',
                 'mdurl', # Added
                 'Mesa', # Added
                 'multidict',
                 'narwhals', # Added
                 'nbformat', # Added
                 'nest_asyncio', # Added
                 'networkx', # Added
                 'numpy',
                 'openpyxl',
                 'packaging', # Added
                 'pandas',
                 'parso',
                 'pefile', # Added
                 'pillow', # Added
                 'platformdirs', # Added
                 'prompt_toolkit',
                 'propcache',
                 'proto_plus',
                 'protobuf',
                 'psutil', # Added
                 'pure_eval',
                 'pyasn1',
                 'pyasn1_modules',
                 'pydantic',
                 'pydantic_core',
                 'Pygments',
                 'pyinstaller', # Added (though not directly imported by your app, PyInstaller itself might need hooks)
                 'pyinstaller_hooks_contrib', # Added
                 'pymdown_extensions', # Added
                 'pyparsing',
                 'PyPDF2', # Added
                 'python_dateutil',
                 'pytz',
                 'pywin32', # Added (if running on Windows and using win32 API)
                 'pywin32_ctypes', # Added
                 'PyYAML', # Added
                 'pyzmq', # Added
                 'reacton', # Added
                 'referencing', # Added
                 'requests',
                 'rich', # Added
                 'rich_click', # Added
                 'rpds_py', # Added
                 'rsa',
                 'scipy', # Added
                 'setuptools', # Added
                 'six',
                 'sniffio', # Added
                 'solara', # Added
                 'solara_server', # Added
                 'solara_ui', # Added
                 'stack_data',
                 'starlette', # Added
                 'tabulate',
                 'tornado', # Added
                 'tqdm',
                 'traitlets',
                 'typing_extensions',
                 'tzdata',
                 'uritemplate',
                 'urllib3',
                 'uvicorn', # Added
                 'watchdog', # Added
                 'watchfiles', # Added
                 'wcwidth',
                 'websockets', # Added
                 'wheel', # Added
                 'widgetsnbextension', # Added
                 'yarl'
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          [],
          name='Literature_Analyzer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          icon='E:\\Projects\\Applications\\LiteraturatureAnalyzer\\programs\\assets\\icon.png')