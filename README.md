# Resume Portfolio Builder Created by AI

Aplikasi web Flask untuk membuat portfolio profesional dengan mudah. Isi form, preview, dan export sebagai ZIP file yang siap deploy.

## Fitur

- **Form Lengkap**: Biodata, pendidikan, pengalaman kerja, skill, dan sosial media
- **Upload Foto**: Foto profil dengan validasi (PNG, JPG, JPEG, GIF - Max 16MB)
- **Preview Real-time**: Lihat portfolio sebelum export
- **Export ZIP**: Download portfolio sebagai file HTML/CSS siap deploy
- **Responsive Design**: Tampilan optimal di desktop dan mobile
- **Cross-platform**: Berjalan di Replit, Termux, NetHunter, dan sistem lain

## Instalasi

### Replit
Project ini sudah dikonfigurasi untuk Replit. Klik "Run" untuk memulai.

### Termux/NetHunter/Linux
```bash
# Install Python 3.11+ dan pip
pkg install python python-pip  # di Termux
# atau
apt install python3 python3-pip  # di NetHunter/Linux

# Install dependencies
pip install flask gunicorn werkzeug email-validator flask-sqlalchemy psycopg2-binary

# Jalankan aplikasi
python main.py
```

### Windows/macOS
```bash
# Install Python 3.11+ dari python.org
# Install dependencies
pip install flask gunicorn werkzeug email-validator flask-sqlalchemy psycopg2-binary

# Jalankan aplikasi
python main.py
```

## Penggunaan

1. **Jalankan aplikasi**: `python main.py`
2. **Buka browser**: `http://localhost:5000` (atau `http://0.0.0.0:5000` di Termux)
3. **Isi form** dengan data diri Anda
4. **Klik "Preview Portfolio"** untuk melihat hasil
5. **Klik "Export ZIP"** untuk download portfolio

## Struktur Project

```
resume-portfolio-builder/
├── app.py              # Aplikasi Flask utama
├── main.py             # Entry point
├── templates/          # Template HTML
│   ├── layout.html     # Layout dasar
│   ├── index.html      # Form input
│   └── preview.html    # Preview portfolio
├── static/             # File statis
│   ├── style.css       # CSS custom
│   ├── app.js          # JavaScript
│   └── uploads/        # Foto yang diupload
├── exports/            # File ZIP sementara
├── pyproject.toml      # Dependencies
└── README.md           # Dokumentasi
```

## File ZIP Export

File ZIP yang dihasilkan berisi:
- `index.html` - Portfolio lengkap
- `style.css` - Styling responsif
- `profile_photo.jpg` - Foto profil (jika ada)

File ini siap deploy ke:
- Netlify
- Vercel
- GitHub Pages
- Web hosting manapun

## Konfigurasi Port

Default port: 5000

Untuk mengubah port:
```python
# Di main.py, ubah baris terakhir:
app.run(host='0.0.0.0', port=8080, debug=True)  # port 8080
```

## Troubleshooting

### Termux
- Jika error "Permission denied": `termux-setup-storage`
- Jika port 5000 diblokir: ubah ke port lain (8080, 8000, dll)

### NetHunter
- Pastikan Python 3.11+ terinstall
- Install dependencies dengan `pip3` jika `pip` tidak ditemukan

### Error Upload
- Pastikan folder `static/uploads/` ada dan writable
- Cek ukuran file (max 16MB)
- Format file harus PNG, JPG, JPEG, atau GIF

## Lisensi

Open source - bebas digunakan dan dimodifikasi.