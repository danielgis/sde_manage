import threading

from packages import *
import pandas as pd
import tempfile
import uuid

path_params = os.path.join(tempfile.gettempdir(), '%s.txt' % uuid.uuid4().get_hex())


def openfile():
    os.startfile(path_params)


def get_params_tool():
    params = get_parameters()
    df = pd.DataFrame.from_records(data=params, columns=['name', 'value'])
    df.to_csv(path_params, index=None, sep=' ', mode='a')
    t = threading.Thread(target=openfile)
    t.start()
    t.join()


if __name__ == '__main__':
    get_params_tool()
