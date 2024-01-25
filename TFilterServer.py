from fastapi import FastAPI, File
from fastapi.responses import FileResponse
import TFilter
import uuid
import os
import shutil

app = FastAPI()

@app.get("/")
def printHello():
	return "This is TFilter Server. POST file to /upload"

## file upload test
@app.post("/filter")
def get_content_filter(file: bytes = File()):
    result = "None"
    UPLOAD_DIR = TFilter.config.uploadTempDir
    filename = str(uuid.uuid4())
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    try:
        data = file
        with open(filepath, "wb") as fp:
            fp.write(data)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)

        tf = TFilter.TFilter()
        tf.open(filepath)
        result = tf.get()
        if os.path.isfile(filepath):
             os.remove(filepath)
    except Exception as err:
        return {"message": f"There was an error uploading {file.filename}",
                "errMsg": f"{err}"}
    return result


@app.post("/image")
def image_zip_download(file: bytes = File()):
    result = "None"
    TEMP_DIR = TFilter.config.tempDir
    UPLOAD_DIR = TFilter.config.uploadTempDir
    upload_filename = str(uuid.uuid4())
    upload_filepath = os.path.join(UPLOAD_DIR, upload_filename)
    download_filename = upload_filename
    download_folder_path = UPLOAD_DIR
    dowload_filepath = os.path.join(download_folder_path, download_filename)

    try:
        data = file
        with open(upload_filepath, "wb") as fp:
            fp.write(data)
        tf = TFilter.TFilter()
        tf.filepath = upload_filepath

        temp_img_folder = os.path.join(TEMP_DIR, upload_filename)
        if not os.path.exists(temp_img_folder):
             os.makedirs(temp_img_folder)
        tf.extract_img(temp_img_folder)
        
        shutil.make_archive(dowload_filepath, 'zip', temp_img_folder)

        if os.path.exists(temp_img_folder):
             shutil.rmtree(temp_img_folder)
        if os.path.exists(upload_filepath):
             os.remove(upload_filepath)

        result = FileResponse(path=dowload_filepath+".zip", media_type="application/zip", filename=download_filename)
    except Exception as err:
        return {"message": f"There was an error uploading {file.filename}",
                "errMsg": f"{err}"}
    return result