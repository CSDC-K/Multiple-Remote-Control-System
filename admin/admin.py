import customtkinter
import tkinter as tk
import ctypes
import threading
import socket
import numpy as np
import cv2
import mss
from vidstream import StreamingServer
import hPyT
import matplotlib.pyplot as plt
import os
from PIL import Image,ImageGrab
from customtkinter import *
from tkinter import Listbox, filedialog
from CTkMessagebox import CTkMessagebox
from pywinstyles import *
import hPyT
from hPyT import *


mainPageICO = Image.open("Sources\\Icons\\home.png")
devicesButICO = Image.open("Sources\\Icons\\devices.png")
settingsButICO = Image.open("Sources\\Icons\\settings.png")
conButICO = Image.open("Sources\\Icons\\conn.png")
adminLabelICO = Image.open("Sources\\Icons\\adminlabel.png")
fileTransferICO = Image.open("Sources\\Icons\\folder.png")
powerButICO = Image.open("Sources\\Icons\\power.png")
shareButICO = Image.open("Sources\\Icons\\share.png")
onlineLabelICO = Image.open("Sources\\Icons\\online.png")
offlineLabelICO = Image.open("Sources\\Icons\\offline.png")
docsButICO = Image.open("Sources\\Icons\\docs.png")
hpLabelICO = Image.open("Sources\\Icons\\hp.png")
greenDownICO = Image.open("Sources\\Icons\\downArrowGreen.png")
refreshButICO = Image.open("Sources\\Icons\\refresh.png")
enterPortAGButICO = Image.open("Sources\\Icons\\change.png")
warnLabICO = Image.open("Sources\\Icons\\warning.png")
sendMsgButICO = Image.open("Sources\\Icons\\sendmsg.png")
lockPcButICO = Image.open("Sources\\Icons\\locked.png")
unlockPcButICO = Image.open("Sources\\Icons\\unlock.png")
reshareButICO = Image.open("Sources\\Icons\\reshare.png")
killTaskButICO = Image.open("Sources\\Icons\\killTask.png")

class PortApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Yönetici | PORT SAYFASI")
        self.root.geometry("725x525")
        self.root.resizable(True, True)
        self.root.iconbitmap("Sources\\Icons\\WindowIcon.ico")

        self.root.minsize(width=725, height=525)
        self.root.maxsize(width=900, height=625)

        
        window_frame.center(self.root)

        # FRAME: PORT
        set_appearance_mode("dark")

        maximize_minimize_button.hide(self.root)

        PortFrame = CTkFrame(self.root, fg_color="#404040", border_width=1, border_color="#FFFFFF", corner_radius=20, width=600, height=450)
        PortFrame.pack(pady=25, padx=60, fill=tk.BOTH, expand=True)


        # LABELS
        mainTitle = CTkLabel(PortFrame, text="Başlangıç", font=("helvetica", 26, "bold"), text_color="#FFFFFF")
        mainTitle.pack(pady=(10, 20))

        # BUTTONS
        portButton = CTkButton(PortFrame, text="Port Gir", font=("Helvetica", 15, "bold"), fg_color="#606060",
                               corner_radius=15, border_width=1, border_color="#FFFFFF", width=250, height=50,
                               hover_color="#006600", command=self.Event_PortDialog)
        portButton.pack(pady=5)

        shareportButton = CTkButton(PortFrame, text="Paylaşım Portu", font=("Helvetica", 15, "bold"), fg_color="#606060",
                               corner_radius=15, border_width=1, border_color="#FFFFFF", width=250, height=50,
                               hover_color="#006600", command=self.Event_SharePortDialog)
        shareportButton.pack(pady=50)

        conButton = CTkButton(PortFrame, text="Devam", font=("Helvetica", 15, "bold"), fg_color="#606060",
                              corner_radius=15, border_width=1, border_color="#FFFFFF", width=250, height=50,
                              hover_color="#006600", command=self.Event_AdminPage)
        conButton.pack(pady=10)
        self.entredPort = None
        self.entredSharePort = None
        self.Sharing = False
        self.lock = threading.Lock()
        self.THmode = "DARKTH"
        self.WMmode = "ON"


    # EVENTS


    def Event_PortDialog(self):

        self.portDialog = CTkInputDialog(text="PORT:", title="PORT GİRİNİZ.", button_hover_color="#006600")
        self.entredPort = self.portDialog.get_input()

    def Event_SharePortDialog(self):

        self.ShareDialog = CTkInputDialog(text="PORT:", title="PAYLAŞIM PORTU GİRİNİZ.", button_hover_color="#006600")
        self.entredSharePort = self.ShareDialog.get_input()

    def show_M(self, message):
        MB_YESNO = 0x04
        ICON_STOP = 0x10
        threading.Thread(target=lambda: ctypes.windll.user32.MessageBoxW(0, message, "HATA", MB_YESNO | ICON_STOP)).start()

    def Event_AdminPage(self):
        if not self.entredPort:
            CTkMessagebox(title="HATA!", message="Port Girişi Yapmadınız!", icon="cancel",option_1="Tamam")
            return
        
        elif not self.entredSharePort:
            CTkMessagebox(title="HATA!", message="Port Girişi Yapmadınız!", icon="cancel",option_1="Tamam")
            return



        elif isinstance(self.entredPort, str):
            try:
                EnterdPORT = int(self.entredPort)
                EntedSHARE = int(self.entredSharePort)
            except:
                CTkMessagebox(title="HATA!", message="Portlara Metinsel Giriş Yapılamaz!", icon="cancel", option_1="Tamam")
                return 
            

        portApp.destroy()

        self.entredPort = str(self.entredPort)
        AppPATH = os.environ["APPDATA"]

        try:
            os.makedirs(AppPATH + "\\MRCS\\CONN", exist_ok=True)
            with open(AppPATH + "\\MRCS\\CONN\\port.txt", "w") as PortW:
                PortW.write(self.entredPort)

        except Exception as e:
            pass

        
        self.ShareServer = StreamingServer("localhost", int(self.entredPort))


        clients = {}
        def sendMessageToClient(client_name, message):
            client_socket = clients.get(client_name)
            if client_socket:
                try:
                    client_socket.send(message.encode('utf-8'))
                except:
                    del clients[client_name]
            else:
                pass

            #for client_name in disconnected_clients:
            #    del clients[client_name]


        def handle_client(client_socket, address):
            client_name = "Bilinmiyor"
            try:
                client_socket.send("PCNAME".encode("utf-8"))
                client_name = client_socket.recv(1024).decode('utf-8')
                clients[client_name] = client_socket
            except Exception as e:
                print(f"Error handling client connection: {e}")
                client_socket.close()
                return

            while True:
                try:
                    message = client_socket.recv(1024)
                    if not message:
                        break
                except Exception as e:
                    print(f"Error receiving message from {client_name}: {e}")
                    break

            if client_name in clients:
                del clients[client_name]
            client_socket.close()


        def start_server(host='0.0.0.0', port=int(self.entredPort)):
            global server
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((host, port))
            server.listen()

            while True:
                client_socket, address = server.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
                client_thread.start()

        def list_connected_clients():
            print("Bağlı bilgisayarlar:")
            for client_name in clients:
                print(client_name)


        def sendMessage(command,msg):
            print(command)
        


            if command == "MSGBOX":
                for client_name,client_socket in clients.items():
                    client_socket.send("MSGBOX".encode("utf-8"))
                    client_socket.send(msg.encode("utf-8"))

            elif command == "SHUTDOWN":
                for client_name,client_socket in clients.items():
                    client_socket.send("SHUTDOWN".encode("utf-8"))

            elif command == "LOCKALL":

                for client_name,client_socket in clients.items():
                    client_socket.send("LOCKALL".encode("utf-8"))


            elif command == "UNLOCKALL":

                for client_name,client_socket in clients.items():
                    client_socket.send("UNLOCKALL".encode("utf-8"))
        

            elif command == "SHARESCREEN":
                with self.lock:
                    if not self.Sharing:
                        for client_name, client_socket in clients.items():
                            client_socket.send("SHARESCREEN".encode("utf-8"))
                        self.Sharing = True
                        threading.Thread(target=self.ShareServer.start_server).start()
                        print(self.Sharing)

                        connStatLab.configure(image=CTkImage(dark_image=onlineLabelICO, size=(35, 35)))
                    else:
                        self.show_M("2. kez ekran paylaşım başlatılamaz.")

            elif command == "STOPSHARE":
                with self.lock:
                    if self.Sharing:
                        try:
                            for client_name, client_socket in clients.items():
                                client_socket.send("STOPSHARE".encode("utf-8"))
                            self.ShareServer.stop_server()
                            connStatLab.configure(image=CTkImage(dark_image=offlineLabelICO, size=(35, 35)))
                            self.Sharing = False
                        except Exception as e:
                            print(f"EXCEPTED: {e}")
                    else:
                        self.show_M("Ekran paylaşımı zaten yok.")

            elif command == "SingledTask":
                SgApp = CTkToplevel(adminApp)
                SgApp.title("Tekli Görevlendirme")
                SgApp.iconbitmap("Sources\\Icons\\WindowIcon.ico")
                SgApp.geometry("300x300")
                SgApp.resizable(False,False)
                SgApp.grab_set()
                SgFrame = CTkFrame(SgApp, fg_color="#202020", border_width=1, border_color="#33FFFF", corner_radius=20, width=275, height=275)
                SgFrame.place(x=12, y=12)

                def selectedClient(event=None):
                    import time
                    selected_index = clientList.curselection()

                    if selected_index:
                        selectedClient = clientList.get(selected_index)


                        ClientApp = CTkToplevel(SgApp)
                        ClientApp.title("Tekli Görevlendirme")
                        ClientApp.iconbitmap("Sources\\Icons\\WindowIcon.ico")
                        ClientApp.geometry("500x500")
                        ClientApp.resizable(False,False)
                        ClientApp.grab_set()
                        ClientFrame = CTkFrame(ClientApp, fg_color="#202020", border_width=1, border_color="#33FFFF", corner_radius=20, width=450, height=450)
                        ClientFrame.place(x=25, y=25)

                        def SEvent_Close():
                            for client_name,client_socket in clients.items():
                                if client_name == selectedClient:
                                    client_socket.send("SHUTDOWN".encode("utf-8"))                    

                        def SEvent_Lock():
                            for client_name,client_socket in clients.items():
                                if client_name == selectedClient:
                                    client_socket.send("LOCKALL".encode("utf-8"))   

                        def SEvent_UnLock():
                            for client_name,client_socket in clients.items():
                                if client_name == selectedClient:
                                    client_socket.send("UNLOCKALL".encode("utf-8"))   
                        def SEvent_MSG():

                            MsgContentDialog = CTkInputDialog(text="Mesaj", title=f"Gönderilecek Mesajı Seçiniz:{selectedClient}", button_hover_color="#006600")
                            MsgContent = MsgContentDialog.get_input()

                            for client_name,client_socket in clients.items():
                                if client_name == selectedClient:
                                    client_socket.send("MSGBOX".encode("utf-8"))   
                                    client_socket.send(MsgContent.encode("utf-8"))


                        def SEvent_taskKiller():
                            def SEvent_refTasks():
                                for client_name,client_socket in clients.items():
                                    if client_name == selectedClient:
                                        client_socket.send("SHOWTASK".encode("utf-8"))
                                        tasklists = client_socket.recv(20024).decode("utf-8")

                                taskList.delete(0,tk.END)
                                for insDe in tasklists.split(","):
                                    taskList.insert(tk.END,insDe)
                                     
                            taskApp = CTkToplevel(ClientApp)
                            taskApp.title("Tekli Görevlendirme")
                            taskApp.iconbitmap("Sources\\Icons\\WindowIcon.ico")
                            taskApp.geometry("300x300")
                            taskApp.resizable(False,False)
                            taskApp.grab_set()
                            taskFrame = CTkFrame(taskApp, fg_color="#202020", border_width=1, border_color="#33FFFF", corner_radius=20, width=275, height=275)
                            taskFrame.place(x=12, y=12)

                            def taskENDEr(event=None):
                                selected_taskindex = taskList.curselection()
                                print(selected_taskindex)

                                if selected_taskindex:
                                    selectedTask = taskList.get(selected_taskindex)
                                    print(selectedTask)
                                    pid = selectedTask.split(':')[1]
                                    print(pid)

                                    for client_name,client_socket in clients.items():
                                        if client_name == selectedClient:
                                            client_socket.send("KILLTASK".encode("utf-8"))
                                            client_socket.send(str(pid).encode("utf-8"))

                                

                            taskList = Listbox(taskFrame,bg="#404040",fg="#FFFFFF",selectmode=tk.SINGLE,width=25,height=15)
                            taskList.place(x=37,y=23)


                            for client_name,client_socket in clients.items():
                                if client_name == selectedClient:
                                    client_socket.send("SHOWTASK".encode("utf-8"))
                                    tasklists = client_socket.recv(20024).decode("utf-8")
                                    

                            for insDe in tasklists.split(","):
                                taskList.insert(tk.END,insDe)

                            taskList.bind('<<ListboxSelect>>',taskENDEr)
                        
                            refTask = CTkButton(taskFrame,text="Yenile", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=45,height=40,command=SEvent_refTasks)
                            refTask.place(x=200,y=100)


                        def SEvent_transferFile():
                            def copyFileSEL(event=None):
                                import time
                                selectedFile = filedialog.askopenfilename()
                                if not selectedFile:
                                    return
                                selectedFileSize = str(os.path.getsize(selectedFile))
                                selectedfileName = os.path.basename(selectedFile)

                                with open(selectedFile, "rb") as sendFile:
                                    for client_name, client_socket in clients.items():

                                        if client_name == selectedClient:
                                            client_socket.send("COPYFILEFROMSERVER".encode("utf-8"))
                                            time.sleep(0.1)
                                            client_socket.send(selectedFileSize.encode())
                                            time.sleep(0.1)
                                            client_socket.send(f"{selectedfileName}".encode("utf-8"))
                                            time.sleep(0.1)
                                            fileContent = sendFile.read(1024)
                                            while fileContent: 
                                                client_socket.send(fileContent)
                                                fileContent = sendFile.read(1024)
                                            
                                            self.show_M(f"Transfer Bitti: Belgeler/{selectedfileName}")

                                    
                                        else:
                                            pass

                            threading.Thread(target=copyFileSEL).start()
                        

                        selectedClientLabel = CTkLabel(ClientApp, text=f"Seçili Cihaz: {selectedClient}", font=("helvetica", 20, "bold"), text_color="#FFFFFF")
                        selectedClientLabel.place(x=85, y=35)

                        CloseClient = CTkButton(ClientFrame,text="Kapat", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=powerButICO),command=SEvent_Close)
                        CloseClient.place(x=15,y=50)

                        LockClient = CTkButton(ClientFrame,text="Kilitle", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=lockPcButICO),command=SEvent_Lock)
                        LockClient.place(x=15,y=100)

                        UnLockClient = CTkButton(ClientFrame,text="Kilidi Aç", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=unlockPcButICO),command=SEvent_UnLock)
                        UnLockClient.place(x=15,y=150)

                        sendMessageClient = CTkButton(ClientFrame,text="Mesaj Gönder", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=sendMsgButICO),command=SEvent_MSG)
                        sendMessageClient.place(x=15,y=200)

                        shareClient = CTkButton(ClientFrame,text="Dosya Paylaş", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=fileTransferICO),command=SEvent_transferFile)
                        shareClient.place(x=15,y=250)

                        killTaskClient = CTkButton(ClientFrame,text="Görev Sonlandır", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=145,height=40,image=CTkImage(dark_image=killTaskButICO),command=SEvent_taskKiller)
                        killTaskClient.place(x=15,y=300)

                        

                clientList = Listbox(SgApp,bg="#404040",fg="#FFFFFF",selectmode=tk.SINGLE,width=25,height=15)
                clientList.place(x=70,y=25)
                for insDe in clients:
                    clientList.insert(tk.END,insDe)

                clientList.bind('<<ListboxSelect>>',selectedClient)


            elif command == "COPYFILEFROMSERVER":

                def copyFileSEL(event=None):
                    import time
                    selectedFile = filedialog.askopenfilename()
                    if not selectedFile:
                        return
                    selectedFileSize = str(os.path.getsize(selectedFile))
                    selectedfileName = os.path.basename(selectedFile)

                    with open(selectedFile, "rb") as sendFile:
                        for client_name, client_socket in clients.items():

                            client_socket.send("COPYFILEFROMSERVER".encode("utf-8"))
                            time.sleep(0.1)
                            client_socket.send(selectedFileSize.encode())
                            time.sleep(0.1)
                            client_socket.send(f"{selectedfileName}".encode("utf-8"))
                            time.sleep(0.1)

                            fileContent = sendFile.read(1024)
                            while fileContent: 
                                client_socket.send(fileContent)
                                fileContent = sendFile.read(1024)

                            self.show_M(f"Transfer Bitti: Belgeler/{selectedfileName}")

                threading.Thread(target=copyFileSEL).start()




        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()





        adminApp = CTk()
        adminApp.title("Yönetici | ANA SAYFA")
        adminApp.geometry("1280x960")
        adminApp.resizable(True, True)
        adminApp.iconbitmap("Sources\\Icons\\WindowIcon.ico")

        window_frame.center(adminApp)
        maximize_minimize_button.hide(adminApp)

        # Minimum boyut ayarı
        adminApp.minsize(width=1024, height=768)

        # Maksimum boyut ayarı
        adminApp.maxsize(width=1280, height=960)


        # FRAME: ADMIN
        set_appearance_mode("dark")
        MainFrame = CTkFrame(adminApp, fg_color="#404040", border_width=2, border_color="#33FFFF", corner_radius=15)
        MainFrame.grid(row=0, column=1, padx=5, pady=25, sticky="nsew")

        # FRAME: SOL PANEL
        LeftFrame = CTkFrame(adminApp, fg_color="#404040", border_width=2, border_color="#33FFFF", corner_radius=15)
        LeftFrame.grid(row=0, column=0, padx=5, pady=25, sticky="ns")

        # Pencere genişliği ve yüksekliğini ayarlayın
        adminApp.grid_rowconfigure(0, weight=1)
        adminApp.grid_columnconfigure(1, weight=1)



        def Event_SendMSG():
            GoMSG = CTkInputDialog(text="Mesaj:", title="MESAJ GÖNDERME", button_hover_color="#006600")
            sendMessage(command="MSGBOX",msg=GoMSG.get_input())

        def Event_ShutDownALL():
            sendMessage(command="SHUTDOWN",msg=None)

        def Event_LockALL():
            sendMessage(command="LOCKALL",msg=None)

        def Event_UnLockALL():
            sendMessage(command="UNLOCKALL",msg=None)

        def Event_ShareScreen():
            sendMessage(command="SHARESCREEN",msg=None)

        def Event_StopShareScreen():
            sendMessage(command="STOPSHARE",msg=None)

        def Event_CopyFileFromClient():
            sendMessage(command="COPYFILEFROMSERVER",msg=None)

        def Event_SingleTask():
            sendMessage(command="SingledTask",msg=None)

        def Event_RefUser():

            userD.delete(0,tk.END)

            for insDe in clients:
                userD.insert(tk.END,insDe)


        def Event_SettingsPage():
            settingsPage = CTkToplevel(adminApp)
            settingsPage.title("Yönetici || Ayarlar Sayfası")
            settingsPage.geometry("300x300")
            settingsPage.iconbitmap("Sources\\Icons\\WindowIcon.ico")

            settingsPage.resizable(False,False)

            settingsPage.grab_set()

            settFrame = CTkFrame(settingsPage, fg_color="#404040", border_width=1, border_color="#33FFFF", corner_radius=20, width=250, height=250)
            settFrame.place(x=25, y=25)

            def Event_dwModeSW():
                if dwModeSW.get() == "DarkTH":
                    set_appearance_mode("dark")
                    self.THmode="DARKTH"
                    LeftFrame.configure(border_color="#33FFFF",border_width=2)
                    MainFrame.configure(border_color="#33FFFF",border_width=2)
                    adminApp.update()

                if dwModeSW.get() == "WhiteTH":
                    set_appearance_mode("light")
                    self.THmode="LIGHTH"
                    LeftFrame.configure(border_color="#000000",border_width=3)
                    MainFrame.configure(border_color="#000000",border_width=3)
                    adminApp.update()

            def Event_mmMode():
                if mmMode.get() == "NO":
                    self.WMmode = "OFF"
                    maximize_minimize_button.unhide(adminApp)

                if mmMode.get() == "YES":
                    self.WMmode = "ON"
                    maximize_minimize_button.hide(adminApp)
                


            setLab = CTkLabel(settFrame, text="Ayarlar", font=("helvetica", 25, "bold"), text_color="#FFFFFF")
            setLab.place(x=275, y=45)

            if self.THmode == "DARKTH":

                dwModeSW = CTkSwitch(settFrame,text="Tema",text_color="#FFFFFF", offvalue="DarkTH",onvalue="WhiteTH", command=Event_dwModeSW)
                dwModeSW.deselect()
                dwModeSW.place(x=10,y=25)

            else:
                dwModeSW = CTkSwitch(settFrame,text="Tema",text_color="#FFFFFF", offvalue="DarkTH",onvalue="WhiteTH", command=Event_dwModeSW)
                dwModeSW.select()
                dwModeSW.place(x=10,y=25)

            if self.WMmode == "OFF":
                mmMode = CTkSwitch(settFrame,text="Pencere Butonlarını Göster",text_color="#FFFFFF", offvalue="NO",onvalue="YES", command=Event_mmMode)
                mmMode.deselect()
                mmMode.place(x=10,y=65)

            else:
                mmMode = CTkSwitch(settFrame,text="Pencere Butonlarını Göster",text_color="#FFFFFF", offvalue="NO",onvalue="YES", command=Event_mmMode)
                mmMode.select()
                mmMode.place(x=10,y=65)


            


        def Event_ConnTopLevel():

            def Event_RefreshPORT():
                HPport = open(AppPATH + "\\MRCS\\CONN\\port.txt","r")
                portContent = HPport.read()
                hpLabel.configure(text=f"localhost:{portContent}")  

            def Event_EnterPORT():
                HPport = open(AppPATH + "\\MRCS\\CONN\\port.txt","w")
                dialog = CTkInputDialog(text="PORT:", title="PORT GİRİNİZ.", button_hover_color="#006600")
                entredPort = dialog.get_input()                                                                                                     

                if entredPort == None:
                    CTkMessagebox(title="HATA!", message="Port Girişi Algılanmadı, Tekrar Giriniz.", icon="cancel", option_1="Tamam")
                    return

                try:
                    int(entredPort)
                except:
                    CTkMessagebox(title="HATA!", message="Porta Metinsel Giriş Yapılamaz!", icon="cancel", option_1="Tamam")
                    return



                HPport.write(str(entredPort))
                HPport.close()
                HPport = open(AppPATH + "\\MRCS\\CONN\\port.txt","r")
                portContent = HPport.read()     
                hpLabel.configure(text=f"localhost:{portContent}")     

            ConnTOP = CTkToplevel(adminApp)
            ConnTOP.title("Yönetici | Bağlantı Sayfası")
            ConnTOP.geometry("600x400")

            ConnTOP.resizable(False,False)

            ConnTOP.grab_set()

            ConnTOP.iconbitmap("Sources\\Icons\\WindowIcon.ico")

            ConnFrame = CTkFrame(ConnTOP, fg_color="#404040", border_width=1, border_color="#FFFFFF", corner_radius=20, width=500, height=300)
            ConnFrame.place(x=50, y=50)

            hpmLabel = CTkLabel(ConnFrame, text="Yönetim Bağlantısı\n\n\n", font=("helvetica", 14, "bold"),image=CTkImage(dark_image=greenDownICO, size=(25,25)),compound=CENTER, text_color="#FFFFFF")
            hpmLabel.place(x=175, y=10)           

            HPport = open(AppPATH + "\\MRCS\\CONN\\port.txt","r")
            portContent = HPport.read()

            hpLabel = CTkLabel(ConnFrame, text=f"localhost:{portContent}", font=("helvetica", 12, "bold"),fg_color="#202020",corner_radius=25, text_color="#FFFFFF")
            hpLabel.place(x=185, y=60)    

            warnLabel = CTkLabel(ConnFrame, text="   Uyarı: değişikliklerin uygulanması için bağlantının\n    yeniden başlatılması gerekir(Programı Yeniden Başlatın)", font=("helvetica", 12, "bold"),image=CTkImage(dark_image=warnLabICO,size=(22,22)),compound=LEFT,fg_color="#202020",corner_radius=25, text_color="#FFFFFF")
            warnLabel.place(x=60, y=100)   

            enterPortAG = CTkButton(ConnFrame,text="Port Değiştir", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=150,height=40,image=CTkImage(dark_image=enterPortAGButICO),command=Event_EnterPORT)
            enterPortAG.place(x=325,y=200)

            connRefreshBut = CTkButton(ConnFrame,text="Yenile", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=150,height=40,image=CTkImage(dark_image=refreshButICO),command=Event_RefreshPORT)
            connRefreshBut.place(x=25,y=200)
            


        # SOL FRAME ELEMENTLERİ

        # 1

        tab1 = CTkLabel(LeftFrame, text="Başlangıç", font=("helvetica", 18, "bold"), text_color="#FFFFFF")
        tab1.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Main = CTkButton(LeftFrame,text="Ana Menü", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=mainPageICO))
        setPage_Main.pack(padx=5,pady=(5,7),fill='both', expand=True)

        setPage_Con = CTkButton(LeftFrame,text="Bağlantı", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=conButICO),command=Event_ConnTopLevel)
        setPage_Con.pack(padx=5,pady=(5,7),fill='both', expand=True)

        setPage_Set = CTkButton(LeftFrame,text="Ayarlar", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=settingsButICO),command=Event_SettingsPage)
        setPage_Set.pack(padx=5,pady=(5,7),fill='both', expand=True)

        # 2

        tab2 = CTkLabel(LeftFrame, text="Yönetim", font=("helvetica", 18, "bold"), text_color="#FFFFFF")
        tab2.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Devic = CTkButton(LeftFrame,text="Cihazlar", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=devicesButICO),command=Event_SingleTask)
        setPage_Devic.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Trans = CTkButton(LeftFrame,text="Aktarma", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=fileTransferICO), command=Event_CopyFileFromClient)
        setPage_Trans.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Share = CTkButton(LeftFrame,text="Ekran Paylaş", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=shareButICO),command=Event_ShareScreen)
        setPage_Share.pack(padx=5,pady=(5,7),fill='both', expand=True)

        setPage_Share = CTkButton(LeftFrame,text="Paylaşımı Durdur", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,command=Event_StopShareScreen)
        setPage_Share.pack(padx=5,pady=(5,7),fill='both', expand=True)



        # 3

        tab3 = CTkLabel(LeftFrame, text="Toplu İşlemler", font=("helvetica", 18, "bold"), text_color="#FFFFFF")
        tab3.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Shut = CTkButton(LeftFrame,text="Kapat", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=130,height=40,image=CTkImage(dark_image=powerButICO),command=Event_ShutDownALL)
        setPage_Shut.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_Shut = CTkButton(LeftFrame,text="Kilitle", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=130,height=40,image=CTkImage(dark_image=lockPcButICO),command=Event_LockALL)
        setPage_Shut.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_SendMSG = CTkButton(LeftFrame,text="Kilidi Aç", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=130,height=40,image=CTkImage(dark_image=unlockPcButICO),command=Event_UnLockALL)
        setPage_SendMSG.pack(padx=5, pady=(5,7),fill='both', expand=True)

        setPage_SendMSG = CTkButton(LeftFrame,text="Mesaj Gönder", text_color="#FFFFFF", fg_color="#606060", corner_radius=10,width=125,height=40,image=CTkImage(dark_image=sendMsgButICO),command=Event_SendMSG)
        setPage_SendMSG.pack(padx=5, pady=(5,7),fill='both', expand=True)

        # ANA FRAME ELEMENTLERİ


        listFrame = CTkFrame(MainFrame, fg_color="#202020", border_width=2,border_color="#00CC00", corner_radius=20, width=275, height=440)
        listFrame.pack(side="left",pady=5, padx=5, fill=tk.NONE, expand=True)

        informationFrame = CTkFrame(MainFrame, fg_color="#202020", border_width=2,border_color="#994C00", corner_radius=20, width=275, height=440)
        informationFrame.pack(side="right",pady=5, padx=5, fill=tk.NONE, expand=True)

        anaLab = CTkLabel(MainFrame, text="Ana Sayfa", font=("helvetica", 35, "bold"), text_color="#FFFFFF")
        anaLab.pack(padx=(10,50),pady=(10,50))


        mrcsLab = CTkLabel(informationFrame, text="Multiple Remote Connection \n System", font=("helvetica", 17, "bold"), text_color="#FFFFFF")
        mrcsLab.place(x=25, y=50)

        connStatLab = CTkLabel(informationFrame, text="Ekran Paylaşma:", font=("helvetica", 15, "bold"),image=CTkImage(dark_image=offlineLabelICO,size=(35, 35)),compound=RIGHT, text_color="#FFFFFF")
        connStatLab.place(x=60, y=400) 

        getDocs = CTkButton(informationFrame,text="Program Dökümanları",font=("helvetica", 15,"bold"), text_color="#FFFFFF", fg_color="#606060", corner_radius=15,width=125,height=35,image=CTkImage(dark_image=docsButICO))
        getDocs.place(x=30,y=350)

        refUser = CTkButton(listFrame,text="Yenile",font=("helvetica", 15,"bold"), text_color="#FFFFFF", fg_color="#606060",command=Event_RefUser,corner_radius=15,width=125,height=35)
        refUser.place(x=75,y=360)

        userD = Listbox(listFrame,bg="#404040",fg="#FFFFFF",selectmode=tk.SINGLE,width=30,height=20)
        userD.place(x=45,y=20)
        for insDe in clients:
            userD.insert(tk.END,insDe)



        adminApp.mainloop()

    def Event_BRIDGE(self):
        if not self.entredPort:
            CTkMessagebox(title="HATA!", message="Port Girişi Yapmadınız!", icon="cancel", option_1="Tamam")
            return

        try:
            port = int(self.entredPort)
            self.entredPort = str(port)  # İleriye dönük kullanım için str olarak kaydediyoruz.
        except ValueError:
            CTkMessagebox(title="HATA!", message="Porta Metinsel Giriş Yapılamaz!", icon="cancel", option_1="Tamam")
            return



# Ana program
portApp = CTk()
app = PortApp(portApp)


# COMMAND: SÜREKLİ AÇIK
portApp.mainloop()
