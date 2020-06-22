import os

BASE_DIR = os.path.dirname(__file__)  # Directorio base dell proyecto
BASE_DIR_C = r'C:\sde_addin_manage'
CONN_SQLITE = os.path.join(BASE_DIR_C, 'manageodb.db')  # Conexion a base de datos sqlite
# LOG_FILE = os.path.join(BASE_DIR_C, 'registry.txt')
REGISTRY_DIR = os.path.join(BASE_DIR_C, 'registro')
CONN = 'conn'
CONN_SDE = 'conn_sde'
USERNAME = 'username'
INCLUDE_SYSTEM = 'include_system'
DELTA_ONLY = 'delta_only'
ANALYZE_BASE = 'analyze_base'
ANALYZE_DELTA = 'analyze_delta'
ANALYZE_ARCHIVE = 'analyze_archive'


OMITED_TABLES = ['calidda.caliddagis.vw_mtclientes_estadostipoinfo',
                 'calidda.caliddagis.vwg_consulta_proyectos',
                 'calidda.caliddagis.perfiles_herramientas_desktop',
                 'ia_bomberos']
