from flask import Flask, render_template, request, send_file
import markdown
from weasyprint import HTML
import io
import logging
import sys

app = Flask(__name__)

# --- Logging Konfiguration ---
# Wir loggen direkt in die Standardausgabe (stdout), 
# damit Docker die Logs sauber erfassen kann.
logging.basicConfig(
    level=logging.INFO,  # Auf DEBUG setzen für noch detailliertere Ausgaben
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info("Web-Interface wurde aufgerufen.")
    return render_template('index.html')

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    logger.info("Starte PDF-Generierung...")
    
    try:
        # Markdown Text vom Frontend empfangen
        md_text = request.form.get('markdown', '')
        
        if not md_text.strip():
            logger.warning("Es wurde ein leerer Text zur Generierung übergeben.")
        else:
            logger.info(f"Empfangener Text: {len(md_text)} Zeichen.")
        
        # Markdown in HTML konvertieren (mit Tabellen und Code-Blöcken)
        html_content = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])
        logger.debug("Markdown erfolgreich in HTML geparst.")
        
        # In ein sauberes HTML-Gerüst packen
        full_html = f"""
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                    line-height: 1.6; 
                    color: #333; 
                }}
                h1, h2, h3 {{ color: #111; page-break-after: avoid; }}
                pre {{ 
                    background: #f4f4f4; 
                    padding: 15px; 
                    border-radius: 5px; 
                    white-space: pre-wrap;
                }}
                code {{ font-family: "Consolas", monospace; font-size: 0.9em; }}
                blockquote {{ border-left: 4px solid #ccc; margin-left: 0; padding-left: 15px; color: #666; }}
                table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; break-inside: avoid; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # PDF mit WeasyPrint generieren
        logger.debug("Übergebe HTML an WeasyPrint...")
        pdf_bytes = HTML(string=full_html).write_pdf()
        
        logger.info(f"PDF erfolgreich generiert. Größe: {len(pdf_bytes)} Bytes.")
        
        # PDF als Download an den Browser zurücksenden
        return send_file(
            io.BytesIO(pdf_bytes),
            download_name='markdown-export.pdf',
            as_attachment=True,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        # Fängt alle Fehler (z.B. WeasyPrint C-Lib Abstürze, Parser-Fehler)
        # exc_info=True schreibt den kompletten Traceback ins Log
        logger.error(f"Kritischer Fehler bei der PDF-Generierung: {e}", exc_info=True)
        return "Interner Serverfehler bei der PDF-Erstellung", 500

if __name__ == '__main__':
    # Wird von Gunicorn ignoriert, ist nur für lokale Dev-Tests relevant
    app.run(host='0.0.0.0', port=5000, debug=True)