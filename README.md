# Projeto Lavajato Backend

Este projeto é um sistema em Django para gerenciamento de agendamentos de lavagem. Ele utiliza o Django REST Framework, JWT para autenticação, filtros, tracking e outras dependências para construir uma API robusta.

---

## Pré-requisitos

- **Python 3.9** ou superior  
- **PostgreSQL** (ou outro banco de dados, com as devidas alterações nas configurações)  
- **Git**

---

## Estrutura do Projeto

A estrutura do projeto (exemplo):

```
lavajato-backend2.0/
├── app/
│   ├── models.py             # Modelos: Veiculo, Funcionario, Lavagem
│   ├── serializers.py        # Serializers para Lavagem e Funcionario
│   ├── views.py              # ViewSets: LavagemViewSet, FuncionarioViewSet
│   └── ...
├── auth/
│   └── views.py              # UserInfoView (para autenticação)
├── config/
│   └── urls.py               # Configuração das URLs do projeto
├── common/
│   └── endpoints.js          # (Opcional) Arquivo de endpoints usado pelo front-end
├── manage.py
└── requirements.txt
```

---

## Passo a Passo para Configuração do Back-End

### Passo 1: Clone o Repositório

Abra o terminal e execute:

```bash
git clone https://github.com/SEU_USUARIO/lavajato-backend2.0.git
cd lavajato-backend2.0
```

### Passo 2: Crie e Ative o Ambiente Virtual

Recomendamos o uso de um ambiente virtual para isolar as dependências do projeto. Execute os seguintes comandos:

```bash
# Instale o virtualenv, se ainda não estiver instalado
pip install virtualenv

# Crie um ambiente virtual (você pode substituir "env" pelo nome desejado)
python3 -m venv env

# Ative o ambiente virtual:
# No macOS/Linux:
source env/bin/activate
# No Windows:
# env\Scripts\activate
```

### Passo 3: Instale as Dependências Python

Com o ambiente virtual ativado, instale as dependências listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

> **Exemplo de requirements.txt:**
> ```
> Django==4.1.7
> djangorestframework==3.15.2
> django-filter==22.1
> djangorestframework-simplejwt==5.2.2
> drf-tracking==1.5.0
> psycopg2-binary==2.9.6
> python-decouple==3.8
> django-cors-headers==3.13.0
> ```

### Passo 4: Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no exemplo abaixo:

```env
SECRET_KEY=your-secret-key
DEBUG=True

# Configuração do banco de dados PostgreSQL
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432

# Outras variáveis, se necessário
```

> **Observação:**  
> O projeto utiliza o pacote **python-decouple** para ler essas variáveis.

### Passo 5: Realize as Migrações do Banco de Dados

Crie as migrações e aplique-as:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Passo 6: Crie um Superusuário

Crie um superusuário para acessar o painel administrativo do Django:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir nome de usuário, e-mail e senha.

### Passo 7: Execute o Servidor de Desenvolvimento

Inicie o servidor:

```bash
python manage.py runserver
```

Acesse:
- **Aplicação:** [http://localhost:8000/](http://localhost:8000/)
- **Admin do Django:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

### Passo 8: Teste os Endpoints da API

- **Agendamentos de Lavagem:**  
  URL padrão: [http://localhost:8000/api/lavagens/](http://localhost:8000/api/lavagens/)

- **Funcionários:**  
  URL padrão: [http://localhost:8000/api/funcionarios/](http://localhost:8000/api/funcionarios/)

- **Autenticação JWT:**  
  - Obter token: [http://localhost:8000/api/token/](http://localhost:8000/api/token/)  
  - Renovar token: [http://localhost:8000/api/token/refresh/](http://localhost:8000/api/token/refresh/)

---

## Observações Adicionais

- **Configuração do Banco de Dados:**  
  Se desejar utilizar outro banco de dados além do PostgreSQL, ajuste as configurações no arquivo **settings.py**.

- **Endpoints e Rotas:**  
  As rotas são geradas via DefaultRouter no arquivo **config/urls.py**. Se você reorganizar pastas como **auth** ou **common**, ajuste as importações correspondentes.

- **Ambiente Virtual:**  
  Sempre ative o ambiente virtual antes de executar os comandos do Django.

- **Documentação:**  
  Consulte a [documentação do Django](https://docs.djangoproject.com/en/4.1/) e do [Django REST Framework](https://www.django-rest-framework.org/) para mais detalhes e melhores práticas.

---
