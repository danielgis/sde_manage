import sqlite3
# from settings import *
from messages import *
from manageodb import *

registry = LogRegistry()
registry.create_file_log()

if not os.path.exists(CONN_SQLITE):
    registry.add_registry([0, ERR_CONN_SQLITE])
    raise RuntimeError(ERR_CONN_SQLITE)

conn = sqlite3.Connection(CONN_SQLITE, isolation_level=None, check_same_thread=False)
cursor = conn.cursor()


def package_decore(func):
    """
    Decorador de funciones de llamada a la base de datos SQLite
    :param func: Funcion que contiene la consulta sql
    :return: Retorna la nueva funcion
    """

    def decorator(*args, **kwargs):
        global conn, cursor
        package = func(*args, **kwargs)
        cursor.execute(package)
        if kwargs.get('iscommit'):
            # conn.commit()
            return
        elif kwargs.get('getcursor'):
            return cursor
        elif kwargs.get('returnsql'):
            return package
        return cursor.fetchall()

    return decorator


@package_decore
def get_conn_geodatabase():
    return "SELECT VALUE FROM TB_CONFIG WHERE NAME = 'conn'"


@package_decore
def get_parameters():
    return "SELECT NAME, VALUE FROM TB_CONFIG"


@package_decore
def get_parameter(*args):
    return "SELECT VALUE from TB_CONFIG WHERE NAME = '{}'".format(*args)


@package_decore
def set_parameter(value, name, iscommit=True):
    return "UPDATE TB_CONFIG SET VALUE = '{}' WHERE NAME = '{}'".format(value, name)
