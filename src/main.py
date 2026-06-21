"""Main Application Entry Point"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta
import logging

from src.config import Settings
from src.utils.logger import LoggerSetup
from src.telegram_client import TelegramClient, SessionManager
from src.analyzer import MessageAnalyzer, AnalysisResult
from src.export import ReportExporter
from src.ui import (
    MainMenu, LoginUI, DialogsUI, ScannerUI, ResultsUI,
    print_header, print_status, console
)


class TelegramComplianceApp:
    """Main application class"""
    
    def __init__(self):
        self.settings = Settings()
        LoggerSetup(self.settings)
        
        self.login_logger = logging.getLogger("login")
        self.scan_logger = logging.getLogger("scan")
        self.main_logger = logging.getLogger("main")
        
        self.current_client: TelegramClient = None
        self.current_user: dict = None
        self.session_manager = SessionManager(
            self.settings.session_path,
            self.settings.session_encryption_key
        )
        
        self.analyzer = MessageAnalyzer(
            self.settings.openai_api_key,
            self.settings.openai_model,
            self.settings.analysis_timeout
        )
        
        self.exporter = ReportExporter(self.settings.export_path)
    
    async def run(self) -> None:
        """Main application loop"""
        self.main_logger.info("Application started")
        
        try:
            while True:
                menu = MainMenu()
                choice = menu.show()
                
                if choice == 'login':
                    await self._handle_login()
                elif choice == 'load_session':
                    await self._handle_load_session()
                elif choice == 'manage_accounts':
                    await self._handle_manage_accounts()
                elif choice == 'exit':
                    print_status("Goodbye!", True)
                    break
                else:
                    print_status("Invalid choice", False)
                
                input("\nPress Enter to continue...")
        
        except KeyboardInterrupt:
            print_status("\nApplication interrupted", False)
        except Exception as e:
            self.main_logger.error(f"Fatal error: {e}")
            print_status(f"Error: {e}", False)
        finally:
            if self.current_client:
                await self.current_client.disconnect()
    
    async def _handle_login(self) -> None:
        """Handle new Telegram account login"""
        try:
            console.clear()
            login_ui = LoginUI()
            
            # Get credentials
            api_id, api_hash, _ = login_ui.get_credentials()
            if not api_id or not api_hash:
                return
            
            # Get phone number
            phone_number = login_ui.get_phone_number()
            if not phone_number:
                return
            
            # Get session name
            session_name = login_ui.get_session_name()
            if not session_name:
                return
            
            # Connect and authenticate
            self.current_client = TelegramClient(
                api_id, api_hash,
                self.settings.session_path,
                session_name
            )
            
            # Step 1: Connect
            login_ui.show_login_progress("Connecting to Telegram...", True)
            if not await self.current_client.connect():
                login_ui.show_login_error("Failed to connect to Telegram")
                return
            
            # Step 2: Send code
            login_ui.show_login_progress("Sending authentication code...", True)
            if not await self.current_client.send_code_request(phone_number):
                login_ui.show_login_error("Failed to send code")
                await self.current_client.disconnect()
                return
            
            # Step 3: Get and validate OTP
            otp_code = login_ui.get_otp_code()
            if not otp_code:
                await self.current_client.disconnect()
                return
            
            # Step 4: Sign in
            login_ui.show_login_progress("Verifying code...", True)
            if not await self.current_client.sign_in(phone_number, otp_code):
                # Try 2FA
                password = login_ui.get_password()
                if password:
                    if not await self.current_client.sign_in(phone_number, otp_code, password):
                        login_ui.show_login_error("Authentication failed")
                        await self.current_client.disconnect()
                        return
                else:
                    login_ui.show_login_error("Authentication failed")
                    await self.current_client.disconnect()
                    return
            
            # Get user info
            self.current_user = await self.current_client.get_me()
            if self.current_user:
                login_ui.show_login_progress("User authenticated", True)
                login_ui.show_login_success(self.current_user)
                
                # Save session
                self.session_manager.save_session(
                    session_name,
                    phone_number,
                    api_id,
                    api_hash
                )
                
                # Start analysis workflow
                await self._handle_analysis()
            else:
                login_ui.show_login_error("Failed to get user info")
                await self.current_client.disconnect()
        
        except Exception as e:
            self.login_logger.error(f"Login error: {e}")
            print_status(f"Login failed: {e}", False)
    
    async def _handle_load_session(self) -> None:
        """Handle loading existing session"""
        try:
            sessions = self.session_manager.get_sessions()
            
            if not sessions:
                console.print("[yellow]No saved sessions found[/yellow]")
                return
            
            console.print("\n[cyan]Saved Sessions:[/cyan]\n")
            for i, session in enumerate(sessions, 1):
                console.print(f"  [{i}] {session['name']} - {session['phone_number']}")
            
            choice_str = console.input("\n[yellow]Select session[/yellow]: ").strip()
            
            try:
                choice = int(choice_str) - 1
                if 0 <= choice < len(sessions):
                    session = sessions[choice]
                    
                    # Connect with saved session
                    self.current_client = TelegramClient(
                        session['api_id'],
                        session['api_hash'],
                        self.settings.session_path,
                        session['name']
                    )
                    
                    print_status("Connecting...", True)
                    if await self.current_client.connect():
                        if await self.current_client.is_user_authorized():
                            self.current_user = await self.current_client.get_me()
                            print_status("Session loaded successfully", True)
                            self.session_manager.update_last_used(session['name'])
                            await self._handle_analysis()
                        else:
                            print_status("Session not authorized", False)
                            await self.current_client.disconnect()
                    else:
                        print_status("Failed to connect", False)
            except (ValueError, IndexError):
                print_status("Invalid selection", False)
        
        except Exception as e:
            self.main_logger.error(f"Load session error: {e}")
            print_status(f"Error: {e}", False)
    
    async def _handle_manage_accounts(self) -> None:
        """Handle account management"""
        sessions = self.session_manager.get_sessions()
        
        if not sessions:
            console.print("[yellow]No saved sessions[/yellow]")
            return
        
        console.print("\n[cyan]Saved Accounts:[/cyan]\n")
        for i, session in enumerate(sessions, 1):
            console.print(f"  [{i}] {session['name']} ({session['phone_number']})")
        
        choice = console.input("\n[yellow]Select account to delete[/yellow]: ").strip()
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sessions):
                session = sessions[idx]
                confirm = console.input(f"Delete '{session['name']}'? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    self.session_manager.delete_session(session['name'])
                    print_status("Session deleted", True)
        except ValueError:
            pass
    
    async def _handle_analysis(self) -> None:
        """Handle message analysis workflow"""
        if not self.current_client or not self.current_user:
            return
        
        try:
            # Get dialogs
            print_status("Fetching channels and groups...", True)
            dialogs = await self.current_client.get_dialogs(limit=200)
            
            if not dialogs:
                print_status("No dialogs available", False)
                return
            
            # Select dialogs
            dialogs_ui = DialogsUI()
            dialogs_ui.show_dialogs(dialogs)
            selected_ids = dialogs_ui.get_dialog_selection(dialogs)
            
            if not selected_ids:
                print_status("No dialogs selected", False)
                return
            
            # Get message range
            message_range = dialogs_ui.show_message_range_menu()
            if message_range is None:
                start_id, end_id = dialogs_ui.get_custom_message_range()
                message_limit = self.settings.max_messages_per_scan
            else:
                message_limit = message_range
            
            # Collect messages
            print_status(f"Collecting messages from {len(selected_ids)} dialog(s)...", True)
            all_messages = []
            
            for entity_id in selected_ids:
                messages = await self.current_client.get_messages(
                    entity_id,
                    limit=message_limit
                )
                all_messages.extend(messages)
            
            print_status(f"Collected {len(all_messages)} messages", True)
            
            if not all_messages:
                print_status("No messages to analyze", False)
                return
            
            # Analyze messages
            console.print("\n[cyan]Analyzing messages with OpenAI...[/cyan]")
            analysis_results = AnalysisResult()
            
            findings = await self.analyzer.analyze_batch(all_messages, self.settings.batch_size)
            
            for finding in findings:
                if finding:
                    analysis_results.add_finding(finding)
            
            # Display results
            summary = analysis_results.get_summary()
            results_ui = ResultsUI()
            
            console.print("\n")
            results_ui.show_findings_summary(
                len(all_messages),
                summary['total_findings'],
                summary['high_risk'],
                summary['medium_risk'],
                summary['low_risk']
            )
            
            if summary['categories']:
                console.print()
                results_ui.show_category_summary(summary['categories'])
            
            # Export results
            export_choice = results_ui.show_export_menu()
            
            scan_info = {
                'account_name': self.current_user.get('username', 'Unknown'),
                'channels_count': len(selected_ids),
                'total_messages': len(all_messages),
            }
            
            if export_choice != 'cancel':
                if export_choice == 'pdf':
                    path = self.exporter.export_pdf(summary, scan_info)
                    if path:
                        results_ui.show_export_result('PDF', path)
                elif export_choice == 'html':
                    path = self.exporter.export_html(summary, scan_info)
                    if path:
                        results_ui.show_export_result('HTML', path)
                elif export_choice == 'json':
                    path = self.exporter.export_json(summary, scan_info)
                    if path:
                        results_ui.show_export_result('JSON', path)
                elif export_choice == 'csv':
                    path = self.exporter.export_csv(summary, scan_info)
                    if path:
                        results_ui.show_export_result('CSV', path)
                elif export_choice == 'all':
                    paths = self.exporter.export_all(summary, scan_info)
                    for fmt, path in paths.items():
                        if path:
                            results_ui.show_export_result(fmt.upper(), path)
            
            # Disconnect
            await self.current_client.disconnect()
            self.current_client = None
        
        except Exception as e:
            self.scan_logger.error(f"Analysis error: {e}")
            print_status(f"Analysis failed: {e}", False)
            if self.current_client:
                await self.current_client.disconnect()


async def main():
    """Entry point"""
    app = TelegramComplianceApp()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Application interrupted[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        sys.exit(1)
