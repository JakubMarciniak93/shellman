# 🔌 open_ports – TCP/UDP and Serial Port Viewer

The `open_ports` command shows currently active local TCP/UDP connections with process information.

It can also list physical serial and parallel ports, such as `COM`, `LPT`, `/dev/ttyUSB*`, `/dev/ttyACM*`, `/dev/ttyS*`, `/dev/cu.*`, and similar devices.

---

## 🔧 Options

| Option                             | Description                                                  |
| ---------------------------------- | ------------------------------------------------------------ |
| `--proto tcp/udp`, `-pro tcp/udp`  | Filter network connections by protocol                       |
| `--port N`, `-p N`                 | Filter network connections by local port number              |
| `--json`, `-j`                     | Output results as JSON                                       |
| `--serial`, `-s`                   | List physical serial/parallel ports instead of TCP/UDP ports |
| `--lang-help pl/eng`, `-lh pl/eng` | Show localized extended help                                 |

---

## 📦 Examples

Show all active TCP/UDP connections:
shellman open_ports

Show only TCP connections:
shellman open_ports --proto tcp

Show only UDP connections on port 53:
shellman open_ports --proto udp --port 53

Show network connections as JSON:
shellman open_ports --json

List serial and parallel ports:
shellman open_ports --serial

List serial and parallel ports as JSON:
shellman open_ports --serial --json

Show Polish help:
shellman open_ports --lang-help pl

---

## 🧩 Notes
For network connections, Shellman uses `psutil`.
For serial port detection, Shellman uses `pyserial`.
Both dependencies should be installed automatically when Shellman is installed from the project configuration.
