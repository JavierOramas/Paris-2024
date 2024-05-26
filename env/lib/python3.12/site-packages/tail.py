# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import time
import glob
from io import open
import click


def shared_open(filename, *args, **kwargs):
    if os.name == "nt":
        import win32file
        import msvcrt
        handle = win32file.CreateFile(
            filename,
            win32file.GENERIC_READ,
            win32file.FILE_SHARE_DELETE | win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None,
            )
        detached_handle = handle.Detach()
        fd = msvcrt.open_osfhandle(int(detached_handle), os.O_APPEND | os.O_RDONLY | os.O_TEXT)
        return os.fdopen(fd, *args, **kwargs)
    else:
        return open(filename, *args, **kwargs)



class TailReader(object):

    def __init__(self, filename, offset_file=None, read_from_end=False, encoding="utf-8", backup_patterns=None):
        self.filename = filename
        self.offset_file = offset_file or filename + ".offset"
        self.read_from_end = read_from_end
        self.encoding = encoding
        self.backup_patterns = backup_patterns
        self.fileobj = None
        self.fileobj_inode = 0
        self.fileobj_offset = 0

    def _read_offset_file(self):
        if not os.path.exists(self.offset_file):
            return 0, 0
        try:
            with open(self.offset_file, "r", encoding="utf-8") as fobj:
                inode, offset = [int(x) for x in fobj.readlines()[:2]]
                return inode, offset
        except:
            return 0, 0

    def _write_offset_file(self, inode, offset):
        with open(self.offset_file, "w", encoding="utf-8") as fobj:
            fobj.write(u"{0}\n".format(inode))
            fobj.write(u"{0}\n".format(offset))

    def _get_file_info(self, filename):
        try:
            info = os.stat(filename)
            return info.st_ino, info.st_size
        except:
            return 0, 0

    def _first_open(self):
        inode, offset = self._read_offset_file()
        target_file_inode, target_file_size = self._get_file_info(self.filename)
        if inode: # 如果有记录
            if inode != target_file_inode: # 记录的是旧文件
                # 根据inode及backup_patterns，找旧文件，如果找到旧文件，且有内容没有读完，则读完文件
                if self.backup_patterns:
                    for filename in glob.glob(self.backup_patterns):
                        old_inode, old_size = self._get_file_info(filename)
                        if inode == old_inode and offset < old_size:
                            self.fileobj = shared_open(filename, "r", encoding=self.encoding)
                            self.fileobj_filename = filename
                            self.fileobj_inode = inode
                            self.fileobj_offset = offset
                            return True
                # 找不到旧文件，或内容已经读完，则打开新文件
                self.fileobj = shared_open(self.filename, "r", encoding=self.encoding)
                self.fileobj_filename = self.filename
                self.fileobj_inode = target_file_inode
                self.fileobj_offset = 0
            else: # 记录的就是目标文件
                if offset > target_file_size: # 记录的位置大于文件大小，说明文件内容异常，从头读过
                    self.fileobj = shared_open(self.filename, "r", encoding=self.encoding)
                    self.fileobj_filename = self.filename
                    self.fileobj_inode = inode
                    self.fileobj_offset = 0
                else: # 记录的位置小于等于文件大小，说明文件内容正常，根据位置继续读取
                    self.fileobj = shared_open(self.filename, "r", encoding=self.encoding)
                    self.fileobj_filename = self.filename
                    self.fileobj_inode = inode
                    self.fileobj_offset = offset
                    self.fileobj.seek(offset, 0)
        else: # 如果没有记录
            self.fileobj = shared_open(self.filename, "r", encoding=self.encoding)
            self.fileobj_filename = self.filename
            self.fileobj_inode = target_file_inode
            if self.read_from_end: # 如果要求从结尾读取
                self.fileobj.seek(0, 2)
            else: # 如果不要求从结尾读取
                self.fileobj.seek(0, 0)
            self.fileobj_offset = self.fileobj.tell()


    def readlines(self):
        u"""按行读取文件，使用yield提供生成器类型结果。
        """
        # 如果文件未打开，则先打开文件
        if not self.fileobj:
            self._first_open()
        # 如果文件已打开，则读取该文件
        if self.fileobj:
            while True:
                line = self.fileobj.readline()
                if line:
                    yield line
                else:
                    break
            self.fileobj_offset = self.fileobj.tell()
            # 读完了旧文件，且新文件存在，就打开新文件吧
            target_file_inode, target_file_size = self._get_file_info(self.filename)
            if target_file_inode: # 新文件存在
                if target_file_inode != self.fileobj_inode: # 新文件存在，并且当前文件不是新文件
                    self.fileobj = shared_open(self.filename, "r", encoding=self.encoding)
                    self.fileobj_filename = self.filename
                    self.fileobj_inode = target_file_inode
                    self.fileobj_offset = 0
                else: # 新文件存在，并且当前文件就是新文件
                    if target_file_size < self.fileobj_offset: # 新文件内容变小了，重新从头读取
                        self.fileobj.seek(0, 0)
                        self.fileobj_offset = 0
                    else: # 新文件内容变大或不变，继续读取
                        pass
            else: # 新文件不存在
                current_inode, current_size = self._get_file_info(self.fileobj_filename)
                if current_inode == self.fileobj_inode: # 当前打开的文件，与当前记录的文件名，是同一文件
                    if current_size < self.fileobj_offset: # 当前文件内容变小了，重新从头读取
                        self.fileobj.seek(0, 0)
                        self.fileobj_offset = 0
                else:
                    pass # 当前打开的文件，与当前记录的文件名，不一致。正常不会出现，如果出现，继续等读着……

    def update_offset(self):
        if self.fileobj:
            self._write_offset_file(self.fileobj_inode, self.fileobj_offset)


