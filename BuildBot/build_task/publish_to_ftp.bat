@echo off
SET _BIN_PACK_DIR=%_BUILTBOT_PUBLISH_PACK_PATH%

set issue_server_ip=172.16.41.114
set issue_kbcp_dir=\KCBP\KCBP\KCBP\

set batch_ftp=%_BIN_PACK_DIR%\batch.ftp
cd %_BIN_PACK_DIR%
echo deploy > %batch_ftp%
echo deploy >> %batch_ftp%
echo binary >> %batch_ftp%
echo cd \KCBP\KCBP\KCBP\bin >> %batch_ftp%
echo put KBSS_WLFS.DLL KCBPSPD_wlfs.xml >> %batch_ftp%
echo quit >> %batch_ftp%

ftp -s:%batch_ftp% %issue_server_ip%
