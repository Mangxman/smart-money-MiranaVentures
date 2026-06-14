import requests
import urllib3

# Menyembunyikan peringatan SSL jika Anda terpaksa menggunakan verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_bybit_mnt_trades():
    """
    Mengambil data riwayat transaksi publik MNT/USDT secara real-time langsung dari Bybit V5.
    Menggunakan domain alternatif resmi (.nl) untuk menghindari blokir ISP lokal.
    """
    # URL resmi Bybit V5 untuk Market Recent Trades
    url = "https://api.bybit.nl/v5/market/recent-trade"
    
    # Parameter query: Spot market, koin MNTUSDT, ambil 50 transaksi terakhir
    query_params = {
        "category": "spot",
        "symbol": "MNTUSDT",
        "limit": 50
    }
    
    # Cukup gunakan Header standar agar tidak diblokir Cloudflare/Sistem Keamanan Bybit
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Eksekusi request GET publik (Tanpa butuh API Key / Signature)
        response = requests.get(url, params=query_params, headers=headers, timeout=10, verify=False)
        
        if response.status_code == 200:
            res_json = response.json()
            
            # retCode 0 berarti Bybit sukses memberikan data transaksi riil
            if res_json.get("retCode") == 0:
                trade_list = res_json.get("result", {}).get("list", [])
                return trade_list
            else:
                print(f"⚠️ Bybit API Menolak (Code {res_json.get('retCode')}): {res_json.get('retMsg')}")
                return []
        else:
            print(f"⚠️ Server Bybit merespons dengan HTTP Status: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Gagal mengambil data transaksi riil dari Bybit: {e}")
        return []