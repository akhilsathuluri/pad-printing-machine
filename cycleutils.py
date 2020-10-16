import pandas as pd
from datetime import datetime
from camutils import *
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

# define register pins here in a dictionary
UNIT = 1

def health(client, map):
    start_register = 50
    block_length = 15
    while True:
        # print('health')
        loop_number = 0
        rq = client.write_registers(map['reg_pi_last_loop'], loop_number, unit=UNIT)
        # Read write health bits
        heartbeat_read = client.read_holding_registers(map['reg_plc_health'], 1, unit=UNIT)
        heartbeat_write = client.write_registers(map['reg_pi_health'], heartbeat_read.registers[0], unit=UNIT)
        # print(heartbeat_read.registers[0])
        # Read write ready to trigger bits
        trigger_read = client.read_holding_registers(map['reg_plc_ready_to_trigger'], 1, unit=UNIT)
        trigger_write = client.write_registers(map['reg_pi_ready_for_trigger'], trigger_read.registers[0], unit=UNIT)
        # Check if PLC is reset in between
        reset = client.read_holding_registers(map['reg_plc_reset'], 1, unit=UNIT)
        if reset.registers[0] == 1:
            # Reset entire memory block data
            rq = client.write_registers(start_register, [0]*block_length, unit=UNIT)
        else:
            pass

def cycle(client, map):
    while True:
        # print('cycle')
        loop_number = 1
        rq = client.write_registers(map['reg_pi_last_loop'], loop_number, unit=UNIT)

        trigger1 = client.read_holding_registers(map['reg_plc_trigger1'], 1, unit=UNIT)
        trigger2 = client.read_holding_registers(map['reg_plc_trigger2'], 1, unit=UNIT)

        # Trigger 1 only after component seat check is verified (handled by PLC)
        # Start cycle
        if trigger1.registers[0] == 1:
            loop_number = 2
            rq = client.write_registers(map['reg_pi_last_loop'], loop_number, unit=UNIT)
            # Read PLC model register
            plc_model = client.read_holding_registers(map['reg_plc_model'], 1, unit=UNIT)
            # Check models
            ret, identified_model = check_model(plc_model.registers[0])
            # Handle not being able to write register
            if ret == True:
                # Write model verify register
                rq = client.write_registers(map['reg_pi_model_ok'], 1, unit=UNIT)
                # Write model number register
                reg_name = 'reg_pi_model_'+str(identified_model)
                rq = client.write_registers(map[reg_name], 1, unit=UNIT)
            elif ret == False:
                rq = client.write_registers(map['reg_pi_model_nok'], 1, unit=UNIT)
                reg_name = 'reg_pi_model_'+str(identified_model)
                rq = client.write_registers(map[reg_name], 1, unit=UNIT)
            elif ret == 'ERROR':
                # To handle camera prediction errors
                rq = client.write_registers(map['reg_pi_error'], 1, unit=UNIT)
            else:
                # To handle unknown read/write or pi errors
                rq = client.write_registers(map['reg_pi_unknown_error'], 1, unit=UNIT)

        # Trigger 2 only after component seat check is verified (handled by PLC)
        if trigger2.registers[0] == 1:
            loop_number = 3
            rq = client.write_registers(map['reg_pi_last_loop'], loop_number, unit=UNIT)
            # Check orientation of the rim
            ret = check_orientation()
            # Handle not being able to write register
            if ret == True:
                rq = client.write_registers(map['reg_pi_ori_ok'], 1, unit=UNIT)
            elif ret == False:
                rq = client.write_registers(map['reg_pi_ori_nok'], 1, unit=UNIT)
            elif ret == 'ERROR':
                rq = client.write_registers(map['reg_pi_error'], 1, unit=UNIT)
            else:
                rq = client.write_registers(map['reg_pi_unknown_error'], 1, unit=UNIT)
