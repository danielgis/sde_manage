from manageodb import *
from packages import *
from inspect import currentframe
import sys


@scripttool_decore
def manage_geodatabase_tool():
    arcpy.AddMessage(MSG_PROCESS_INI)
    cf = currentframe()
    registry.add_registry([MSG_PROCESS_INI, 1])

    params = dict()
    params[CONN] = get_parameter(CONN)[0][0]
    params[USERNAME] = get_parameter(USERNAME)[0][0]
    params[INCLUDE_SYSTEM] = get_parameter(INCLUDE_SYSTEM)[0][0]
    params[DELTA_ONLY] = get_parameter(DELTA_ONLY)[0][0]
    params[ANALYZE_BASE] = get_parameter(ANALYZE_BASE)[0][0]
    params[ANALYZE_DELTA] = get_parameter(ANALYZE_DELTA)[0][0]
    params[ANALYZE_ARCHIVE] = get_parameter(ANALYZE_ARCHIVE)[0][0]

    # Valida configuracion
    if not params[CONN]:
        raise RuntimeError('%s (line %s)' % (ERR_CONNGDB, cf.f_lineno))

    # Valida existencia de archivo de conexion a la gdb
    if not arcpy.Exists(params['conn']):
        raise RuntimeError('%s (line %s)' % (ERR_CONNGDB_PATH, cf.f_lineno))

    if not params[USERNAME]:
        raise RuntimeError('%s (line %s)' % (ERR_USERNAME, cf.f_lineno))
    if not params[INCLUDE_SYSTEM]:
        raise RuntimeError('%s (line %s)' % (ERR_INCLUDE_SYSTEM, cf.f_lineno))
    if not params[DELTA_ONLY]:
        raise RuntimeError('%s (line %s)' % (ERR_DELTA_ONLY, cf.f_lineno))
    if not params[ANALYZE_BASE]:
        raise RuntimeError('%s (line %s)' % (ERR_ANALYZE_BASE, cf.f_lineno))
    if not params[ANALYZE_DELTA]:
        raise RuntimeError('%s (line %s)' % (ERR_ANALYZE_DELTA, cf.f_lineno))
    if not params[ANALYZE_ARCHIVE]:
        raise RuntimeError('%s (line %s)' % (ERR_ANALYZE_ARCHIVE, cf.f_lineno))

    poo = ManageGeoDatabase(**params)
    poo.main()
    registry.add_registry([MSG_PROCESS_FIN, 1])
    arcpy.AddMessage(MSG_PROCESS_FIN)


if __name__ == '__main__':
    response = manage_geodatabase_tool()
    arcpy.AddMessage(response[1:])
    execute = sys.executable
    if sys.executable.endswith('ArcMap.exe'):
        import pythonaddins

        pythonaddins.MessageBox(response[-1], TITLE_MESSAGE_BOX)
    else:
        print(response[-1])
