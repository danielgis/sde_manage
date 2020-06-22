import threading

import arcpy
import pythonaddins
from datetime import datetime
import os
import subprocess

MSG_MESSAGE_BOX = 'Esta seguro que desea ejecutar el proceso de mantenimiento de la Geodatabase'
MSG_MESSAGE_BOX_CONCILE = 'Recuerde realizar la conciliacion de versiones antes de ejecutar este proceso.'
TITLE_MESSAGE_BOX = 'SDEManager {}'.format(datetime.now().year)

TBX = os.path.join(os.path.dirname(__file__), 'Toolbox.tbx')
arcpy.ImportToolbox(TBX)

PROCESS_BAT = r'C:\sde_addin_manage\sde_manage.bat'


# BASE_DIR_C = r''


class ConfigTool(object):
    """Implementation for addin_addin.config_tool (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pythonaddins.GPToolDialog(TBX, 'setparameters')


class ExecuteProcess(object):
    """Implementation for addin_addin.execute_process (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False
        self.message = '{}\n{}'.format(MSG_MESSAGE_BOX, MSG_MESSAGE_BOX_CONCILE)

    def onClick(self):
        response = pythonaddins.MessageBox(self.message, TITLE_MESSAGE_BOX, 3)
        if response.lower() == 'yes':
            # arcpy.mantenimientoGeodatabase()
            subprocess.Popen(PROCESS_BAT)


class UserGuide(object):
    """Implementation for addin_addin.user_guide (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        pass


class GetConfig(object):
    """Implementation for addin_addin.get_config (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        arcpy.getconfiguracion()


def open_registro(f):
    os.startfile(f)


class GetRegistry(object):
    """Implementation for addin_addin.get_registry (Button)"""

    def __init__(self):
        self.enabled = True
        self.checked = False

    def onClick(self):
        response = arcpy.openregistry()[0]
        if os.path.exists(response):
            t = threading.Thread(target=open_registro, args=(response,))
            t.start()
            t.join()
        else:
            pythonaddins.MessageBox(response, TITLE_MESSAGE_BOX)
