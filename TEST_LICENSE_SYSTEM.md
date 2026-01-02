# 🧪 TESTE RÁPIDO - VALIDAR SISTEMA DE LICENÇAS

## ✅ Checklist de Implementação

Execute cada passo abaixo para validar que tudo está funcionando:

---

## 📋 Teste 1: Gerar Primeira Licença

```bash
python generate_license.py
```

**O que deve aparecer:**
```
════════════════════════════════════════════════════════════════
    BRP PORTFOLIO OPTIMIZER - LICENSE MANAGER
════════════════════════════════════════════════════════════════

What would you like to do?

1. Generate new license
2. Validate license
3. List all licenses
4. Extend license
5. Revoke license
6. Exit

Enter your choice (1-6): 
```

**Escolha: `1`**

```bash
Enter user email: test@example.com
Days valid (default 30): 30
```

**Resultado Esperado:**
```
✅ License Generated Successfully!

══════════════════════════════════════════════════════════════════
Email:             test@example.com
Expiration Date:   2026-02-01
Days Valid:        30

License Key (share with client):
──────────────────────────────────────────────────────────────────
test@example.com|2026-02-01|[CHAVE_HMAC]
──────────────────────────────────────────────────────────────────
```

✅ **SUCESSO** se viu isso acima

---

## 📋 Teste 2: Validar Licença Gerada

```bash
python generate_license.py
```

**Escolha: `2`**

```bash
Enter user email: test@example.com
Enter license key: test@example.com|2026-02-01|[CHAVE_HMAC]
```

**Resultado Esperado:**
```
✅ License valid for 30 more days
```

✅ **SUCESSO** se viu mensagem de válida

---

## 📋 Teste 3: Listar Licenses

```bash
python generate_license.py
```

**Escolha: `3`**

**Resultado Esperado:**
```
│ test@example.com  │ 2026-02-01     │ ACTIVE   │ 2026-01-02 10:00 │
```

✅ **SUCESSO** se viu sua email na tabela

---

## 📋 Teste 4: Testar com Streamlit

```bash
streamlit run app.py
```

**O que deve acontecer:**
1. Browser abre automaticamente
2. Você vê tela: **"🔐 License Verification"**
3. Dois campos: Email e License Key
4. Um botão: "✅ Verify License"

**Teste:**
```
Email: test@example.com
Key: test@example.com|2026-02-01|[CHAVE_HMAC]
Clique: ✅ Verify License
```

**Resultado Esperado:**
```
✅ License valid for 30 more days
[App abre normalmente com todos os tabs]
```

✅ **SUCESSO** se o app abriu após validação

---

## 📋 Teste 5: Verificar Sidebar

Após o app abrir, veja no **Sidebar esquerdo**:

**Deve aparecer:**
```
Licensed to: test@example.com
```

✅ **SUCESSO** se viu essa mensagem

---

## 📋 Teste 6: Testar Rejeição de License Inválida

```bash
streamlit run app.py
```

**Teste com dados errados:**
```
Email: test@example.com
Key: teste_errado_123456
Clique: ✅ Verify License
```

**Resultado Esperado:**
```
❌ License key is invalid (corrupted or tampered)
```

✅ **SUCESSO** se bloqueou e mostrou erro

---

## 📋 Teste 7: Testar Email Não Correspondente

```bash
streamlit run app.py
```

**Teste com email diferente:**
```
Email: outroemail@company.com
Key: test@example.com|2026-02-01|[CHAVE_HMAC]
Clique: ✅ Verify License
```

**Resultado Esperado:**
```
❌ License email does not match
```

✅ **SUCESSO** se bloqueou por email incorreto

---

## 📋 Teste 8: Validar Arquivo de Licenses

Abra com editor de texto:
```
licenses.json
```

**Deve conter:**
```json
{
  "test@example.com": {
    "license_key": "test@example.com|2026-02-01|...",
    "email": "test@example.com",
    "expiration_date": "2026-02-01",
    "created_at": "2026-01-02 ...:...:...",
    "status": "active"
  }
}
```

✅ **SUCESSO** se a estrutura está correta

---

## 📋 Teste 9: Estender License

```bash
python generate_license.py
```

**Escolha: `4`**

```bash
Enter user email: test@example.com
Additional days to add (default 30): 30
```

