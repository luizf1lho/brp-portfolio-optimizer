# 🔑 QUICK REFERENCE - LICENSE MANAGEMENT

## 📌 Para Você (Developer)

### 1️⃣ Gerar Uma Nova Licença

```bash
python generate_license.py
```

**Menu:**
```
1. Generate new license         ← Escolha isso
2. Validate license
3. List all licenses
4. Extend license
5. Revoke license
6. Exit
```

**Exemplo:**
```
Email: john.doe@company.com
Days valid: 30
```

**Resultado:**
```
✅ License Generated Successfully!
License Key: john.doe@company.com|2026-02-01|A1B2C3D4E5F6G7H8
```

### 2️⃣ Enviar Para o Cliente

**Via Email:**
```
Subject: Seu License para BRP Portfolio Optimizer

Olá John,

Seu license foi gerado com sucesso:

EMAIL: john.doe@company.com
LICENSE KEY: john.doe@company.com|2026-02-01|A1B2C3D4E5F6G7H8
VÁLIDO ATÉ: 01 de Fevereiro de 2026

Arquivos anexados:
- BRP_Portfolio_Optimizer.exe
- README_CLIENT.txt

Instruções:
1. Extraia os arquivos
2. Execute o .exe
3. Coloque seu email e license key
4. Clique em Verify License

Qualquer dúvida, contate support@...
```

---

## 👥 Para o Cliente

### 1️⃣ Primeiro Acesso

