import requests
import time

# Node RPC Publik Resmi Jaringan Mantle Mainnet (100% Gratis & Tanpa API Key)
MANTLE_RPC_URL = "https://rpc.mantle.xyz"

# Batas minimum deteksi paus on-chain (Misal: deteksi jika ada transfer >= 10,000 MNT)
MANTLE_WHALE_THRESHOLD = 10000.0

# Menyimpan riwayat block terakhir yang sudah diperiksa agar tidak terjadi duplikasi
last_checked_block = 0

def get_latest_block_number():
    """Mengambil nomor block terbaru di blockchain Mantle."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1
    }
    try:
        r = requests.post(MANTLE_RPC_URL, json=payload, timeout=10).json()
        return int(r['result'], 16)
    except Exception as e:
        print(f"⚠️ Gagal mengambil block number Mantle: {e}")
        return None

def get_block_transactions(block_number):
    """Mengambil semua daftar transaksi di dalam satu block spesifik."""
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],  # True untuk memuat objek transaksi lengkap
        "id": 1
    }
    try:
        r = requests.post(MANTLE_RPC_URL, json=payload, timeout=10).json()
        return r.get('result', {}).get('transactions', [])
    except Exception as e:
        print(f"⚠️ Gagal memuat data transaksi block {block_number}: {e}")
        return []

def scan_mantle_onchain_whales():
    """Memantau block terbaru dan menyaring transaksi MNT bernilai raksasa."""
    global last_checked_block
    whale_alerts = []
    
    current_block = get_latest_block_number()
    if not current_block:
        return []
        
    # Jika baru pertama kali dinyalakan, mulai dari block terbaru saat ini
    if last_checked_block == 0:
        last_checked_block = current_block - 1
        
    # Periksa jika ada block baru yang belum diaudit
    if current_block > last_checked_block:
        for block_to_check in range(last_checked_block + 1, current_block + 1):
            print(f"🔍 Menjelajahi Jaringan Mantle — Blok: #{block_to_check}")
            transactions = get_block_transactions(block_to_check)
            
            for tx in transactions:
                # Ambil nilai transaksi (dalam satuan Wei/Hex)
                raw_value = tx.get('value', '0x0')
                if raw_value == '0x0':
                    continue
                    
                # Konversi dari Hex Wei ke nilai koin MNT riil (dibagi 10^18)
                value_mnt = int(raw_value, 16) / 10**18
                
                # Saring hanya transaksi yang menyentuh ambang batas paus
                if value_mnt >= MANTLE_WHALE_THRESHOLD:
                    alert_data = {
                        "hash": tx.get("hash"),
                        "from": tx.get("from"),
                        "to": tx.get("to"),
                        "amount_mnt": value_mnt,
                        "block": block_to_check
                    }
                    whale_alerts.append(alert_data)
                    
        last_checked_block = current_block
        
    return whale_alerts