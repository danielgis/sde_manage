from manageodb import *


@scripttool_decore
def update_parameters(**kwargs):
    import packages
    for k, v in kwargs.items():
        if v == 'true':
            v = 1
        elif v == 'false':
            v = 0
        # arcpy.AddMessage('{}: {}'.format(k, v))
        packages.set_parameter(v, k)
    return 'success'


if __name__ == '__main__':
    params = dict()
    params[CONN] = arcpy.GetParameterAsText(0)
    params[USERNAME] = arcpy.GetParameterAsText(1)
    params[CONN_SDE] = arcpy.GetParameterAsText(2)
    params[INCLUDE_SYSTEM] = arcpy.GetParameterAsText(3)
    params[DELTA_ONLY] = arcpy.GetParameterAsText(4)
    params[ANALYZE_BASE] = arcpy.GetParameterAsText(5)
    params[ANALYZE_DELTA] = arcpy.GetParameterAsText(6)
    params[ANALYZE_ARCHIVE] = arcpy.GetParameterAsText(7)
    response = update_parameters(**params)
    arcpy.AddMessage(response)
