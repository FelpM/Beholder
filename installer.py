import os
import winshell
import sys

def criar_atalho_e_substituir_icone():
    # Obtém o diretório atual do script (onde o script .py está localizado)
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

    # Define o nome do atalho e seu caminho na área de trabalho
    atalho_nome = "beholder.lnk"
    atalho_path = os.path.join(winshell.desktop(), atalho_nome)

    # Caminho relativo para o beholder.exe e o ícone personalizado (b.ico)
    beholder_exe_path = "beholder.exe"
    icone_personalizado_path = "b.ico"

    # Caminho completo para o beholder.exe e o ícone personalizado
    caminho_completo_exe = os.path.join(script_dir, beholder_exe_path)
    caminho_completo_icone = os.path.join(script_dir, icone_personalizado_path)

    # Verifica se o beholder.exe e o ícone personalizado existem
    if not os.path.isfile(caminho_completo_exe):
        print(f"O arquivo beholder.exe não foi encontrado em {caminho_completo_exe}.")
        return
    if not os.path.isfile(caminho_completo_icone):
        print(f"O ícone personalizado não foi encontrado em {caminho_completo_icone}.")
        return

    # Cria o atalho na área de trabalho
    with winshell.shortcut(atalho_path) as atalho:
        atalho.path = caminho_completo_exe
        atalho.icon_location = (caminho_completo_icone, 0)  # Define o ícone personalizado
        atalho.working_directory = script_dir

    print(f"Atalho criado com sucesso na área de trabalho: {atalho_path}")


def criar_pasta_e_arquivos():
    # Verificar se o sistema operacional é Windows
    if os.name == 'nt':
        # Caminho para o diretório C:\
        diretorio_c = "C:\\"
        
        # Nome da pasta a ser criada
        nome_pasta = "honeypot"
        
        # Caminho completo da pasta
        caminho_pasta = os.path.join(diretorio_c, nome_pasta)
        
        try:
            # Criar a pasta
            os.mkdir(caminho_pasta)
            print(f"Pasta '{nome_pasta}' criada com sucesso em {caminho_pasta}")
            
            # Criar os arquivos de texto dentro da pasta
            for i in range(2):
                nome_arquivo = f"arquivo_de_seguranca_{i + 1}.txt"
                caminho_arquivo = os.path.join(caminho_pasta, nome_arquivo)
                
                with open(caminho_arquivo, 'w') as arquivo:
                    arquivo.write("Conteúdo do arquivo de segurança.")
                    print(f"Arquivo '{nome_arquivo}' criado em {caminho_arquivo}")
        
        except FileExistsError:
            print(f"A pasta '{nome_pasta}' já existe em {caminho_pasta}")

    else:
        print("Este código funciona apenas em sistemas Windows.")

def criar_arquivo_processos_permitidos():
    # Solicitar entrada de processos permitidos ao usuário
    processos_permitidos = input("Digite os nomes dos processos permitidos separados por vírgula: ")
    
    # Obter o diretório atual do script
    diretorio_script = os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # Caminho completo para o arquivo de texto
    caminho_arquivo = os.path.join(diretorio_script, 'process.txt')
    
    # Escrever a entrada exata do usuário no arquivo de texto
    with open(caminho_arquivo, 'w') as arquivo:
        arquivo.write(processos_permitidos)
    
    print(f"Processos permitidos foram salvos em {caminho_arquivo}")


if __name__ == "__main__":
    criar_atalho_e_substituir_icone()
    criar_pasta_e_arquivos()
    criar_arquivo_processos_permitidos()