# coding=utf-8
from tasks import *


class TaskBuilder(object):
    def __init__(self, mkvs):
        self.mkvs = mkvs

    def BuildTask(self, cxt, task):
        if task['id'] == 'ShellTask':
            return ShellTask(cxt, task['name'], parse_macro(task['cmd'], self.mkvs))
        elif task['id'] == 'LoadBuildbotInfoFile':
            return LoadBuildbotInfoFile(cxt)
        elif task['id'] == 'UpdBuildbotInfoFile':
            return UpdBuildbotInfoFile(cxt)
        elif task['id'] == 'GetCurRev':
            return LoadBuildbotInfoFile(cxt)
        elif task['id'] == 'UpdateSvn':
            return UpdateSvn(cxt)
        elif task['id'] == 'MakeLog':
            return MakeLog(cxt)
        elif task['id'] == 'MakeBuildbotEnv':
            return MakeBuildbotEnv(cxt)
        elif task['id'] == 'StartKcbp':
            return StartKcbp(cxt)

        return None
