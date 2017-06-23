"""Controls selection of proper class based on the device type."""
from __future__ import unicode_literals
from netmiko.cisco import CiscoIosBase
from netmiko.cisco import CiscoAsaSSH
from netmiko.cisco import CiscoNxosSSH
from netmiko.cisco import CiscoXrSSH
from netmiko.cisco import CiscoWlcSSH
from netmiko.cisco import CiscoS300SSH
from netmiko.eltex import EltexSSH
from netmiko.arista import AristaSSH
from netmiko.hp import HPProcurveSSH, HPComwareSSH
from netmiko.huawei import HuaweiSSH
from netmiko.f5 import F5LtmSSH
from netmiko.juniper import JuniperSSH
from netmiko.brocade import BrocadeNosSSH
from netmiko.brocade import BrocadeNetironSSH
from netmiko.brocade import BrocadeFastironSSH
from netmiko.fortinet import FortinetSSH
from netmiko.checkpoint import CheckPointGaiaSSH
from netmiko.a10 import A10SSH
from netmiko.avaya import AvayaVspSSH
from netmiko.avaya import AvayaErsSSH
from netmiko.linux import LinuxSSH
from netmiko.ovs import OvsLinuxSSH
from netmiko.enterasys import EnterasysSSH
from netmiko.extreme import ExtremeSSH
from netmiko.extreme import ExtremeWingSSH
from netmiko.alcatel import AlcatelSrosSSH
from netmiko.alcatel import AlcatelAosSSH
from netmiko.dell import DellForce10SSH
from netmiko.dell import DellPowerConnectSSH
from netmiko.dell import DellPowerConnectTelnet
from netmiko.paloalto import PaloAltoPanosSSH
from netmiko.quanta import QuantaMeshSSH
from netmiko.aruba import ArubaSSH
from netmiko.vyos import VyOSSSH
from netmiko.ubiquiti import UbiquitiEdgeSSH
from netmiko.ciena import CienaSaosSSH
from netmiko.cisco import CiscoTpTcCeSSH
from netmiko.terminal_server import TerminalServerSSH
from netmiko.terminal_server import TerminalServerTelnet
from netmiko.mellanox import MellanoxSSH
from netmiko.pluribus import PluribusSSH
from netmiko.accedian import AccedianSSH


# The keys of this dictionary are the supported device_types
CLASS_MAPPER_BASE = {
    'cisco_ios': CiscoIosBase,
    'cisco_xe': CiscoIosBase,
    'cisco_asa': CiscoAsaSSH,
    'cisco_nxos': CiscoNxosSSH,
    'cisco_xr': CiscoXrSSH,
    'cisco_wlc': CiscoWlcSSH,
    'cisco_s300': CiscoS300SSH,
    'eltex': EltexSSH,
    'arista_eos': AristaSSH,
    'hp_procurve': HPProcurveSSH,
    'hp_comware': HPComwareSSH,
    'huawei': HuaweiSSH,
    'f5_ltm': F5LtmSSH,
    'juniper': JuniperSSH,
    'juniper_junos': JuniperSSH,
    'brocade_vdx': BrocadeNosSSH,
    'brocade_nos': BrocadeNosSSH,
    'brocade_fastiron': BrocadeFastironSSH,
    'brocade_netiron': BrocadeNetironSSH,
    'vyos': VyOSSSH,
    'brocade_vyos': VyOSSSH,
    'vyatta_vyos': VyOSSSH,
    'a10': A10SSH,
    'avaya_vsp': AvayaVspSSH,
    'avaya_ers': AvayaErsSSH,
    'linux': LinuxSSH,
    'ovs_linux': OvsLinuxSSH,
    'enterasys': EnterasysSSH,
    'extreme': ExtremeSSH,
    'extreme_wing': ExtremeWingSSH,
    'alcatel_sros': AlcatelSrosSSH,
    'alcatel_aos': AlcatelAosSSH,
    'fortinet': FortinetSSH,
    'checkpoint_gaia': CheckPointGaiaSSH,
    'dell_force10': DellForce10SSH,
    'dell_powerconnect': DellPowerConnectSSH,
    'paloalto_panos': PaloAltoPanosSSH,
    'quanta_mesh': QuantaMeshSSH,
    'aruba_os': ArubaSSH,
    'ubiquiti_edge': UbiquitiEdgeSSH,
    'ciena_saos': CienaSaosSSH,
    'cisco_tp': CiscoTpTcCeSSH,
    'generic_termserver': TerminalServerSSH,
    'mellanox_ssh': MellanoxSSH,
    'pluribus': PluribusSSH,
    'accedian': AccedianSSH
}

# Also support keys that end in _ssh
new_mapper = {}
for k, v in CLASS_MAPPER_BASE.items():
    new_mapper[k] = v
    alt_key = k + u"_ssh"
    new_mapper[alt_key] = v
CLASS_MAPPER = new_mapper

# Add telnet drivers
CLASS_MAPPER['cisco_ios_telnet'] = CiscoIosBase
CLASS_MAPPER['dell_powerconnect_telnet'] = DellPowerConnectTelnet
CLASS_MAPPER['generic_termserver_telnet'] = TerminalServerTelnet

# Add general terminal_server driver and autodetect
CLASS_MAPPER['terminal_server'] = TerminalServerSSH
CLASS_MAPPER['autodetect'] = TerminalServerSSH

platforms = list(CLASS_MAPPER.keys())
platforms.sort()
platforms_base = list(CLASS_MAPPER_BASE.keys())
platforms_base.sort()
platforms_str = u"\n".join(platforms_base)
platforms_str = u"\n" + platforms_str


def ConnectHandler(*args, **kwargs):
    """Factory function selects the proper class and creates object based on device_type."""
    if kwargs['device_type'] not in platforms:
        raise ValueError('Unsupported device_type: '
                         'currently supported platforms are: {0}'.format(platforms_str))
    ConnectionClass = ssh_dispatcher(kwargs['device_type'])
    return ConnectionClass(*args, **kwargs)


def ssh_dispatcher(device_type):
    """Select the class to be instantiated based on vendor/platform."""
    return CLASS_MAPPER[device_type]


def redispatch(obj, device_type, session_prep=True):
    """Dynamically change Netmiko object's class to proper class.

    Generally used with terminal_server device_type when you need to redispatch after interacting
    with terminal server.
    """
    new_class = ssh_dispatcher(device_type)
    obj.device_type = device_type
    obj.__class__ = new_class
    if session_prep:
        obj.session_preparation()