**Resultado Esperado:**
```
✅ License Extended Successfully!

New Expiration: 2026-03-02
Days Added: 30

New License Key:
────────────────────────────────────────────
test@example.com|2026-03-02|[NOVO_HMAC]
────────────────────────────────────────────
```

✅ **SUCESSO** se data foi estendida por 30 dias

---

## 📋 Teste 10: Revogar License

```bash
python generate_license.py
```

**Escolha: `5`**

```bash
Enter user email: test@example.com
Are you sure you want to revoke license for test@example.com? (yes/no): yes
```

**Resultado Esperado:**
```
✅ License revoked for test@example.com
```

**Verificação:**
```bash
python generate_license.py
3  (List all licenses)
```

Deve aparecer:
```
│ test@example.com  │ 2026-03-02     │ REVOKED  │ ... │
```

✅ **SUCESSO** se status mudou para REVOKED

---

## 📋 Teste 11: Compilar .EXE

```bash
build_exe.bat
```

**Aguarde 2-5 minutos**

**Resultado Esperado:**
```
BUILD COMPLETE! Executable is in: dist\BRP_Portfolio_Optimizer.exe
```

**Verifique:**
- [ ] Arquivo existe: `dist/BRP_Portfolio_Optimizer.exe`
- [ ] Tamanho: 50-200 MB
- [ ] Duplo clique funciona

✅ **SUCESSO** se .exe foi criado e roda

---

## 📋 Teste 12: Testar .EXE com License

1. Gere nova license:
```bash
python generate_license.py
# Escolha 1
# Email: exe_test@company.com
# Days: 30
```

2. Execute o .exe:
```bash
dist\BRP_Portfolio_Optimizer.exe
```

**O que deve aparecer:**
- Tela de "License Verification"
- Dois campos: Email e Key
- Botão: "✅ Verify License"

3. Teste com a chave gerada:
```
Email: exe_test@company.com
Key: exe_test@company.com|2026-02-01|[HMAC]
Clique: ✅ Verify License
```

**Resultado Esperado:**
```
✅ License valid for 30 more days
[App abre normalmente]
```

✅ **SUCESSO** se .exe bloqueou sem license e abriu com license válida

---

## 🎯 Resumo de Testes

| # | Teste | Status | Notas |
|---|-------|--------|-------|
| 1 | Gerar License | ☐ ✅ | |
| 2 | Validar License | ☐ ✅ | |
| 3 | Listar Licenses | ☐ ✅ | |
| 4 | App com Streamlit | ☐ ✅ | |
| 5 | Sidebar mostra Email | ☐ ✅ | |
| 6 | Rejeita Inválida | ☐ ✅ | |
| 7 | Rejeita Email Errado | ☐ ✅ | |
| 8 | licenses.json correto | ☐ ✅ | |
| 9 | Estender License | ☐ ✅ | |
| 10 | Revogar License | ☐ ✅ | |
| 11 | Compilar .EXE | ☐ ✅ | |
| 12 | .EXE com License | ☐ ✅ | |

---

## 🔍 Se Algo Falhar

### "ModuleNotFoundError: No module named 'tabulate'"

```bash
pip install tabulate pyperclip
```

---

### ".EXE não inicia"

```bash
# Teste primeiro com Streamlit
streamlit run app.py

# Se funcionar, execute novamente:
build_exe.bat
```

---

### "License validation fails"

1. Verifique: Email exato (maiúsculas/minúsculas)
2. Verifique: Chave não foi modificada
3. Copie exatamente da saída do generate_license.py

---

### "licenses.json não encontrado"

Deve estar na raiz do projeto:
```
brp-portfolio-optimizer/
├── licenses.json  ← Aqui
├── app.py
├── generate_license.py
└── ...
```

---

## ✅ Todos os Testes Passaram?

**Se SIM, você está pronto para:**

1. ✅ Gerar licenses para clientes
2. ✅ Distribuir .exe
3. ✅ Gerenciar renovações
4. ✅ Revogar acessos

**Próximo passo:** Leia `LICENSE_QUICK_REFERENCE.md` para fluxo com clientes reais

---

## 📞 Suporte

Se algo não funcionou:

1. Verifique: Python 3.8+ instalado
2. Verifique: Requirements instalados: `pip install -r requirements.txt`
3. Verifique: Diretório correto: `cd brp_optimize_portfolio`
4. Releia: `LICENSE_SYSTEM_COMPLETE.md`

---

**Parabéns por implementar o sistema de licenças! 🎉**