1. **Baixe os arquivos:**
   - `BRP_Portfolio_Optimizer.exe`
   - Salve em pasta segura (ex: `C:\Portfolio Optimizer\`)

2. **Execute o programa:**
   - Duplo clique no `.exe`

3. **Tela de License:**
   - Email: `john.doe@company.com`
   - License Key: `john.doe@company.com|2026-02-01|A1B2C3D4E5F6G7H8`
   - Clique: ✅ Verify License

4. **Pronto!** 🎉
   - Aplicação abre normalmente

### 2️⃣ Durante o Uso

- License info aparece no canto superior esquerdo (Sidebar)
- Mostra: "Licensed to: john.doe@company.com"

### 3️⃣ License Expirando

**Aviso antes de expirar:**
```
⚠️ Your license expires in 5 days
Contact support for renewal
```

**Após expirar:**
```
❌ License expired 3 days ago
Contact support@yourcompany.com to renew
```

---

## 🔧 Operações Comuns

### Listar Todas as Licenças

```bash
python generate_license.py
→ Escolha: 3. List all licenses
```

**Resultado:**
```
┌──────────────────────┬────────────────┬──────────┬────────────────────┐
│ Email                │ Expiration     │ Status   │ Created            │
├──────────────────────┼────────────────┼──────────┼────────────────────┤
│ client1@company.com  │ 2026-02-01     │ ACTIVE   │ 2026-01-02 10:00   │
│ client2@company.com  │ 2026-03-15     │ ACTIVE   │ 2026-01-02 11:30   │
│ old.client@email.com │ 2025-12-15     │ REVOKED  │ 2025-11-01 09:00   │
└──────────────────────┴────────────────┴──────────┴────────────────────┘
```

### Estender Uma Licença

```bash
python generate_license.py
→ Escolha: 4. Extend license
→ Email: john.doe@company.com
→ Additional days: 30
```

**Resultado:**
```
✅ License Extended Successfully!
New License Key: john.doe@company.com|2026-03-02|X9Y8Z7W6V5U4T3S2
```

### Revogar Uma Licença

```bash
python generate_license.py
→ Escolha: 5. Revoke license
→ Email: old.client@company.com
→ Confirme: yes
```

---

## 🚀 Compilar para .EXE

### Pré-requisitos

```bash
pip install pyinstaller
```

### Compilar

```bash
build_exe.bat
```

**Resultado:**
```
dist\BRP_Portfolio_Optimizer.exe
```

---

## 📊 Fluxo Completo - Exemplo Real

### Cenário: Novo Cliente "João Silva"

**Passo 1 - Você gera license:**
```bash
python generate_license.py
1
joao.silva@empresa.com.br
30
```

**Resultado:**
```
✅ License Generated!
Key: joao.silva@empresa.com.br|2026-02-01|ABC123DEF456GHI789
```

**Passo 2 - Você envia email:**
```
Olá João,

Seu sistema está pronto! Segue:

EMAIL: joao.silva@empresa.com.br
CHAVE: joao.silva@empresa.com.br|2026-02-01|ABC123DEF456GHI789
VÁLIDO: 30 dias

Arquivo: BRP_Portfolio_Optimizer.exe
```

**Passo 3 - João executa:**
- Duplo clique no `.exe`
- Insere email
- Insere chave
- Clica "Verify License"
- Sistema abre! ✅

**Passo 4 - 29 dias depois:**
- João recebe aviso: "License expira em 1 dia"

**Passo 5 - Você renova:**
```bash
python generate_license.py
4  (Extend license)
joao.silva@empresa.com.br
30
```

**Passo 6 - Você envia nova chave por email**
- João atualiza e continua usando! ✅

---

## 🛡️ Segurança - Importante!

### O que NÃO fazer:

❌ Compartilhar `licenses.json` publicamente
❌ Commitar `licenses.json` em GitHub público
❌ Usar a mesma chave para múltiplos clientes
❌ Deixar chaves expiradas ativas

### O que FAZER:

✅ Manter `licenses.json` privado (servidor seu)
✅ Gerar chave única por cliente
✅ Definir expiração curta (30 dias)
✅ Renovar regularmente
✅ Revogar ex-clientes

---

## 📝 Arquivo de Licenças (licenses.json)

**Estrutura:**
```json
{
  "client@email.com": {
    "license_key": "client@email.com|2026-02-01|ABC123",
    "email": "client@email.com",
    "expiration_date": "2026-02-01",
    "created_at": "2026-01-02 10:00:00",
    "status": "active"
  }
}
```

**Campos:**
- `license_key`: Chave para o cliente usar
- `email`: Email do cliente
- `expiration_date`: Data de vencimento (YYYY-MM-DD)
- `created_at`: Quando foi gerada
- `status`: "active" ou "revoked"

---

## ❓ FAQ Rápido

**P: Cliente digitou email errado. O que fazer?**
A: Gere uma nova chave com o email correto.

**P: Cliente perdeu a chave. Como recuperar?**
A: Vire o arquivo `licenses.json`, copie a `license_key` para aquele email.

**P: Quero mudar a chave secreta?**
A: Edite `license_manager.py`, mude `SECRET_KEY`, regenere todas as chaves.

**P: Posso usar online/offline?**
A: Agora está offline (no arquivo). Para online, veja BUILD_EXE_GUIDE.md

**P: Cliente copiou a chave para outro amigo?**
A: Chave vinculada ao email, precisa do email correto. Pode revogar original.

---

## 🎯 Checklist Antes de Distribuir

- [ ] License system testado localmente
- [ ] `generate_license.py` funcionando
- [ ] `.exe` compilado com sucesso
- [ ] Teste com license verdadeira no `.exe`
- [ ] Documentação cliente preparada
- [ ] Email de suporte definido
- [ ] Plano de renovação definido
- [ ] Backup de `licenses.json` feito

---

## 📞 Problemas Comuns

**"License invalid"**
→ Check: Email match (case-sensitive)
→ Check: Chave não foi modificada
→ Check: Data não expirou

**"Cannot find license_manager"**
→ Instale requirements: `pip install -r requirements.txt`
→ Verifique: `brp_portfolio_optimizer/src/license_manager.py` existe

**".EXE não inicia"**
→ Rode: `streamlit run app.py` primeiro (teste)
→ Verifique: Todos requirements instalados
→ Tente: `build_exe.bat` novamente

---

**Você está pronto para distribuir! 🚀**
