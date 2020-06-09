from packages import *
import pandas as pd
import tempfile
import uuid


def get_params_tool():
    path_params = os.path.join(tempfile.gettempdir(), '%s.txt' % uuid.uuid4().get_hex())
    params = get_parameters()
    df = pd.DataFrame.from_records(data=params, columns=['name', 'value'])
    df.to_csv(path_params, index=None, sep=' ', mode='a')
    arcpy.SetParameterAsText(0, path_params)


if __name__ == '__main__':
    get_params_tool()
