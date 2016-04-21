@echo off
SET _BIN_PACK_DIR=%_BUILTBOT_PUBLISH_PACK_PATH%

set issue_server_ip=172.16.41.114
set issue_kbcp_dir=\\%issue_server_ip%\d$\KCBP\KCBP\KCBP\bin\

net use \\%issue_server_ip% /del /yes
net use \\%issue_server_ip% "SZadmin898" /user:administrator

copy %_BIN_PACK_DIR%\*.* %issue_kbcp_dir%

call %issue_kbcp_dir%\merge_spd.bat
