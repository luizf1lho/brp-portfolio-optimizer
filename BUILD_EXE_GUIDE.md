# 📦 Building BRP Portfolio Optimizer as .EXE

This guide explains how to compile the Streamlit application into a standalone Windows executable (.exe) file.

---

## 🎯 Why Create an .EXE?

1. **Protection**: Customers cannot see or modify the source code
2. **Distribution**: Easy to share - just one file to distribute
3. **Convenience**: No Python installation required on client machine
4. **Licensing**: License keys are embedded and validated

---

## 📋 Prerequisites

You need to have:
- Python 3.8+ installed
- All dependencies installed (pip install -r requirements.txt)
- PyInstaller (we'll install it)

---

## 🚀 Step-by-Step Guide

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Create a Build Script

Create a file called `build_exe.bat` in the project root:

```batch
@echo off
echo Building BRP Portfolio Optimizer...
echo.

REM Clean previous builds
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del *.spec

REM Run PyInstaller
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --name="BRP_Portfolio_Optimizer" ^
    --add-data="brp_portfolio_optimizer;brp_portfolio_optimizer" ^
    --add-data="licenses.json;." ^
    --hidden-import=streamlit ^
    --hidden-import=pandas ^
    --hidden-import=numpy ^
    --hidden-import=scipy ^
    --hidden-import=matplotlib ^
    --hidden-import=quantstats ^
    --hidden-import=yfinance ^
    app.py

echo.
echo Build complete! Executable is in: dist\BRP_Portfolio_Optimizer.exe
pause
```

### Step 3: Create Application Icon (Optional)

To make the .exe look professional, create an icon file:

1. Create or download a 256x256 PNG image
2. Convert to .ico format using online tool: https://convertio.co/png-ico/
3. Save as `icon.ico` in the project root

If you don't have an icon, the build will still work without the `--icon` parameter.

### Step 4: Build the Executable

Run the build script:

```bash
build_exe.bat
```

The process will take 2-5 minutes. After completion:
- ✅ File: `dist/BRP_Portfolio_Optimizer.exe`
- ✅ This is your standalone executable!

---

## 📤 Distribution Package

### For Each Client, Provide:

```
Client Package/
├── BRP_Portfolio_Optimizer.exe         (The application)
├── licenses.json                       (Empty - filled by client)
├── README_CLIENT.txt                   (Setup instructions)
├── INSTALL.txt                         (Step-by-step guide)
└── SUPPORT.txt                         (Your contact info)
```

### README_CLIENT.txt Example:

```
╔════════════════════════════════════════════════════════════╗
║      BRP PORTFOLIO OPTIMIZER - CLIENT SETUP GUIDE          ║
╚════════════════════════════════════════════════════════════╝

1. INSTALLATION
   - Extract all files to a folder
   - No additional software installation needed!

2. GETTING YOUR LICENSE
   - You received an EMAIL with your license key
   - Email: your.email@example.com
   - License Key: email|date|hmac

3. RUNNING THE APPLICATION
   - Double-click: BRP_Portfolio_Optimizer.exe
   - Enter your EMAIL and LICENSE KEY
   - Click "Verify License"
   - Application starts!

4. USING THE APP
   - Upload your CSV file with trade data
   - Click "Analyze" to optimize allocation
   - View results and generate reports

5. SUPPORT
   - Contact: support@yourcompany.com
   - License issues: licensing@yourcompany.com
   - Technical help: support@yourcompany.com

═══════════════════════════════════════════════════════════════
```

---

## 🔒 License Management

### How Licensing Works:

1. **You (Developer):**
   ```bash
   python generate_license.py
   → Select option 1 (Generate new license)
   → Enter: client@example.com
   → Enter: 30 (days valid)
   → Copy: CLIENT@EXAMPLE.COM|2026-02-01|A1B2C3D4E5F6G7H8
   ```

2. **Send to Client:**
   - Email with their license key
   - Standalone .exe file
   - Client setup guide

3. **Client Uses App:**
   - Opens .exe
   - Enters email: client@example.com
   - Enters key: CLIENT@EXAMPLE.COM|2026-02-01|A1B2C3D4E5F6G7H8
   - Clicks verify
   - App runs for 30 days

4. **After Expiration:**
   - Client sees: "License expired 5 days ago"
   - Must renew license
   - You generate new key with extended date

---

## 🔄 Updating the License System

### Option A: Update licenses.json file
- Keep `licenses.json` in the application folder
- Client updates it manually (if you provide new versions)
- Requires app restart

### Option B: Keep licenses.json unchanged
- Each time you create a license, it's stored server-side
- You send the KEY to client
- Client enters it at runtime
- ✅ **Recommended** - more secure

---

## 📊 License Workflow Example

```
DEVELOPER SIDE:
┌─────────────────────────────────┐
│ python generate_license.py      │
│ 1. Generate new license         │
│ Email: john@company.com         │
│ Days: 30                        │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ License Key Generated:          │
│ john@company.com|2026-02-01|... │
└─────────────────────────────────┘
         ↓
    EMAIL TO CLIENT
         ↓

CLIENT SIDE:
┌─────────────────────────────────┐
│ Run: BRP_Portfolio_Optimizer.exe│
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ License Verification Screen:    │
│ Email: john@company.com         │
│ Key: john@company.com|2026-...  │
│ Button: ✅ Verify License       │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ ✅ License valid for 29 days    │
│ Application starts normally     │
└─────────────────────────────────┘
```

---

## 🛠️ Troubleshooting

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### "Module not found" error in .exe
Add to `build_exe.bat` under `--hidden-import`:
```batch
--hidden-import=modulename
```

### .exe takes long time to start
This is normal for Streamlit apps in .exe format (first load can be 10-30 seconds).

### "Cannot find licenses.json"
Make sure `licenses.json` is in the same folder as the .exe file.

### "Invalid HMAC" when validating
- Check that license key was not altered
- Ensure email matches exactly (case-insensitive but must match)

---

## 🔐 Security Best Practices

1. **Keep licenses.json secure**
   - Don't commit to public GitHub
   - Store in private location

2. **Change SECRET_KEY (Optional)**
   - Edit `license_manager.py`
   - Change `SECRET_KEY = "BRP_PORTFOLIO_OPTIMIZER_2026"`
   - This makes keys generated with different secrets incompatible

3. **Expire licenses regularly**
   - Generate licenses for limited periods
   - Require renewal for continued access

4. **Monitor license usage**
   - Keep track of generated keys
   - Revoke keys for former clients

---

## 📈 Advanced: Server-Side Validation

For maximum security, you can validate licenses on a server:

1. **Keep licenses.json on your server**
2. **Modify license_manager.py to call your API**
3. **Client .exe calls your server to validate**
4. **You can revoke instantly without client update**

Example API endpoint:
```
GET https://your-server.com/validate?email=john@company.com&key=xxx|yyy|zzz
Response: {"valid": true, "days_remaining": 15}
```

---

## ✅ Checklist Before Distribution

- [ ] Built .exe file successfully
- [ ] Tested .exe on clean Windows machine
- [ ] Generated test license key
- [ ] Tested license verification
- [ ] Created client setup guide
- [ ] Added your support email
- [ ] Created deployment package
- [ ] Tested with client email/key combination
- [ ] Documented expiration date
- [ ] Created renewal process

---

## 🚀 Your Distribution Package Template

Create a folder for each client:

```
Client_Name_2026-01/
├── BRP_Portfolio_Optimizer.exe
├── licenses.json (empty or template)
├── README_CLIENT.txt (with their email)
├── LICENSE_KEY.txt (their key - separate secure channel)
├── SUPPORT_CONTACT.txt
└── TROUBLESHOOTING.txt
```

---

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify Python version: `python --version`
3. Verify all packages: `pip list`
4. Test the app before building: `streamlit run app.py`
5. Check PyInstaller docs: https://pyinstaller.org/

---

**Happy distributing! 🎉**
