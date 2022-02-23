import asyncio
from bleak import BleakScanner

count = 0
last_scan = 0
lock = False
async def detection_callback(device, advertisement_data):
    global count
    global last_scan
    global lock

    if device.name == 'IF_B7': 
        print(device, advertisement_data)
        value = int.from_bytes(advertisement_data.manufacturer_data[256][10:12],"big")
        
        if value <= 1000:
            return
        if value == last_scan:
            count = count + 1
        else:
            count = 0
            last_scan = value
        if count > 3:
            if lock == False:
                lock = True
                print("Detected")
                print(value)
                
                await asyncio.sleep(10.0)
                lock = False

        
async def run():
    scanner = BleakScanner()
    scanner.register_detection_callback(detection_callback)
    await scanner.start()

    while True:
        await asyncio.sleep(10.0)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

