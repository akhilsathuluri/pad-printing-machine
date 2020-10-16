"""
-----------------------------------------------------------------------------
Two layer pokayoke written for orientation check and model identification of
wheel rims on the pad printing machine
Written: Akhil Sathuluri, akhilsathuluri@gmail.com
Maintianed: Venkat Sai Raghavendra, Saravanan K
Date: 25-05-2020
 -----------------------------------------------------------------------------
 """

from camutils import *
from cycleutils import *
from datetime import datetime
import time
import threading
import multiprocessing as mp
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

map = {'reg_plc_health': 0, 'reg_plc_autoready': 1, 'reg_plc_ready_to_trigger': 2, 're
g_plc_trigger1': 3, 'reg_plc_trigger2': 4, 'reg_plc_cycle_complete': 5, 'reg_plc
_reset': 6, 'reg_plc_error': 7, 'reg_plc_model': 8, 'Label-10': 9, 'Label-11': 1
0, 'Label-12': 11, 'Label-13': 12, 'Label-14': 13, 'Label-15': 14, 'reg_pi_healt
h': 50, 'reg_pi_ready_for_trigger': 51, 'reg_pi_error': 52, 'reg_pi_spoke': 53,
'reg_pi_alloy': 54, 'reg_pi_ori_ok': 55, 'reg_pi_ori_nok': 56, 'reg_pi_model_1':
 57, 'reg_pi_model_2': 58, 'reg_pi_model_3': 59, 'reg_pi_model_4': 60, 'reg_pi_m
odel_nok': 61, 'reg_pi_model_ok': 62, 'reg_pi_unknown_error': 63, 'reg_pi_last_l
oop': 64}

# Enter code of connecting with pymodbus

def main_funcs(client, map):
    t1 = threading.Thread(target=health, args=(client,map, ))
    t2 = threading.Thread(target=cycle, args=(client,map, ))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

if __name__=="__main__":
    main_funcs()
