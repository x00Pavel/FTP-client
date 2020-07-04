from ftputil import FTPHost, error
from ftplib import FTP
import os
from builtins import open

USER_NAME = os.getlogin()

class Host:
    def __init__(self):

        self.host = None
        while True:
            host = user_input("Set FTP server: ")
            if host == "":
                host = "192.168.0.81"
            user = user_input("Login: ")
            if user == "":
                user = "sammy"
            psswd = user_input("Password: ")
            if psswd == "":
                psswd = "1234"
            
            try:
                self.host = FTPHost(host, user, psswd)
                break
            except:
                info(["FTP server is not responsing, try again"])
                continue

        self.actions = {"1": self.upload, 
               "upload": self.upload, 
               "2": self.download, 
               "download": self.download,
               "ftp_cd": self.change_dir}
            #    TODO commands

    def change_dir(self, path, host="ftp"):
        try:
            if host == "ftp":
                self.host.chdir(path)
            else:
                os.chdir(path)
        except:
            info(["Path doesn't exits"])
            
    
    def show_dir(self, host="ftp"):
        if host == "ftp":
            self.host.listdir(self.host.curdir)
        else:
            info(os.listdir())

    def download(self):
        info(["Choose: download"])
        # TODO downloading

    def upload(self):
        # self.show_dir()
        file = user_input("Choose file or directory: ")
        # TODO uploading


class Session:

    def __init__(self):
        while True:
            try:
                os.chdir(f"/home/{USER_NAME}/")
                self.ftp_host = Host()
            except:
                info(["There is problem with loging. Try again..."])
                continue

        self.keep_alive = True

    
def info(args=[""]):
    for item in args:
        print(f"ftp > {item}")


def user_input(string):
    return input(f"ftp > {string}")


def choose_action(host):
    info(["Choose action:", "\t1 - Upload", "\t2 - Download"])
    while True:
        action = user_input("")
        if action.lower() not in host.actions.keys():
            info(["Wrong command. Try again..."])
        else:
            return host.actions[action]


def print_cmd():
    info(["Commands:",
        "\tcd <path> - change directory",
        "\tmkdir <path> - create directory",
        "\trm <path> - remove file",
        "This commands similar in meaning to standart bash commands and can be inserted in any time of processing"])
        # TODO commands


def main():
    session = Session()
    print_cmd()
    while session.keep_alive:
        
        action = choose_action(session.ftp_host)
        try:
            action()
        except Exception as e:
            info([e])
            break

if __name__ == "__main__":
    main()