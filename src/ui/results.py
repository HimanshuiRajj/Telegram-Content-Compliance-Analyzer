"""Results Display UI"""

from typing import List, Dict
from .components import print_table, console


class ResultsUI:
    """Results display interface"""
    
    def show_findings_summary(
        self,
        total_messages: int,
        total_findings: int,
        high_risk: int,
        medium_risk: int,
        low_risk: int
    ) -> None:
        """Show findings summary"""
        rows = [
            ["Total Messages", f"[cyan]{total_messages:,}[/cyan]"],
            ["Total Findings", f"[red]{total_findings}[/red]"],
            ["High Risk", f"[red]{high_risk}[/red]"],
            ["Medium Risk", f"[yellow]{medium_risk}[/yellow]"],
            ["Low Risk", f"[green]{low_risk}[/green]"],
        ]
        
        print_table("Findings Summary", ["Metric", "Count"], rows, "cyan")
    
    def show_category_summary(self, categories: Dict[str, int]) -> None:
        """Show findings by category"""
        rows = []
        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            rows.append([category, f"[yellow]{count}[/yellow]"])
        
        print_table("Findings by Category", ["Category", "Count"], rows, "magenta")
    
    def show_findings_details(self, findings: List[Dict]) -> None:
        """Show detailed findings"""
        if not findings:
            console.print("[yellow]No findings to display[/yellow]")
            return
        
        console.print("\n[cyan]Detailed Findings[/cyan]\n")
        
        rows = []
        for finding in findings[:20]:  # Show first 20
            rows.append([
                str(finding['message_id']),
                finding['category'][:20],
                f"[{'red' if finding['risk_score'] >= 0.7 else 'yellow' if finding['risk_score'] >= 0.4 else 'green'}]{finding['risk_score']:.2f}[/]",
                finding['explanation'][:40] + "...",
            ])
        
        print_table(
            f"Details (showing {len(findings[:20])} of {len(findings)})",
            ["Message ID", "Category", "Risk Score", "Explanation"],
            rows
        )
        
        if len(findings) > 20:
            console.print(f"\n[dim]... and {len(findings) - 20} more findings[/dim]")
    
    def show_export_menu(self) -> str:
        """Show export format menu"""
        console.print("\n[cyan]Export Report[/cyan]\n")
        
        options = [
            "[1] Export PDF",
            "[2] Export HTML",
            "[3] Export JSON",
            "[4] Export CSV",
            "[5] Export All",
            "[6] Cancel",
        ]
        
        for option in options:
            console.print(f"  {option}")
        
        from .components import get_input
        choice = get_input("Enter choice", "1")
        
        choice_map = {
            '1': 'pdf',
            '2': 'html',
            '3': 'json',
            '4': 'csv',
            '5': 'all',
            '6': 'cancel',
        }
        
        return choice_map.get(choice, 'cancel')
    
    def show_export_result(self, format_type: str, file_path: str) -> None:
        """Show export result"""
        console.print(f"\n[green]✓ {format_type.upper()} exported successfully[/green]")
        console.print(f"[dim]Location: {file_path}[/dim]")
