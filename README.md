# E-commerce Flask (Bootstrap + Auth + CRUD)

## Páginas e Controle de Acesso
- Públicas: `/`, `/login`, `/cadastro`
- Protegidas (apenas após login): `/anuncios`, `/anuncios/novo`, `/anuncios/editar/<id>`, `/anuncios/excluir/<id>`, `/logout`

## Rodar localmente
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
python app.py
# abrir http://127.0.0.1:5000
```

## Publicar no GitHub (resumo)
```bash
git init
git add .
git commit -m "Projeto Flask: auth + CRUD + Bootstrap"
git branch -M main
git remote add origin https://github.com/<seu-usuario>/<seu-repo>.git
git push -u origin main
```

## Deploy no PythonAnywhere (resumo)
1. Crie conta e faça login no PythonAnywhere.
2. Abra um **Bash console** e rode:
```bash
git clone https://github.com/<seu-usuario>/<seu-repo>.git
cd <seu-repo>
python -m venv venv
source venv/bin/activate  # no console do PythonAnywhere
pip install -r requirements.txt
```
3. Vá em **Web** → **Add a new web app** → Manual config (Flask). Escolha a mesma versão de Python do seu venv.
4. Em **Code** (path da app), aponte para o diretório do projeto clonado.
5. Em **WSGI configuration file**, substitua o conteúdo pelo mostrado em `wsgi.py` deste projeto (ajuste caminhos).
6. Em **Static files**, adicione: URL `/static/` → path `/home/<usuario>/<repo>/static`
7. **Reload** a app. Acesse `https://<usuario>.pythonanywhere.com`.
