import socket
import threading
import paramiko
import sys
import time
import logging
import re
from typing import Optional

# =========================
# Config
# =========================
SSH_HOST = "0.0.0.0"
SSH_PORT = 22                     # Standard SSH port
HOST_KEY_PATH = "host_arista.key"   # Auto-generated if missing

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Suppress paramiko's verbose logging
logging.getLogger("paramiko").setLevel(logging.WARNING)

# =========================
# Host key (generate if absent)
# =========================
def _load_or_create_host_key(path: str) -> paramiko.RSAKey:
    try:
        return paramiko.RSAKey(filename=path)
    except FileNotFoundError:
        logger.info(f"Generating new host key: {path}")
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(path)
        return key
    except Exception as e:
        logger.error(f"Error loading host key: {e}")
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(path)
        return key

HOST_KEY = _load_or_create_host_key(HOST_KEY_PATH)

# =========================
# Paramiko server interface
# =========================
class SSHHandler(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.exec_command = None
        self.is_exec_request = False

    def check_auth_password(self, username, password):
        logger.debug(f"Password auth attempt: username={username}")
        return paramiko.AUTH_SUCCESSFUL

    def check_auth_none(self, username):
        logger.debug(f"No-auth attempt: username={username}")
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password,none"

    def check_channel_request(self, kind, chanid):
        logger.debug(f"Channel request: kind={kind}, chanid={chanid}")
        return paramiko.OPEN_SUCCEEDED if kind == "session" else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        logger.debug("Shell request received")
        self.is_exec_request = False
        self.event.set()
        return True

    def check_channel_exec_request(self, channel, command):
        logger.info(f"Exec request: {command}")
        self.exec_command = command.decode('utf-8') if isinstance(command, bytes) else command
        self.is_exec_request = True
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        logger.debug(f"PTY request: term={term}")
        return True

# =========================
# Arista Switch command responses
# =========================
def get_arista_responses():
    """
    Return command-response mappings for Arista switch
    """
    return {
        # 1. Show Version - Basic system information (Probe command)
        'show version': '''
Arista DCS-7050TX-64
Hardware version:    01.01
Serial number:       JPE12345678
System MAC address:  00:1c:73:aa:bb:cc

Software image version: 4.28.0F
Architecture:           i386
Internal build version: 4.28.0F-24305004.4280F
Internal build ID:      a1b2c3d4e5f6g7h8
Image format version:   1.0

Uptime:                 45 days, 12 hours and 34 minutes
Total memory:            4096 MB
Free memory:             2048 MB

''',

        # 2. Show Interface - Interface information (Probe command)
        'show interface': '''
Ethernet1
  Hardware is Ethernet, address is 001c.73aa.bb01
  Description: Uplink to Core Router
  Internet address is 10.10.1.1/24
  Broadcast address is 10.10.1.255
  BW 1000000 kbit

Ethernet2
  Hardware is Ethernet, address is 001c.73aa.bb02
  Description: Server Connection 1
  Internet address is 10.10.1.2/24
  Broadcast address is 10.10.1.255
  BW 1000000 kbit

Ethernet3
  Hardware is Ethernet, address is 001c.73aa.bb03
  Description: Server Connection 2
  Internet address is 10.10.1.3/24
  Broadcast address is 10.10.1.255
  BW 1000000 kbit

Ethernet4
  Hardware is Ethernet, address is 001c.73aa.bb04
  Description: Unused Port
  Internet address is not set
  BW 1000000 kbit

Management1
  Hardware is Ethernet, address is 001c.73aa.bbff
  Description: Management Interface
  Internet address is 192.168.1.1/24
  Broadcast address is 192.168.1.255
  BW 1000000 kbit

Vlan11
  Hardware is Vlan, address is 001c.73aa.bbcc
  Internet address is 10.10.1.1/24
  Broadcast address is 10.10.1.255

Vlan110
  Hardware is Vlan, address is 001c.73aa.bbdd
  Internet address is 192.168.10.1/24
  Broadcast address is 192.168.10.255

Vlan1110
  Hardware is Vlan, address is 001c.73aa.bbee
  Internet address is 10.10.100.1/24
  Broadcast address is 10.10.100.255
''',

        # 3. Show Running-Config - Configuration and hostname (Probe command)
        'show running-config': '''
! Command: show running-config
! device: ARISTA-CORE-SW01 (DCS-7050TX-64, EOS-4.28.0F)
!
! boot system flash:/EOS-4.28.0F.swi
!
hostname ARISTA-CORE-SW01
!
spanning-tree mode mstp
!
no aaa root
!
username admin privilege 15 role network-admin secret sha512 $6$rounds=5000$salt1234$hashedpassword
!
interface Ethernet1
   description Uplink to Core Router
   no switchport
   ip address 10.10.1.1/24
!
interface Ethernet2
   description Server Connection 1
   switchport mode access
   switchport access vlan 100
!
interface Ethernet3
   description Server Connection 2
   switchport mode access
   switchport access vlan 100
!
interface Ethernet4
   description Unused Port
   shutdown
!
interface Management1
   ip address 192.168.1.1/24
!
vlan 1
   name DEFAULT_VLAN
!
vlan 10
   name MANAGEMENT_VLAN
!
vlan 100
   name SERVER_VLAN
!
vlan 200
   name WIRELESS_VLAN
!
vlan 300
   name USER_VLAN
!
ip routing
!
''',

        # 4. Show MAC Address Table - MAC address table for L2 mapping (Direct SSH command)
        'show mac address-table': '''
          Mac Address Table
------------------------------------------------------------------
Vlan    Mac Address       Type        Ports      Moves   Last Move
----    -----------       ----        -----      -----   ----------
   1    0011.2233.4455    DYNAMIC     Et1        1       2 days, 5 hours, 30 minutes ago
   1    0011.2233.4456    DYNAMIC     Et2        1       1 days, 10 hours, 15 minutes ago
   1    0011.2233.4457    DYNAMIC     Et3        1       3 days, 8 hours, 20 minutes ago
   1    0011.2233.4458    DYNAMIC     Et4        0       -
 100    0011.2233.4459    DYNAMIC     Et7        1       1 days, 2 hours, 45 minutes ago
 100    0011.2233.445a    DYNAMIC     Et8        1       2 days, 3 hours, 10 minutes ago
 100    0011.2233.445b    DYNAMIC     Et9        1       5 hours, 30 minutes ago
 200    0011.2233.445c    DYNAMIC     Et10       1       1 days, 12 hours, 20 minutes ago
 200    0011.2233.445d    DYNAMIC     Et11       1       3 days, 4 hours, 15 minutes ago
   1    aabb.cc11.2233    DYNAMIC     Et25       1       4 days, 6 hours, 45 minutes ago
   1    aabb.cc11.2234    DYNAMIC     Et26       1       2 days, 8 hours, 30 minutes ago
 100    5566.aabb.ccdd    DYNAMIC     Et2        1       1 days, 10 hours, 15 minutes ago
 100    5566.aabb.ccde    DYNAMIC     Et3        1       3 days, 8 hours, 20 minutes ago
 100    5566.aabb.ccdf    DYNAMIC     Et4        0       -
 300    7788.bbcc.ddee    DYNAMIC     Et9        1       5 hours, 30 minutes ago
 300    7788.bbcc.ddef    DYNAMIC     Et10       1       1 days, 12 hours, 20 minutes ago
Total Mac Addresses for this criterion: 15
''',

        # 5. Show ARP - ARP table for L3 mapping (Direct SSH command)
        'show arp': '''
Address         Age (min)  Hardware Addr   Interface
10.10.1.1       0          0011.2233.4455  Ethernet1
10.10.1.10      5          0011.2233.4456  Ethernet2
10.10.1.11      10         0011.2233.4457  Ethernet3
10.10.1.12      15         0011.2233.4458  Ethernet4
10.10.1.100     20         5566.aabb.ccdd  Ethernet2
10.10.1.101     25         5566.aabb.ccde  Ethernet3
10.10.1.102     30         5566.aabb.ccdf  Ethernet4
192.168.10.5    35         0011.2233.445b  Ethernet9
192.168.10.6    40         0011.2233.445c  Ethernet10
192.168.20.10   45         0011.2233.4459  Ethernet7
192.168.20.11   50         0011.2233.445a  Ethernet8
''',

        # 6. Show LLDP Neighbors Detail - LLDP neighbors for topology (Direct SSH command)
        'show lldp neighbors detail': '''
LLDP neighbors:

Port Ethernet1 has 1 neighbor(s):

Neighbor 0011.22ff.eedd, age 2 days, 5 hours, 30 minutes
  Chassis ID: mac 0011.22ff.eedd
  Port ID: interface-name GigabitEthernet0/0/1
  Port Description: GigabitEthernet0/0/1
  System Name: CORE-ROUTER-01
  System Description: 
Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.2(7)E
  System Capabilities: Bridge, Router
  Enabled Capabilities: Bridge, Router
  Management Address: 10.10.1.1
  Management Address Type: ipv4

Port Ethernet2 has 1 neighbor(s):

Neighbor 0050.56aa.bbcc, age 1 days, 10 hours, 15 minutes
  Chassis ID: mac 0050.56aa.bbcc
  Port ID: interface-name vmnic0
  Port Description: vmnic0
  System Name: ESXI-HOST-01
  System Description: 
VMware ESXi 7.0.3 build-19193900
  System Capabilities: Bridge
  Enabled Capabilities: Bridge
  Management Address: 10.10.1.10
  Management Address Type: ipv4

Port Ethernet3 has 1 neighbor(s):

Neighbor 0050.56aa.bbcd, age 3 days, 8 hours, 20 minutes
  Chassis ID: mac 0050.56aa.bbcd
  Port ID: interface-name vmnic0
  Port Description: vmnic0
  System Name: ESXI-HOST-02
  System Description: 
VMware ESXi 7.0.3 build-19193900
  System Capabilities: Bridge
  Enabled Capabilities: Bridge
  Management Address: 10.10.1.11
  Management Address Type: ipv4

Port Ethernet9 has 1 neighbor(s):

Neighbor aabb.cc11.2233, age 2 days, 8 hours, 30 minutes
  Chassis ID: mac aabb.cc11.2233
  Port ID: interface-name 25
  Port Description: 25
  System Name: ACCESS-SW-01
  System Description: 
ArubaOS-Switch WC.16.09.0012
  System Capabilities: Bridge
  Enabled Capabilities: Bridge
  Management Address: 192.168.10.5
  Management Address Type: ipv4

Port Ethernet25 has 1 neighbor(s):

Neighbor aabb.ccdd.eeff, age 4 days, 6 hours, 45 minutes
  Chassis ID: mac aabb.ccdd.eeff
  Port ID: interface-name 1
  Port Description: 1
  System Name: ARISTA-CORE-SW02
  System Description: 
Arista DCS-7050TX-64
Software image version: 4.28.0F
  System Capabilities: Bridge
  Enabled Capabilities: Bridge
  Management Address: 10.10.1.2
  Management Address Type: ipv4
''',

        # 7. Show VLAN Brief - VLAN information (Direct SSH command)
        'show vlan brief': '''
VLAN Name                             Status    Ports
----- -------------------------------- --------- -------------------------------
1    DEFAULT_VLAN                     active    Et1, Et9, Et10, Et25, Et26
10   MANAGEMENT_VLAN                  active    Et9, Et10
100  SERVER_VLAN                      active    Et2, Et3, Et4
200  WIRELESS_VLAN                    active    Et7, Et8
300  USER_VLAN                        active    Et9, Et10
999  QUARANTINE_VLAN                  active    
''',

        # 8. Show MLAG - MLAG status and peer information (Stack/MLAG detection)
        'show mlag': '''
MLAG Configuration:                   enabled
MLAG Status:                           active
MLAG Ports:                           
  Configured:                          4
  Inactive:                            0
MLAG Peers:                           
  peer-link:                           active
  peer-address:                        10.10.100.2
  system-id:                           001c.73aa.bbdd
  local-id:                            001c.73aa.bbcc
  peer-id:                             001c.73aa.bbdd
MLAG Dual-primary detection:           disabled
MLAG Dual-primary interface errdisabled: disabled
MLAG reload-delay:                     300 seconds (non-default)
MLAG init-delay:                       0 seconds
MLAG mac-address:                     001c.73aa.bbcc
MLAG system priority:                  32768
MLAG shutdown:                         false
''',

        # 9. Show MLAG Detail - Detailed MLAG information (Stack/MLAG detection - fallback)
        'show mlag detail': '''
MLAG Configuration:                   enabled
MLAG Status:                           active
MLAG Ports:                           
  Configured:                          4
  Inactive:                            0
  Active-partial:                      0
  Active-full:                         4
MLAG Peers:                           
  peer-link:                           active
  peer-address:                        10.10.100.2
  system-id:                           001c.73aa.bbdd
  local-id:                            001c.73aa.bbcc
  peer-id:                             001c.73aa.bbdd
  peer-version:                        4.28.0F
  peer-mac-address:                    001c.73aa.bbdd
  peer-role:                           secondary
  peer-priority:                       32768
  peer-state:                          active
  peer-oper-address:                    10.10.100.2
  peer-link-status:                    up
  peer-link-local-interface:           Port-Channel1
  peer-link-peer-interface:            Port-Channel1
MLAG Dual-primary detection:           disabled
MLAG Dual-primary interface errdisabled: disabled
MLAG reload-delay:                     300 seconds (non-default)
MLAG init-delay:                       0 seconds
MLAG mac-address:                     001c.73aa.bbcc
MLAG system priority:                  32768
MLAG shutdown:                         false
MLAG interfaces:
  Port-Channel10                       active-full    peer-link Port-Channel1
  Port-Channel11                       active-full    peer-link Port-Channel1
  Port-Channel12                       active-full    peer-link Port-Channel1
  Port-Channel13                       active-full    peer-link Port-Channel1
''',

        # 10. Show Inventory - Hardware inventory for serial numbers (Stack/MLAG detection)
        'show inventory': '''
Name: "Chassis",  DESCR: "Arista Networks DCS-7050TX-64"
PID: DCS-7050TX-64              , VID: 01.01, SN: JPE12345678

Name: "Management1",  DESCR: "Management1"
PID: Arista Networks             , VID: N/A, SN: N/A

Name: "PowerSupply1",  DESCR: "Power Supply 1"
PID: PWR-400AC-F                  , VID: N/A, SN: PWR12345678

Name: "PowerSupply2",  DESCR: "Power Supply 2"
PID: PWR-400AC-F                  , VID: N/A, SN: PWR12345679

Name: "Fan1",  DESCR: "Fan Module 1"
PID: FAN-7050X-AC-F              , VID: N/A, SN: FAN12345678

Name: "Fan2",  DESCR: "Fan Module 2"
PID: FAN-7050X-AC-F              , VID: N/A, SN: FAN12345679

Name: "Ethernet1",  DESCR: "Ethernet1"
PID: 10GBASE-SR                  , VID: N/A, SN: SFP12345678

Name: "Ethernet2",  DESCR: "Ethernet2"
PID: 10GBASE-SR                  , VID: N/A, SN: SFP12345679

Name: "Ethernet25",  DESCR: "Ethernet25"
PID: 10GBASE-SR                  , VID: N/A, SN: SFP12345680

Name: "Ethernet26",  DESCR: "Ethernet26"
PID: 10GBASE-SR                  , VID: N/A, SN: SFP12345681
''',

        # Common system commands
        'hostname': 'ARISTA-CORE-SW01',
        'show hostname': 'ARISTA-CORE-SW01',
        
        # Exit commands
        'exit': '',
        'quit': '',
        'logout': '',
        'bye': '',
    }

# =========================
# Command lookup
# =========================
def find_command_output(command: str) -> str:
    """
    Look up command and return appropriate Arista response
    """
    responses = get_arista_responses()
    clean_command = command.strip()
    
    # Try exact match first
    if clean_command in responses:
        logger.info(f"Found exact Arista response for '{clean_command}'")
        return responses[clean_command]
    
    # Try case-insensitive match
    clean_lower = clean_command.lower()
    for cmd, output in responses.items():
        if cmd.lower() == clean_lower:
            logger.info(f"Found case-insensitive match for '{clean_command}'")
            return output
    
    # Try partial match for complex commands
    for cmd, output in responses.items():
        if cmd in clean_command or clean_command in cmd:
            logger.info(f"Found partial match for '{clean_command}'")
            return output
    
    logger.warning(f"No response found for command: '{clean_command}'")
    return f"% Invalid input detected at '^' marker.\n"

# =========================
# Handle exec command
# =========================
def handle_exec_command(channel, command):
    """Handle a single exec command and return the result"""
    logger.info(f"Processing exec command: {command[:100]}...")
    try:
        result = find_command_output(command)
        channel.send(result.encode('utf-8'))
        if not result.endswith('\n'):
            channel.send(b'\n')
        channel.send_exit_status(0)
    except Exception as e:
        logger.error(f"Error handling exec command: {e}")
        error_msg = f"Error processing command: {e}\n"
        channel.send(error_msg.encode('utf-8'))
        channel.send_exit_status(1)
    finally:
        try:
            channel.close()
        except:
            pass
        logger.debug(f"Exec command completed: {command[:50]}...")

# =========================
# Handle interactive shell
# =========================
def handle_interactive_shell(channel):
    """Handle interactive shell session"""
    logger.info("Starting interactive shell session")
    try:
        welcome_msg = (
            "\r\n"
            "Last login: Mon Nov 27 12:34:56 2025 from 192.168.1.100\r\n"
            "\r\n"
        )
        channel.send(welcome_msg.encode('utf-8'))

        while True:
            try:
                # Send prompt
                channel.send(b"ARISTA-CORE-SW01# ")
                
                cmd = ""
                start_time = time.time()
                
                # Read input - wait for complete line
                while not cmd.endswith("\n") and not cmd.endswith("\r\n"):
                    if time.time() - start_time > 300:
                        logger.warning("Interactive command input timeout")
                        return
                    
                    if channel.recv_ready():
                        chunk = channel.recv(4096)
                        if not chunk:
                            logger.info("Client disconnected from interactive shell")
                            return
                        cmd += chunk.decode('utf-8', errors='replace')
                    else:
                        time.sleep(0.1)
                
                cmd = cmd.strip()

                if not cmd:
                    continue

                logger.info(f"Interactive command: {cmd}")

                if cmd.lower() in ("exit", "quit", "logout", "bye"):
                    channel.send(b"Goodbye!\r\n")
                    break

                result = find_command_output(cmd)
                if result:
                    channel.send(result.encode('utf-8'))
                channel.send(b"\r\n")

            except Exception as e:
                logger.error(f"Error in interactive command loop: {e}")
                import traceback
                logger.debug(traceback.format_exc())
                break

    except Exception as e:
        logger.error(f"Error in interactive shell: {e}")
    finally:
        try:
            channel.close()
        except:
            pass
        logger.info("Interactive shell session ended")

# =========================
# Client handler
# =========================
def handle_client(client_socket, client_addr):
    logger.info(f"New connection from {client_addr}")
    try:
        client_socket.settimeout(60)
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

        transport = paramiko.Transport(client_socket)
        transport.add_server_key(HOST_KEY)
        transport.set_subsystem_handler('sftp', paramiko.SFTPServer)

        server = SSHHandler()

        try:
            logger.debug("Starting SSH server transport")
            transport.start_server(server=server)

            logger.debug("Waiting for channel")
            channel = transport.accept(30)
            if not channel:
                logger.warning("No channel established")
                return

            logger.debug("Channel established, waiting for shell/exec request")
            server.event.wait(30)

            if not server.event.is_set():
                logger.warning("No shell/exec request received")
                return

            logger.info("SSH session established successfully")

            if server.is_exec_request and server.exec_command:
                handle_exec_command(channel, server.exec_command)
            else:
                handle_interactive_shell(channel)

        except Exception as e:
            logger.error(f"SSH transport error: {e}")
        finally:
            try:
                transport.close()
            except Exception as e:
                logger.debug(f"Error closing transport: {e}")

    except Exception as e:
        logger.error(f"Client handler error: {e}")
    finally:
        try:
            client_socket.close()
        except Exception as e:
            logger.debug(f"Error closing client socket: {e}")
        logger.debug(f"Connection from {client_addr} closed")

# =========================
# Server bootstrap
# =========================
def start_ssh_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.bind((SSH_HOST, SSH_PORT))
    except OSError as e:
        logger.error(f"Failed to bind to {SSH_HOST}:{SSH_PORT} ({e})")
        print(
            f"Failed to bind to {SSH_HOST}:{SSH_PORT} ({e}). "
            f"Port may already be in use. Try a different port.",
            file=sys.stderr,
        )
        sys.exit(1)

    sock.listen(100)
    logger.info(f"Arista Switch SSH Simulator running on {SSH_HOST}:{SSH_PORT}")
    print(f"\n{'='*60}")
    print(f"Arista Switch SSH Simulator")
    print(f"{'='*60}")
    print(f"Server running on {SSH_HOST}:{SSH_PORT}")
    print(f"Press Ctrl+C to stop the server")
    print(f"")
    print(f"Available commands:")
    print(f"  - show version")
    print(f"  - show interface")
    print(f"  - show running-config")
    print(f"  - show mac address-table")
    print(f"  - show arp")
    print(f"  - show lldp neighbors detail")
    print(f"  - show vlan brief")
    print(f"  - show mlag")
    print(f"  - show mlag detail")
    print(f"  - show inventory")
    print(f"")
    print(f"Test connection:")
    print(f"  ssh admin@localhost -p {SSH_PORT}")
    print(f"  (Any username/password will work - for testing only)")
    print(f"{'='*60}\n")

    try:
        while True:
            try:
                client, addr = sock.accept()
                logger.debug(f"Accepted connection from {addr}")
                threading.Thread(
                    target=handle_client,
                    args=(client, addr),
                    daemon=True,
                    name=f"SSH-{addr[0]}:{addr[1]}"
                ).start()
            except Exception as e:
                logger.error(f"Error accepting connection: {e}")
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    finally:
        sock.close()
        logger.info("Server socket closed")

if __name__ == "__main__":
    try:
        start_ssh_server()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)

