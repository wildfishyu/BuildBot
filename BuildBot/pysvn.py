# coding=utf-8
import os
import xml2dict


class PySVN(object):
    def __init__(self, local_path):
        self.local_path = local_path

    def __convert_data(self, data):
        rs = {}
        for (k, v) in data.items():
            rs[k] = v.get('value', '')
        return rs

    def Info(self):
        cmd = 'svn info --xml %s' % self.local_path
        rs = self._DoCmd(cmd)
        info_xml = ''.join(rs)
        info_xml = info_xml.replace('>\n', '>')

        x2d = xml2dict.XML2Dict()
        info_data = x2d.fromstring(info_xml)
        infos = self.__convert_data(info_data['info']['entry'])
        return infos

    def Log(self, start_rev, end_rev = 'HEAD'):
        cmd = 'svn log --xml -r %s:%s %s' % (start_rev, end_rev, self.local_path)
        rs = self._DoCmd(cmd)
        xml = ''.join(rs)
        xml = xml.replace('>\n', '>')

        x2d = xml2dict.XML2Dict()
        log_data = x2d.fromstring(xml)

        logs = []
        raw_logs = log_data['log']['logentry']
        if not isinstance(raw_logs, list):
            raw_logs = [raw_logs]
        for log in raw_logs:
            logs.append(self.__convert_data(log))
        return logs

    def Update(self):
        cmd = 'svn update %s' % self.local_path
        return os.system(cmd)

    def _DoCmd(self, cmd):
        print cmd
        rs = os.popen(cmd).readlines()
        return rs


if __name__ == '__main__':
    import config
    pysvn = PySVN(config.SVN_PATH)

    print pysvn.Info()
    print pysvn.Log(465)
