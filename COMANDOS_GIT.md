# Comandos para subir o projeto no GitHub

## 1. Primeiro, crie um repositório no GitHub
1. Acesse https://github.com
2. Clique em "New repository"
3. Nome: `sistema-gerenciamento-escola-infantil`
4. Descrição: `Sistema completo para gerenciamento de escola infantil`
5. Marque como "Public" ou "Private" conforme preferir
6. NÃO marque "Initialize with README" (já temos um)
7. Clique em "Create repository"

## 2. Execute os comandos no terminal (PowerShell como administrador)

```bash
# Navegue até o diretório do projeto
cd "C:\Users\administrador\Documents\Projeto alexandre\Sistema-de-gerenciamento-escola-infantil-main"

# Inicialize o repositório Git
git init

# Adicione todos os arquivos
git add .

# Faça o primeiro commit
git commit -m "Initial commit: Sistema de Gerenciamento Escolar Infantil"

# Adicione o repositório remoto (substitua SEU_USUARIO pelo seu nome de usuário do GitHub)
git remote add origin https://github.com/SEU_USUARIO/sistema-gerenciamento-escola-infantil.git

# Configure sua branch principal
git branch -M main

# Envie os arquivos para o GitHub
git push -u origin main
```

## 3. Se for solicitado login
- Username: seu nome de usuário do GitHub
- Password: seu token de acesso pessoal (não a senha da conta)

### Como criar um token de acesso pessoal:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token → Generate new token (classic)
3. Marque as permissões: `repo`, `workflow`, `write:packages`
4. Copie o token gerado (guarde em local seguro)

## 4. Comandos para atualizações futuras

```bash
# Adicionar arquivos modificados
git add .

# Fazer commit das mudanças
git commit -m "Descrição das mudanças"

# Enviar para o GitHub
git push origin main
```

## 5. Estrutura de branches (opcional)

```bash
# Criar branch para desenvolvimento
git checkout -b develop

# Criar branch para features
git checkout -b feature/nova-funcionalidade

# Voltar para a branch main
git checkout main

# Fazer merge de uma branch
git merge develop
```

## 6. Comandos úteis

```bash
# Ver status dos arquivos
git status

# Ver histórico de commits
git log --oneline

# Ver diferenças
git diff

# Desfazer mudanças não commitadas
git checkout -- arquivo.py

# Ver branches
git branch -a
```