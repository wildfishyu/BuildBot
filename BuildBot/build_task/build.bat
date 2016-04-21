@ECHO OFF
set VS9=C:\Program Files (x86)\Microsoft Visual Studio 9.0

call "%VS9%\VC\vcvarsall.bat" x86

set sln=%_BUILDBOT_SVN_PATH%\solution\KBSS.sln
set platf=Win32
set conf=Release_MSSQL

set cmd=vcbuild /useenv %sln% %build% "%conf%|%platf%"
echo %cmd%
%cmd%
