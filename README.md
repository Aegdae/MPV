# Rede Social - Projeto com Backend e Frontend

Este projeto é uma aplicação de rede social completa, com funcionalidades de **backend** desenvolvidas em Flask e um **frontend** construído com HTML, CSS e JavaScript.

---

### 🖥️ Frontend
- Páginas dinâmicas e responsivas.
- Estilização moderna com CSS.
- JavaScript para interatividade (validações e ações dinâmicas).

### 🛠️ Backend
- **Flask** como framework principal.
- **Banco de Dados PostgreSQL** para armazenar usuários e dados.
- **Autenticação completa**:
  - Registro de novos usuários.
  - Login seguro com hash de senhas (bcrypt).
  - Recuperação de senha por e-mail.
- Rotas RESTful organizadas.

---

## 🚀 Estrutura do Projeto
  ```plaintext
    Social/
    │
    ├── Static/
    │   ├── script.js
    │   └── style.css
    │
    ├── templates/
    │   ├── edit_profile.html
    │   ├── forgot_password.html
    │   ├── home.html
    │   ├── login.html
    │   ├── profile.html
    │   ├── register.html
    │   └── reset_password.html
    │
    ├── app.py
    ├── Procfile
    └── requirements.txt
  ```




## 🚀 Como Rodar o Projeto

### Requisitos

Antes de rodar o projeto, verifique se você tem as seguintes ferramentas instaladas:

- **Python 3.x** - Para rodar o backend.
- **PostgreSQL** - Para o banco de dados.
- **pip** - Para instalar dependências do Python.

### 1. Instalar Dependências

Primeiro, clone o repositório para sua máquina local:

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio 
```

## 🚀 Uso do Projeto

Depois de rodar o projeto, você poderá acessar a aplicação no seu navegador e interagir com as funcionalidades da rede social. Abaixo estão as instruções para navegação e funcionalidades principais.

### 1. Acessando a Aplicação

Abra o navegador e acesse a URL do servidor local (geralmente `http://127.0.0.1:5000`), onde a aplicação estará rodando.

### 2. Funcionalidades

- **Página de Registro**: Permite que novos usuários se registrem na plataforma com um nome de usuário, e-mail e senha.
- **Página de Login**: Usuários registrados podem fazer login na plataforma.
- **Página de Perfil**: Cada usuário tem seu próprio perfil com a opção de editar informações.
- **Postagens**: Os usuários podem fazer postagens, que ficam visíveis para seus amigos ou para todos os usuários, dependendo da configuração.
- **Recuperação de Senha**: Caso o usuário esqueça a senha, ele pode solicitar uma recuperação por e-mail.

### 3. Testando a Aplicação

Você pode realizar testes no seu ambiente local para verificar se tudo está funcionando corretamente. Use a aplicação para:

- Criar uma conta e realizar o login.
- Alterar dados no perfil do usuário.
- Criar, visualizar e excluir postagens.

---

## 📚 Como Contribuir

1. **Fork** o repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Faça as alterações necessárias e commit (`git commit -am 'Adiciona nova feature'`).
4. Push para a branch (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.

---

## 📝 Licença

Este projeto está licenciado sob a [LICENSE](LICENSE).

---

## 📧 Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato.

- **Email**: jonnathasg@gmail.com
- **GitHub**: [Aegdae](https://github.com/Aegdae)




