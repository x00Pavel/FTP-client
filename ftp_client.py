from ftputil import FTPHost, error
from ftplib import FTP
import os
from builtins import open

USER_NAME = os.getlogin()
CMD = ["cd", "mkdir", "upload", "download", "os_ls", "ftp_ls", "help"]

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Host:
    def __init__(self):

        self.host = None
        while True:
            host = user_input("Set FTP server: ")
            if host == "":
                host = "192.168.0.81"
            
            try:
                self.host = FTP(host)
                break
            except Exception as e:
                print(e)
                info(["FTP server is not responsing, try again"])
                continue

        while True:
            user = user_input("Login: ")
            if user == "":
                user = "sammy"
            psswd = user_input("Password: ")
            if psswd == "":
                psswd = "1234"
                        
            try:
                self.host.login(user, psswd)
                break
            except Exception as e:
                print(e)
                info(["Wrong user info. Try again..."])
                continue
        info([self.host.getwelcome()])

    def change_dir(self, path, host="ftp"):
        try:
            if host == "ftp":
                self.host.cwd(path)
            else:
                os.chdir(path)
        except:
            info(["Path doesn't exits"])
            
    
    def show_dir(self, host="ftp"):
        if host == "ftp":
            self.host.nlst(self.host.pwd())
        else:
            info(os.listdir())

    def create_dir(self, name):
        self.host.mkd(name)

    def download(self):
        info(["Choose: download"])
        # TODO downloading

    def upload(self):
        src = user_input("Choose file or directory: ")
        if os.path.exists(os.path.abspath(src)):
            dst = user_input(f"Destination (default {src}): ")
            cur_dir = self.host.pwd() # save direcotry to return after uploading
            if dst == "":
                dst = src
            else:
                path_parts = dst.split("/")
                for part in path_parts[0:-1:1]:
                    if part not in self.host.nlst():
                        print_error(2, "/".join(path_parts[path_parts.index(part)::]))
                        answer = user_input("Do you want to create this folder? [yes(default)|no] ")
                        if answer == "yes":
                            self.create_dir(part)
                            self.change_dir(part)
                        elif answer == "no":
                            continue
                    else:
                        self.change_dir(part)
                
            if os.path.isdir(src):
                pass
            elif os.path.isfile(src):
                with open(src, "rb") as source:
                    self.host.storbinary(f"STOR {dst}", source)
                self.change_dir(cur_dir)
        else:
            print_error(2, src)

class Session:

    def __init__(self):
        while True:
            try:
                os.chdir(f"/home/{USER_NAME}/")
                self.ftp_host = Host()
                break
            except Exception as e:
                info([e])
                info(["There is problem with loging. Try again..."])
                continue

        self.keep_alive = True
    
    def close_session(self):
        self.keep_alive = False

def info(args=[""]):
    for item in args:
        print(f"ftp > {item}")


def user_input(string):
    return input(f"ftp > {string}")


def print_help():
    info([Colors.BOLD + "Commands:" + Colors.ENDC,
        "\thelp - print this help message",
        "\tcd <path> - change directory",
        "\tmkdir <path> - create directory",
        "\trm <path> - remove file",
        "\tos_ls - list current directory on system",
        "\tftp_ls - list current directory on ftp server",
        "\tupload - to start uploading process",
        "\tdownload - to start downloading process",
        "This commands similar in meaning to standart bash commands and can be inserted in any time of processing"])
        # TODO commands 


def print_error(code=0, *args):
    args = ": {}".format(" ".join(args)) if args is not None else ""
    if code == 1:
        print(Colors.FAIL + "Command do not exist" + args + Colors.ENDC)
    elif code == 2:
        print(Colors.FAIL + "Directory does not exist"  + args + Colors.ENDC)

def parse_input(session):
        answer = user_input("").lower()
        print(answer)
        if answer not in CMD:
            print_error(1)
        elif answer == "help":
            print_help()
        elif answer == "upload":
            session.ftp_host.upload()
        elif answer == "download":
            session.ftp_host.download()
        elif answer == "exit":
            session.close_session()

def main():
    try:
        session = Session()
        print_help()
        while session.keep_alive:
            parse_input(session)
    except KeyboardInterrupt:
        info([Colors.FAIL + "Force exit..." + Colors.ENDC])
    except Exception as e:
        info([e])
    finally:
        session.ftp_host.host.close()
        
if __name__ == "__main__":
    main()
