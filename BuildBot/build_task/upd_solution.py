import os, sys, re
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import XMLTreeBuilder


class ProjectMaker:
    def __init__(self, prj_file, prj_src_dir):
        self._prj_file = prj_file
        self._prj_src_dir = prj_src_dir

    def Make(self):
        None

    def LoadFile(self, prj_file):
        tree = ElementTree()
        tree.parse(prj_file)
        filters = tree.findall('./Files/Filter')
        for filter in filters:
            dir_name = filter.attrib['Name']
            files = os.listdir(self.prj_src_dir + '\\' + dir_name)
            print files

def test():
    prj = ProjectMaker(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    test()






