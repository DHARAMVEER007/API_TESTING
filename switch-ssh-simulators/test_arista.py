#!/usr/bin/env python3
"""
Test script for Arista Switch SSH Simulator
"""

import paramiko
import sys
import time

# Configuration
SSH_HOST = 'localhost'
SSH_PORT = 22
SSH_USER = 'admin'
SSH_PASS = 'admin'

def test_command(host, port, user, password, command):
    """Execute a command and print the result"""
    print(f"\n{'='*70}")
    print(f"Command: {command}")
    print(f"{'='*70}")
    try:
        # Create a new connection for each command
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=user, password=password, timeout=10)
        
        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode('utf-8')
        error = stderr.read().decode('utf-8')
        
        client.close()
        
        if output:
            print(output)
        if error:
            print(f"Error: {error}", file=sys.stderr)
        
        return True
    except Exception as e:
        print(f"Failed to execute command: {e}", file=sys.stderr)
        return False

def main():
    """Main test function"""
    print("="*70)
    print("Arista Switch SSH Simulator - Test Script")
    print("="*70)
    
    print(f"\nTesting connection to {SSH_HOST}:{SSH_PORT}...")
    
    # List of commands to test (based on the Arista commands from the image)
    commands = [
        # Probe commands (via sensors)
        'show version',
        'show interface',
        'show running-config',
        # Direct SSH commands (in aristaSwitchScan)
        'show mac address-table',
        'show arp',
        'show lldp neighbors detail',
        'show vlan brief',
        # Stack/MLAG detection commands (in getAristaStackMembersInfo)
        'show mlag',
        'show mlag detail',
        'show inventory',
    ]
    
    # Test each command (each creates its own connection)
    success_count = 0
    for cmd in commands:
        if test_command(SSH_HOST, SSH_PORT, SSH_USER, SSH_PASS, cmd):
            success_count += 1
        time.sleep(0.5)  # Small delay between commands
    
    # Summary
    print(f"\n{'='*70}")
    print(f"Test Summary")
    print(f"{'='*70}")
    print(f"Total commands tested: {len(commands)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {len(commands) - success_count}")
    print(f"{'='*70}\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

