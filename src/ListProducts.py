#!/usr/bin/python

from holmosapien.AAA      import AAA
from holmosapien.Products import Products

def handler(event, context):
    print 'ListProducts called with event {}, context {}'.format(event, context)

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
    # Get a list of all organizations the user is allowed to view, and pre-select the default.
    #

    organizations = aaa.getOrganizations(user)
    allowed       = [ o['organization_id'] for o in organizations ]

    #
    # If the user has requested a specific organization, make sure he has access.
    #

    if 'organization_id' in path:
        organizationId = path['organization_id']

        if organizationId in allowed:
            allowed = [ organizationId ]
        else:
            raise Exception('Not Found')

    #
    # Now we can fetch the products for that organization.
    #

    out = []

    for organizationId in allowed:
        print 'Fetching products for organization ID {}'.format(organizationId)

        p = Products()

        products = p.list(organizationId)

        for product in products:
            out.append(product)

    return { 'products' : out }

if __name__ == '__main__':
    event = {
        'params' : {
            'path'   : { 'organization_id' : '65968D14-5555-42DB-BBA2-48F8244CE1EF' },
            'header' : { 'X-API-Key' : 'vqvjr7bbjss86cxwh9ys8a9n' }
        }
    }

    print handler(event, {})
