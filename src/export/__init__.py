"""Export functionality for generating reports"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from jinja2 import Template
import logging


class ReportExporter:
    """Export analysis results to various formats"""
    
    def __init__(self, export_path: str):
        self.export_path = Path(export_path)
        self.export_path.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger("export")
    
    def _get_filename(self, format_type: str) -> str:
        """Generate filename with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"compliance_report_{timestamp}.{format_type}"
    
    def export_json(self, results: Dict, scan_info: Dict) -> Optional[str]:
        """Export results to JSON"""
        try:
            data = {
                "scan_info": scan_info,
                "results": results,
                "generated_at": datetime.now().isoformat(),
            }
            
            file_path = self.export_path / self._get_filename("json")
            
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.logger.info(f"JSON report exported to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error exporting JSON: {e}")
            return None
    
    def export_csv(self, results: Dict, scan_info: Dict) -> Optional[str]:
        """Export findings to CSV"""
        try:
            file_path = self.export_path / self._get_filename("csv")
            
            findings = results.get('findings', [])
            
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                if not findings:
                    writer = csv.writer(f)
                    writer.writerow(["No findings to export"])
                    return str(file_path)
                
                fieldnames = [
                    'Message ID',
                    'Category',
                    'Risk Score',
                    'Confidence Score',
                    'Explanation',
                    'Evidence'
                ]
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for finding in findings:
                    writer.writerow({
                        'Message ID': finding.get('message_id', ''),
                        'Category': finding.get('category', ''),
                        'Risk Score': finding.get('risk_score', 0),
                        'Confidence Score': finding.get('confidence_score', 0),
                        'Explanation': finding.get('explanation', ''),
                        'Evidence': ', '.join(finding.get('evidence', []))
                    })
            
            self.logger.info(f"CSV report exported to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error exporting CSV: {e}")
            return None
    
    def export_html(self, results: Dict, scan_info: Dict) -> Optional[str]:
        """Export results to HTML"""
        try:
            html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Telegram Compliance Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .section {
            background: white;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #667eea;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .high-risk { color: #d32f2f; font-weight: bold; }
        .medium-risk { color: #f57c00; font-weight: bold; }
        .low-risk { color: #388e3c; font-weight: bold; }
        .summary {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 20px;
        }
        .summary-card {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        .footer {
            text-align: center;
            color: #666;
            margin-top: 20px;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Telegram Content Compliance Report</h1>
        <p>Generated: {{ generated_at }}</p>
    </div>
    
    <div class="section">
        <h2>Scan Information</h2>
        <table>
            <tr>
                <td><strong>Account:</strong></td>
                <td>{{ scan_info.account_name }}</td>
            </tr>
            <tr>
                <td><strong>Channels Scanned:</strong></td>
                <td>{{ scan_info.channels_count }}</td>
            </tr>
            <tr>
                <td><strong>Messages Analyzed:</strong></td>
                <td>{{ scan_info.total_messages }}</td>
            </tr>
        </table>
    </div>
    
    <div class="section">
        <h2>Findings Summary</h2>
        <div class="summary">
            <div class="summary-card">
                <h3>Total Findings</h3>
                <p style="font-size: 24px; font-weight: bold;">{{ results.total_findings }}</p>
            </div>
            <div class="summary-card">
                <h3 class="high-risk">High Risk</h3>
                <p style="font-size: 24px; font-weight: bold; color: #d32f2f;">{{ results.high_risk }}</p>
            </div>
            <div class="summary-card">
                <h3 class="medium-risk">Medium Risk</h3>
                <p style="font-size: 24px; font-weight: bold; color: #f57c00;">{{ results.medium_risk }}</p>
            </div>
        </div>
    </div>
    
    <div class="section">
        <h2>Findings by Category</h2>
        <table>
            <thead>
                <tr>
                    <th>Category</th>
                    <th>Count</th>
                </tr>
            </thead>
            <tbody>
                {% for category, count in results.categories.items() %}
                {% if count > 0 %}
                <tr>
                    <td>{{ category }}</td>
                    <td>{{ count }}</td>
                </tr>
                {% endif %}
                {% endfor %}
            </tbody>
        </table>
    </div>
    
    <div class="section">
        <h2>Detailed Findings</h2>
        <table>
            <thead>
                <tr>
                    <th>Message ID</th>
                    <th>Category</th>
                    <th>Risk Level</th>
                    <th>Explanation</th>
                </tr>
            </thead>
            <tbody>
                {% for finding in results.findings[:50] %}
                <tr>
                    <td>#{{ finding.message_id }}</td>
                    <td>{{ finding.category }}</td>
                    <td>
                        {% if finding.risk_score >= 0.7 %}
                        <span class="high-risk">HIGH ({{ "%.2f" % finding.risk_score }})</span>
                        {% elif finding.risk_score >= 0.4 %}
                        <span class="medium-risk">MEDIUM ({{ "%.2f" % finding.risk_score }})</span>
                        {% else %}
                        <span class="low-risk">LOW ({{ "%.2f" % finding.risk_score }})</span>
                        {% endif %}
                    </td>
                    <td>{{ finding.explanation }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% if results.findings|length > 50 %}
        <p style="text-align: center; color: #666; margin-top: 10px;">
            ... and {{ results.findings|length - 50 }} more findings
        </p>
        {% endif %}
    </div>
    
    <div class="footer">
        <p>This report contains sensitive information. Handle with care.</p>
        <p>Generated by Telegram Content Compliance Analyzer v1.0</p>
    </div>
</body>
</html>"""
            
            template = Template(html_template)
            html_content = template.render(
                results=results,
                scan_info=scan_info,
                generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            file_path = self.export_path / self._get_filename("html")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML report exported to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error exporting HTML: {e}")
            return None
    
    def export_pdf(self, results: Dict, scan_info: Dict) -> Optional[str]:
        """Export results to PDF (via ReportLab)"""
        try:
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib import colors
            
            file_path = self.export_path / self._get_filename("pdf")
            
            doc = SimpleDocTemplate(str(file_path), pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#667eea'),
                spaceAfter=30,
            )
            story.append(Paragraph("Telegram Compliance Report", title_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Scan Info
            story.append(Paragraph("Scan Information", styles['Heading2']))
            scan_data = [
                ["Account", scan_info.get('account_name', 'N/A')],
                ["Channels Scanned", str(scan_info.get('channels_count', 0))],
                ["Messages Analyzed", str(scan_info.get('total_messages', 0))],
            ]
            scan_table = Table(scan_data, colWidths=[2*inch, 4*inch])
            scan_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(scan_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Summary
            story.append(Paragraph("Findings Summary", styles['Heading2']))
            summary_data = [
                ["Metric", "Value"],
                ["Total Findings", str(results.get('total_findings', 0))],
                ["High Risk", str(results.get('high_risk', 0))],
                ["Medium Risk", str(results.get('medium_risk', 0))],
                ["Low Risk", str(results.get('low_risk', 0))],
            ]
            summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.beige, colors.white])
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 0.2*inch))
            
            story.append(Paragraph(
                "For detailed findings, see the HTML or JSON report.",
                styles['Normal']
            ))
            
            doc.build(story)
            
            self.logger.info(f"PDF report exported to {file_path}")
            return str(file_path)
        
        except Exception as e:
            self.logger.error(f"Error exporting PDF: {e}")
            return None
    
    def export_all(self, results: Dict, scan_info: Dict) -> Dict[str, Optional[str]]:
        """Export to all formats"""
        return {
            'json': self.export_json(results, scan_info),
            'csv': self.export_csv(results, scan_info),
            'html': self.export_html(results, scan_info),
            'pdf': self.export_pdf(results, scan_info),
        }
