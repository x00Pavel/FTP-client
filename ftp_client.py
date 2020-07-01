from ftputil import FTPHost, error
from ftplib import FTP
import builtins
from os import *

USER_NAME = getlogin()

class MySession(FTP):

    def __init__(self, host, userid, password):
        FTP.__init__(self)
        try:
            self.connect(host)
        except:
            print("FTP server is not responsing, try again")
        
        try:
            self.login(userid, password)
        except:
            print("Cant to log in, try again")
        print(self.getwelcome())


def print(*args):
    for string in args:
        builtins.print(f"ftp > {string}")


def input(string=""):
    return builtins.input("ftp > " + string)


def main():
    ftp_host = None
    try:
        while True:
            server = input("Set server address: ")
            user = input("User: ")
            password = input("Password: ")
            try:
                ftp_host = FTPHost(server, user, password)
                break
            except error as e:
                print(e)


        keep_connection = True
        while keep_connection:
            print("", "Upload - 1", "Download - 2")
            action = int(input("Choose action: "))
            if action == 1:
                upload(ftp_host)
            elif action == 2:
                download(ftp_host)
            else:
                print("Wrong action, try again...")
                continue

    except KeyboardInterrupt:
        print("Force exit...")
        if ftp_host:
            ftp_host.close()


def download(ftp_host):
    pass


def upload(ftp_host):
    
    def upload_file(file, ftp_host):
        target = input(f"Destination file name (default {file}): ")
        print(path.abspath(file))
        print(type(path.abspath(file)))
        with builtins.open(path.abspath(file), 'rb') as source:
            with ftp_host.open(target, 'wb') as target:
                ftp_host.copyfileobj(source, target)


    source = input("Path to file: ")
    if not path.exists(source):
        print("File does not exist, try again...")
    else:
        if path.isdir(source):
            print(f"{source} is a directory.", 
                  "1 - choose another file (default)",
                  f"2 - upload all files in {source}", 
                  "3 - upload recursively")
            answer = None
            while True:
                answer = input("Choose command: ")
                if answer == "":
                    break
                else:
                    try:
                        answer = int(answer)
                        if answer < 1 or answer > 3:
                            raise ValueError
                        else:
                            break
                    except ValueError:   
                        print("Unexpected command, please try again...")
                        continue
            if answer == 1:
                upload()
            elif answer == 2:
                chdir(path.dirname(path.abspath(source)))
                files = listdir(curdir())
                for file in files:
                    if path.isdir(file):
                        continue
                    else:
                        upload_file(file)
            elif answer == 3:
                items = walk(source)
                for item in items:
                    if not ftp_host.path.exists(item[0]):
                        ftp_host.mkdir(item[0])
                    ftp_host.chdir(item[0])
                    for file in item[2]:
                        upload_file(item[0] + "/" + file, ftp_host)

        else:
            upload_file(source, ftp_host)
            

if __name__ == "__main__":
    main()
