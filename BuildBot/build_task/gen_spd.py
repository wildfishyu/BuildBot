import os, sys, re
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLTreeBuilder

PRJ_ROOT_PATH = '..\\'
SLN_DIR = 'solution'

SLN_FILENAME = 'KBSS.sln'
sln_prj = {'KBSS_WLFS': {'filters': ('lbm'), 'dll_name': 'KBSS_WLFS.dll'},
          }

SPD_FILENAME = 'KCBPSPD.xml'
spd_head = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<kcbpspd>
"""
spd_foot = """</kcbpspd>"""
spd_fmt = r' <program acm="public" cache="no" comment="" concurrence="-1" name="%s" path="%s" module="%s" node="0"  priority="1" rsl="1" timeout="60" type="biz" userexitnumber="10" xa="0"/>'

class MyXMLTreeBuild(XMLTreeBuilder):
  def __init_(self, html=0, target=None):
    XMLTreeBuilder.__init__(self, html, target)

  def feed(self, data):
    XMLTreeBuilder.feed(self, data.replace("gb2312","utf-8",1))

def get_prj_file(file_name):
  print file_name
  sln_file = open(file_name, 'r')
  sf = sln_file.read()
  sln_file.close()

  sln_dir = os.path.split(file_name)[0]

  prjs = []
  res = re.compile(r'Project\([\d\w"\{\-\}]*\)\s*=\s*"([\w.]*)"\s*,\s*"([\w.]*)"\s*,\s*')
  m = res.search(sf)
  while m is not None:
    prjs.append((m.group(1), sln_dir + '\\' + m.group(2)))
    m = res.search(sf, m.end())

  return prjs

def get_lbm_file(file_name, filters):
  print file_name
  lbm_dir = os.path.split(file_name)[0]

  tree = ElementTree()
  tree.parse(file_name, MyXMLTreeBuild())
  p = tree.findall('./Files/Filter')
  lbms = []
  if p is not None:
    for ele in p:
      if ele.attrib['Name'] in filters:
        fls = ele.getiterator('File')
        for f in fls:
          lbms.append(lbm_dir + '\\' + f.attrib['RelativePath'])
  return lbms

def parse_file(file_name):
  print file_name
  lbm_file = open(file_name, 'r')
  sf = lbm_file.read()
  sre = r"extern\s*\"C\"\s*\{\s*(XSDK|KBSS)_DLL_EXPORT\s*void\s*\*\s*(\w*)\s*\([\w\s\b&\*]*\)\s*;\}"
  m = re.search(sre, sf)
  lbm_file.close()
  if m is not None:
    return (os.path.splitext(os.path.split(file_name)[1])[0], m.groups()[1])

def main():
  sln_filepath = sys.argv[1]
  spd_filename = sys.argv[2]  #os.getenv('_SPD_FILE')
  if sln_filepath is None:
    sln_filepath = PRJ_ROOT_PATH + SLN_DIR + '\\' + SLN_FILENAME
  if spd_filename is None:
    spd_filename = SPD_FILENAME
		

  spd_file = open(spd_filename, 'w')
  spd_file.write(spd_head)

  prj_files = get_prj_file(sln_filepath)

  mod_info = [ ]
  for (prj_name, prj_file) in prj_files:
    prj_opt = sln_prj.get(prj_name)
    if prj_opt is not None:
      lbm_files = get_lbm_file(prj_file, prj_opt['filters'])
      lbms = []
      for lbm in lbm_files:
        r = parse_file(lbm)
        if r != None:
          lbms.append(r)
      if len(lbms) > 0:
        lbm_info = {}
        lbm_info['dll_name'] = prj_opt['dll_name']
        lbms.sort(cmp=lambda x, y: x[0] > y[0])
        lbm_info['lbms'] = lbms
        mod_info.append(lbm_info)

  for mod in mod_info:
      for lbm_id, lbm_name in mod['lbms']:
          sline = spd_fmt % (lbm_id, mod['dll_name'], lbm_name)
          spd_file.write(sline)
          spd_file.write('\n')
          #print sline

  spd_file.write(spd_foot)

if __name__ == '__main__':
  main()


