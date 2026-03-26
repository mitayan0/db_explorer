import sys
import os
import shutil

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_appdata_path(file_name):
    """ Get path to a file in the user's AppData directory for writability """
    # On Windows: C:\Users\<User>\AppData\Roaming\DB_Explorer
    appdata_root = os.getenv('APPDATA') or os.path.expanduser('~')
    app_dir = os.path.join(appdata_root, 'DB_Explorer')
    
    if not os.path.exists(app_dir):
        os.makedirs(app_dir)
        
    return os.path.join(app_dir, file_name)

def initialize_database():
    """ 
    Ensures a writable copy of hierarchy.db exists in AppData.
    If it doesn't exist, we copy the template from our bundled assets.
    """
    appdata_db_path = get_appdata_path("hierarchy.db")
    
    if not os.path.exists(appdata_db_path):
        # Find the original (read-only) database bundled with the app
        template_db_path = get_resource_path("databases/hierarchy.db")
        
        if os.path.exists(template_db_path):
            try:
                shutil.copy2(template_db_path, appdata_db_path)
                print(f"Successfully initialized database at: {appdata_db_path}")
            except Exception as e:
                print(f"Failed to copy template database: {e}")
        else:
            print(f"Template database not found at: {template_db_path}")
    
    return appdata_db_path
