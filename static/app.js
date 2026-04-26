const markdownInput = document.getElementById('markdown-input');
const htmlPreview = document.getElementById('html-preview');
const themeSelector = document.getElementById('theme-selector');
const downloadPdfBtn = document.getElementById('download-pdf');
const clearBtn = document.getElementById('clear-storage');
const editorPane = document.querySelector('.editor-pane');
const previewPane = document.querySelector('.preview-pane');

const defaultText = '# Willkommen\n\nSchreibe dein Markdown hier.\n\n- Punkt 1\n- Punkt 2\n\n```python\nprint("Hallo Welt")\n```';
markdownInput.value = localStorage.getItem('md-content') || defaultText;
updatePreview();

markdownInput.addEventListener('input', () => {
    updatePreview();
    localStorage.setItem('md-content', markdownInput.value);
});

themeSelector.addEventListener('change', (e) => {
    htmlPreview.className = `theme-${e.target.value}`;
});

clearBtn.addEventListener('click', () => {
    if(confirm('Möchtest du den gesamten Text wirklich löschen?')) {
        markdownInput.value = '';
        updatePreview();
        localStorage.removeItem('md-content');
    }
});

let syncing = false;

markdownInput.addEventListener('scroll', () => {
    if (syncing) return;
    syncing = true;
    const percentage = markdownInput.scrollTop / (markdownInput.scrollHeight - markdownInput.clientHeight);
    previewPane.scrollTop = percentage * (previewPane.scrollHeight - previewPane.clientHeight);
    requestAnimationFrame(() => { syncing = false; });
});

previewPane.addEventListener('scroll', () => {
    if (syncing) return;
    syncing = true;
    const percentage = previewPane.scrollTop / (previewPane.scrollHeight - previewPane.clientHeight);
    markdownInput.scrollTop = percentage * (markdownInput.scrollHeight - markdownInput.clientHeight);
    requestAnimationFrame(() => { syncing = false; });
});

function updatePreview() {
    htmlPreview.innerHTML = marked.parse(markdownInput.value);
}

const pdfPulse = document.getElementById('pdf-pulse');

downloadPdfBtn.addEventListener('click', async () => {
    const originalText = downloadPdfBtn.lastChild.textContent;
    downloadPdfBtn.lastChild.textContent = 'Generiere PDF...';
    downloadPdfBtn.disabled = true;
    pdfPulse.classList.add('active');

    // Formulardaten für den POST-Request erstellen
    const formData = new FormData();
    formData.append('markdown', markdownInput.value);

    try {
        const response = await fetch('/generate-pdf', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            // Blob (Datei) empfangen und Download triggern
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            const h1Match = markdownInput.value.match(/^#\s+(.+)$/m);
            const filename = h1Match
                ? h1Match[1].trim().replace(/[^a-zA-Z0-9äöüÄÖÜß\s-]/g, '').replace(/\s+/g, '_') + '.pdf'
                : 'markdown-export.pdf';
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
        } else {
            alert('Fehler bei der PDF-Generierung durch den Server.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Netzwerkfehler beim Kontaktieren des Flask-Servers.');
    } finally {
        downloadPdfBtn.lastChild.textContent = originalText;
        downloadPdfBtn.disabled = false;
        pdfPulse.classList.remove('active');
    }
});
