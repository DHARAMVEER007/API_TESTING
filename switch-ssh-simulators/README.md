# Aruba Switch SSH Simulator

This is a mock SSH server that simulates an Aruba switch for testing network discovery tools.

## Features

- Simulates Aruba switch SSH responses
- Supports all common Aruba discovery commands
- Interactive shell and exec command modes
- No authentication required (for testing purposes)
- Runs on port 22 (configurable)

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Start the Simulator

```bash
python aruba_switch.py
```

The simulator will start on port 22 by default.

### Connect to the Simulator

Using SSH client:
```bash
ssh admin@localhost -p 22
```

Using Python Paramiko:
```python
import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('localhost', port=22, username='admin', password='any')

stdin, stdout, stderr = client.exec_command('show version')
print(stdout.read().decode())

client.close()
```

## Supported Commands

### Probe-based Commands
- `show version` - System version and basic information
- `show interface` - Interface status and configuration
- `show system` - System information and hostname

### Direct SSH Commands
- `show mac-address-table` - MAC address table
- `show arp` - ARP table
- `show vlan` - VLAN configuration
- `show lldp neighbor detail` - LLDP neighbor information

### Stack/Cluster Commands
- `show switch` - Stack information
- `show vsf` - Virtual Switching Framework
- `show vsx` - Virtual Switching Extension
- `show inventory` - Hardware inventory

## Configuration

Edit the following variables in `aruba_switch.py`:

```python
SSH_HOST = "0.0.0.0"  # Listen on all interfaces
SSH_PORT = 22        # Port to listen on
HOST_KEY_PATH = "host_aruba.key"  # SSH host key file
```

## Notes

- This simulator is for testing purposes only
- No authentication is required (accepts any username/password)
- The simulator runs independently from the NetApp simulator
- All responses are hardcoded mock data

## Troubleshooting

If you get a "port already in use" error, either:
1. Stop the process using port 22
2. Change SSH_PORT in the script to a different port (e.g., 2222)

## License

This is a testing tool for internal use.


