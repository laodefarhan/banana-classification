import os
import cv2
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from ultralytics import YOLO

# ===============================
# KONFIGURASI APLIKASI
# ===============================
UPLOAD_FOLDER = "upload"

# Path model klasifikasi kematangan (hasil training Anda)
MODEL_PATH = "model/klasifikasi_pisang.pt"

# Model deteksi objek pre-trained (COCO) — untuk memverifikasi apakah gambar berisi pisang
DETECTOR_MODEL_PATH = "model/yolov8n_deteksi_pisang_non_pisang.pt"

# Kelas "banana" di dataset COCO memiliki index 46
COCO_BANANA_CLASS_ID = 46

# Confidence minimum untuk deteksi pisang oleh model COCO
DETECTION_CONFIDENCE = 0.30

# Label kelas sesuai folder dataset training (matang, mentah, setengah_matang)
# YOLO otomatis membaca nama kelas dari subfolder dataset, jadi mapping ini opsional
# tapi berguna untuk tampilan yang lebih rapi di UI.
CLASS_LABEL_MAP = {
    "matang": "Matang 🍌",
    "mentah": "Mentah 🌿",
    "setengah_matang": "Setengah Matang 🍃",
}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ===============================
# LOAD MODEL YOLO (HASIL TRAINING)
# ===============================
try:
    model = YOLO(MODEL_PATH)
    print(f"✅ Model klasifikasi berhasil dimuat dari: {MODEL_PATH}")
    print(f"   Kelas yang dikenali: {list(model.names.values())}")
except Exception as e:
    print(f"⚠️  Peringatan: Model '{MODEL_PATH}' gagal dimuat.")
    print(f"   Pastikan Anda telah men-download 'best_model_pisang.pt' dari Kaggle")
    print(f"   dan meletakkannya di folder model/")
    print(f"   Error: {e}")
    model = None

# ===============================
# LOAD MODEL DETEKSI PISANG (PRE-TRAINED COCO)
# ===============================
try:
    detector = YOLO(DETECTOR_MODEL_PATH)
    print(f"✅ Model deteksi (COCO) berhasil dimuat: {DETECTOR_MODEL_PATH}")
except Exception as e:
    print(f"⚠️  Peringatan: Model deteksi '{DETECTOR_MODEL_PATH}' gagal dimuat.")
    print(f"   Error: {e}")
    detector = None

# ===============================
# ROUTE UNTUK SERVE GAMBAR UPLOAD
# ===============================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ===============================
# ROUTE HALAMAN UTAMA
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None
    image_path = None
    all_probs = None  # Semua probabilitas kelas untuk ditampilkan

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename:
            filename = file.filename
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            if model:
                # ===============================
                # TAHAP 1: DETEKSI APAKAH ADA PISANG
                # ===============================
                is_banana = False
                boxes_to_draw = []

                if detector:
                    det_results = detector.predict(source=save_path, verbose=False, conf=DETECTION_CONFIDENCE)
                    for box in det_results[0].boxes:
                        cls_id = int(box.cls[0].item())
                        # Periksa apakah ini pisang (index 46 untuk COCO, atau sesuaikan jika model custom)
                        # Kita gunakan pengecekan nama kelas agar lebih fleksibel seperti sebelumnya
                        class_name = detector.names[cls_id].lower()
                        if "banana" in class_name or "pisang" in class_name:
                            is_banana = True
                            boxes_to_draw.append(box.xyxy[0].tolist()) # Simpan koordinat [x1, y1, x2, y2]
                else:
                    is_banana = True

                if not is_banana:
                    # Gambar tidak mengandung pisang
                    prediction = "Bukan Pisang ❌"
                    confidence = 0.0
                    all_probs = [{
                        "label": "Objek pisang tidak terdeteksi dalam gambar",
                        "raw_label": "error",
                        "prob": 0.0
                    }]
                else:
                    # GABUNGAN: Gambar garis hijau hanya di BAGIAN TENGAH pisang
                    if boxes_to_draw:
                        img = cv2.imread(save_path)
                        for box in boxes_to_draw:
                            x1, y1, x2, y2 = map(int, box)
                            
                            # Hitung titik tengah dan ukuran box asli
                            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                            bw, bh = (x2 - x1), (y2 - y1)
                            
                            # Tentukan ukuran kotak tengah (Misal: ambil 40% dari lebar dan tinggi asli)
                            # Ini akan membuat kotak fokus di bagian tengah kulit pisang
                            nw, nh = int(bw * 0.4), int(bh * 0.4)
                            nx1, ny1 = cx - nw // 2, cy - nh // 2
                            nx2, ny2 = cx + nw // 2, cy + nh // 2
                            
                            # Gambar kotak hijau fokus di tengah
                            cv2.rectangle(img, (nx1, ny1), (nx2, ny2), (0, 255, 0), 3)
                            
                            # Tambahkan label 'Area Fokus' di atas kotak tengah
                            cv2.putText(img, "Fokus", (nx1, ny1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Simpan kembali gambar yang sudah ditandai
                        cv2.imwrite(save_path, img)

                    # ===============================
                    # TAHAP 2: KLASIFIKASI KEMATANGAN PISANG
                    # ===============================
                    results = model.predict(source=save_path, verbose=False, imgsz=224)
                    conf_val = 0.0

                    if results[0].probs is not None:
                        # Ambil kelas dengan probabilitas tertinggi
                        class_index = results[0].probs.top1
                        raw_label = results[0].names[class_index]
                        conf_val = float(results[0].probs.top1conf.item())
                        confidence = round(conf_val * 100, 2)

                        # Tampilkan label yang lebih rapi (gunakan mapping jika ada)
                        prediction = CLASS_LABEL_MAP.get(raw_label, raw_label)

                        # Kumpulkan semua probabilitas untuk ditampilkan sebagai bar chart
                        probs_tensor = results[0].probs.data.tolist()
                        all_probs = []
                        for idx, prob in enumerate(probs_tensor):
                            class_raw = results[0].names[idx]
                            all_probs.append({
                                "label": CLASS_LABEL_MAP.get(class_raw, class_raw),
                                "raw_label": class_raw,
                                "prob": round(float(prob) * 100, 2),
                            })
                        # Urutkan berdasarkan probabilitas tertinggi
                        all_probs.sort(key=lambda x: x["prob"], reverse=True)
                    else:
                        prediction = "❌ Error: Model yang dimuat bukan model klasifikasi. Pastikan menggunakan best_model_pisang.pt"
                        confidence = 0.0
            else:
                prediction = "⚠️ Model belum tersedia. Letakkan best_model_pisang.pt di folder model/"
                confidence = 0.0

            image_path = save_path

    return render_template(
        "index.html",
        prediction=prediction,
        confidence=confidence,
        image_path=image_path,
        all_probs=all_probs,
    )

# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs("model", exist_ok=True)
    app.run(debug=True)
