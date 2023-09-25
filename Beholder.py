import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import time
import threading
import getpass
import sys

class MeuServico(win32serviceutil.ServiceFramework):
    _svc_name_ = "MeuServico"
    _svc_display_name_ = "Meu Serviço do Windows"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_,))
        self.main()

    def main(self):
        while self.is_alive:
            try:
                import threading
                import getpass

               

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
                        target_path = r'C:\monitorados'

                        allowed_processes_input = input("Digite os nomes dos processos permitidos no Honeypot (separados por vírgula): ")
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
                            self.allowed_processes = set(allowed_processes)
                            self.cache_process_name = None

                        def get_current_process_name(self):
                            if self.cache_process_name is None:
                                try:
                                    foreground_window = win32gui.GetForegroundWindow()
                                    _, process_id = win32process.GetWindowThreadProcessId(foreground_window)
                                    process = psutil.Process(process_id)
                                    self.cache_process_name = process.name()
                                except Exception as e:
                                    self.cache_process_name = ''
                                    print('Erro ao obter informações do processo:', e)

                            return self.cache_process_name

                        def on_any_event(self, event):
                            #print('Evento', event.event_type, 'caminho:', event.src_path, 'diretório?', event.is_directory)

                            if event.src_path and event.src_path.startswith(self.monitored_path):
                                process_name = self.get_current_process_name()

                                if process_name:
                                    if process_name != 'explorer.exe' and process_name not in self.allowed_processes:
                                        print(f'O processo {process_name} não é permitido nesta pasta. Encerrando...')
                                        terminate_process_by_name(process_name)

                            if not event.is_directory and event.src_path.lower().endswith('.exe'):
                                try:
                                    os.remove(event.src_path)
                                    print(f'Arquivo .exe removido: {event.src_path}')
                                except Exception as e:
                                    print('Erro ao remover o arquivo .exe:', e)

                    def terminate_process_by_name(self, process_name):
                            process_list = psutil.process_iter(attrs=['pid', 'name'])
                            for process in process_list:
                                try:
                                    if process.info['name'] == process_name:
                                        ctypes.windll.kernel32.TerminateProcess(process.handle, -1)
                                        print(f'Processo {process_name} encerrado com sucesso.')
                                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                                    pass

                    if __name__ == "__main__":
                        # Solicitar a pasta a ser monitorada
                        monitored_path = r'C:\\'

                        # Solicitar os processos permitidos (separados por vírgula)
                        # Defina o caminho do arquivo de texto contendo os processos permitidos
                        allowed_processes_file = "processos.txt"

                        # Ler os nomes dos processos permitidos a partir do arquivo
                        with open(allowed_processes_file, 'r') as file:
                            allowed_processes_input = file.read()

                        allowed_processes = [process.strip() for process in allowed_processes_input.split(',')]

                        

                        # Configurar o hook
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
                            32768,
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

                    
            except Exception as e:
                print("Erro:", str(e))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MeuServico)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MeuServico)
