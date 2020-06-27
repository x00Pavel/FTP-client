from ftputil import FTPHost, error
from ftplib import FTP
import builtins


def print(*args):
    for string in args:
        builtins.print("ftp > " + string)


def input(string=""):
    return builtins.input("ftp > " + string)



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


def download():
    pass

def upload():
    pass


def actions(ftp_host):
    keep_connection = True
    while keep_connection:
        print("", "Upload - 1", "Download - 2")
        action = int(input("Choose action"))
        if action == 1:
            upload()
        elif action == 2:
            download()
        else:
            print("Wrong action, try again...")
            continue
        



if __name__ == "__main__":
    ftp_host = None
    try:
        while True:
            server = input("Set server address: ")
            if server == "":
                server = "192.168.0.81"
            user = input("User: ")
            if user == "":
                user = "sammy"
            password = input("Password: ")
            if password == "":
                password = "1234"
            try:
                ftp_host =  FTPHost(server, user, password)
                break
            except error.PermanentError as e:
                print(e)
        
        actions(ftp_host)
        

        
    except KeyboardInterrupt:
        print("Force exit...")
        if ftp_host:
            ftp_host.close()
        # names = ftp_host.listdir(ftp_host.curdir)
    # for name in names:
    #     if ftp_host.path.isfile(name):
    #         ftp_host.download(name, name)  # remote, local
    # # Make a new directory and copy a remote file into it.
    # with ftp_host.open("~/test.txt", "rb") as source:
    #     with ftp_host.open("index.html", "wb") as target:
    #         ftp_host.copyfileobj(source, target)  # similar to shutil.copyfileobj
