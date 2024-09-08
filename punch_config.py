__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = [
    'dcs_py.py',
    'dcspy/__init__.py',
    'dcspy/qt_gui.py',
    'dcspy/run.py',
    'dcspy/starter.py',
    'dcspy/migration.py',
    'dcspy/utils.py',
    'dcspy.spec',
    'dcspy_cli.spec',
    'dcspy_onedir.spec',
]

VERSION = ['major', 'minor', 'patch']
