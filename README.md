# Tech Week - 5.1. Programability

This is the Git repo containing the scripts used in Tech Week - 5.1. Programability.

## General Information

- Nornir: https://nornir.readthedocs.io/en/3.0.0/index.html
- Genie Parser: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers
- PrettyTable: https://ptable.readthedocs.io/en/latest/tutorial.html

## Requirements

- Linux
- macOS
- Python 3

Is not supported by the windows platform.


## Getting Started

#### SandBox DevNet used in this laboratory.

- Cisco Modeling Labs Enterprise: https://devnetsandbox.cisco.com/RM/Diagram/Index/45100600-b413-4471-b28e-b014eb824555?diagramType=Topology
- Topology: https://devnetsandbox.cisco.com/sandbox-instructions/Cisco_Modeling_Ent/CML%20Sandbox%20Topology.pdf

#### Enable SSH on NX-OS in the SandBox

User: cisco
Pass: cisco

```
bash$ telnet <ip-address-nx-os>
dist-sw01# config t
dist-sw01(config)# feature ssh
dist-sw01(config)# end
dist-sw01# copy running-config startup-config 
```

#### Clone this repo

```
bash$ git clone https://gitlab.com/eduardo.dytz/tech-week
bash$ cd tech-week
bash$ pip install -r requirements.txt
```