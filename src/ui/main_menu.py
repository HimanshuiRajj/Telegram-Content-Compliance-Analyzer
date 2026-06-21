"""Main Menu UI"""

from typing import Optional
from .components import (
    print_header, create_menu_table, get_menu_choice, console
)


class MainMenu:
    """Main menu interface"""
    
    def __init__(self):
        self.app_name = "Telegram Content Compliance Analyzer"
        self.app_version = "1.0"
    
    def show(self) -> Optional[str]:
        """Display main menu and get user choice"""
        print_header(self.app_name, self.app_version)
        
        console.print()
        menu_options = [
            "[1] Login Telegram Account",
            "[2] Load Existing Session",
            "[3] Manage Accounts",
            "[4] Exit",
        ]
        
        for option in menu_options:
            console.print(f"  {option}")
        
        choice = console.input("\n[yellow]Enter your choice (1-4)[/yellow]: ").strip()
        
        choice_map = {
            '1': 'login',
            '2': 'load_session',
            '3': 'manage_accounts',
            '4': 'exit',
        }
        
        return choice_map.get(choice)
    
    def show_account_menu(self) -> Optional[str]:
        """Show account management menu"""
        console.print("\n[cyan]Account Management[/cyan]")
        
        options = [
            "[1] View Sessions",
            "[2] Delete Session",
            "[3] Switch Account",
            "[4] Back",
        ]
        
        for option in options:
            console.print(f"  {option}")
        
        choice = console.input("\n[yellow]Enter your choice (1-4)[/yellow]: ").strip()
        
        choice_map = {
            '1': 'view_sessions',
            '2': 'delete_session',
            '3': 'switch_account',
            '4': 'back',
        }
        
        return choice_map.get(choice)
