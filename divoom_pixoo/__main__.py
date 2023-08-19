import struct
from time import sleep

DIVOOM_PIXOO_PROTOCOL_MESSAGE_START = b'\x01'
DIVOOM_PIXOO_PROTOCOL_MESSAGE_END = b'\x02'


def checksum(data: bytes) -> bytes:
    result = 0
    for b in data:
        result += b

    return struct.pack('h', result)


def msg_with_payload(payload: bytes):
    crc = checksum(payload)

    return struct.pack(f'<cH{len(payload)}s2sc',
                       DIVOOM_PIXOO_PROTOCOL_MESSAGE_START,
                       len(payload) + len(crc),
                       payload,
                       crc,
                       DIVOOM_PIXOO_PROTOCOL_MESSAGE_END
                       )


def set_brightness_msg(brightness=100):
    brightness = min(100, max(0, brightness))
    payload = struct.pack('<Bh', 0x74, brightness)
    return msg_with_payload(payload)


def bytes_repr(data: bytes) -> str:
    return data.hex(' ', 1)


if __name__ == '__main__':
    rfcomm_dev = '/dev/rfcomm0'


    brightness_max = set_brightness_msg(100)
    brightness_min = set_brightness_msg(1)


    print(f'Max: {bytes_repr(brightness_max)}\nMin: {bytes_repr(brightness_min)}')

    with open(rfcomm_dev, 'w') as rfcomm:
        for i in range(10):
            print(f'round {i}')
            rfcomm.write(brightness_max.hex())
            sleep(1)
            rfcomm.write(brightness_min.hex())
            sleep(1)
