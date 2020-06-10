import os

import arcpy

''' Update the following five variables before running the script.'''
version = "10.4"
myWorkspace = r'C:\sde_addin_manage\admin.sde'
gp_history_xslt = r"C:\Program Files (x86)\ArcGIS\Desktop10.4\Metadata\Stylesheets\gpTools\remove geoprocessing history.xslt"
output_dir = r"C:\daniel\desarrollo\manage-gdb\sqlserver\gp-registry"
db_type = "SQL"  # Set this to either "SQL" or "Oracle" if your db has spatial views. If not you may set it to "".


def RemoveHistory(myWorkspace, gp_history_xslt, output_dir):
    arcpy.env.workspace = myWorkspace
    walk = map(lambda i: i[1], arcpy.da.Walk(myWorkspace, datatype="FeatureDataset"))
    # for fds in arcpy.ListDatasets('', 'feature') + ['']:
    for fds in walk[0]:
        for fc in arcpy.ListFeatureClasses('', '', fds):
            data_path = os.path.join(myWorkspace, fds, fc)
            if isNotSpatialView(myWorkspace, fc):
                try:
                    removeAll(data_path, fc, gp_history_xslt, output_dir)
                except Exception as e:
                    print e.message

def isNotSpatialView(myWorkspace, fc):
    if db_type != "":
        desc = arcpy.Describe(fc)
        fcName = desc.name
        egdb_conn = arcpy.ArcSDESQLExecute(myWorkspace)
        if db_type == "SQL":
            db, schema, tableName = fcName.split(".")
            print tableName
            sql = r"IF EXISTS(select * FROM sys.views where name = '{0}') SELECT 1 ELSE SELECT 0".format(tableName.encode('utf-8'))
            egdb_return = egdb_conn.execute(sql)
            if egdb_return == 0:
                return True
            else:
                return False
        elif db_type == "Oracle":
            schema, tableName = fcName.split(".")
            sql = r"SELECT count(*) from dual where exists (select * from user_views where view_name = '{0}')".format(
                tableName)
            egdb_return = egdb_conn.execute(sql)
            if egdb_return == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return True


def removeAll(data_path, feature, gp_history_xslt, output_dir):
    arcpy.ClearWorkspaceCache_management()
    name_xml = os.path.join(output_dir, str(feature)) + ".xml"

    arcpy.XSLTransform_conversion(data_path, gp_history_xslt, name_xml)
    print "Completed xml coversion on {0}".format(feature)

    arcpy.MetadataImporter_conversion(name_xml, data_path)
    print "Imported XML on {0}".format(feature)
    arcpy.GetMessages()


def makeDirectory(output_dir):
    if not arcpy.Exists(output_dir):
        os.mkdir(output_dir)


if __name__ == "__main__":
    makeDirectory(output_dir)
    RemoveHistory(myWorkspace, gp_history_xslt, output_dir)
