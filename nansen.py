import requests
from config import NANSEN_API_KEY

BASE_URL = "https://api.nansen.ai"

# Daftar wallet whale/smart money Mantle yang ingin dipantau
TARGET_WALLETS = [
    "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 
    "0x3cDb321526964aF9D7eEd9e03E53415D37aA96045" 
]

def get_smart_money():
    """
    Memantau transaksi terbaru dari daftar wallet target di Mantle.
    Menggunakan endpoint Profiler -> Address Transactions (Free Plan).
    """
    headers = {
        "api-key": NANSEN_API_KEY,
        "Content-Type": "application/json"
    }

    all_trades = []
    is_limited = False

    for wallet in TARGET_WALLETS:
        url = f"{BASE_URL}/api/v1/profiler/address/transactions"
        params = {
            "address": wallet,
            "chain": "mantle", 
            "limit": 5
        }

        try:
            r = requests.get(url, headers=headers, params=params, timeout=20)
            if r.status_code == 200:
                result = r.json()
                transactions = result.get("transactions", [])
                for tx in transactions:
                    tx["trader_address"] = wallet
                    tx["trader_address_label"] = "Monitored Whale"
                    all_trades.append(tx)
            elif r.status_code == 402:
                print(f"⚠️ Endpoint atau limitasi gratis menyentuh batas untuk wallet {wallet}")
                is_limited = True
        except Exception as e:
            print(f"Error memindai wallet {wallet}: {e}")
            is_limited = True

    # Jika terkena limit atau error, kembalikan None agar mengaktifkan mode Failover Simulator
    if is_limited and len(all_trades) == 0:
        return None

    return {"data": all_trades}

def get_label(address):
    headers = {
        "api-key": NANSEN_API_KEY
    }
    params = {
        "address": address
    }
    r = requests.get(
        f"{BASE_URL}/api/v1/profiler/address/labels",
        headers=headers,
        params=params,
        timeout=30
    )
    print("LABEL STATUS:", r.status_code)
    return r.json()

def detect_anomaly(smart_money_count, netflow, sentiment):
    score = 0
    if smart_money_count >= 3: score += 1
    if netflow > 100000: score += 1
    if sentiment > 80: score += 1
    return score >= 2