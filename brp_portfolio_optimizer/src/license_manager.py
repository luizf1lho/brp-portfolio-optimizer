"""
License Manager - Handles license generation, validation, and expiration
Supports per-user licenses with expiration dates
"""

import json
import hmac
import hashlib
from datetime import datetime, timedelta
from pathlib import Path


class LicenseManager:
    """
    Manages license generation and validation with expiration dates
    """
    
    # Secret key for HMAC validation (change this for production)
    SECRET_KEY = "BRP_PORTFOLIO_OPTIMIZER_2026"
    
    def __init__(self, licenses_file: str = "licenses.json"):
        """
        Initialize License Manager
        
        Args:
            licenses_file: Path to licenses JSON file
        """
        self.licenses_file = Path(licenses_file)
        self.licenses = self._load_licenses()
    
    def _load_licenses(self) -> dict:
        """Load licenses from JSON file"""
        if self.licenses_file.exists():
            try:
                with open(self.licenses_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading licenses: {e}")
                return {}
        return {}
    
    def _save_licenses(self):
        """Save licenses to JSON file"""
        try:
            with open(self.licenses_file, 'w', encoding='utf-8') as f:
                json.dump(self.licenses, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving licenses: {e}")
    
    def _generate_hmac(self, email: str, expiration_date: str) -> str:
        """
        Generate HMAC signature for license key
        
        Args:
            email: User email
            expiration_date: Expiration date (YYYY-MM-DD format)
        
        Returns:
            HMAC signature (first 16 chars)
        """
        message = f"{email}|{expiration_date}".encode('utf-8')
        signature = hmac.new(
            self.SECRET_KEY.encode('utf-8'),
            message,
            hashlib.sha256
        ).hexdigest()
        return signature[:16].upper()
    
    def generate_license(self, email: str, days_valid: int = 30) -> dict:
        """
        Generate a new license key
        
        Args:
            email: User email (license identifier)
            days_valid: Number of days the license is valid
        
        Returns:
            Dictionary with license info
        """
        # Calculate expiration date
        expiration_date = datetime.now() + timedelta(days=days_valid)
        exp_str = expiration_date.strftime("%Y-%m-%d")
        
        # Generate HMAC
        hmac_sig = self._generate_hmac(email, exp_str)
        
        # Create license key format: EMAIL|EXPIRATION|HMAC
        license_key = f"{email}|{exp_str}|{hmac_sig}"
        
        # Store in memory
        self.licenses[email] = {
            "license_key": license_key,
            "email": email,
            "expiration_date": exp_str,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "active"
        }
        
        # Save to file
        self._save_licenses()
        
        return {
            "email": email,
            "license_key": license_key,
            "expiration_date": exp_str,
            "days_valid": days_valid
        }
    
    def validate_license(self, email: str, license_key: str) -> tuple[bool, str]:
        """
        Validate a license key
        
        Args:
            email: User email
            license_key: License key to validate
        
        Returns:
            Tuple (is_valid, message)
        """
        # Parse license key
        try:
            parts = license_key.split("|")
            if len(parts) != 3:
                return False, "Invalid license format"
            
            key_email, exp_date, provided_hmac = parts
            
            # Check email matches
            if key_email.lower() != email.lower():
                return False, "License email does not match"
            
            # Regenerate HMAC to verify
            expected_hmac = self._generate_hmac(key_email, exp_date)
            if provided_hmac != expected_hmac:
                return False, "License key is invalid (corrupted or tampered)"
            
            # Check expiration
            try:
                exp_datetime = datetime.strptime(exp_date, "%Y-%m-%d")
                if exp_datetime < datetime.now():
                    days_expired = (datetime.now() - exp_datetime).days
                    return False, f"License expired {days_expired} days ago"
            except ValueError:
                return False, "Invalid expiration date format"
            
            # License is valid
            days_remaining = (exp_datetime - datetime.now()).days
            return True, f"License valid for {days_remaining} more days"
            
        except Exception as e:
            return False, f"Error validating license: {str(e)}"
    
    def revoke_license(self, email: str) -> bool:
        """
        Revoke a license (mark as inactive)
        
        Args:
            email: User email
        
        Returns:
            True if successful
        """
        if email in self.licenses:
            self.licenses[email]["status"] = "revoked"
            self._save_licenses()
            return True
        return False
    
    def extend_license(self, email: str, additional_days: int = 30) -> dict:
        """
        Extend an existing license
        
        Args:
            email: User email
            additional_days: Days to add
        
        Returns:
            Updated license info or None if not found
        """
        if email not in self.licenses:
            return None
        
        # Parse current expiration
        current_lic = self.licenses[email]["license_key"]
        parts = current_lic.split("|")
        old_exp = datetime.strptime(parts[1], "%Y-%m-%d")
        
        # Calculate new expiration
        new_exp = old_exp + timedelta(days=additional_days)
        exp_str = new_exp.strftime("%Y-%m-%d")
        
        # Generate new HMAC
        hmac_sig = self._generate_hmac(email, exp_str)
        new_license_key = f"{email}|{exp_str}|{hmac_sig}"
        
        # Update
        self.licenses[email].update({
            "license_key": new_license_key,
            "expiration_date": exp_str,
            "extended_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        self._save_licenses()
        
        return {
            "email": email,
            "license_key": new_license_key,
            "expiration_date": exp_str,
            "additional_days": additional_days
        }
    
    def list_licenses(self) -> list:
        """List all active licenses"""
        return [
            {
                "email": lic["email"],
                "expiration_date": lic["expiration_date"],
                "status": lic["status"],
                "created_at": lic["created_at"]
            }
            for lic in self.licenses.values()
        ]
    
    def get_license_info(self, email: str) -> dict:
        """Get license information for a user"""
        if email in self.licenses:
            return self.licenses[email]
        return None


def check_license_startup(email: str, license_key: str, licenses_file: str = "licenses.json") -> bool:
    """
    Check license at application startup
    Returns True if valid, False otherwise
    """
    manager = LicenseManager(licenses_file)
    is_valid, message = manager.validate_license(email, license_key)
    return is_valid
