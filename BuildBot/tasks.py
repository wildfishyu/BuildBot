#coding=utf-8

import sys, os
import urllib
import urllib2
from pysvn import PySVN
import config


def parse_macro(path, mkv):
    new_path = path
    for k, v in mkv:
        new_path = new_path.replace(k, v)
    return new_path


class Task:
    def __init__(self, context, name = 'Task'):
        self.context = context
        self.name = name

    def DoTask(self):
        self.PreTask()
        if not self._DoTask():
            raise Exception('%s - Do task exception.' % self.name.decode('utf-8'))
        self.PostTask()

    def PreTask(self):
        print 'Start Task: %s' % self.name.decode('utf-8')

    def PostTask(self):
        print 'End Task.'

    def _DoTask(self):
        print 'Task:_DoTask'
        return True


class ShellTask(Task):
    def __init__(self, context, name, cmd):
        Task.__init__(self, context, name)
        self.cmd = cmd

    def _DoTask(self):

        print 'Exec command: %s' % self.cmd
        if os.system(self.cmd) != 0:
            return False
        return True


class LoadBuildbotInfoFile(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        pf = open(self.context.buildbot_path + config.BUILDBOT_INFO_FILE)
        ver_file = pf.readlines()
        pf.close()

        for line in ver_file:
            kv = line.split('=')
            if kv[0] == 'last_rev':
                self.context.last_rev = int(kv[1])
            elif kv[0] == 'last_build':
                if self.context.ext_build_no <= 0:
                    self.context.build_no = int(kv[1]) + 1

        print 'Current Revision: %s' %self.context.last_rev
        return True


class UpdBuildbotInfoFile(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        lines = []
        pf = open(self.context.buildbot_path + config.BUILDBOT_INFO_FILE, 'w')
        lines.append('last_rev=%d\n' % (self.context.cur_rev))
        lines.append('last_build=%d\n' % (self.context.build_no))
        pf.writelines(lines)
        pf.close()
        return True


class GetCurRev(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        if self.context.cur_rev <= 0:
            pysvn = PySVN(self.context.svn_path)
            svn_info = pysvn.Info()
            self.context.cur_rev = int(svn_info['revision'])
        return True


class UpdateSvn(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        pysvn = PySVN(self.context.svn_path)
        if pysvn.Update() != 0:
            return False
        return True


class MakeLog(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        logs = []
        pysvn = PySVN(self.context.svn_path)
        if (self.context.cur_rev > self.context.last_rev):
            logs = pysvn.Log(self.context.last_rev + 1, self.context.cur_rev)

        lines = []
        pf = open(self.context.publish_pack_path + 'CHANGE.log', 'w')
        for log in logs:
            line = 'r%s: %s\n' % (log['revision'], log['msg'].encode('gbk'))
            pf.write(line)
        pf.close()
        return True

    def __GetSvnLogs(self):
        pysvn = PySVN(self.context.svn_path)
        return pysvn.Log(self.context.last_rev, self.context.cur_rev)

class PreProc(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        self.context.workspace = config.WORKSPACE
        exp_workspace = os.getenv('_BUILDBOT_WORKSPACE', '')
        if len(self.context.workspace) <= 0 and exp_workspace is not None:
            self.context.workspace = exp_workspace

        build_no = int(os.getenv('_BUILTBOT_BUILD_NO', '0'))
        if build_no > 0:
            self.context.build_no = self.context.ext_build_no = build_no
        self.context.cur_rev = int(os.getenv('_BUILTBOT_REV', '0'))

        mkv = (('%WORKSPACE%', self.context.workspace),)
        self.context.svn_path = parse_macro(config.SVN_PATH, mkv)
        self.context.solution_path = parse_macro(config.SOLUTION_PATH, mkv)
        self.context.solution = parse_macro(config.SOLUTION, mkv)
        self.context.publish_path = parse_macro(config.PUBLISH_PATH, mkv)

        return True

class MakeBuildbotEnv(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        self.context.publish_pack_name = config.VERSION_TAG
        self.context.publish_pack_path = '%s\\%s_%s_#%04d_r%d\\' % (self.context.publish_path,
                                                                self.context.build_date,
                                                                self.context.build_time,
                                                                self.context.build_no,
                                                                self.context.cur_rev)
        envs = (
                ('_BUILDBOT_WORKSPACE', self.context.workspace),
                ('_BUILDBOT_SVN_PATH', self.context.svn_path),
                ('_BUILDBOT_VERSION_TAG', config.VERSION_TAG),
                ('_BUILDBOT_SOLUTION', self.context.solution),
                ('_BUILTBOT_LAST_REV', str(self.context.last_rev)),
                ('_BUILTBOT_REV', str(self.context.cur_rev)),
                ('_BUILTBOT_BUILD_NO', str(self.context.build_no)),
                ('_BUILTBOT_BUILD_DATE', self.context.build_date),
                ('_BUILTBOT_BUILD_TIME', self.context.build_time),
                ('_BUILTBOT_PUBLISH_PACK_NAME', self.context.publish_pack_name),
                ('_BUILTBOT_PUBLISH_PACK_PATH', self.context.publish_pack_path),
                )

        for env_key, env_val in envs:
            print('%s: %s' % (env_key, env_val))
            os.putenv(env_key, env_val)

        return True

class StartKcbp(Task):
    def __init__(self, context):
        Task.__init__(self, context, self.__class__.__name__)

    def _DoTask(self):
        req = urllib2.Request(config.KCBP_CONTROL_SERVICE)
        response = urllib2.urlopen(req)
        print response.read()
        return True
