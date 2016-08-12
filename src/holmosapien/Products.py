import boto3
import json

class Products:
    def __init__(self):
        self.ddb = boto3.resource('dynamodb', region_name = 'us-east-1')

    def list(self, organizationId):
        table = self.ddb.Table('Products')

        request = {
            'TableName'                 : 'Products',
            'KeyConditionExpression'    : 'organization_id = :orgId',
            'ExpressionAttributeValues' : { ':orgId' : organizationId }
        }

        products = table.query(**request)
        count    = products['Count']

        out = []

        for product in products['Items']:
            p = self._parseProduct(product)

            out.append(p)

        return out

    def get(self, organizationId, sku):
        table = self.ddb.Table('Products')

        request = {
            'TableName' : 'Products',
            'Key'       : { 'organization_id' : organizationId, 'sku' : sku }
        }

        product = table.get_item(**request)

        if 'Item' in product:
            p = product['Item']

            return self._parseProduct(p)

        return None

    def update(self, organizationId, sku, details):
        table = self.ddb.Table('Products')

        return None

    def _parseProduct(self, product):
        organizationId = product['organization_id']
        sku            = product['sku']
        details        = product['product']
        details        = json.loads(details)

        d = {}

        for key in [ 'name', 'summary', 'insured_value', 'sale_price', 'tariff_code', 'weight', 'length', 'width', 'height' ]:
            try:
                d[key] = details[key]

            except KeyError:
                d[key] = None

        out = {
            'organization_id' : organizationId,
            'name'            : d['name'],
            'summary'         : d['summary'],
            'sku'             : sku,
            'insured_value'   : d['insured_value'],
            'sale_price'      : d['sale_price'],
            'tariff_code'     : d['tariff_code'],
            'weight'          : d['weight'],
            'length'          : d['length'],
            'width'           : d['width'],
            'height'          : d['height']
        }

        return out
