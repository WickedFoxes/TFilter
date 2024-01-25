from datetime import datetime
import olefile
import zlib
import os
import re

class Parser:
    def __init__(self):
        self.ole = None
        self.fileName = ""
        self.fileType = ""
        self.streamList = None

    def open(self, filepath):
        self.ole = olefile.OleFileIO(filepath)
        self.fileName = os.path.splitext(filepath)[0]
        self.fileType = os.path.splitext(filepath)[1]
        self.streamList = self.getOLEStreamList()

    def getOLEStreamList(self):
        sl = []
        for stream in self.ole.listdir(streams=True, storages=False):
            d = stream[0]
            if len(stream) > 1:
                d = ""
                for s in stream: d += (s+"/")
                d = d[:len(d)-1]
            sl.append(d)
        return sl

    def get_images(self, outfilepath):
        if(outfilepath[-1] != '/'):
            outfilepath = outfilepath + '/'
        
        imgNames = list()
        for stream in self.streamList:
            if('jpg' in stream or 'png' in stream or 'bmp' in stream):
                fileName = stream.replace("/", "_")
                imgNames.append(self.hwp_img_zlib(self.ole.openstream(stream).read(), outfilepath, fileName))
        return imgNames

    def hwp_img_zlib(self, binData, outfilepath, fileName):
        try:
            data = zlib.decompress(binData, -15)
        except:
            data = binData
        now = datetime.now().strftime("%Y%m%d_%H%M%S_")
        imgName = os.path.join(outfilepath, now + fileName)
        fp = open(imgName, 'wb')
        fp.write(data)
        fp.close()
        return imgName
    
    def close(self):
        self.ole.close()