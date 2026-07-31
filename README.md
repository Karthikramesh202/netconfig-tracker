# Network Configuration Backup & Change Tracker

A Python-based NetDevOps automation tool built using **Nornir**, **Netmiko**, and **GitPython** to automate network device backups and track configuration drift in version control.

## Features
- Multi-threaded device backups powered by **Nornir**.
- Automated SSH communication via **Netmiko**.
- Automatic Git staging and timestamped commits using **GitPython**.
- Live terminal diff reporting for detecting configuration drift.

## Project Structure
```text
netconfig-tracker/
├── config.yaml          # Nornir configuration
├── main.py              # Main execution script
├── inventory/
│   ├── hosts.yaml       # Device inventory
│   └── groups.yaml      # Connection credentials
└── backups/             # Saved device configurations