\
# Exemplo de WSGI para usar no PythonAnywhere.
# No painel Web do PythonAnywhere, edite o WSGI file e use algo parecido com isso,
# ajustando os caminhos para o seu usuário e diretório do projeto.

import sys
import os

# Caminho do seu projeto no PythonAnywhere (ajuste):
project_home = os.path.expanduser('~/ecommerce_flask_bootstrap')
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Define variável de ambiente se quiser (opcional)
os.environ['FLASK_ENV'] = 'production'

# Importa a aplicação Flask
from app import app as application
