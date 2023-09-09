import lcsc
from inventree.api import InvenTreeAPI
from inventree.part import Part, PartCategory, Parameter, ParameterTemplate
from inventree.stock import StockItem, StockLocation

import os
from dotenv import load_dotenv
load_dotenv()

api = InvenTreeAPI(os.getenv('INVENTREE_SERVER'), token='')

PARENT_CATEGORY = os.getenv('ROOT_CATEGORY_ID')
LOCATION_ID = os.getenv('LOCATION_ID')

# ----------------------------

all_categories = PartCategory.list(api, parent=PARENT_CATEGORY)
parameter_templates = ParameterTemplate.list(api)
package_parameter = ParameterTemplate(api, next((item for item in parameter_templates if item.name == 'Package')).pk)

# ----------------------------

if __name__ == "__main__":
    while True:
        inp = input()
        part = lcsc.LCSC(inp)

        print(f'Enter quantity [{part.quantity}]: ', end='')
        qty = input()

        category = next((item for item in all_categories if item.name == part.part_info['parentCatalogName']), None)
        if not category:
            category = PartCategory.create(api, {
                'name': part.part_info['parentCatalogName'],
                'parent': PARENT_CATEGORY
            })

        created_part = None
        is_part_created = True
        find_part = Part.list(api, IPN=part.part_info['productCode'])
        if len(find_part):
            created_part = find_part[0]
            is_part_created = False
        else:
            created_part = Part.create(api, {
                'name': part.mpn,
                'description': part.part_info['productIntroEn'],
                'IPN': part.part_info['productCode'],
                'category': category.pk,
                'remote_image': part.part_info['productImages'][0]
            })

        stock = StockItem.create(api, {
            'location': LOCATION_ID,
            'part': created_part.pk,
            # 'quantity': part.quantity,
            'quantity': qty,
            'purchase_price': part.part_info['productPriceList'][0]['usdPrice'], # needs to be fixed to use correct ladder
            'purchase_price_currency': 'USD'
        })

        if is_part_created:
            Parameter.create(api, {
                'part': created_part.pk,
                'template': package_parameter.pk,
                'data': part.part_info['encapStandard']
            })

            for parm_name in ['Resistance', 'Capacitance', 'Voltage Rated', 'Tolerance']:
                if part.part_info['paramVOList']:
                    parm_in_part = next((item for item in part.part_info['paramVOList'] if parm_name == item['paramNameEn']), None)
                    if parm_in_part:
                        template = next((item for item in parameter_templates if item.name == parm_name))

                        value = parm_in_part['paramValueEn']
                        if parm_name == 'Tolerance':
                            value = value.replace('±', '')

                        Parameter.create(api, {
                            'part': created_part.pk,
                            'template': template.pk,
                            'data': value
                        })
        

        print(f"Added: [{part.mpn} -- {part.part_info['productCode']}] {qty} pcs")
