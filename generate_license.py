"""
Generate License Tool - Command-line tool to generate and manage licenses
Run: python generate_license.py
"""

import sys
from pathlib import Path
from tabulate import tabulate

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "brp_portfolio_optimizer" / "src"))

from license_manager import LicenseManager


def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print("    BRP PORTFOLIO OPTIMIZER - LICENSE MANAGER")
    print("="*70 + "\n")


def print_menu():
    """Print menu options"""
    print("What would you like to do?\n")
    print("1. Generate new license")
    print("2. Validate license")
    print("3. List all licenses")
    print("4. Extend license")
    print("5. Revoke license")
    print("6. Exit")
    print()


def generate_new_license(manager):
    """Generate a new license"""
    print("\n--- Generate New License ---\n")
    
    email = input("Enter user email: ").strip()
    if not email or "@" not in email:
        print("❌ Invalid email format")
        return
    
    try:
        days = int(input("Days valid (default 30): ") or "30")
        if days < 1:
            print("❌ Days must be at least 1")
            return
    except ValueError:
        print("❌ Invalid number")
        return
    
    result = manager.generate_license(email, days)
    
    print("\n✅ License Generated Successfully!\n")
    print("=" * 70)
    print(f"Email:             {result['email']}")
    print(f"Expiration Date:   {result['expiration_date']}")
    print(f"Days Valid:        {result['days_valid']}")
    print("\nLicense Key (share with client):")
    print("-" * 70)
    print(f"{result['license_key']}")
    print("-" * 70 + "\n")
    
    # Offer to copy to clipboard
    try:
        import pyperclip
        pyperclip.copy(result['license_key'])
        print("✅ License key copied to clipboard!\n")
    except:
        print("💡 Tip: Install pyperclip to auto-copy: pip install pyperclip\n")


def validate_license(manager):
    """Validate a license key"""
    print("\n--- Validate License ---\n")
    
    email = input("Enter user email: ").strip()
    license_key = input("Enter license key: ").strip()
    
    is_valid, message = manager.validate_license(email, license_key)
    
    print()
    if is_valid:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    print()


def list_licenses(manager):
    """List all licenses"""
    print("\n--- All Licenses ---\n")
    
    licenses = manager.list_licenses()
    
    if not licenses:
        print("No licenses found.\n")
        return
    
    # Prepare data for table
    table_data = []
    for lic in licenses:
        table_data.append([
            lic['email'],
            lic['expiration_date'],
            lic['status'].upper(),
            lic['created_at']
        ])
    
    headers = ["Email", "Expiration", "Status", "Created"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    print()


def extend_license(manager):
    """Extend an existing license"""
    print("\n--- Extend License ---\n")
    
    email = input("Enter user email: ").strip()
    
    lic_info = manager.get_license_info(email)
    if not lic_info:
        print(f"❌ License not found for {email}\n")
        return
    
    print(f"Current expiration: {lic_info['expiration_date']}")
    
    try:
        days = int(input("Additional days to add (default 30): ") or "30")
        if days < 1:
            print("❌ Days must be at least 1")
            return
    except ValueError:
        print("❌ Invalid number")
        return
    
    result = manager.extend_license(email, days)
    
    print("\n✅ License Extended Successfully!\n")
    print("=" * 70)
    print(f"Email:             {result['email']}")
    print(f"New Expiration:    {result['expiration_date']}")
    print(f"Days Added:        {result['additional_days']}")
    print("\nNew License Key:")
    print("-" * 70)
    print(f"{result['license_key']}")
    print("-" * 70 + "\n")


def revoke_license(manager):
    """Revoke a license"""
    print("\n--- Revoke License ---\n")
    
    email = input("Enter user email: ").strip()
    
    lic_info = manager.get_license_info(email)
    if not lic_info:
        print(f"❌ License not found for {email}\n")
        return
    
    confirm = input(f"Are you sure you want to revoke license for {email}? (yes/no): ").lower()
    
    if confirm == "yes":
        manager.revoke_license(email)
        print(f"✅ License revoked for {email}\n")
    else:
        print("❌ Revocation cancelled\n")


def main():
    """Main application loop"""
    manager = LicenseManager("licenses.json")
    
    while True:
        print_header()
        print_menu()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == "1":
            generate_new_license(manager)
        elif choice == "2":
            validate_license(manager)
        elif choice == "3":
            list_licenses(manager)
        elif choice == "4":
            extend_license(manager)
        elif choice == "5":
            revoke_license(manager)
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid choice. Please try again.\n")
        
        input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
