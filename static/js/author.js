/* Aksi khusus halaman profil peneliti. */
const copyPipelineButton = document.getElementById('copy-pipeline');
const pipelineCode = document.getElementById('pipeline-code');

if (copyPipelineButton && pipelineCode) {
    const sourceUrl = pipelineCode.dataset.source;
    const defaultButtonLabel = 'Salin kode';
    let feedbackTimeout;

    fetch(sourceUrl)
        .then(response => {
            if (!response.ok) throw new Error('Kode aplikasi gagal dimuat.');
            return response.text();
        })
        .then(source => {
            pipelineCode.textContent = source;
            copyPipelineButton.disabled = false;
            copyPipelineButton.textContent = defaultButtonLabel;
        })
        .catch(() => {
            pipelineCode.textContent = 'Kode aplikasi tidak dapat dimuat. Silakan muat ulang halaman.';
            copyPipelineButton.textContent = 'Kode tidak tersedia';
        });

    copyPipelineButton.addEventListener('click', async () => {
        try {
            await navigator.clipboard.writeText(pipelineCode.textContent.trim());
            copyPipelineButton.textContent = 'Pipeline tersalin';
        } catch (error) {
            copyPipelineButton.textContent = 'Tidak dapat menyalin';
        }

        window.clearTimeout(feedbackTimeout);
        feedbackTimeout = window.setTimeout(() => {
            copyPipelineButton.textContent = defaultButtonLabel;
        }, 1800);
    });
}
