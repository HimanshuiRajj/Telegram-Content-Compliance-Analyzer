"""Rich-based UI components"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from typing import List, Dict, Optional
import sys

console = Console()


def print_header(title: str, version: str = "1.0") -> None:
    """Print application header"""
    header_text = f"{title} v{version}"
    console.print(Panel(
        header_text,
        expand=False,
        border_style="cyan",
        style="bold cyan"
    ))


def print_box(content: str, title: Optional[str] = None, style: str = "green") -> None:
    """Print a box with content"""
    console.print(Panel(
        content,
        title=title,
        expand=False,
        border_style=style,
        style=f"bold {style}"
    ))


def print_status(status: str, success: bool = True) -> None:
    """Print status message"""
    symbol = "✓" if success else "✗"
    color = "green" if success else "red"
    console.print(f"[{color}]{symbol}[/{color}] {status}")


def print_table(
    title: str,
    headers: List[str],
    rows: List[List[str]],
    style: str = "cyan"
) -> None:
    """Print a rich table"""
    table = Table(title=title, style=style, show_header=True, header_style="bold magenta")
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        table.add_row(*row)
    
    console.print(table)


def print_progress(
    description: str,
    total: int,
    completed: int,
    elapsed: str = "",
    findings: int = 0
) -> None:
    """Print progress information"""
    percentage = (completed / total * 100) if total > 0 else 0
    progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
    
    output = f"\n[cyan]{description}[/cyan]\n"
    output += f"[yellow]{progress_bar}[/yellow] {percentage:.1f}%\n"
    output += f"[white]{completed:,} / {total:,} Messages[/white]"
    
    if findings > 0:
        output += f"\n[red]Current Risk Findings: {findings}[/red]"
    
    if elapsed:
        output += f"\n[dim]Elapsed Time: {elapsed}[/dim]"
    
    console.print(output)


def print_findings_summary(
    total_messages: int,
    total_findings: int,
    high_risk: int,
    medium_risk: int,
    low_risk: int
) -> None:
    """Print findings summary"""
    summary_data = [
        ["Total Messages", str(total_messages)],
        ["Total Findings", f"[red]{total_findings}[/red]"],
        ["High Risk", f"[red]{high_risk}[/red]"],
        ["Medium Risk", f"[yellow]{medium_risk}[/yellow]"],
        ["Low Risk", f"[green]{low_risk}[/green]"],
    ]
    
    print_table("Findings Summary", ["Metric", "Count"], summary_data)


def print_category_summary(categories: Dict[str, int]) -> None:
    """Print category summary"""
    rows = [[cat, str(count)] for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True)]
    print_table("Findings by Category", ["Category", "Count"], rows, "magenta")


def create_menu_table(options: List[Dict[str, str]]) -> str:
    """Create menu table"""
    table = Table(show_header=False, show_footer=False, border_style="blue")
    
    for option in options:
        table.add_row(f"[cyan]{option['key']}[/cyan]", option['label'])
    
    console.print(table)


def print_user_info(user_data: Dict) -> None:
    """Print user information box"""
    if not user_data:
        console.print("[red]No user data available[/red]")
        return
    
    user_text = f"""[cyan]Name[/cyan]: {user_data.get('first_name', '')} {user_data.get('last_name', '')}
[cyan]Username[/cyan]: @{user_data.get('username', 'N/A')}
[cyan]Phone[/cyan]: {user_data.get('phone', 'N/A')}
[cyan]ID[/cyan]: {user_data.get('id', 'N/A')}"""
    
    console.print(Panel(
        user_text,
        title="[bold]Logged In Successfully[/bold]",
        expand=False,
        border_style="green",
        style="bold green"
    ))


def print_dialogs_info(dialogs: List[Dict], selected_count: int = 0) -> None:
    """Print dialogs information"""
    table = Table(title="Available Dialogs", style="cyan", show_header=True, header_style="bold magenta")
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Type")
    table.add_column("Members")
    table.add_column("Unread")
    
    for dialog in dialogs:
        table.add_row(
            str(dialog['id']),
            dialog['name'][:30],
            dialog['type'],
            str(dialog['members']),
            str(dialog['unread_count'])
        )
    
    console.print(table)
    
    if selected_count > 0:
        console.print(f"\n[green]✓ {selected_count} dialog(s) selected[/green]")


def clear_screen() -> None:
    """Clear terminal screen"""
    import os
    os.system('cls' if sys.platform == 'win32' else 'clear')


def get_input(prompt: str, default: str = "") -> str:
    """Get user input with prompt"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    return console.input(prompt).strip() or default


def get_menu_choice(options: List[str]) -> Optional[str]:
    """Get menu choice from user"""
    console.print("\n[cyan]Select an option:[/cyan]")
    
    for i, option in enumerate(options, 1):
        console.print(f"  [{i}] {option}")
    
    choice = console.input("\n[yellow]Enter your choice[/yellow]: ").strip()
    
    try:
        index = int(choice) - 1
        if 0 <= index < len(options):
            return options[index]
    except ValueError:
        pass
    
    console.print("[red]Invalid choice[/red]")
    return None


def confirm_action(message: str) -> bool:
    """Ask for confirmation"""
    response = console.input(f"\n[yellow]{message} (y/n): [/yellow]").strip().lower()
    return response == 'y'
