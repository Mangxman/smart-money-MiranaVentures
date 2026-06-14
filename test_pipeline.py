# test_pipeline.py
from database import init_db, exists
from main import process_trade
import uuid

def run_test():
    print("=== MEMULAI TEST PIPELINE ===")
    
    # 1. Inisialisasi Database
    init_db()
    print("[1] Database berhasil diinisialisasi atau sudah ada.")

    # 2. Buat Data Simulasi Transaksi (Mantle Network)
    # Menggunakan UUID random pada transaction_hash agar tidak terblokir oleh filter duplikat di DB
    random_tx = f"0x{uuid.uuid4().hex}"
    
    mock_trade = {
        "transaction_hash": random_tx,
        "trader_address": "0x3cDb32...67B9",
        "trader_address_label": "Smart Trader (Whale)",
        "token_bought_symbol": "WMNT",
        "token_sold_symbol": "USDT",
        "trade_value_usd": "75000"  # Simulasi trade senilai $75,000
    }
    print(f"[2] Data simulasi berhasil dibuat. TX: {random_tx}")

    # 3. Jalankan Proses Trade (Hit Surf AI & Kirim ke Telegram)
    print("[3] Mengirim data ke Surf AI untuk analisis dan meneruskan ke Telegram...")
    try:
        process_trade(mock_trade)
        print("[4] Proses selesai! Periksa grup/channel Telegram kamu.")
        
        # 5. Cek apakah TX tersimpan di DB
        if exists(random_tx):
            print("[5] Sukses: Transaction hash berhasil disimpan ke database (anti-duplikasi bekerja).")
        else:
            print("[5] Gagal: Transaction hash tidak tertulis di database.")
            
    except Exception as e:
        print(f"❌ TEST GAGAL: Terjadi error saat eksekusi: {e}")

if __name__ == "__main__":
    run_test()