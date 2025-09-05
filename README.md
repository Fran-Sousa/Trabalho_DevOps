# Gerenciador de Tarefas - DevOps

Um sistema completo de gerenciamento de tarefas desenvolvido como projeto prático para a disciplina de DevOps e Integração Contínua, implementando um pipeline DevOps completo com todas as práticas modernas de desenvolvimento.

## 📋 Sobre o Projeto

Este projeto consiste em uma aplicação web para gerenciamento de tarefas pessoais, onde usuários podem se cadastrar, fazer login e organizar suas atividades diárias. O foco principal está na implementação de práticas DevOps em todas as fases do desenvolvimento.

## 🚀 Funcionalidades

### Gerenciamento de Usuários

- **Cadastro de usuários**: Criação de novos usuários no sistema
- **Autenticação**: Login seguro com validação de credenciais
- **Perfil do usuário**: Visualização e edição das informações pessoais
- **Controle de acesso**: Autorização baseada em tokens para proteger recursos

### Gerenciamento de Tarefas

- **Criar tarefas**: Adicionar novas tarefas com título e descrição
- **Listar tarefas**: Visualizar todas as tarefas do usuário logado
- **Editar tarefas**: Modificar informações de tarefas existentes
- **Excluir tarefas**: Remover tarefas concluídas ou desnecessárias
- **Status de tarefas**: Marcar tarefas como pendentes, em andamento ou concluídas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python com FastAPI
- **Banco de Dados**: SQLite
- **Frontend**: Interface via Swagger UI
- **Containerização**: Docker
- **Infraestrutura**: AWS (EC2/ECS)
- **CI/CD**: GitHub Actions
- **Monitoramento**: AWS CloudWatch
- **Gerenciamento de Segredos**: GitHub Secrets

## 🏗️ Arquitetura

O sistema segue uma arquitetura de microsserviços simples:

```
Frontend (Swagger UI) ←→ API REST (FastAPI) ←→ Banco de Dados
                                ↓
                        Sistema de Autenticação (JWT)
                                ↓
                        Middleware de Autorização
```

## 📋 Requisitos DevOps Implementados

### 1. Planejamento

- **Ferramenta**: Trello para gestão de backlog

### 2. Desenvolvimento e Versionamento

- **IDE**: VSCode com ambiente configurado com extensões Python
- **Git**: Controle de versão com GitHub
- **Workflow**: Pull Requests obrigatórios com code review

### 3. Build e Qualidade

- **Containerização**: Docker para build consistente
- **Linting**: Black, Flake8, isort para qualidade de código
- **Pre-commit hooks**: Validações automáticas antes do commit

### 4. Testes

- **Testes Unitários**: pytest para cobertura de código
- **Testes de Integração**: Validação de endpoints da API
- **Cobertura**: Relatórios automáticos de cobertura

### 5. CI/CD

- **GitHub Actions**: Pipeline automatizado com jobs para:
  - Execução de testes
  - Verificação de qualidade de código
  - Build e push de imagens Docker
  - Deploy automático em ambientes

### 6. Deploy e Infraestrutura

- **Cloud Provider**: AWS (EC2/ECS)
- **IaC**: CDK para provisionamento
- **Ambientes**: Separação entre dev, staging e produção
- **Segurança**: VPC, Security Groups e IAM configurados

### 7. Operação

- **Process Management**: systemd ou Supervisor
- **Load Balancer**: AWS ALB para distribuição de carga

### 8. Monitoramento

- **Métricas**: AWS CloudWatch para monitoramento de infraestrutura
- **Dashboards**: Grafana para visualização de métricas personalizadas
- **Logs**: Centralização e análise de logs da aplicação
- **Alertas**: Notificações automáticas para problemas críticos

### 9. Segurança

- **Secrets Management**: GitHub Secrets
- **Autenticação**: JWT tokens para segurança da API
- **HTTPS**: Certificados SSL/TLS obrigatórios
- **Vulnerability Scanning**: Análise automática de dependências

### 10. Feedback e Comunicação

