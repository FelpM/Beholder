import threading

def run_beholder():
    import os
    import time
    import win32gui
    import win32process
    import psutil
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import win32security
    import ntsecuritycon as con
    
    class MyHandler(FileSystemEventHandler):
        def __init__(self, monitored_path, target_path, allowed_processes):
            self.monitored_path = monitored_path
            self.target_path = target_path
            self.allowed_processes = allowed_processes
            self.unauthorized_process_detected = False

        def on_any_event(self, event):
            if event.src_path and event.src_path.startswith(self.monitored_path):
                try:
                    foreground_window = win32gui.GetForegroundWindow()
                    _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
                    process = psutil.Process(process_id)
                    process_name = process.name()

                    if process_name not in self.allowed_processes:
                        print(f'O processo {process_name} não é permitido nesta pasta. Ativando segurança!')
                        self.unauthorized_process_detected = True
                except Exception as e:
                    print('Erro ao obter informações do processo:', e)


   
    def capture_sids(folder_path):
        captured_sids = []
        try:
            sd = win32security.GetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()

            for ace_index in range(dacl.GetAceCount()):
                ace = dacl.GetAce(ace_index)
                sid = ace[2]
                captured_sids.append(sid)
                print('Captured SID:', win32security.LookupAccountSid(None, sid)[0])

        except Exception as e:
            print('Error capturing SIDs:', str(e))

        return captured_sids

    
    def remove_permissions(folder_path, captured_sids):
        try:
            sd = win32security.GetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = sd.GetSecurityDescriptorDacl()

            while dacl.GetAceCount() > 0:
                dacl.DeleteAce(0)

            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION, sd)
            print('Permissions removed for', folder_path)

        except Exception as e:
            print('Error removing permissions:', str(e))

   
    def restore_permissions(folder_path, captured_sids):
        try:
            sd = win32security.GetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION)
            dacl = win32security.ACL()

            for sid in captured_sids:
                dacl.AddAccessAllowedAce(win32security.ACL_REVISION, con.FILE_ALL_ACCESS, sid)

            sd.SetSecurityDescriptorDacl(1, dacl, 0)
            win32security.SetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION, sd)
            print('Permissions restored for', folder_path)

        except Exception as e:
            print('Error restoring permissions:', str(e))

    try:
        monitored_path = r'C:\HONEYPOT'  
        target_path = r'C:\shares'
        allowed_processes_input_path = r'honeyprocess.txt'

        
        with open(allowed_processes_input_path, 'r') as file:
            allowed_processes_input = file.read()

        
        allowed_processes = [process.strip() for process in allowed_processes_input.split(',')]


        observer = Observer()
        handler = MyHandler(monitored_path, target_path, allowed_processes)
        observer.schedule(handler, monitored_path, recursive=True)
        observer.start()

        while True:
            if handler.unauthorized_process_detected:
                
                captured_sids = capture_sids(target_path)
                print('Captured SIDs:', captured_sids)

                
                remove_permissions(target_path, captured_sids)
                print('Permissions removed. Waiting for 2 minutes...')
                
                
                time.sleep(20)

               
                restore_permissions(target_path, captured_sids)
                print('Permissions restored using captured SIDs.')

                handler.unauthorized_process_detected = False

    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def run_gazer():
    import os
    import time
    import win32file
    import win32con
    import win32gui
    import win32process
    import pythoncom
    import psutil
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import ctypes

    class MyHandler(FileSystemEventHandler):
        def __init__(self, monitored_path, allowed_processes):
            self.monitored_path = monitored_path
            self.allowed_processes = allowed_processes

        def on_any_event(self, event):
            

            if event.src_path and event.src_path.startswith(self.monitored_path):
                try:
                    foreground_window = win32gui.GetForegroundWindow()
                    _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
                    process = psutil.Process(process_id)
                    process_name = process.name()
                    
                    
                    if process_name != 'explorer.exe' and process_name not in self.allowed_processes:
                        print(f'O processo {process_name} não é permitido nesta pasta. Encerrando...')
                        terminate_process(process_id)
                except Exception as e:
                    print('Erro ao obter informações do processo:', e)
            
            if not event.is_directory and event.src_path.lower().endswith('.exe'):
                try:
                    os.remove(event.src_path)
                    print(f'Arquivo .exe removido: {event.src_path}')
                except Exception as e:
                    print('Erro ao remover o arquivo .exe:', e)
            
            if not event.is_directory and event.src_path.lower().endswith('.dll'):
                try:
                    os.remove(event.src_path)
                    print(f'Arquivo .exe removido: {event.src_path}')
                except Exception as e:
                    print('Erro ao remover o arquivo .dll:', e)

    def terminate_process(process_id):
        try:
            handle = ctypes.windll.kernel32.OpenProcess(win32con.PROCESS_TERMINATE, False, process_id)
            if handle:
                ctypes.windll.kernel32.TerminateProcess(handle, -1)
                ctypes.windll.kernel32.CloseHandle(handle)
                print('Processo encerrado com sucesso.')
            else:
                print('Não foi possível abrir o processo.')
        except Exception as e:
            print('Erro ao encerrar o processo:', e)

    monitored_path = r'C:\\'

    allowed_processes_input_path = r'process.txt'

    with open(allowed_processes_input_path, 'r') as file:
        allowed_processes_input = file.read()

    allowed_processes = [process.strip() for process in allowed_processes_input.split(',')]


    def file_system_callback(hDir, action, file_name):
        if action == win32file.FILE_ACTION_MODIFIED or action == win32file.FILE_ACTION_ADDED:
            print(f'Arquivo modificado ou adicionado: {file_name}')

    hDir = win32file.CreateFile(
        monitored_path,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    pythoncom.CoInitialize()
    win32file.ReadDirectoryChangesW(
        hDir,
        8192,
        True,
        win32con.FILE_NOTIFY_CHANGE_FILE_NAME | win32con.FILE_NOTIFY_CHANGE_DIR_NAME | win32con.FILE_NOTIFY_CHANGE_SIZE,
        None,
        None
    )

    observer = Observer()
    observer.schedule(MyHandler(monitored_path, allowed_processes), monitored_path, recursive=True)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

def run_pen_monitor():

    import win32file
    import os
    import time

    def list_usb_drives():
        drives = []
        drive_bits = win32file.GetLogicalDrives()
        
        for drive_bit in range(26):
            mask = 1 << drive_bit
            if drive_bits & mask:
                drive_letter = chr(65 + drive_bit)
                drive_info = win32file.GetDriveType(f"{drive_letter}:\\")
                
                if drive_info == win32file.DRIVE_REMOVABLE:
                    drives.append(f"{drive_letter}:\\")
        
        return drives

    def remove_exe_dll_files(drive):
        file_extensions_to_remove = ['.exe', '.dll']
        
        for root, _, files in os.walk(drive):
            for filename in files:
                _, file_extension = os.path.splitext(filename)
                if file_extension.lower() in file_extensions_to_remove:
                    file_to_remove = os.path.join(root, filename)
                    try:
                        os.remove(file_to_remove)
                        print(f'Arquivo removido: {file_to_remove}')
                    except Exception as e:
                        print(f'Erro ao remover {file_to_remove}: {str(e)}')

    while True:
        usb_drives = list_usb_drives()
        if usb_drives:
            print("Pendrives USB conectados:")
            for drive in usb_drives:
                print(drive)
                remove_exe_dll_files(drive)
        else:
            print("Nenhum pendrive USB conectado.")
        time.sleep(5)


if __name__ == "__main__":
    
    thread1 = threading.Thread(target=run_beholder)
    thread2 = threading.Thread(target=run_gazer)
    thread3 = threading.Thread(target=run_pen_monitor)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    print("Ambos os programas foram abertos")

while True:
    pass
