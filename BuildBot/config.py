# coding=utf-8

#
# WORKSPACE = 'D:\\workset\\Welan\\WLFS_ISSUE\\'
WORKSPACE = ''
SVN_PATH = '%WORKSPACE%' + '\\KBSS_WLFS\\'

SOLUTION_PATH =  SVN_PATH + '\\solution\\'
SOLUTION = SOLUTION_PATH + '\\KBSS.sln'

VERSION_TAG = 'KBSS_WLFS_V1.0_SP4'

PUBLISH_PATH = '%WORKSPACE%' + '\\issue\\KBSS_WLFS\\'

KCBP_CONTROL_SERVICE = 'http://172.16.41.114:8001/restartkcbp'

# BUILDBOT_FILE`
BUILDBOT_INFO_FILE = 'buildbot.info'

TASKS = (
    {'id': 'LoadBuildbotInfoFile'},
    {'id': 'UpdateSvn'},
    {'id': 'GetCurRev'},
    {'id': 'MakeBuildbotEnv'},
    #{'id': 'ShellTask', 'name': 'Build Solution', 'cmd': '%BUILDBOT_PATH%\\build_task\\build.bat'},
    #{'id': 'ShellTask', 'name': 'Make KBSSSPD.XML', 'cmd': '%BUILDBOT_PATH%\\build_task\\bpxml.bat'},
    #{'id': 'ShellTask', 'name': 'Publish Pack', 'cmd': '%BUILDBOT_PATH%\\build_task\\publish_packet.bat'},
    #{'id': 'ShellTask', 'name': 'Publish To Kcbp', 'cmd': '%BUILDBOT_PATH%\\build_task\\publish_to_kcbp.bat'},
    #{'id': 'ShellTask', 'name': 'Publish To Kcbp', 'cmd': '%BUILDBOT_PATH%\\build_task\\publish_to_ftp.bat'},
    #{'id': 'UpdBuildbotInfoFile'},
    #{'id': 'StartKcbp'}
    {'id': 'ShellTask', 'name': 'UpdateProject', 'cmd': '%BUILDBOT_PATH%\\build_task\\upd_solution.bat'},
    )

