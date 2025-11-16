# 🎯 Planejamento: Sistema de Workflow com Nodes

## 📋 Visão Geral

O sistema de nodes do Arquiteto será um **editor visual de workflows** onde o usuário pode:
- Montar fluxos de automação visualmente
- Conectar ações em sequência ou paralelo
- Salvar e reutilizar workflows
- Executar workflows com um clique

## 🧩 Categorias de Nodes

### 1. 🚀 Iniciadores (Entry Points)
Nodes que iniciam um workflow:
- **Projeto Iniciado**: Define qual projeto será trabalhado
- **Abrir Workspace**: Carrega um workspace específico
- **Evento Trigger**: Dispara em horários/eventos específicos

### 2. 💻 Aplicações (IDEs & Editores)
Nodes que abrem aplicações:
- **Zed**: Abre o editor Zed com projeto/arquivo específico
- **VSCode**: Abre o VSCode
- **Terminal**: Abre terminal em diretório específico
- **Browser**: Abre navegador em URL específica

### 3. 🐳 Serviços (Backend Services)
Nodes que gerenciam serviços:
- **Docker Compose**: Sobe/desce containers
- **PM2**: Inicia/para processos
- **Caddy**: Gerencia reverse proxy
- **Database**: Conecta/inicializa banco de dados

### 4. ⚡ Ações (Commands & Scripts)
Nodes que executam comandos:
- **Executar Comando**: Executa comando shell
- **Executar Script**: Roda script Python/Bash
- **Criar Arquivo/Diretório**: Operações de filesystem
- **Git**: Comandos git (pull, push, commit)

### 5. 🔀 Lógica & Controle
Nodes que controlam fluxo:
- **Condição (If)**: Verifica condição antes de continuar
- **Aguardar**: Espera X segundos
- **Loop**: Repete ações N vezes
- **Paralelo**: Executa múltiplos branches simultaneamente

### 6. 📊 Monitoramento
Nodes que checam estado:
- **Verificar Serviço**: Checa se serviço está rodando
- **Verificar Arquivo**: Verifica se arquivo existe
- **Health Check**: Faz ping em endpoint
- **Ler Logs**: Captura logs de serviços

## 🎨 Exemplos de Workflows

### Workflow 1: "Iniciar Dev Use Gaba"
```
[Projeto Iniciado: Use Gaba]
    ↓
[Docker Compose: Convex] ──→ [Aguardar: 5s]
    ↓                              ↓
[Zed: /root/convex]          [Health Check: api.usegaba.com]
    ↓                              ↓
[Terminal: npm run dev]      [Browser: localhost:3000]
```

### Workflow 2: "Deploy Painel VPS"
```
[Projeto Iniciado: VPS Panel]
    ↓
[Git: Pull]
    ↓
[Executar: npm run build]
    ↓
[PM2: Restart vps-panel]
    ↓
[Health Check: painel.usegaba.com]
    ↓
[Notificação: "Deploy OK!"]
```

### Workflow 3: "Backup Completo"
```
[Projeto Iniciado: Backup]
    ↓
[Docker: Stop all containers]
    ↓
[Executar Script: backup.sh] ──→ [Paralelo]
    ↓                                  ├─→ [Comprimir: /root/convex/data]
[Aguardar conclusão]  ←───────────────├─→ [Comprimir: /root/vps-panel]
    ↓                                  └─→ [Dump: PostgreSQL]
[Docker: Start all containers]
    ↓
[Notificação: "Backup concluído!"]
```

## 🔧 Propriedades dos Nodes

Cada tipo de node terá configurações específicas:

### Node: Zed
```python
{
    "type": "application.zed",
    "label": "Zed Editor",
    "config": {
        "project_path": "/root/convex",
        "open_files": ["src/index.ts", "README.md"],
        "workspace": "use-gaba.code-workspace"
    }
}
```

