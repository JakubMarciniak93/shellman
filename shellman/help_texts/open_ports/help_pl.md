# 🔌 open_ports – Podgląd portów TCP/UDP i portów szeregowych

Komenda `open_ports` pokazuje aktualnie aktywne lokalne połączenia TCP/UDP razem z informacjami o procesie, PID, adresie lokalnym, adresie zdalnym i stanie połączenia.

Może też wyświetlać fizyczne porty szeregowe i równoległe, takie jak `COM`, `LPT`, `/dev/ttyUSB*`, `/dev/ttyACM*`, `/dev/ttyS*`, `/dev/cu.*` i podobne urządzenia.

---

## 🔧 Opcje

| Opcja                              | Opis                                                                |
| ---------------------------------- | ------------------------------------------------------------------- |
| `--proto tcp/udp`, `-pro tcp/udp`  | Filtruje połączenia sieciowe według protokołu                       |
| `--port N`, `-p N`                 | Filtruje połączenia sieciowe według lokalnego numeru portu          |
| `--json`, `-j`                     | Wyświetla wynik w formacie JSON                                     |
| `--serial`, `-s`                   | Pokazuje fizyczne porty szeregowe/równoległe zamiast portów TCP/UDP |
| `--lang-help pl/eng`, `-lh pl/eng` | Wyświetla rozszerzoną pomoc językową                                |

---

## 📦 Przykłady

Pokaż wszystkie aktywne połączenia TCP/UDP:
shellman open_ports

Pokaż tylko połączenia TCP:
shellman open_ports --proto tcp

Pokaż tylko połączenia UDP na porcie 53:
shellman open_ports --proto udp --port 53

Pokaż połączenia sieciowe w formacie JSON:
shellman open_ports --json

Wyświetl porty szeregowe i równoległe:
shellman open_ports --serial

Wyświetl porty szeregowe i równoległe w formacie JSON:
shellman open_ports --serial --json


Wyświetl pomoc po angielsku:
shellman open_ports --lang-help eng

---

## 🧩 Uwagi

Do odczytu połączeń sieciowych Shellman używa biblioteki `psutil`.
Do wykrywania portów szeregowych Shellman używa biblioteki `pyserial`.
Obie zależności powinny zostać zainstalowane automatycznie podczas instalacji Shellmana na podstawie konfiguracji projektu.
