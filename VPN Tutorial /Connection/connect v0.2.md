Для подключения к WireGuard VPN, необходимо настроить клиентскую конфигурацию и использовать её для установления соединения. Вот как это сделать:

### Шаги для подключения к VPN

1. **Создайте клиентский ключ и публичный ключ:** На устройстве клиента выполните команду:
    
    bash
    
    КопиранеРедактиране
    
    `wg genkey | tee privatekey | wg pubkey > publickey`
    
    - `privatekey` — это приватный ключ клиента.
    - `publickey` — это публичный ключ клиента.
2. **Добавьте клиента на сервер:**
    
    - Откройте конфигурацию вашего сервера WireGuard (например, `/etc/wireguard/wg0.conf`).
    - Добавьте секцию `[Peer]` для нового клиента:
        
        makefile
        
        КопиранеРедактиране
        
        `[Peer] PublicKey = <публичный_ключ_клиента> AllowedIPs = <IP-адрес_клиента>/32`
        
        Замените `<публичный_ключ_клиента>` на сгенерированный ключ из шага 1, и укажите уникальный IP-адрес для клиента.
3. **Сгенерируйте конфигурационный файл клиента:** Создайте файл `wg-client.conf` с содержимым:
    
    makefile
    
    КопиранеРедактиране
    
    `[Interface] PrivateKey = <приватный_ключ_клиента> Address = <IP-адрес_клиента>/24 DNS = <DNS-серверы>  [Peer] PublicKey = <публичный_ключ_сервера> Endpoint = <IP_сервера>:<порт> AllowedIPs = 0.0.0.0/0 PersistentKeepalive = 25`
    
    - `<приватный_ключ_клиента>`: приватный ключ, сгенерированный на клиенте.
    - `<IP-адрес_клиента>`: IP-адрес, назначенный сервером.
    - `<DNS-серверы>`: например, `8.8.8.8` или другой DNS.
    - `<публичный_ключ_сервера>`: публичный ключ сервера.
    - `<IP_сервера>:<порт>`: IP-адрес и порт сервера WireGuard (по умолчанию порт 51820).
4. **Запустите VPN-клиент:** Скопируйте файл `wg-client.conf` на устройство клиента и выполните:
    
    bash
    
    КопиранеРедактиране
    
    `wg-quick up wg-client.conf`
    
    Для остановки VPN используйте:
    
    bash
    
    КопиранеРедактиране
    
    `wg-quick down wg-client.conf`
    
5. **Проверьте подключение:** Убедитесь, что VPN работает, проверив свой IP-адрес:
    
    bash
    
    КопиранеРедактиране
    
    `curl ifconfig.me`
    

### Дополнительно

- Убедитесь, что порт сервера WireGuard открыт в брандмауэре.
- Сервер должен иметь статический или динамический (через DDNS) внешний IP.

Если нужно, могу помочь с настройкой конфигурационного файла или любыми другими вопросами!
