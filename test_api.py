# test_api.py
from nansen import get_smart_money
from surf import SurfAI
from config import SURF_API_KEY

print("====================================")
print("🚀 MEMULAI PENGUJIAN SISTEM INTELLIGENT BOT")
print("====================================")

# 1. Tes API Nansen Baru
print("\n1. Menguji API Key Nansen Baru...")
nansen_result = get_smart_money()
if nansen_result is not None:
    print("✅ SUKSES: API Nansen merespons dengan baik!")
    print("Data yang didapat:", nansen_result)
else:
    print("⚠️ INFO: API Nansen terkena limit/free tier restriction. Sistem otomatis bersiap menggunakan Real-Data Streamer.")

# 2. Tes API Surf AI
print("\n2. Menguji Koneksi Otak Surf AI...")
try:
    surf = SurfAI(SURF_API_KEY)
    test_prompt = "Say hello in one short sentence to Mantle Network developers."
    ai_response = surf.ask(test_prompt)
    print("✅ SUKSES: Surf AI merespons!")
    print("Jawaban AI:", ai_response)
except Exception as e:
    print(f"❌ GAGAL: Ada masalah pada Surf AI API Key kamu: {e}")

print("\n====================================")
print("🏁 PENGUJIAN SELESAI")
print("====================================")