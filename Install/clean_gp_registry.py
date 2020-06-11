import os

import arcpy

workspace = arcpy.GetParameterAsText(0)
gp_history_xslt = arcpy.GetParameterAsText(1)
output_dir = arcpy.GetParameterAsText(2)
database_type = arcpy.GetParameterAsText(2)


def remove_history(work_space, gphistory_xslt, out_dir, db_type):
    elements = list()
    arcpy.env.workspace = work_space
    data_list = arcpy.ListFeatureClasses() + arcpy.ListTables()

    for fc in data_list:
        data_path = os.path.join(work_space, fc)
        if is_not_spatial_view(work_space, fc, db_type):
            elements.append(data_path)

    walk = map(lambda i: i[1], arcpy.da.Walk(work_space, datatype="FeatureDataset"))
    for fds in walk[0]:
        for fc in arcpy.ListFeatureClasses('', '', fds):
            data_path = os.path.join(work_space, fds, fc)
            if is_not_spatial_view(work_space, fc, db_type):
                elements.append(data_path)
                # try:
                #     remove_all(data_path, fc, gphistory_xslt, out_dir)
                # except Exception as e:
                #     arcpy.AddMessage(e.message)

    for i in elements:
        try:
            remove_all(i, gphistory_xslt, out_dir)
        except Exception as e:
            arcpy.AddMessage(e.message)


def is_not_spatial_view(work_space, fc, db_type):
    if db_type != "":
        desc = arcpy.Describe(fc)
        fc_name = desc.name
        egdb_conn = arcpy.ArcSDESQLExecute(work_space)
        egdb_return = 1

        if db_type == "SQLServer":
            db, schema, tb_name = fc_name.split(".")
            sql = r"IF EXISTS(SELECT * FROM SYS.VIEWS WHERE NAME = '{0}') SELECT 1 ELSE SELECT 0".format(
                tb_name.encode('utf-8'))
            egdb_return = egdb_conn.execute(sql)

        elif db_type == "Oracle":
            schema, tb_name = fc_name.split(".")
            sql = r"SELECT COUNT(*) FROM DUAL WHERE EXISTS (SELECT * FROM USER_VIEWS WHERE VIEW_NAME = '{0}')".format(
                tb_name.encode('utf-8'))
            egdb_return = egdb_conn.execute(sql)

        egdb_return = True if egdb_return else False
        return egdb_return
    else:
        return True


def remove_all(data_path, gphistory_xslt, out_dir):
    arcpy.ClearWorkspaceCache_management()
    feature = os.path.basename(data_path)
    name_xml = os.path.join(out_dir, str(feature)) + ".xml"

    arcpy.XSLTransform_conversion(data_path, gphistory_xslt, name_xml)
    arcpy.AddMessage("Completed xml coversion on {0}".format(feature))

    arcpy.MetadataImporter_conversion(name_xml, data_path)
    arcpy.AddMessage("Imported XML on {0}".format(feature))
    arcpy.GetMessages()


def make_dir(out_dir):
    if not arcpy.Exists(out_dir):
        os.mkdir(out_dir)


if __name__ == "__main__":
    make_dir(output_dir)
    remove_history(workspace, gp_history_xslt, output_dir, database_type)
