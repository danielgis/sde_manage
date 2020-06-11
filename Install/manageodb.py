import arcpy
import sys
from settings import *
from messages import *
from datetime import datetime
import pandas as pd


def scripttool_decore(func):
    def decorator(*args, **kwargs):
        registry = LogRegistry()
        registry.create_file_log()
        response, state, message = object(), 1, MSG_FINALLY_PROCESS_SUCCSSES
        try:
            response = func(*args, **kwargs)
        except AssertionError as e:
            state = 0
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = exc_obj.message
            line = exc_tb.tb_lineno
            message = 'Error: %s, Motivo: %s, Linea: %s' % ('ValidationError', msg, line)
        except Exception as e:
            state = 0
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = exc_obj.message
            line = exc_tb.tb_lineno
            message = 'Error: %s, Motivo: %s, Linea: %s' % (exc_type, msg, line)
        finally:
            registry.add_registry([message, state])
            return [response, state, message]

    return decorator


class LogRegistry(object):
    def __init__(self):
        self.path = LOG_FILE
        self.date = datetime.now().__str__()
        self.structure = [{'state': 1, 'message': MSG_CREATE_LOG_FILE, 'datetime': self.date}]
        self.df = None

    def create_file_log(self):
        if os.path.exists(self.path):
            return
        df = pd.DataFrame(self.structure)
        df.to_csv(self.path, index=False)

    def _get_dataframe_log(self):
        self.df = pd.read_csv(self.path)

    def add_registry(self, row):
        row.insert(0, datetime.now().__str__())
        self._get_dataframe_log()
        self.df = self.df.append(pd.Series(row, index=self.df.columns[:len(row)]), ignore_index=True)
        self.df.to_csv(self.path, index=False)

    def open_registry(self):
        if os.path.exists(self.path):
            os.startfile(self.path)


class ManageGeoDatabase(object):
    def __init__(self, **kwargs):
        self.datalist = list()
        self.conn = kwargs.get(CONN)
        self.conn_sde = kwargs.get(CONN_SDE)
        self.username = kwargs.get(USERNAME)

        # Reconstruccion de indices
        # Analisis de dataset
        self.include_system = int(kwargs.get(INCLUDE_SYSTEM))  # True, False
        self.delta_only = int(kwargs.get(DELTA_ONLY))  # True, False

        # Analisis de dataset
        self.analyze_base = int(kwargs.get(ANALYZE_BASE))  # True, False
        self.analyze_delta = int(kwargs.get(ANALYZE_DELTA))  # True, False
        self.analyze_archive = int(kwargs.get(ANALYZE_ARCHIVE))  # True, False

        self.registry = LogRegistry()
        self.registry.create_file_log()

    # def start_service(self, turn=True):
    # if not self.name_service:
    #     return 'No se especifico el nombre del servicio'
    # turn = 'start' if turn else 'stop'
    # command = 'runas /noprofile /user:administrator "net {} \'{}\'"'.format(turn, self.name_service)
    # subprocess.call(command)
    # pass

    def preprocess(self):
        arcpy.AddMessage(MSG_ACCEPT_CONECTION_FALSE)
        arcpy.AcceptConnections(self.conn, False)
        arcpy.AddMessage(MSG_DISCONNECT_USERS)
        arcpy.DisconnectUser(self.conn_sde, 'ALL')

    def compress(self):
        arcpy.AddMessage(MSG_COMPRESS)
        arcpy.env.workspace = ""
        arcpy.ClearWorkspaceCache_management(self.conn)
        arcpy.Compress_management(self.conn)
        print arcpy.GetMessages()

    def get_data_processing(self):
        arcpy.AddMessage(MSG_GET_DATA_PROCESSING)
        arcpy.env.workspace = self.conn
        fcs = arcpy.ListFeatureClasses()
        fts = arcpy.ListTables()
        frs = arcpy.ListRasters()

        data_list = fcs + fts + frs

        walk = map(lambda i: i[1], arcpy.da.Walk(self.conn, datatype="FeatureDataset"))
        dataset_list = walk[0]

        for ds in dataset_list:
            ws = os.path.join(self.conn, ds)
            arcpy.env.workspace = ws
            for fc in arcpy.ListFeatureClasses():
                data_list.append(os.path.join(ds, fc))

        data_list = filter(lambda i: self.username.lower() in i.lower(), data_list)

        for ot in OMITED_TABLES:
            for i, m in enumerate(data_list):
                if ot.lower() in m.lower():
                    del data_list[i]
                    break

        self.datalist = list(set(data_list))

        arcpy.AddMessage(MSG_DATA_LIST.format(len(self.datalist)))

    def rebuild_index(self):
        system = 'SYSTEM' if self.include_system else 'NO_SYSTEM'
        deltas = 'ONLY_DELTAS' if self.delta_only else 'ALL'
        self.get_data_processing()
        arcpy.AddMessage(MSG_REBUILD_INDEX)
        arcpy.RebuildIndexes_management(self.conn, system, self.datalist, deltas)
        print arcpy.GetMessages()

    def analyst_dataset(self):
        arcpy.AddMessage(MSG_ANALIZE_DATASET)
        system = 'SYSTEM' if self.include_system else 'NO_SYSTEM'
        base = 'ANALYZE_BASE' if self.analyze_base else 'NO_ANALYZE_BASE'
        deltas = 'ANALYZE_DELTA' if self.analyze_delta else 'NO_ANALYZE_DELTA '
        archive = 'ANALYZE_ARCHIVE' if self.analyze_archive else 'NO_ANALYZE_ARCHIVE '
        arcpy.AnalyzeDatasets_management(self.conn, system, '#', base, deltas, archive)
        print arcpy.GetMessages()

    def postprocess(self):
        arcpy.AddMessage(MSG_ACCEPT_CONECTION_TRUE)
        arcpy.AcceptConnections(self.conn, True)

    def main(self):
        self.preprocess()
        self.compress()
        self.rebuild_index()
        self.analyst_dataset()
        self.postprocess()
