from ftplib import FTP
import config
import shutil

def ftp_login():
    ftp_object = FTP()
    ftp_object.encoding = config.FTP_ENCODING_TYPE
    ftp_object.connect(config.HOST,config.PORT)
    ftp_object.login(config.USER_NAME,config.USER_PASSWORD)
    return ftp_object


def ftp_upload(ftp_object, path_upload):
    if config.UPLOAD_FILE_NAME not in ftp_object.nlst(path_upload) or path_upload not in ftp_object.nlst():
        ftp_object.cwd(path_upload) 
        with open(config.UPLOAD_FILE_PATH,"rb") as file:
            ftp_object.storbinary("STOR " + config.UPLOAD_FILE_NAME, file, 1024)
    else:
        pass


def ftp_download(ftp_object,path_download):
    ftp_object.cwd(path_download)
    filenames = ftp_object.nlst()
    for filename in filenames:
        try:
            with open(filename,"wb") as file:
                if filename not in config.DOWNLOADED_FILE_NEW_PATH:
                    ftp_object.retrbinary("RETR "+ filename, file.write)
                else:
                    pass
            file.close()
        except Exception:
            pass


def redirect_to_download_location():
    shutil.move(config.DOWNLOADED_FILE_PATH, config.DOWNLOADED_FILE_NEW_PATH)


ftp = ftp_login()
ftp_upload(ftp,"files")
ftp_download(ftp,"files")
redirect_to_download_location()
ftp.quit()