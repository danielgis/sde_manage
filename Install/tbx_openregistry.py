if __name__ == '__main__':
    from settings import *
    from messages import *
    import arcpy

    if not os.path.exists(LOG_FILE):
        import pythonaddins

        arcpy.AddMessage(ERR_LOG_NOT_EXIST)
        pythonaddins.MessageBox(ERR_LOG_NOT_EXIST, TITLE_MESSAGE_BOX)
    arcpy.SetParameterAsText(0, LOG_FILE)
