import sys
import os

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # Better: use the directory of this file (project root)
            base_path = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        # Fallback to current directory
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
