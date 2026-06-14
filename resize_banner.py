# resize_banner.py
from PIL import Image

try:
    # Membuka gambar asli mirana1.jpg yang ada di foldermu
    image = Image.open("mirana1.jpg")
    
    # Mengubah ukurannya secara paksa menjadi standar ketat BotFather: 640x360
    resized_image = image.resize((640, 360), Image.Resampling.LANCZOS)
    
    # Menyimpan hasil modifikasi dengan nama baru
    resized_image.save("mirana1_fixed.jpg", "JPEG", quality=95)
    print("✅ Berhasil! Gambar baru 'mirana1_fixed.jpg' dengan ukuran tepat 640x360 telah dibuat.")
    
except Exception as e:
    print(f"❌ Gagal memproses gambar. Pastikan file 'mirana1.jpg' ada di folder yang sama. Detail: {e}")