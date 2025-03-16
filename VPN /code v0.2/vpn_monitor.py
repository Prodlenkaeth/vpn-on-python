import os
import subprocess
import psutil
import time

# Настройка WireGuard
WG_INTERFACE = "wg0"
ALLOWED_IPS = "0.0.0.0/0"
CHECK_INTERVAL = 5  # Интервал проверки в секундах

def check_wireguard_status(interface):
    """Проверяет, работает ли интерфейс WireGuard."""
    try:
        result = subprocess.run(["wg", "show", interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except FileNotFoundError:
        print("Команда 'wg' не найдена. Убедитесь, что WireGuard установлен.")
        return False

def disconnect_clients(interface):
    """Отключает всех клиентов от WireGuard интерфейса."""
    try:
        # Получение списка пиров
        peers = subprocess.check_output(["wg", "show", interface, "peers"], text=True).strip().split("\n")
        for peer in peers:
            if peer:
                subprocess.run(["wg", "set", interface, "peer", peer, "remove"], check=True)
                print(f"Отключен пир: {peer}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при отключении клиентов: {e}")

def restart_wireguard(interface):
    """Перезапускает WireGuard интерфейс."""
    try:
        subprocess.run(["wg-quick", "down", interface], check=True)
        subprocess.run(["wg-quick", "up", interface], check=True)
        print(f"Интерфейс {interface} успешно перезапущен.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при перезапуске WireGuard: {e}")

def monitor_vpn():
    """Мониторинг VPN сервера и отключение клиентов при падении."""
    while True:
        if not check_wireguard_status(WG_INTERFACE):
            print("VPN сервер недоступен. Отключаем клиентов...")
            disconnect_clients(WG_INTERFACE)
            restart_wireguard(WG_INTERFACE)
        else:
            print("VPN сервер работает нормально.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        print(f"Запуск мониторинга VPN интерфейса: {WG_INTERFACE}")
        monitor_vpn()
    except KeyboardInterrupt:
        print("Мониторинг остановлен пользователем.")
