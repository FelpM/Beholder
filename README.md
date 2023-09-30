 
<h1 align="center"> Beholder </h1>

![img](https://github.com/FelpM/Beholder/blob/main/beholderimg.png)
Eye of the Beholder (1991)

# Índice 

* [Índice](#índice)
* [Requisitos mínimos de hardware](#requisitos-mínimos-de-hardware)
* [Manual de instalação](#manual-de-instalação)
* [Manual do usuário](#manual-do-usuário)
* [Dependências](#dependências)
* [Recomendações de Uso](#recomendações-de-uso)
* [Sobre o projeto e o Desenvolvedor](#sobre-o-projeto-e-o-desenvolvedor)
* [Status do projeto](#status-do-projeto)

# Desenvolvido por Felipe Madeira

O Beholder é uma aplicação, livre e código aberto, que busca promover a segurança de 
dispositivos e diretórios compartilhados por meio do tratamento de exceções e controle 
do ambiente. Em sua versão atual, o programa conta com cinco funções principais. 
Monitoramento de diretórios, controle de criação de executáveis (.exe e .dll), suspensão
de processos não autorizados, proteção de diretório específico, monitoramento e 
varredura de dispositivo externos plugados nas portas USB.

Estas funções em conjunto ajudam a mitigar riscos de ataque pelos principais ransowares 
do mercado, além de limitar a ação de um agente mal-intencionado que tenha acesso 
físico ou remoto ou host. Sugere-se a utilização em terminais ou end points destinados a 
poucas ou somente uma operação específica.


# Requisitos mínimos de hardware

Testado em dispositivos com recursos de hardware:
 * 4 gb de memória ram
 * 2 núcleos de processamento
 * 80 gb de espaço disco rígido

# Manual de instalação

 * Após baixar o arquivo .zip descompacte na pasta desejada.
 * Certifique-se de ter a pasta "Shares" no diretório rais (C:). Este será o diretório
protegido 
 * Execute o installer.exe. Ele criará os outros diretórios necessários para o monitoramento 
e um atalho para iniciar o programa
 * Insira os nomes dos processos .exe que desseja permitir a execusão (O beholder encerrará
qualquer outro processo aberto após sua inicialização que não estiver na lista de
permissões. A lista pode ser alterada no arquivo processes.txt na pasta do programa).

![exemplo](https://github.com/FelpM/Beholder/blob/main/exemplo.png)

# Manual do usuário

 * Recomenda-se executar o Beholder como administrador a partir do perfil do usuário no 
qual se deseja atribuir as limitações.
 * Ao registrar os processos permitidos sempre coloque o "beholder.exe", afim de que ele
não se encerre
 * Os processos permitidos podem ser adicionados posteriormente a instalação no arquivo process.txt na pasta da aplicação
 * A aplicação iniciará em segundo plano, não permitindo que o usuário logado encerre o 
processo. 
 * Para encerrar o processo é necessário voltar ao perfil de administrador através do 
comando ctrl + alt + del e pará-lo através do Gerenciador de Tarefas

ATENÇÃO - Nunca execute o Beholder no ambiente de administração do host!!! Quando ativo no sistema, a aplicação deverá apagar qualquer executavel ou dll
identificado dentro de um dispositivo móvel instalado no dispositivo!!!

CUIDADO: Ao tentar domar um Beholder, ele pode se virar contra você

# Dependências

Projetado com base na arquitetura de Windows 10 e Windows server

O código fonte foi desenvolvido inteiramente em Python 3.10

Não é necessário a instalação de nenhuma aplicação que esteja fora do padrão do sistema 
operacional

# Recomendações de Uso

Quando bem aplicado, o beholder pode evitar a inclusão de executáveis ou dll's não
desejadas no sistema, garantindo uma navegação segura e limitada ao usuário final.
A aplicação pode ser útil para terminais coletores e compartilhadores de dados onde 
se usam poucos executaveis, ou necessitam de poucos recursos para realizar o serviço. 
Além da primeira camada de proteção, o programa também protege o diretório compartilhado 
(Shares) de ransonwares que executam movimentação lateral, inibindo estes ativos de 
alcançarem os dados sensíveis compartilhados e evitando seu sequestro ou 
criptografia.

# Sobre o projeto e o Desenvolvedor

Felipe Madeira é aluno do primeiro ano do curso de Defesa Cibernética da Faculdade de
Informática e Administração Paulista (FIAP). O projeto foi desenvoldido em atividade de 
desafio, proposto pela Prdide Security juntamente com o corpo
docente do curso.

# Status do projeto

Projeto em desenvolvimento. Aberto a colaborações e disponível para melhorias, adaptações
ou uso!

Caso tenha dúvidas. Entre em contato! 
