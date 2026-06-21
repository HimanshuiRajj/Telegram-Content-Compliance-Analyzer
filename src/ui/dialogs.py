"""Dialogs Selection UI"""

from typing import List, Optional
from .components import print_table, get_input, console


class DialogsUI:
    """Dialogs selection interface"""
    
    def show_dialogs(self, dialogs: List[dict]) -> None:
        """Display available dialogs"""
        console.print("\n[cyan]Available Channels & Groups[/cyan]\n")
        
        if not dialogs:
            console.print("[yellow]No dialogs available[/yellow]")
            return
        
        rows = []
        for dialog in dialogs:
            rows.append([
                str(dialog['id']),
                dialog['name'][:40],
                dialog['type'],
                str(dialog['members']),
                str(dialog['unread_count']),
            ])
        
        print_table(
            "Dialogs",
            ["ID", "Name", "Type", "Members", "Unread"],
            rows
        )
    
    def get_dialog_selection(self, dialogs: List[dict]) -> List[int]:
        """Get dialog selection from user"""
        console.print("\n[cyan]Select Dialogs[/cyan]")
        console.print("[dim]Options: 1 | 1,5,8 | 1-20 | all[/dim]\n")
        
        selection_input = get_input("Enter selection")
        
        if not selection_input:
            return []
        
        selected_ids = []
        
        try:
            if selection_input.lower() == 'all':
                selected_ids = [d['id'] for d in dialogs]
            
            elif '-' in selection_input:
                # Range selection
                parts = selection_input.split('-')
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                selected_ids = [d['id'] for d in dialogs if start <= d['id'] <= end]
            
            elif ',' in selection_input:
                # Multiple selection
                ids = [int(x.strip()) for x in selection_input.split(',')]
                selected_ids = [d['id'] for d in dialogs if d['id'] in ids]
            
            else:
                # Single selection
                dialog_id = int(selection_input)
                if any(d['id'] == dialog_id for d in dialogs):
                    selected_ids = [dialog_id]
        
        except (ValueError, IndexError):
            console.print("[red]Invalid selection format[/red]")
            return []
        
        if selected_ids:
            console.print(f"\n[green]✓ Selected {len(selected_ids)} dialog(s)[/green]")
        else:
            console.print("[red]No valid dialogs selected[/red]")
        
        return selected_ids
    
    def show_message_range_menu(self) -> Optional[int]:
        """Show message range selection menu"""
        console.print("\n[cyan]Select Message Range[/cyan]\n")
        
        options = [
            "[1] Last 100 Messages",
            "[2] Last 500 Messages",
            "[3] Last 1000 Messages",
            "[4] Last 2000 Messages",
            "[5] Last 5000 Messages",
            "[6] Custom Range",
        ]
        
        for option in options:
            console.print(f"  {option}")
        
        choice = get_input("Enter choice", "1")
        
        range_map = {
            '1': 100,
            '2': 500,
            '3': 1000,
            '4': 2000,
            '5': 5000,
            '6': None,  # Custom
        }
        
        return range_map.get(choice, 100)
    
    def get_custom_message_range(self) -> tuple[Optional[int], Optional[int]]:
        """Get custom message range"""
        console.print("\n[cyan]Custom Message Range[/cyan]\n")
        
        console.print("[yellow]Option 1: By Message ID[/yellow]")
        start_id_str = get_input("Start Message ID", "")
        end_id_str = get_input("End Message ID", "")
        
        if start_id_str and end_id_str:
            try:
                return int(start_id_str), int(end_id_str)
            except ValueError:
                pass
        
        console.print("\n[yellow]Option 2: By Date[/yellow]")
        from_date = get_input("From Date (YYYY-MM-DD)", "")
        to_date = get_input("To Date (YYYY-MM-DD)", "")
        
        if from_date and to_date:
            return from_date, to_date
        
        console.print("[red]Invalid range specified[/red]")
        return None, None
