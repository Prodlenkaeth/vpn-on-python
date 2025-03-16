import os
import psutil
import time

def is_vpn_running(vpn_process_name):
    """Проверяет, работает ли процесс VPN."""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == vpn_process_name:
            return True
    return False

def block_traffic():
    """Блокирует трафик через iptables."""
    os.system("iptables -A OUTPUT -j DROP")
    os.system("iptables -A INPUT -j DROP")
    print("Трафик заблокирован.")

def unblock_traffic():
    """Разблокирует трафик через iptables."""
    os.system("iptables -F OUTPUT")
    os.system("iptables -F INPUT")
    print("Трафик разблокирован.")

def monitor_vpn(vpn_process_name, check_interval):
    """Мониторит VPN-сервер и управляет трафиком."""
    vpn_was_running = is_vpn_running(vpn_process_name)

    if vpn_was_running:
        print("VPN-сервер работает.")
    else:
        print("VPN-сервер не работает, блокирую трафик.")
        block_traffic()

    while True:
        vpn_running = is_vpn_running(vpn_process_name)

        if vpn_running and not vpn_was_running:
            print("VPN-сервер запущен, разблокирую трафик.")
            unblock_traffic()

        elif not vpn_running and vpn_was_running:
            print("VPN-сервер упал, блокирую трафик.")
            block_traffic()

        vpn_was_running = vpn_running

        time.sleep(check_interval)

if __name__ == "__main__":
    VPN_PROCESS_NAME = "openvpn"  # Название процесса VPN, например, "openvpn"
    CHECK_INTERVAL = 5  # Интервал проверки в секундах

    try:
        monitor_vpn(VPN_PROCESS_NAME, CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\nОстановка мониторинга. Разблокирую трафик...")
        unblock_traffic()



Этот софт лежит уже в коде питона для компилятора  ![[vpn_server_manager.py]]