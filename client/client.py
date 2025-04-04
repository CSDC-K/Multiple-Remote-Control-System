import socket
import threading
from customtkinter import *
from screeninfo import get_monitors
import psutil
import ctypes
from vidstream import ScreenShareClient
from CTkMessagebox import *
import os
import cv2
import numpy as np
import psutil


class ClientApp:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientShare = None
        self.shareport = None
        self.remADDR = None

    def frontend(self):

        appdata_roaming = os.path.join(os.getenv('APPDATA'), 'MRCS')
        os.makedirs(appdata_roaming, exist_ok=True)
        file_path = os.path.join(appdata_roaming, 'portapp.txt')
        spfile_path = os.path.join(appdata_roaming, 'port.txt')
        shpfile_path = os.path.join(appdata_roaming, 'shport.txt')
        remfile_path = os.path.join(appdata_roaming, 'remadr.txt')
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read().strip()
                if content != '1':
                    self.entredPort = None
                    self.shentredPort = None
                    self.root = CTk()
                    self.root.title("İstemci | PORT SAYFASI")
                    self.root.geometry("400x400")
                    self.root.resizable(False, False)

                    set_appearance_mode("dark")



                    PortFrame = CTkFrame(self.root, fg_color="#404040", border_width=1, border_color="#FFFFFF", corner_radius=20, width=375, height=375)
                    PortFrame.place(x=12,y=12)

                    def enterport():
                        portDialog = CTkInputDialog(text="Port Giriniz", title="PORT YÖNLENDİRME",button_hover_color="#006600")
                        self.entredPort = portDialog.get_input()

                    def enterportSh():
                        shportDialog = CTkInputDialog(text="Port Giriniz", title="PORT YÖNLENDİRME",button_hover_color="#006600")
                        self.shentredPort = shportDialog.get_input()

                    def enterRem():
                        remtDialog = CTkInputDialog(text="Bağlantı Adresi:", title="ADRES YÖNLENDİRME",button_hover_color="#006600")
                        self.remADDR = remtDialog.get_input()

                    def cont():
                       
                        if not self.entredPort:
                            CTkMessagebox(title="HATA!", message="Port Girişi Yapmadınız!", icon="cancel",option_1="Tamam")
                            return
                        
                        elif not self.shentredPort:
                            CTkMessagebox(title="HATA!", message="Port Girişi Yapmadınız!", icon="cancel",option_1="Tamam")
                            return

                        
                        elif not self.remADDR:
                            CTkMessagebox(title="HATA!", message="Adres Girişi Yapmadınız!", icon="cancel",option_1="Tamam")
                            return

                        elif isinstance(self.entredPort, str):
                            try:
                                EnterdPORT = int(self.entredPort)
                                EntedSHARE = int(self.shentredPort)
                            except:
                                CTkMessagebox(title="HATA!", message="Portlara Metinsel Giriş Yapılamaz!", icon="cancel", option_1="Tamam")
                                return 


                        if os.path.exists(file_path):
                            with open(file_path, 'w') as fileP:
                                fileP.write("1")
                                fileP.close()

                            with open(shpfile_path, 'w') as fileSP:
                                fileSP.write(f"{self.shentredPort}")
                                fileSP.close()
                            
                            with open(spfile_path, 'w') as fileSH:
                                fileSH.write(f"{self.entredPort}")
                                fileSH.close()

                            with open(remfile_path, 'w') as fileSHR:
                                fileSHR.write(f"{self.remADDR}")
                                fileSHR.close()

                        self.root.destroy()
                        app.connect_to_server()

                    conaButton = CTkButton(PortFrame, text="Port Gir", font=("Helvetica", 15, "bold"), fg_color="#606060",
                              corner_radius=15, border_width=1, border_color="#FFFFFF", width=200, height=50,
                              hover_color="#006600", command=enterport)
                    conaButton.place(x=85,y=30)

                    convButton = CTkButton(PortFrame, text="Paylaşım Portu", font=("Helvetica", 15, "bold"), fg_color="#606060",
                              corner_radius=15, border_width=1, border_color="#FFFFFF", width=200, height=50,
                              hover_color="#006600", command=enterportSh)
                    convButton.place(x=85,y=120)


                    consButton = CTkButton(PortFrame, text="Yönetici Adresi", font=("Helvetica", 15, "bold"), fg_color="#606060",
                              corner_radius=15, border_width=1, border_color="#FFFFFF", width=200, height=50,
                              hover_color="#006600", command=enterRem)
                    consButton.place(x=85,y=210)

                    conssButton = CTkButton(PortFrame, text="Devam", font=("Helvetica", 15, "bold"), fg_color="#606060",
                              corner_radius=15, border_width=1, border_color="#FFFFFF", width=200, height=50,
                              hover_color="#006600", command=cont)
                    conssButton.place(x=85,y=300)
  


                    self.root.mainloop()          

                else:
                    app.connect_to_server() 



        else:
            with open(file_path, 'w') as file:
                file.write('0')


    def receive_messages(self):
        while True:
            raw_data = self.client_socket.recv(1024)
            message = raw_data.decode("utf-8")
            print(message)

            if message == "PCNAME":
                hostname = socket.gethostname()
                self.client_socket.send(hostname.encode())
            elif message == "MSGBOX":
                Message = self.client_socket.recv(1024).decode()
                MB_YESNO = 0x04
                ICON_STOP = 0x10

                def mess():
                    ctypes.windll.user32.MessageBoxW(0, Message, "Message from admin", MB_YESNO | ICON_STOP)

                threading.Thread(target=mess).start()
                print("OK")

            elif message == "SHUTDOWN":
                os.system("shutdown /p")

            elif message == "COPYFILEFROMSERVER":
                fileSizeSTR = self.client_socket.recv(1024).decode()
                print(fileSizeSTR)
                fileSize = int(fileSizeSTR)
                copyName = self.client_socket.recv(1024).decode("utf-8")
                print(fileSize)

                user_profile = os.environ["USERPROFILE"]
                documents_path = os.path.join(user_profile, "Documents")
                full_path = os.path.join(documents_path, copyName)


                with open(full_path, "wb") as copyFILE:
                    bytes_recived = 0
                    while bytes_recived < fileSize:
                        bytes_to_write = min(1024,fileSize - bytes_recived)
                        copyFILE.write(self.client_socket.recv(bytes_to_write))
                        bytes_recived += bytes_to_write


            elif message == "KILLTASK":
                import time
                taskpid = str(self.client_socket.recv(1024).decode("utf-8"))
                os.system(f"taskkill /f /im {taskpid}")






            elif message == "SHOWTASK":
                processes = []
                for proc in psutil.process_iter(['pid', 'name']):
                    processes.append(f"{proc.info['pid']}:{proc.info['name']}")

                processes_str = ",".join(processes) 
                print(processes_str)

                self.client_socket.sendall(processes_str.encode("utf-8"))
                print("ss")

            elif message == "UNLOCKALL":
                print("Ekran kilidi açılıyor...")
                os.system("start Sources\\Tools\\taskBypass.exe -t USIA72781SVAXQQQ__$FHBD")
                    
            elif message == "LOCKALL":
                print("Ekran kilitleniyor...")
                process_found = any(proc.name() == "taskLOCK.exe" for proc in psutil.process_iter())
                if process_found:
                    pass
                else:
                    os.system("start Sources\\Tools\\taskLOCK.exe -t QUSJZZZZ_SNQU431jsuuq@$")

            elif message == "SHARESCREEN":
                self.start_client()

            elif message == "STOPSHARE":
                try:
                    self.stop_share()
                except:
                    return

    def start_client(self):
        self.clientShare = ScreenShareClient("localhost", self.shareport)

        def client_thread():
            cv2.namedWindow("Share Screen", cv2.WINDOW_NORMAL)
            cv2.setWindowProperty("Share Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            for monitor in get_monitors():
                CLwidth = monitor.width
                CLheight = monitor.height

            while self.clientShare:  # clientShare None değilse devam et
                frame = self.clientShare._get_frame()
                
                if frame is not None:
                    height, width, _ = frame.shape
                    new_width = CLwidth
                    new_height = int((new_width / width) * height)

                    if new_height > CLheight:
                        new_height = CLheight
                        new_width = int((new_height / height) * width)

                    frame_resized = cv2.resize(frame, (new_width, new_height))
                    cv2.imshow("Share Screen", frame_resized)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("Boş çerçeve alındı.")

            cv2.destroyAllWindows()

        threading.Thread(target=client_thread).start()

    def stop_share(self):
        if self.clientShare:
            try:
                self.clientShare.stop_stream()
                self.clientShare = None  # Durum güncelleme
            except Exception as e:
                print(f"Excepted: {e}")

    def connect_to_server(self, host='localhost', port=252):
        appdata_roaming = os.path.join(os.getenv('APPDATA'), 'MRCS')
        spfile_path = os.path.join(appdata_roaming, 'port.txt')
        shpfile_path = os.path.join(appdata_roaming, 'shport.txt')
        remfile_path = os.path.join(appdata_roaming, 'remadr.txt')

        if os.path.exists(spfile_path):
            with open(spfile_path, 'r') as file:
                port = int(file.read())
        
        elif os.path.exists(shpfile_path):
            with open(shpfile_path, 'r') as file:
                self.shareport = int(file.read())

        elif os.path.exists(remfile_path):
            with open(shpfile_path, 'r') as file:
                host = file.read()

        try:
            self.client_socket.connect((host, port))
        except:
            return
        threading.Thread(target=self.receive_messages).start()


if __name__ == "__main__":
    app = ClientApp()
    app.frontend()