- **Ferramentas**: Discord/WhatsApp para comunicação da equipe
- **Notificações**: Integração com pipelines para status de deploy
- **Documentação**: Wiki do projeto e documentação da API

## 📊 Status do Projeto

![Build Status](https://github.com/[username]/task-manager/workflows/CI/badge.svg)
![Deploy Status](https://github.com/[username]/task-manager/workflows/CD/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🚦 Como Executar

### Pré-requisitos

- **Docker Desktop** instalado e executando
- **VS Code** com a extensão **Dev Containers** instalada
- **Git** para clonar o repositório

### Configuração e Execução (Dev Container)

1. **Clone o repositório**

   ```bash
   git clone <repository-url>
   cd trabalho-devops
   ```

2. **Configure o ambiente de desenvolvimento (opcional)**

   ```bash
   # Copie o arquivo de configuração de exemplo
   cp .env.example .env
   ```

3. **Abra no VS Code**

   ```bash
   code .
   ```

4. **Inicialize o Dev Container**

   - Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
   - Digite: `Dev Containers: Reopen in Container`
   - Aguarde o container ser construído (primeira vez pode demorar alguns minutos)

5. **Execute as migrações do banco de dados**

   No terminal integrado do VS Code (já dentro do container):

   ```bash
   # Execute as migrações do banco de dados
   python migrate.py upgrade
   ```

6. **Execute a aplicação**

   ```bash
   # A aplicação inicia automaticamente, mas se precisar executar manualmente:
   fastapi dev src/main.py --host 0.0.0.0 --port 8001
   ```

6. **Acesse a aplicação**
   - **API**: `http://localhost:8001`
   - **Documentação Swagger**: `http://localhost:8001/docs`
   - **Health Check**: `http://localhost:8001/health`

## 🗄️ Gerenciamento do Banco de Dados

### Migrações (No Dev Container)

```bash
# No terminal do VS Code dentro do dev container:

# Executar todas as migrações pendentes
python migrate.py upgrade

# Criar uma nova migração
python migrate.py create "Adicionar nova coluna na tabela users"

# Verificar migração atual
python migrate.py current

# Ver histórico de migrações
python migrate.py history

# Reverter uma migração
python migrate.py downgrade
```

### Executando com Docker

```bash
# Build e execução com migrações automáticas
docker build --target development -t task-manager-dev .
docker run -p 8001:8001 task-manager-dev

# Para desenvolvimento direto
docker build --target production -t task-manager-prod .
docker run -p 8000:8000 task-manager-prod
```

## 🧪 Testes

### No Dev Container (Recomendado)

```bash
# No terminal do VS Code dentro do dev container:

# Executar todos os testes
pytest

# Testes com cobertura
pytest --cov=src --cov-report=html

# Testes específicos
pytest tests/test_tasks.py
pytest tests/test_auth.py
```

## 🔧 Qualidade de Código

### No Dev Container (Recomendado)

```bash
# No terminal do VS Code dentro do dev container:

# Formatação com Black
black src/

# Ordenação de imports
isort src/

# Linting com Flake8
flake8 src/

# Executar todos os comandos de lint
black src/ && isort src/ && flake8 src/

# Pre-commit hooks (já instalados automaticamente no dev container)
pre-commit run --all-files

# Verificar configuração do pre-commit
pre-commit --version
```

### Integração com VS Code

O dev container já vem configurado com:

- **Black**: Formatação automática ao salvar
- **Flake8**: Linting em tempo real
- **isort**: Organização de imports ao salvar
- **Pre-commit hooks**: Instalados automaticamente

## 👥 Equipe

- **Desenvolvedor 1**: [Nome] - Backend e DevOps
- **Desenvolvedor 2**: [Nome] - Frontend e Testes
- **Desenvolvedor 3**: [Nome] - Infraestrutura e Monitoramento

---

**Disciplina**: DevOps e Integração Contínua  
**Professor**: Prof. MSc. Guilherme Ditzel Patriota  
**Instituição**: Centro Universitário Internacional Uninter  
**Ano**: 2025
