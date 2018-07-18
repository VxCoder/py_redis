# -*- coding: utf-8 -*-
import string
import io


class sds(object):
    """ sds simple dynamic string 
    """
    SDS_MAX_PREALLOC = 1024 * 1024
    CHAR_TRANS = str.maketrans(string.whitespace, '.' * len(string.whitespace))

    def __init__(self, init_data=None, initlen: int=0):

        if init_data is None:
            self.buf = bytearray(initlen)
        else:
            if isinstance(init_data, str):
                self.buf = bytearray(init_data.encode('utf-8'))
                initlen = len(init_data)

            elif isinstance(init_data, bytes):
                self.buf = bytearray(init_data)
                initlen = len(init_data)

            elif isinstance(init_data, sds):
                self.buf = bytearray(init_data.buf)
                initlen = init_data.len + 1

            else:
                raise TypeError(f"not support {type(init_data)} now")

        self.len: int = initlen
        self.free: int = 0

    @classmethod
    def sdsempty(cls):
        return sds()

    @classmethod
    def sdsnew(cls, init_data):
        return sds(init_data)

    sdsup = sdsnew

    def sdslen(self):
        "T = O(1)"
        return self.len

    def sdsavail(self):
        "T = O(1)"
        return self.free

    def sdsclear(self):
        self.free += self.len
        self.len = 0

    def sdsMakeRoomFor(self, addlen):
        free = self.sdsavail()

        if free >= addlen:
            return self

        len = self.sdslen()
        newlen = len + addlen

        if newlen < self.SDS_MAX_PREALLOC:
            newlen *= 2
        else:
            newlen += self.SDS_MAX_PREALLOC

        self.free = newlen - len
        self.buf += bytearray(self.free)

    def sdsRemoveFreeSpace(self):
        self.buf = self.buf[:self.len]
        self.free = 0

    def sdsAllocSize(self):
        return self.free + self.len

    def sdsIncrLen(self, incr: int):
        assert(self.free >= incr)

        self.len += incr
        self.free -= incr

    def sdsgrowzero(self, len):

        if self.len >= len:
            return self

        self.sdsMakeRoomFor(len - self.len)
        total = self.sdsAllocSize()
        self.len = len
        self.free = total - self.len

        return self

    def sdscatlen(self, cat_sds, len):
        curlen = self.sdslen()
        self.sdsMakeRoomFor(len)

        for index, data in enumerate(cat_sds.buf):
            self.buf[curlen + index] = data

        self.len = curlen + len
        self.free -= len

        return self

    def sdscat(self, cat_sds):
        return self.sdscatlen(cat_sds, cat_sds.len)

    __add__ = sdscatsds = sdscat

    def __str__(self):
        return self.buf.decode("utf-8")

    def show_byte_array(self):
        total = len(self.buf)
        if total == 0:
            return ""

        width = len(hex(total)) - 2

        outstring = io.StringIO()
        print(" " * (width + 1), "{}".format(' '.join(f"{index:0>2x}" for index in range(16))), file=outstring)  # 标题行
        for start_post in range(0, total, 16):
            print(f"{start_post:0>{width}x}:", end=' ', file=outstring)
            print("{:<48}".format(' '.join(f"{data:0>2x}" for data in self.buf[start_post: start_post + 16])), end="  ", file=outstring)
            print(self.buf[start_post: start_post + 16].decode('utf-8').translate(self.CHAR_TRANS), file=outstring)

        return outstring.getvalue()

    def __repr__(self):
        return f"len {self.len}\nfree {self.free}\nbuf ==> \n{self.show_byte_array()}"


if __name__ == "__main__":
    a = sds('hello')
    print(f"{a!r}")
    b = sds('world')
    c = a + b + b
    print(f"{a!r}\n{b!r}")