### Node: Docker Compose
```python
{
    "type": "service.docker",
    "label": "Convex Backend",
    "config": {
        "action": "up",  # up, down, restart
        "compose_file": "/root/convex/docker-compose.yml",
        "services": ["backend", "dashboard"],
        "detached": true
    }
}
```

### Node: Executar Comando
```python
{
    "type": "action.command",
    "label": "Build Frontend",
    "config": {
        "command": "npm run build",
        "cwd": "/root/vps-panel",
        "env": {"NODE_ENV": "production"},
        "wait_completion": true
    }
}
```

### Node: Condição
```python
{
    "type": "logic.condition",
    "label": "Se serviço online",
    "config": {
        "condition_type": "service_running",
        "service": "docker",
        "on_true": "continue",
        "on_false": "start_service"
    }
}
```

## 🎯 Implementação Técnica

### Fase 1: Editor Visual (✅ Em andamento)
- [x] Node Editor com DearPyGUI
- [x] Painel lateral com cards clicáveis
- [x] Adicionar nodes ao canvas
- [x] Conectar nodes com links
- [x] Deletar nodes (tecla Delete)
- [ ] Salvar/carregar grafo de nodes
- [ ] Arrastar nodes no canvas
- [ ] Editar propriedades de nodes

### Fase 2: Sistema de Execução
- [ ] Parser de grafo (ler conexões)
- [ ] Engine de execução sequencial
- [ ] Engine de execução paralela
- [ ] Sistema de logs em tempo real
- [ ] Tratamento de erros
- [ ] Rollback em caso de falha

### Fase 3: Nodes Básicos
- [ ] Implementar 5 tipos de nodes iniciais:
  - Projeto Iniciado
  - Abrir (aplicação genérica)
  - Terminal (executar comando)
  - Docker Compose
  - Condição (if)

### Fase 4: Interface de Configuração
- [ ] Janela modal para editar propriedades
- [ ] Formulário dinâmico baseado no tipo de node
- [ ] Validação de campos
- [ ] Preview de comando a ser executado

### Fase 5: Biblioteca de Workflows
- [ ] Salvar workflows como templates
- [ ] Galeria de workflows prontos
- [ ] Import/export de workflows (.json)
- [ ] Compartilhamento de workflows

## 🚀 Próximos Passos Imediatos

1. **Definir estrutura de dados do grafo:**
   - Como serializar nodes + links
   - Formato JSON para salvar workflows
   - Schema de validação

2. **Implementar editor de propriedades:**
   - Modal que abre ao clicar duas vezes no node
   - Campos dinâmicos baseados no tipo
   - Salvar configurações no node

3. **Criar engine de execução básico:**
   - Percorrer grafo a partir do node inicial
   - Seguir links (output → input)
   - Executar ação de cada node
   - Mostrar progresso visual no canvas

4. **Adicionar mais tipos de nodes:**
   - Cada node com sua própria imagem/ícone
   - Paleta organizada por categorias
   - Search/filtro na paleta

## 💡 Ideias Futuras

- **Variáveis de contexto**: Nodes podem passar dados entre si
- **Debugging**: Pausar execução, executar step-by-step
- **Versionamento**: Git para workflows
- **Execução agendada**: Cron-like scheduling
- **Notificações**: Discord, Telegram quando workflow terminar
- **Métricas**: Tempo de execução, taxa de sucesso
- **Validação**: Verificar se workflow é válido antes de executar

---

**🎨 Conceito Visual:**

Imagine poder ver todo o setup do seu ambiente de desenvolvimento em um diagrama visual, e com um clique tudo é configurado e iniciado automaticamente. Isso é o poder do sistema de nodes!

**Exemplo prático:**
```
Segunda-feira 9h → Você abre o Arquiteto
    ↓
Seleciona workflow "Dev Use Gaba"
    ↓
Clica em "Executar"
    ↓
Em 30 segundos:
    ✓ Convex rodando
    ✓ Zed aberto no projeto
    ✓ Terminal com logs
    ✓ Browser na aplicação
    ✓ Tudo pronto para codar! 🚀
```
