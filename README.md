
# LCSC QR Code to [InvenTree](https://github.com/inventree/InvenTree) scanner

![LCSC Packet](https://github.com/Yabzik/lcsc-qr-inventree/blob/main/packet.jpg?raw=true "LCSC Packet")

This is the MVP of the LCSC packet QR code scanner with integration with [InvenTree](https://github.com/inventree/InvenTree) server via API.

*Eventually I would like to integrate this functionality into the built-in QR code handler in InvenTree, but I don't have time for that at the moment. Maybe this project will help someone to do it, or just help to organize the storage of LCSC parts*

The script accepts QR code data as plain text input from the keyboard, so it can be used with any USB 2D scanner (QR code scanner) that works in keyboard mode. You can also use your phone (or other mobile device with a camera) bundled with software that will allow you to use the device's camera as a 2D scanner, and then transfer scanned data to PC. You can find some free software (possibly with limitations, but it was enough for me for personal use).

*You can also modify the script to use QR code input from the webcam, but due to the large size of the data in the code and the relative poor focus and resolution of the webcam (despite it being a 1080p camera) I was unable to get a stable scan results.*
## Environment Variables

To run this project you need to do certain actions in InvenTree and fill in the appropriate variables in the .env file (you can copy it from the .env.example):

`INVENTREE_SERVER` - InvenTree server URL (e.g. https://example.com:1337)

`INVENTREE_TOKEN` - your InvenTree account token. You can get it by going to `/api/user/token/` of your server (be sure to be logged into your account)

`ROOT_CATEGORY_ID` - the root category ID for all categories that will be created automatically (e.g. named Parts). The ID can be found from the URL of the subcategory

`LOCATION_ID` - ID of the location in the warehouse to which components will be added. The ID can be found from the URL of the location

**You also need to create part parameter templates (Settings - Parameter Templates):**

- Package
- Resistance - ohm
- Capacitance - farad
- Tolerance - percent
- Voltage Rated - volt

Currently, the script does not create parameter templates automatically, but only uses the listed ones.
## Installation

```bash
  # create and activate python virtual environment (optional)

  pip3 install -r requirements.txt
  cp .env.example .env
  # fill .env file with appropriate values
  python3 main.py
```
    
## QR code data format

The data in a QR code usually looks like this:
`{pbn:PICK23060XXXXX,on:WM23060XXXXX,pc:C78960,pm:BH1750FVI-TR,qty:2,mc:MuS-A,cc:1,pdi:82706XXX,hp:0,wc:ZH}`
The names of the parameters in the list:

- `pbn` - Unknown, possibly the packer's number. Has the format `PICK` `YYMMDD` `XXXX`, usually the same for all or most packages in an order
- `on` - Order Number
- `pc` - LCSC catalog part number
- `pm` - Manufacturer's part name
- `qty` - Quantity
- `mc` - Customer Number (any value can be entered at checkout)
- `cc` - Unknown
- `pdi` - Unknown, different for each package in the order, possibly internal sequence number
- `hp` - Unknown
- `wc` - Unknown
