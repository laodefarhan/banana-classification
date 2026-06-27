/* ============================================================
   BananaAI — main.js
   ============================================================ */

const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const previewWrap = document.getElementById('preview-wrap');
const previewImg = document.getElementById('preview-img');
const fileNameText = document.getElementById('file-name-text');
const submitBtn = document.getElementById('submit-btn');
const uploadForm = document.getElementById('upload-form');

/* ── Click to open file picker ── */
uploadArea.addEventListener('click', () => fileInput.click());

/* ── Drag & Drop ── */
uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('dragover'));
uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const f = e.dataTransfer.files[0];
    if (f && f.type.startsWith('image/')) {
        setFile(f);
        /* Transfer file ke native input agar form dapat di-submit */
        const dt = new DataTransfer();
        dt.items.add(f);
        fileInput.files = dt.files;
    }
});

/* ── File input change ── */
fileInput.addEventListener('change', e => {
    if (e.target.files.length > 0) setFile(e.target.files[0]);
});

/* ── Handle file selection ── */
function setFile(file) {
    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        previewWrap.classList.add('active');
        uploadArea.classList.add('has-file');
        fileNameText.textContent = file.name;
        submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

/* ── Loading state on submit ── */
uploadForm.addEventListener('submit', () => {
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
});