def print_line(line):
    if line.endswith(u"\n"):
        print(line[:-1])
    elif line.endswith(u"\r"):
        print(line[:-1])
    elif line.endswith(u"\r\n"):
        print(line[:-2])
    else:
        print(line)


class LineCounter(object):
    def __init__(self, verboes=False):
        self.counter = 0
        self.verboes = verboes
    
    def update(self, line):
        self.counter += 1
        if self.verboes:
            print_line(line)

    def result(self):
        return self.counter


def tail(filename, line_handler, offset_file=None, read_from_end=False, encoding="utf-8", backup_patterns=None, sleep_interval=1, update_offset_every_n=100, non_blocking=False):
    filereader = TailReader(filename, offset_file, read_from_end, encoding, backup_patterns)
    total = 0
    while True:
        c = 0
        for line in filereader.readlines():
            line_handler(line)
            c += 1
            if c % update_offset_every_n:
                filereader.update_offset()
        total += c
        filereader.update_offset()
        if non_blocking:
            break
        if c < 1:
            time.sleep(sleep_interval)
    return total

@click.command()
@click.option("-o", "--offset-file", required=False, help=u"偏移量文件路径。默认为：在文件名后加.offset后缀。")
@click.option("-x", "--read-from-end", is_flag=True, help=u"如果不存在偏移量文件的话，指定该参数后则从文件的最后开始读取；不指定该参数的话则从文件开始读取。")
@click.option("-e", "--encoding", default="utf-8", help=u"文件读取编码，默认为utf-8。")
@click.option("-p", "--backup-patterns", help=u"文件可能通过logrotate等方式被备份出来，通过inode识别这些文件，先读取完备份文件中的剩余内容，再读取新文件内容。")
@click.option("-s", "--sleep-interval", type=int, default=1, help=u"读完文件后，休息一段时间后再续读。休息时间单位为：秒，默认为1秒。")
@click.option("-u", "--update-offset-every-n", type=int, default=100, help=u"每读取指定行后，更新偏移量文件。默认为100行。")
@click.option("-n", "--non-blocking", is_flag=True, help=u"指定该参数后，表示读取完文件内容后直接退出，同时sleep-interval参数无效；不指定的话则休眠sleep-interval秒后重新续读。")
@click.argument("filename", nargs=1, required=True)
def main(offset_file, read_from_end, encoding, backup_patterns, sleep_interval, update_offset_every_n, non_blocking, filename):
    u"""文件tail工具。引入“偏移量文件”记录文件读取信息，支持文件内容续读。
    """
    tail(filename, print_line, offset_file, read_from_end, encoding, backup_patterns, sleep_interval, update_offset_every_n, non_blocking)


if __name__ == "__main__":
    main()
