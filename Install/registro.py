from datetime import datetime
from settings import *
from messages import *


class LogRegistry(object):
    def __init__(self):
        self.date = datetime.today().__str__()
        self.name = 'registro_{}.txt'.format(datetime.today().strftime("%Y%m%d_%H%M%S"))
        self.structure = [{'state': 1, 'message': MSG_CREATE_LOG_FILE, 'datetime': self.date}]
        self.path = os.path.join(REGISTRY_DIR, self.name)
        self.data = list()

    def create_dir(self):
        if not os.path.exists(REGISTRY_DIR):
            os.makedirs(REGISTRY_DIR)

    def create_file(self):
        self.create_dir()
        with open(self.path, 'wb') as f:
            for i in self.data:
                f.write(str(i) + '\n')
            f.close()
        del f

    def add_row(self, row):
        self.data.append([row, datetime.today().__str__()])
