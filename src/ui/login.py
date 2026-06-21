"""Login UI"""

from typing import Optional, Tuple
from .components import (
    print_header, get_input, print_status, print_box, console
)


class LoginUI:
    """Login interface"""
    
    def __init__(self):
        self.app_name = "Telegram Content Compliance Analyzer"
        self.app_version = "1.0"
    
    def get_credentials(self) -> Tuple[Optional[int], Optional[str], Optional[str]]:
        """Get API credentials from user"""
        print_header(self.app_name, self.app_version)
        console.print("\n[cyan]Telegram API Credentials[/cyan]")
        console.print("[dim]Get credentials from https://my.telegram.org[/dim]\n")
        
        try:
            api_id_str = get_input("API ID")
            if not api_id_str.isdigit():
                print_status("Invalid API ID format", False)
                return None, None, None
            
            api_id = int(api_id_str)
            api_hash = get_input("API Hash")
            
            if not api_hash or len(api_hash) < 32:
                print_status("Invalid API Hash", False)
                return None, None, None
            
            return api_id, api_hash, None
            
        except Exception as e:
            print_status(f"Error getting credentials: {e}", False)
            return None, None, None
    
    def get_phone_number(self) -> Optional[str]:
        """Get phone number from user"""
        console.print("\n[cyan]Phone Number[/cyan]")
        console.print("[dim]Format: +<country_code><number>[/dim]\n")
        
        phone = get_input("Phone number")
        
        if not phone or not phone.startswith('+'):
            print_status("Invalid phone number format", False)
            return None
        
        return phone
    
    def get_otp_code(self) -> Optional[str]:
        """Get OTP code from user"""
        console.print("\n[cyan]One-Time Password[/cyan]")
        console.print("[dim]Check your Telegram app for the code[/dim]\n")
        
        code = get_input("Enter OTP code")
        
        if not code:
            return None
        
        return code
    
    def get_password(self) -> Optional[str]:
        """Get password for 2FA if needed"""
        console.print("\n[cyan]Two-Factor Authentication[/cyan]")
        console.print("[dim]Your account has 2FA enabled[/dim]\n")
        
        from rich.prompt import Prompt
        password = Prompt.ask("Enter password", password=True)
        
        return password if password else None
    
    def get_session_name(self) -> Optional[str]:
        """Get session name for saving"""
        console.print("\n[cyan]Session Configuration[/cyan]\n")
        
        session_name = get_input("Session name", default="default")
        
        if not session_name:
            return None
        
        return session_name
    
    def show_login_progress(self, step: str, status: bool = True) -> None:
        """Show login progress"""
        symbol = "✓" if status else "✗"
        color = "green" if status else "red"
        console.print(f"[{color}]{symbol}[/{color}] {step}")
    
    def show_login_success(self, user_info: dict) -> None:
        """Show successful login"""
        user_text = f"""[cyan]Name[/cyan]: {user_info.get('first_name', '')} {user_info.get('last_name', '')}
[cyan]Username[/cyan]: @{user_info.get('username', 'N/A')}
[cyan]Phone[/cyan]: {user_info.get('phone', 'N/A')}"""
        
        print_box(user_text, "Logged In Successfully", "green")
    
    def show_login_error(self, error: str) -> None:
        """Show login error"""
        print_box(error, "Login Error", "red")
