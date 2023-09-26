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

    # Classe para manipular eventos do sistema de arquivos
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
                        #terminate_process(process_id)
                        self.unauthorized_process_detected = True
                except Exception as e:
                    print('Erro ao obter informações do processo:', e)


    # Função para capturar os SIDs das permissões permitidas
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

    # Função para remover permissões usando os SIDs capturados
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

    # Função para restaurar permissões usando os SIDs capturados
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
        monitored_path = r'C:\HONEYPOT'  # Pasta para monitorar (default)
        target_path = r'C:\protegido'
        allowed_processes_input_path = r'honeyprocess.txt'

        # Lê o conteúdo do arquivo allowed_processes_input
        with open(allowed_processes_input_path, 'r') as file:
            allowed_processes_input = file.read()

        # Divide o conteúdo do arquivo usando a vírgula como separador e remove espaços em branco em excesso
        allowed_processes = [process.strip() for process in allowed_processes_input.split(',')]


        observer = Observer()
        handler = MyHandler(monitored_path, target_path, allowed_processes)
        observer.schedule(handler, monitored_path, recursive=True)
        observer.start()

        while True:
            if handler.unauthorized_process_detected:
                # Capturar SIDs das permissões permitidas
                captured_sids = capture_sids(target_path)
                print('Captured SIDs:', captured_sids)

                # Remover permissões (se um processo não autorizado for detectado)
                remove_permissions(target_path, captured_sids)
                print('Permissions removed. Waiting for 2 minutes...')
                
                # Esperar por 2 minutos
                time.sleep(20)

                # Restaurar permissões usando os SIDs capturados
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
            #print('Evento', event.event_type, 'caminho:', event.src_path, 'diretório?', event.is_directory)

            if event.src_path and event.src_path.startswith(self.monitored_path):
                try:
                    foreground_window = win32gui.GetForegroundWindow()
                    _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
                    process = psutil.Process(process_id)
                    process_name = process.name()
                    #print(f'Processo atual ({process_id}): {process_name}')
                    
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

    # Solicitar a pasta a ser monitorada
    monitored_path = r'C:\\'

    allowed_processes_input_path = r'process.txt'

        # Lê o conteúdo do arquivo allowed_processes_input
    with open(allowed_processes_input_path, 'r') as file:
        allowed_processes_input = file.read()

        # Divide o conteúdo do arquivo usando a vírgula como separador e remove espaços em branco em excesso
    allowed_processes = [process.strip() for process in allowed_processes_input.split(',')]


    # Configurar o hook
    def file_system_callback(hDir, action, file_name):
        if action == win32file.FILE_ACTION_MODIFIED or action == win32file.FILE_ACTION_ADDED:
            print(f'Arquivo modificado ou adicionado: {file_name}')

    # Registrar o hook
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

# Função para solicitar a senha do administrador
# def get_admin_password():
    # while True:
        # senha_digitada = getpass.getpass("Digite a senha de administrador: ")
        # if senha_digitada == senha_admin:
        #     return True
        # else:
        #    print("Senha incorreta. Tente novamente.")

# Verificar a senha de administrador
if __name__ == "__main__":
    # Criar threads para executar os programas
    thread1 = threading.Thread(target=run_beholder)
    thread2 = threading.Thread(target=run_gazer)

    # Iniciar as threads
    thread1.start()
    thread2.start()

    # Aguardar até que ambas as threads terminem
    thread1.join()
    thread2.join()

    print("Ambos os programas foram abertos")

while True:
        pass
