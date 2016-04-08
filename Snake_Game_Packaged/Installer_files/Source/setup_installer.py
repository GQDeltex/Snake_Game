from distutils.core import setup
import py2exe

setup(
    console=['Windows_Installation.py'],
    options={
        "py2exe":{
            "dist_dir": 'Installer/',
            "compressed": True,
            "optimize": 2,
            "bundle_files": 1,
        }
    }
)
