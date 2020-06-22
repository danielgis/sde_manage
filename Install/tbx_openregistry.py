if __name__ == '__main__':
    from settings import *
    from messages import *
    import arcpy

    if not os.path.exists(REGISTRY_DIR):
        import pythonaddins

        arcpy.AddMessage(ERR_DIRLOG_NOT_EXIST)
        pythonaddins.MessageBox(ERR_DIRLOG_NOT_EXIST, TITLE_MESSAGE_BOX)
    registros = os.listdir(REGISTRY_DIR)
    if not len(registros):
        arcpy.AddMessage()
        pythonaddins.MessageBox(ERR_LOG_NOT_EXIST, TITLE_MESSAGE_BOX)
        arcpy.SetParameterAsText(0, ERR_LOG_NOT_EXIST)
    registros.sort(reverse=True)
    registro = os.path.join(REGISTRY_DIR, registros[0])
    arcpy.SetParameterAsText(0, registro)
