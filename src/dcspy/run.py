import os
import signal
import subprocess
import sys
from argparse import Namespace
from logging import getLogger
from os import environ, unlink
from pathlib import Path
from tempfile import gettempdir

try:
    import lupa.luajit21 as lupa
except ImportError:
    try:
        import lupa.lua51 as lupa
    except ImportError:
        pass
from PySide6.QtWidgets import QApplication

from dcspy import get_config_yaml_item
from dcspy.qt_gui import DcsPyQtGui

LOG = getLogger(__name__)
__version__ = '3.7.0'

def lua21():
    lua = (lupa.LuaRuntime())
    print(f"Using {lupa.LuaRuntime().lua_implementation} (compiled with {lupa.LUA_VERSION})")
    with open('./Scripts/DCS-BIOS/test/compile/LocalCompile.lua') as lua_file:
        lua_script = lua_file.read()
    lua.execute(lua_script)


def dcs_lua():
    lua_exec = Path(r'C:\Program Files\Eagle Dynamics\DCS World OpenBeta\bin\luae.exe')
    subprocess.run([lua_exec, r'Scripts\DCS-BIOS\test\compile\LocalCompile.lua'], check=True, shell=False)


def change_directory_and_run(new_dir, function_to_run):
    previous_dir = os.getcwd()

    try:
        print(f"Running in directory: {os.getcwd()}")
        os.chdir(new_dir)
        print(f"Changed to {new_dir}")

        function_to_run()

    finally:
        os.chdir(previous_dir)
        print(f"Running in directory: {os.getcwd()}")


def run(cli_args: Namespace = Namespace()) -> None:
    """Run DCSpy Qt6 GUI."""
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.setStyle('fusion')
    new_directory = Path(r'C:\Users\mplic\Saved Games\DCS.openbeta')
    change_directory_and_run(new_directory, lua21)
    try:
        window = DcsPyQtGui(cli_args)
        if get_config_yaml_item('show_gui', True):
            window.show()
        unlink(Path(gettempdir()) / f'onefile_{environ["NUITKA_ONEFILE_PARENT"]}_splash_feedback.tmp')
        app.aboutToQuit.connect(window.event_set)
    except (KeyError, FileNotFoundError):
        pass
    except Exception as exp:
        LOG.exception(f'Critical error: {exp}', exc_info=True)
    finally:
        sys.exit(app.exec())
