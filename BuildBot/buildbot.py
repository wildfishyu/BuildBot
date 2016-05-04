# coding=utf-8

import sys, os
from pysvn import PySVN
import config
import time
import taskbuilder
from tasks import *


class BuildBotContext:
    def __init__(self):
        self.last_rev = 0
        self.cur_rev = 0
        self.build_no = 0
        self.ext_build_no = 0
        self.build_date = ''
        self.build_time = ''
        self.workspace = ''
        self.svn_path = ''
        self.solution_path = ''
        self.solution = ''
        self.publish_path = ''
        self.publish_pack_name = ''
        self.publish_pack_path = ''
        self.buildbot_path = ''


class BuildBot:
    def __init__(self):
        self.tasks = []
        self.context = BuildBotContext()
        self.context.build_date = time.strftime('%Y%m%d')
        self.context.build_time = time.strftime('%H%M')

        self._MakeEvnPath()
        print self.context.build_date

    def _MakeEvnPath(self):
        self.context.workspace = config.WORKSPACE
        exp_workspace = os.getenv('_BUILDBOT_WORKSPACE', '')
        if len(self.context.workspace) <= 0 and exp_workspace is not None:
            self.context.workspace = exp_workspace

        build_no = int(os.getenv('_BUILTBOT_BUILD_NO', '0'))
        if build_no > 0:
            self.context.build_no = self.context.ext_build_no = build_no
        self.context.cur_rev = int(os.getenv('_BUILTBOT_REV', '0'))

        path = sys.argv[0].replace('/', '\\')
        self.context.buildbot_path = path[0 : path.rfind('\\')+1]

        mkv = (('%WORKSPACE%', self.context.workspace),)
        self.context.svn_path = parse_macro(config.SVN_PATH, mkv)
        self.context.solution_path = parse_macro(config.SOLUTION_PATH, mkv)
        self.context.solution = parse_macro(config.SOLUTION, mkv)
        self.context.publish_path = parse_macro(config.PUBLISH_PATH, mkv)

    def BuildTask(self):
        mkvs = mkv = (('%WORKSPACE%', self.context.workspace),
                      ('%BUILDBOT_PATH%', self.context.buildbot_path),
                      )
        builder = taskbuilder.TaskBuilder(mkvs)
        for task in config.TASKS:
            self.tasks.append(builder.BuildTask(self.context, task))

    def Run(self):
        for task in self.tasks:
            task.DoTask()
            print('\n')


if __name__ == '__main__':
    bot = BuildBot()
    bot.BuildTask()
    bot.Run()

