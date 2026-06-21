"""Scanner UI"""

from typing import Optional
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn
from .components import console


class ScannerUI:
    """Scanner interface for showing progress"""
    
    def __init__(self):
        self.progress = None
        self.task_id = None
    
    def start_scan(self, total_messages: int) -> "ScannerUI":
        """Start scan progress display"""
        self.progress = Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.1f}%"),
            TimeRemainingColumn(),
            console=console,
        )
        
        self.progress.__enter__()
        self.task_id = self.progress.add_task(
            f"[cyan]Scanning {total_messages:,} messages...",
            total=total_messages
        )
        
        return self
    
    def update_progress(self, current: int, findings: int = 0) -> None:
        """Update scan progress"""
        if self.progress and self.task_id is not None:
            description = f"[cyan]Scanned {current:,} messages"
            if findings > 0:
                description += f" • [red]{findings} findings[/red]"
            description += "[/cyan]"
            
            self.progress.update(self.task_id, advance=1, description=description)
    
    def stop_scan(self) -> None:
        """Stop scan progress display"""
        if self.progress:
            self.progress.__exit__(None, None, None)
            self.progress = None
    
    def show_analysis_progress(self, current: int, total: int) -> None:
        """Show analysis progress"""
        percentage = (current / total * 100) if total > 0 else 0
        
        console.print(
            f"[cyan]Analyzing messages... {current:,}/{total:,} ({percentage:.1f}%)[/cyan]"
        )
    
    def show_scan_summary(
        self,
        total_messages: int,
        total_findings: int,
        high_risk: int,
        medium_risk: int,
        low_risk: int,
        elapsed_time: str
    ) -> None:
        """Show scan summary"""
        console.print("\n")
        console.print("[green]═" * 40 + "═[/green]")
        console.print("[cyan]Scan Summary[/cyan]")
        console.print("[green]═" * 40 + "═[/green]")
        
        console.print(f"\n[white]Total Messages Scanned:[/white] [cyan]{total_messages:,}[/cyan]")
        console.print(f"[white]Total Findings:[/white] [red]{total_findings}[/red]")
        console.print(f"[white]High Risk:[/white] [red]{high_risk}[/red]")
        console.print(f"[white]Medium Risk:[/white] [yellow]{medium_risk}[/yellow]")
        console.print(f"[white]Low Risk:[/white] [green]{low_risk}[/green]")
        console.print(f"[white]Elapsed Time:[/white] [dim]{elapsed_time}[/dim]")
        console.print("\n")
