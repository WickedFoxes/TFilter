import olefile

import config
import hwpImgParser

import re
import os
import platform
import subprocess


class TFilter:
    def __init__(self):
        self.filter = config.regularExpress
        self.osName = self.get_osName()
        self.filepath = ""
        self.content = b""
        
    def open(self, filepath):
        self.filepath = filepath
        self.content = self.get_content()

    def put(self, key, value):
        self.filter[key] = value

    def delete(self, key):
        del self.filter[key]
    
    def get(self):
        content_text = self.content.decode(encoding="utf-8")
        counts = dict()
        keys = list()
        values = dict()
        for key in self.filter.keys():
            keys.append(key)
            counts[key] = 0
            values[key] = list()

            reg = self.filter[key]
            pattern = re.compile(reg)
            items = pattern.finditer(content_text)
            for item in items: 
                values[key].append(item.group())
                counts[key] += 1
        result = {"keys" : keys, "counts" : counts, "values" : values}
        return result

    def get_content(self):
        if(self.osName == "Windows"):
            return self.get_content_win()
        return b""

    def get_content_win(self):
        content = b""

        cmd = "curl -T \""+ self.filepath + "\""\
				+ " \""+config.tikaServerName + "\""\
				+ " --header \"X-Tika-OCRLanguage: " + config.tikaOCRLang\
				+"\" --header \"Accept: text/plain\""
        print(cmd)
        content += subprocess.check_output(cmd, text=False)

        doc_type_cmd = "java -jar \"" + config.tikaDir + "\""\
                + " -d \"" + self.filepath + "\""
        doc_type = subprocess.check_output(doc_type_cmd, text=False)
        if(doc_type == b"application/x-hwp-v5\r\n"):
            content += self.extract_text_from_hwp_img()
        return content
    
    def extract_img(self, imgDir):
        if(self.osName == "Windows"):
            self.extract_img_win(imgDir)
    
    def extract_img_win(self, imgDir):
        cmd = "java -jar \"" + config.tikaDir + "\""\
                + " -z --extract-dir=\"" + imgDir + "\""\
                + " \"" + self.filepath + "\""
        subprocess.check_output(cmd, text=False)

        doc_type_cmd = "java -jar \"" + config.tikaDir + "\""\
                + " -d \"" + self.filepath + "\""
        doc_type = subprocess.check_output(doc_type_cmd, text=False)
        if(doc_type == b"application/x-hwp-v5\r\n"):
            self.extract_img_from_hwp(self.filepath, imgDir)

    def extract_img_from_hwp(self, filepath, outDir):
        hwpParser = hwpImgParser.Parser()
        hwpParser.open(filepath)
        imgNames = hwpParser.get_images(outDir)
        hwpParser.close()
        return imgNames

    def extract_text_from_hwp_img(self):
        imgNames = self.extract_img_from_hwp(self.filepath, config.tempDir)
        img_content = b""

        for imgPath in imgNames:
            cmd = "curl -T \""+ imgPath + "\""\
                    + " \""+config.tikaServerName + "\""\
                    + " --header \"X-Tika-OCRLanguage: " + config.tikaOCRLang\
                    +"\" --header \"Accept: text/plain\""
            img_content += (imgPath.split("/")[-1]+"\r\n").encode(encoding='UTF-8')
            img_content += subprocess.check_output(cmd, text=False)
        
        for imgPath in imgNames:
            if os.path.isfile(imgPath): 
                os.remove(imgPath)

        return img_content
    
    def get_osName(self):
        osName = platform.system()
        return osName
