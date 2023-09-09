import requests

class LCSC():
    def __init__(self, qr_code):
        self._qr_data = {}
        for param in qr_code[1:-1].split(','):
            key, value = param.split(':')
            self._qr_data[key] = value
        
        self.mpn = self._qr_data['pm']
        self.quantity = self._qr_data['qty']
        self._get_info()

    def _get_info(self):
        r = requests.get(f'https://wmsc.lcsc.com/wmsc/product/detail?productCode={self._qr_data["pc"]}')
        self.part_info = r.json()['result']
