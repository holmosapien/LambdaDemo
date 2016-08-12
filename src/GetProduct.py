#!/usr/bin/python

from holmosapien.AAA      import AAA
from holmosapien.Products import Products

def handler(event, context):
    print 'GetProduct called with event {}, context {}'.format(event, context)

    headers = event['params']['header']
    path    = event['params']['path']

    #
    # Extract the API key from the headers and figure out who it belongs to.
    #

    try:
        token = headers['X-API-Key']

    except KeyError:
        raise Exception('Not Authorized')

    aaa  = AAA()
    user = aaa.getUserFromToken(token)

    if user is None:
        raise Exception('Not Authorized')

    #
    # Extract the organization ID and product ID from the path.
    #

    organizationId = path['organization_id']
    sku            = path['sku']

    #
    # Verify the user is allowed access to the requested organization.
    #

    organizations = aaa.getOrganizations(user)
    allowed       = [ o['organization_id'] for o in organizations ]

    if organizationId not in allowed:
        print 'User attempted to access forbidden organization {}'.format(organizationId)

        raise Exception('Not Found')

    #
    # Attempt to fetch the product.
    #

    p = Products()

    product = p.get(organizationId, sku)

    if product is None:
        raise Exception('Not Found')

    return { 'product' : product }

if __name__ == '__main__':
    event = {
        'params' : {
            'path' : {
                'organization_id' : '65968D14-5555-42DB-BBA2-48F8244CE1EF',
                'sku'             : '08-0000-01'
            },
            'header'      : { 'X-API-Key' : 'vqvjr7bbjss86cxwh9ys8a9n' }
        }
    }

    print handler(event, {})
