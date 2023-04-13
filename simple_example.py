from pyModbusTCP.server import ModbusServer
from pyModbusTCP.client import ModbusClient
from pyModbusTCP.utils import encode_ieee, decode_ieee, \
                              long_list_to_word, word_list_to_long
import time

host = "localhost"
port = 12345


def write_coils(coils):
    for position, bit in enumerate(coils):
        is_ok = plc.write_single_coil(position, bit)
        if is_ok:
            print('coil #%s: write to %s' % (position, bit))
        else:
            print('coil #%s: unable to write %s' % (position, bit))
        time.sleep(0.5)


def read_coils(address, coils_len=1):
    return plc.read_coils(address, coils_len)


def read_float(address, len=1):
    """Read float(s) with read holding registers."""
    reg_l = plc.read_holding_registers(address, len * 2)
    if reg_l:
        return [decode_ieee(f) for f in word_list_to_long(reg_l)]
    else:
        return None


def write_float(address, floats_list):
    """Write float(s) with write multiple registers."""
    b32_l = [encode_ieee(f) for f in floats_list]
    b16_l = long_list_to_word(b32_l)
    return plc.write_multiple_registers(address, b16_l)


if __name__ == '__main__':
    host = "localhost"
    port = 12345

    s = ModbusServer(host, port, no_block=True)
    try:
        print("starting server")
        s.start()
        print("server started")
        plc = ModbusClient(host=host, port=port, auto_open=True, auto_close=True)

        plc.open()

        # bits = [True, False, True, True, False, False, False, True]
        # write_coils(bits)
        # print(read_coils(0, len(bits)))

        # floats = [4, 3.21, 19, -2.1, 0.0009]
        # write_float(0, floats)
        # print(read_float(0, len(floats)))

        plc.close()
    except Exception as e:
        print("exception in server", str(e))
        pass
    print("closing server")
    s.stop()
    print("server stopped")