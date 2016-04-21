SET _SLN_FILE=%_BUILDBOT_SOLUTION%
SET _SPD_FILE=%_BUILDBOT_SVN_PATH%\_BinR\KCBPSPD_wlfs.xml

echo %_SLN_FILE%
echo %_SPD_FILE%
python %~dp0gen_spd.py "%_SLN_FILE%" "%_SPD_FILE%"
