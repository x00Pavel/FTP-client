from ftputil import FTPHost, error
from ftplib import FTP
from os import *
from builtins import open

USER_NAME = getlogin()


class MySession(FTP):

    def __init__(self, host, userid, password):
        FTP.__init__(self)
        try:
            self.connect(host)
        except:
            ftp_print("FTP server is not responsing, try again")

        try:
            self.login(userid, password)
        except:
            ftp_print("Cant to log in, try again")
        ftp_print(self.getwelcome())


def ftp_print(*args):
    for string in args:
        print(f"ftp > {string}")


def ftp_input(string=""):
    return input("ftp > " + string)


def main():
    ftp_host = None
    try:
        while True:
            server = ftp_input("Set server address: ")
            user = ftp_input("User: ")
            password = ftp_input("Password: ")
            try:
                ftp_host = FTPHost(server, user, password)
                break
            except error as e:
                ftp_print(e)

        keep_connection = True
        while keep_connection:
            ftp_print("", "Upload - 1", "Download - 2")
            action = int(ftp_input("Choose action: "))
            if action == 1:
                upload(ftp_host)
            elif action == 2:
                download(ftp_host)
            else:
                ftp_print("Wrong action, try again...")
                continue

    except KeyboardInterrupt:
        ftp_print("Force exit...")
        if ftp_host:
            ftp_host.close()


def download(ftp_host):
    pass


def upload(ftp_host):
    def upload_file(file, ftp_host):
        target = ftp_input(f"Destination file name (default {file}): ")
        ftp_print(path.abspath(file))
        ftp_print(type(path.abspath(file)))
        with open(path.abspath(file), 'rb') as source:
            with ftp_host.open(target, 'wb') as target:
                ftp_host.copyfileobj(source, target)

    source = ftp_input("Path to file: ")
    if not path.exists(source):
        ftp_print("File does not exist, try again...")
    else:
        if path.isdir(source):
            ftp_print(f"{source} is a directory.",
                      "1 - choose another file (default)",
                      f"2 - upload all files in {source}",
                      "3 - upload recursively")
            answer = None
            while True:
                answer = ftp_input("Choose command: ")
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
                        ftp_print("Unexpected command, please try again...")
                        continue

            if answer == 1:
                upload(ftp_host)
            elif answer == 2:
                chdir(path.dirname(path.abspath(source)))
                files = listdir(path.curdir)
                for file in files:
                    if path.isdir(file):
                        continue
                    else:
                        upload_file(file, ftp_host)

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
