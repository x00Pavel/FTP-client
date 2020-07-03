# FTP-client

Command line application for uploading and downloading data to and from FTP server. Now there is no support of TLS encryption, but maybe in future.. 

### Requirements

* Python3 with ftputils installed
For Python2 not tested

For installation on Linux system using snap 
`sudo snap install python38` 

### Use

1. write in terminal `python3 ftp_client.py`
2. insert address of FTP server
3. insert login and password for your account on server
4. if authentication succeed, then you will be asked for action: upload or download
5. choose one and then you will be offered to choose file to provide action 

## Specification

This FTP client provides basic manipulation with FTP server without any encryption (yet). It has two main functions: upload data to server and download from it.
For every operation ftputils creates new sub-session from main session. As result, connection is keeping alive.

### Commands

There are some commands that user can use to manipulate with server. This commands are similar in meaning in basic bash commands: 

* `h`, `help` - display basic information about commands and server
* `cd <directory name>` - change current directory on server
* `ls` - list all files in current directory
* `cp <source path> <destination path>` - copy files from given path. If it is directory,then user would be prommed to specify if copying should be recursive or not.
* `mkdir <directory name>` - create directory (if it is allowed by server)
* `rm <path>` - remove file on given path. If it is directory, then user would be prommed to specify if removing should be recursive or not.
* `perms` - display all permissions that user have on server
* `tree <directory name>` - display file structure from given directory (root directory by default) 
  
### Connecting to server

First of all there is step of connecting to required FTP server. User will be invited to input address of server and then specify login and password to 
users account. By default address of server should be in IPv4 format. Any another addresses are not supported yet. If address is not valid or credentials are not 
correct, then the user will be prompted to input is again.

After successful connecting to server, user should choose one of two options: upload or download files.

### Upload

This action allows user to specify path to upload. This path may be path to source file or directory. In case of file, it would be simply uploaded to given path 
or to current directory on server (by default it is root directory) to file with same name as source file. If some of directories are not exist on server, 
then missing would be created. 
 
 ### Downloading
 
This action allowed user to download specific file or folder from server. When user choose this action, then content of current directory is shown (output is 
similar to `ls` command). User should choose a file to download. If the selected file is directory, then user would be asked if necessary download recursively. 
