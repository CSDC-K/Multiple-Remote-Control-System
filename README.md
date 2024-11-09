# MRCS

## What is the MRCS?

__MRCS (Multiple Remote Control System)__ allows you to manage one or more computers on the _same network_: send them messages, transfer files, share your screen—these are just some of the tasks you can perform.

## how to use?

Converting .py Files to .exe
To convert Python (.py) files into executable (.exe) files, use the admin and client files. The admin file is the main administrative program, while the client file is managed through it.

__Important:__ Both the admin and client must be on the same network. If needed, you can adjust this setup for your own server by modifying the open-source code.

### Connection:
The admin program must be running before the client tries to connect. If the admin is not running, the client will not be able to connect.
The port number entered in the admin program must be the same as the one entered in the client.
Note: You only need to enter the port number once on the client.
If it is the first time running the client, it will not open. Simply close it and open it again.


### Conversion Process:
To convert the Python programs into .exe files, you can use the PyInstaller (recommended) or cx_Freeze module. After conversion, do not forget to share the "Source" folder when distributing the client file.


