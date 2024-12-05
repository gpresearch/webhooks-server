import base64
import struct
import base58

data = {
    "discriminator": {
        "type": "u8",
        "data": 2
    },
    "units": {
        "type": "u32",
        "data": 1400000
    }
}

bytes_data = struct.pack(
    '<BI',  # < for little-endian, B for u8, I for u32
    data["discriminator"]["data"],  # u8 value
    data["units"]["data"]  # u32 value
)

print(base64.b64encode(bytes_data))
print(base64.b64encode(bytes_data).decode())
print(base58.b58encode(bytes_data).decode())
