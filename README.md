Projeto Lavajato Backend
Este projeto é um sistema em Django para gerenciamento de agendamentos de lavagem. Ele utiliza o Django REST Framework, JWT para autenticação, filtros, tracking e outras dependências para construir uma API robusta.

Pré-requisitos
Python 3.9 ou superior
PostgreSQL (ou outro banco de dados, com as devidas alterações nas configurações)
Git
Estrutura do Projeto
A estrutura do projeto (exemplo):

bash
Copiar
lavajato-backend2.0/
├── app/
│   ├── models.py             # Modelos: Veiculo, Funcionario, Lavagem
│   ├── serializers.py        # Serializers para Lavagem e Funcionario
│   ├── views.py              # ViewSets: LavagemViewSet, FuncionarioViewSet
│   └── ...
├── auth/
│   └── views.py              # (Exemplo) UserInfoView para autenticação
├── config/
│   └── urls.py               # Configuração das URLs
├── common/
│   └── endpoints.js          # (Opcional) Arquivo usado pelo front-end
├── manage.py
└── requirements.txt
Passo a Passo para Configuração do Back-End
1. Clonar o Repositório
Abra o terminal e execute:

bash
Copiar
git clone https://seurepositorio.git
cd lavajato-backend2.0
2. Criar e Ativar o Ambiente Virtual
Crie um ambiente virtual usando o venv:

bash
Copiar
python -m venv env
Ative o ambiente virtual:

No Windows:

bash
Copiar
env\Scripts\activate
No macOS/Linux:

bash
Copiar
source env/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativado, instale as dependências listadas no arquivo requirements.txt:

bash
Copiar
pip install -r requirements.txt
Exemplo de conteúdo do requirements.txt:

txt
Copiar
Django==4.1.7
djangorestframework==3.15.2
django-filter==22.1
djangorestframework-simplejwt==5.2.2
drf-tracking==1.5.0
psycopg2-binary==2.9.6
python-decouple==3.8
django-cors-headers==3.13.0
4. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com as variáveis necessárias. Um exemplo:

env
Copiar
SECRET_KEY=your-secret-key
DEBUG=True

# Configuração do banco de dados PostgreSQL
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Outras variáveis, se necessário
O projeto utiliza o pacote python-decouple para ler essas variáveis. Certifique-se de que o arquivo .env esteja na raiz do projeto.

5. Realizar as Migrações do Banco de Dados
Crie as migrações e aplique-as:

bash
Copiar
python manage.py makemigrations
python manage.py migrate
6. Criar um Superusuário
Crie um superusuário para acessar o admin do Django:

bash
Copiar
python manage.py createsuperuser
Siga as instruções para definir nome de usuário, e-mail e senha.

7. Executar o Servidor de Desenvolvimento
Inicie o servidor:

bash
Copiar
python manage.py runserver
Acesse:

Aplicação: http://localhost:8000/
Admin do Django: http://localhost:8000/admin/
8. Testar os Endpoints da API
Agendamentos de Lavagem:
A URL padrão será: http://localhost:8000/api/lavagens/
Use ferramentas como Postman ou cURL para testar requisições GET, POST, etc.

Funcionários:
A URL padrão será: http://localhost:8000/api/funcionarios/

Autenticação JWT:
Utilize as rotas:

http://localhost:8000/api/token/ para obter o token.
http://localhost:8000/api/token/refresh/ para renovar o token.
Observações Adicionais
Configuração do Banco de Dados:
Se você deseja usar outro banco de dados além do PostgreSQL, ajuste as configurações no arquivo de settings.py.

Estrutura dos Endpoints:
As rotas são geradas via DefaultRouter. Verifique o arquivo config/urls.py para confirmar se as rotas estão corretas.

Organização dos Arquivos:
Se mover pastas como auth ou common, ajuste as importações nos arquivos de URL e nas demais views.

