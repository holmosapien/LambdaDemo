import boto3
import json

class Product:
    client = None
    ddb    = None

    organizationId = None,
    sku            = None,

    properties = {
        'name'            : None,
        'summary'         : None,
        'insured_value'   : None,
        'sale_price'      : None,
        'tariff_code'     : None,
        'weight'          : None,
        'length'          : None,
        'width'           : None,
        'height'          : None
    }

    _ok = False

    def __init__(self, **options):
        self.client = boto3.client('dynamodb')
        self.ddb    = boto3.resource('dynamodb', region_name = 'us-east-1')

        organizationId = options.get('organization_id')
        sku            = options.get('sku')
        product        = options.get('item')

        if organizationId:
            self.organizationId = organizationId

        if sku:
            self.sku = sku

        if product:
            self.parseItem(product)

    def __setitem__(self, key, val):
        self.properties[key] = val

        return

    def __getitem__(self, key):
        return self.properties[key]

    def get(self):
        table = self.ddb.Table('Products')

        request = {
            'TableName' : 'Products',
            'Key'       : { 'organization_id' : self.organizationId, 'sku' : self.sku }
        }

        product = table.get_item(**request)

        if 'Item' in product:
            item = product['Item']

            self.parseItem(item)
            self._ok = True

            return

        raise Exception('Not Found')

    def update(self, update):
        if self._ok == False:
            raise Exception()

        #
        # This allows partial updates of product attributes.
        #
        # First we need to map out the attributes that have changed.
        #

        details = {}

        for key in self.properties.keys():
            if key == 'organization_id' or key == 'sku':

                #
                # Can't change these!
                #

                continue

            if key in update:
                details[key] = update[key]
                self[key]    = update[key]

            details[key] = self[key]

        #
        # Update the DynamoDB record.
        #

        request = {
            'TableName' : 'Products',
            'Key' : { 'organization_id' : { 'S' : self.organizationId }, 'sku' : { 'S' : self.sku } },
            'UpdateExpression' : 'SET product = :product',
            'ExpressionAttributeValues' : { ':product' : { 'S' : json.dumps(details) } }
        }

        #
        # If this fails, it will throw an exception that will bubble up to the caller.
        #

        self.client.update_item(**request)

        return

    #
    # Populate the properties with a Product item in a DynamoDB record.
    #

    def parseItem(self, product):
        self.organizationId = product['organization_id']
        self.sku            = product['sku']

        details = json.loads(product['product'])

        for key in self.properties.keys():
            try:
                self[key] = details[key]

            except KeyError:
                self[key] = None

        return

    #
    # Return a copy of the object as a dictionary.
    #

    def dict(self):
        product = {}

        product['organization_id'] = self.organizationId
        product['sku']             = self.sku

        for key in self.properties.keys():
            product[key] = self[key]

        return product

class ProductList:
    ddb = None

    organizationId = None
    products       = []

    def __init__(self, organizationId):
        self.ddb = boto3.resource('dynamodb', region_name = 'us-east-1')
        self.organizationId = organizationId

        return

    def get(self):
        table = self.ddb.Table('Products')

        request = {
            'TableName'                 : 'Products',
            'KeyConditionExpression'    : 'organization_id = :orgId',
            'ExpressionAttributeValues' : { ':orgId' : self.organizationId }
        }

        items = table.query(**request)
        count = items['Count']

        products = []

        for item in items['Items']:
            p = Product(item = item)

            products.append(p)

        self.products = products

        return

    #
    # Transform the object into an array of Product dictionaries.
    #

    def array(self):
        products = []

        for product in self.products:
            products.append(product.dict())

        return products
