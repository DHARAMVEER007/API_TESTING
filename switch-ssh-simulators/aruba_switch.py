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
HOST_KEY_PATH = "host_aruba.key"   # Auto-generated if missing

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
# Aruba Switch command responses
# =========================
def get_aruba_responses():
    """
    Return command-response mappings for Aruba switch
    """
    return {
        # 1. Show Version - Basic system information
        'show version': '''
ArubaOS-Switch
Software revision WC.16.10.0015

  (c) Copyright 2016-2021 Hewlett Packard Enterprise Development LP

  System Name        : ARUBA-CORE-SW01
  System Contact     : Network Admin <netadmin@virima.com>
  System Location    : Building A - Data Center
  
  Chassis Type       : JL322A
  Hardware Version   : WC.16.10.0015
  ROM Version        : WC.16.03.0001
  BIOS Version       : PC.04.08
  Serial Number      : SG45FCD001
  Base MAC Address   : 00:11:22:AA:BB:CC
  System ID          : 0x11223344

  Up Time            : 45 days, 12 hours, 34 minutes
  CPU Utilization    : 8%
  Memory Usage       : 42% (256 MB used / 612 MB total)
  Flash Usage        : 35% (1.2 GB used / 3.4 GB total)
  
  Module           Type                    Status
  ---------------- ----------------------- --------
  1                Aruba 3810M-48G         Up
  2                VSF Module              Up
  
  Software image stamp:
    /ws/swbuildm/rel_salt_qadev_/code/build/lvm(swbuildm_rel_salt_qadev_)
    Nov 15 2021 12:34:56
    WC.16.10.0015
''',

        # 2. Show Interface - Interface information
        'show interface': '''
Interface 1/1/1
Description: Uplink to Core Switch
Hardware: Ethernet
MAC Address: 00:11:22:AA:BB:01
Speed 1000 Mb/s
Type 1000Base-T
Admin state: Up
Operational state: Up
Last change: 2d 5h 30m
Last time operational: 2d 5h 30m
RX
  Octets: 1234567890
  Unicast packets: 987654
  Multicast packets: 12345
  Broadcast packets: 678
  Errors: 0
TX
  Octets: 9876543210
  Unicast packets: 876543
  Multicast packets: 23456
  Broadcast packets: 789
  Errors: 0

Interface 1/1/2
Description: Server Connection
Hardware: Ethernet
MAC Address: 00:11:22:AA:BB:02
Speed 1000 Mb/s
Type 1000Base-T
Admin state: Up
Operational state: Up
Last change: 1d 10h 15m
Last time operational: 1d 10h 15m
RX
  Octets: 5678901234
  Unicast packets: 456789
  Multicast packets: 9876
  Broadcast packets: 543
  Errors: 0
TX
  Octets: 3456789012
  Unicast packets: 234567
  Multicast packets: 8765
  Broadcast packets: 432
  Errors: 0

Interface 1/1/3
Description: Server Connection
Hardware: Ethernet
MAC Address: 00:11:22:AA:BB:03
Speed 1000 Mb/s
Type 1000Base-T
Admin state: Up
Operational state: Up
Last change: 3d 8h 20m
Last time operational: 3d 8h 20m
RX
  Octets: 2345678901
  Unicast packets: 345678
  Multicast packets: 5678
  Broadcast packets: 321
  Errors: 0
TX
  Octets: 4567890123
  Unicast packets: 123456
  Multicast packets: 5432
  Broadcast packets: 234
  Errors: 0

Interface 1/1/4
Description: 
Hardware: Ethernet
MAC Address: 00:11:22:AA:BB:04
Speed 1000 Mb/s
Type 1000Base-T
Admin state: Down
Operational state: Down
Last change: 5d 2h 45m
Last time operational: Never
RX
  Octets: 0
  Unicast packets: 0
  Multicast packets: 0
  Broadcast packets: 0
  Errors: 0
TX
  Octets: 0
  Unicast packets: 0
  Multicast packets: 0
  Broadcast packets: 0
  Errors: 0

Interface vlan1
Description: Default VLAN

Hardware: VLAN

MAC Address: 00:11:22:AA:BB:FF

Admin state: Up

Operational state: Up

IPv4 address 10.10.1.1/24

L3 Counters: RX: 1234567, TX: 9876543

Interface vlan10
Description: Management VLAN

Hardware: VLAN

MAC Address: 00:11:22:AA:BB:FF

Admin state: Up

Operational state: Up

IPv4 address 192.168.10.1/24

L3 Counters: RX: 2345678, TX: 8765432

Interface vlan100
Description: User VLAN

Hardware: VLAN

MAC Address: 00:11:22:AA:BB:FF

Admin state: Up

Operational state: Up

IPv4 address 10.10.100.1/24

L3 Counters: RX: 3456789, TX: 7654321
''',

        # 3. Show System - System information
        'show system': '''
 Status and Counters - General System Information

  System Name        : ARUBA-CORE-SW01
  Hostname           : ARUBA-CORE-SW01
  System Contact     : Network Admin <netadmin@virima.com>
  System Location    : Building A - Data Center

  MAC Age Time (sec) : 300

  Time Zone          : UTC
  Time               : Mon Nov 27 12:34:56 2025
  Up Time            : 45 days, 12 hrs, 34 mins

  Memory - Total     : 628,097,024 (599 MB)
           Free      : 363,147,264 (346 MB)

  CPU Utilization    : 8%
  
  Base MAC Addr      : 001122-aabbcc
  Serial Number      : SG45FCD001
  
  Software Version   : WC.16.10.0015
  ROM Version        : WC.16.03.0001
  
  FIPS Mode          : No
  
  Switch Type        : JL322A Aruba 3810M-48G Switch
''',

        # 4. Show MAC Address Table
        'show mac-address-table': '''
 Status and Counters - Port Address Table

  MAC Address       | Port | VLAN
  ----------------- + ---- + ------
  001122-334455     | 1    | 1
  001122-334456     | 2    | 100
  001122-334457     | 3    | 100
  001122-334458     | 4    | 100
  001122-334459     | 7    | 200
  001122-33445a     | 8    | 200
  001122-33445b     | 9    | 1
  001122-33445c     | 10   | 1
  aabbcc-112233     | 25   | 1
  aabbcc-112234     | 26   | 1
  5566aa-bbccdd     | 2    | 100
  5566aa-bbccde     | 3    | 100
  5566aa-bbccdf     | 4    | 100
  7788bb-ccddee     | 9    | 300
  7788bb-ccddef     | 10   | 300

  Total MAC Addresses : 15
''',

        # 5. Show ARP
        'show arp': '''
 IP ARP table

  IP Address       MAC Address       Type    Port
  --------------- ----------------- ------- ----
  10.10.1.1        001122-334455     dynamic 1
  10.10.1.10       001122-334456     dynamic 2
  10.10.1.11       001122-334457     dynamic 3
  10.10.1.12       001122-334458     dynamic 4
  10.10.1.100      5566aa-bbccdd     dynamic 2
  10.10.1.101      5566aa-bbccde     dynamic 3
  10.10.1.102      5566aa-bbccdf     dynamic 4
  192.168.10.5     001122-33445b     dynamic 9
  192.168.10.6     001122-33445c     dynamic 10
  192.168.20.10    001122-334459     dynamic 7
  192.168.20.11    001122-33445a     dynamic 8

  Total ARP Entries : 11
''',

        # 6. Show VLAN
        'show vlan': '''
 Status and Counters - VLAN Information

  VLAN ID Name                             | Status     Ports
  ------- -------------------------------- + ---------- ---------
  1       DEFAULT_VLAN                     | Port-based 1,9-10,25-26
  100     SERVER_VLAN                      | Port-based 2-4
  200     WIRELESS_VLAN                    | Port-based 7-8
  300     MANAGEMENT_VLAN                  | Port-based 9-10
  999     QUARANTINE_VLAN                  | Port-based 
''',

        # 7. Show LLDP Neighbor Detail
        'show lldp neighbor detail': '''
 LLDP Neighbor Information Detail

 Local Port   : 1
 ChassisType  : mac-address
 ChassisId    : 00:11:22:ff:ee:dd
 PortType     : interface-name
 PortId       : GigabitEthernet0/0/1
 SysName      : CORE-ROUTER-01
 System Descr : Cisco IOS Software, C2960 Software (C2960-LANBASEK9-M), Version 15.2(7)E
 PortDescr    : GigabitEthernet0/0/1

   Capabilities Supported : Bridge, Router
   Capabilities Enabled   : Bridge, Router

   Management Address
     Type   : ipv4
     Address: 10.10.1.1

   System Capabilities : Bridge, Router
   Enabled Capabilities: Bridge, Router

 Local Port   : 2
 ChassisType  : mac-address
 ChassisId    : 00:50:56:aa:bb:cc
 PortType     : interface-name
 PortId       : vmnic0
 SysName      : ESXI-HOST-01
 System Descr : VMware ESXi 7.0.3 build-19193900
 PortDescr    : vmnic0

   Capabilities Supported : Bridge
   Capabilities Enabled   : Bridge

   Management Address
     Type   : ipv4
     Address: 10.10.1.10

 Local Port   : 3
 ChassisType  : mac-address
 ChassisId    : 00:50:56:aa:bb:cd
 PortType     : interface-name
 PortId       : vmnic0
 SysName      : ESXI-HOST-02
 System Descr : VMware ESXi 7.0.3 build-19193900
 PortDescr    : vmnic0

   Capabilities Supported : Bridge
   Capabilities Enabled   : Bridge

   Management Address
     Type   : ipv4
     Address: 10.10.1.11

 Local Port   : 9
 ChassisType  : mac-address
 ChassisId    : aa:bb:cc:11:22:33
 PortType     : interface-name
 PortId       : 25
 SysName      : ACCESS-SW-01
 System Descr : ArubaOS-Switch WC.16.09.0012
 PortDescr    : 25

   Capabilities Supported : Bridge
   Capabilities Enabled   : Bridge

   Management Address
     Type   : ipv4
     Address: 192.168.10.5

 Local Port   : 25
 ChassisType  : mac-address
 ChassisId    : aa:bb:cc:dd:ee:ff
 PortType     : interface-name
 PortId       : 1
 SysName      : ARUBA-CORE-SW02
 System Descr : ArubaOS-Switch WC.16.10.0015
 PortDescr    : 1

   Capabilities Supported : Bridge
   Capabilities Enabled   : Bridge

   Management Address
     Type   : ipv4
     Address: 10.10.1.2

   System Capabilities : Bridge
   Enabled Capabilities: Bridge
''',

        # 8. Show Switch (Stack Information)
        'show switch': '''
        Switch Information
        
          Switch ID  | MAC Address      | Role     | Priority | Status  | Model
          ---------- + ---------------- + -------- + -------- + ------- + ----------------
          1          | 001122-aabbcc    | Master   | 128      | Up      | JL322A
          2          | 001122-aabbcd    | Member   | 64       | Up      | JL322A
          3          | 001122-aabbce    | Member   | 64       | Up      | JL322A
        
          Stack Topology : Ring
          Stack Status   : Ready
          
          Switch 1 Details:
            Serial Number      : SG45FCD001
            Software Version   : WC.16.10.0015
            ROM Version        : WC.16.03.0001
            Up Time            : 45 days, 12 hrs, 34 mins
            
          Switch 2 Details:
            Serial Number      : SG45FCD002
            Software Version   : WC.16.10.0015
            ROM Version        : WC.16.03.0001
            Up Time            : 45 days, 12 hrs, 33 mins
            
          Switch 3 Details:
            Serial Number      : SG45FCD003
            Software Version   : WC.16.10.0015
            ROM Version        : WC.16.03.0001
            Up Time            : 45 days, 12 hrs, 32 mins
        ''',

        # 9. Show VSF (Virtual Switching Framework)
        'show vsf': '''
VSF Domain ID : 12345
MAC Address   : 001122-aabbcc
VSF Topology  : Ring
Status        : Active

Member ID  MAC Address       Model               Pri  Status
---------  ----------------  ------------------  ---  ---------------
1          001122-aabbcc     Aruba JL322A        255  Commander
2          001122-aabbcd     Aruba JL322A        128  Standby
3          001122-aabbce     Aruba JL322A        128  Member
''',

        # 10. Show VSX (Virtual Switching Extension)
        'show vsx': '''
 VSX Operational Status

  VSX Status            : Enabled
  Device Role           : Primary
  ISL Status            : Up
  
  Peer Information:
    Peer IP Address     : 10.10.100.2
    Peer MAC Address    : 001122-aabbdd
    Peer Device Role    : Secondary
    Peer Status         : Up
    Peer Sync Status    : In-sync
    
  ISL Link Information:
    ISL Port 1          : 1/1/49
    ISL Port 2          : 1/1/50
    ISL Channel Status  : Up
    ISL LAG             : lag 256
    
  Keepalive Information:
    Keepalive Status    : Alive
    Keepalive Interface : VLAN 4000
    Keepalive Peer IP   : 10.10.100.2
    Keepalive Interval  : 1000 ms
    Keepalive Timeout   : 3000 ms
    
  Split Recovery Status : Disabled
  
  Multi-chassis LAG Information:
    Total MC-LAGs       : 4
    MC-LAGs Up          : 4
    MC-LAGs Down        : 0
''',

        # 11. Show Inventory
        'show inventory': '''
 System Inventory

  Chassis Information:
    Product Number : JL322A
    Product Name   : Aruba 3810M 48G PoE+ 4SFP+ Switch
    Serial Number  : SG45FCD001
    MAC Address    : 001122-aabbcc
    
  Module 1:
    Product Number : JL322A
    Product Name   : Aruba 3810M 48G PoE+ 4SFP+ Switch
    Serial Number  : SG45FCD001
    MAC Address    : 001122-aabbcc
    Hardware Rev   : A.01
    VSF Role       : Commander
    
  Module 2:
    Product Number : JL322A
    Product Name   : Aruba 3810M 48G PoE+ 4SFP+ Switch
    Serial Number  : SG45FCD002
    MAC Address    : 001122-aabbcd
    Hardware Rev   : A.01
    VSF Role       : Standby
    
  Module 3:
    Product Number : JL322A
    Product Name   : Aruba 3810M 48G PoE+ 4SFP+ Switch
    Serial Number  : SG45FCD003
    MAC Address    : 001122-aabbce
    Hardware Rev   : A.01
    VSF Role       : Member
    
  Power Supply 1:
    Product Number : JL086A
    Product Name   : Aruba X372 54VDC 680W PS
    Serial Number  : SG45PWR001
    Status         : OK
    
  Power Supply 2:
    Product Number : JL086A
    Product Name   : Aruba X372 54VDC 680W PS
    Serial Number  : SG45PWR002
    Status         : OK
    
  Fan Tray 1:
    Product Number : JL085A
    Product Name   : Aruba 3810M Fan Tray
    Serial Number  : SG45FAN001
    Status         : OK
    Speed          : Normal
    
  Transceivers:
    Port 25        : SFP-10G-SR (J9150A)
    Port 26        : SFP-10G-SR (J9150A)
    Port 27        : Not Present
    Port 28        : Not Present
''',

        # Common system commands
        'hostname': 'ARUBA-CORE-SW01',
        'show hostname': 'Hostname : ARUBA-CORE-SW01',
        
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
    Look up command and return appropriate Aruba response
    """
    responses = get_aruba_responses()
    clean_command = command.strip()
    
    # Try exact match first
    if clean_command in responses:
        logger.info(f"Found exact Aruba response for '{clean_command}'")
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
            "ArubaOS-Switch\r\n"
            "Software revision WC.16.10.0015\r\n"
            "\r\n"
            "(c) Copyright 2016-2021 Hewlett Packard Enterprise Development LP\r\n"
            "\r\n"
            "Connected to ARUBA-CORE-SW01\r\n"
            "Type 'exit' to close the session.\r\n\r\n"
        )
        channel.send(welcome_msg.encode('utf-8'))

        while True:
            try:
                channel.send(b"ARUBA-CORE-SW01# ")
                cmd = ""
                start_time = time.time()

                while not cmd.endswith("\n") and not cmd.endswith("\r\n"):
                    if time.time() - start_time > 300:
                        logger.warning("Interactive command input timeout")
                        return
                    if channel.recv_ready():
                        chunk = channel.recv(1024)
                        if not chunk:
                            logger.info("Client disconnected from interactive shell")
                            return
                        cmd += chunk.decode(errors="replace")
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
                channel.send((result + "\r\n").encode('utf-8'))

            except Exception as e:
                logger.error(f"Error in interactive command loop: {e}")
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
    logger.info(f"Aruba Switch SSH Simulator running on {SSH_HOST}:{SSH_PORT}")
    print(f"\n{'='*60}")
    print(f"Aruba Switch SSH Simulator")
    print(f"{'='*60}")
    print(f"Server running on {SSH_HOST}:{SSH_PORT}")
    print(f"Press Ctrl+C to stop the server")
    print(f"")
    print(f"Available commands:")
    print(f"  - show version")
    print(f"  - show interface")
    print(f"  - show system")
    print(f"  - show mac-address-table")
    print(f"  - show arp")
    print(f"  - show vlan")
    print(f"  - show lldp neighbor detail")
    # print(f"  - show switch (Stack Information)")
    print(f"  - show vsf (Virtual Switching Framework)")
    print(f"  - show vsx (Virtual Switching Extension)")
    print(f"  - show inventory")
    print(f"")
    print(f"Test connection:")
    print(f"  ssh admin@localhost -p {SSH_PORT}")
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


