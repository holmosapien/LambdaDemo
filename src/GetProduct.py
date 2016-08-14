#!/usr/bin/python

from holmosapien.AAA      import AAA
from holmosapien.Products import Products

def handler(event, context):
    print 'GetProduct called with event {}, context {}'.format(event, context)

    principal = event['context']['authorizer-principal-id']
    path      = event['params']['path']

    #
    # Extract the organization ID and product ID from the path.
    #

    organizationId = path['organization_id']
    sku            = path['sku']

    #
    # Verify the user is allowed access to the requested organization.
    #

    aaa = AAA()

    email         = principal.split('|')[1]
    organizations = aaa.getOrganizations(email)
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
            }
        },
        'context' : {
            'authorizer-principal-id' : 'email|nobody@invalid'
        }
    }

    print handler(event, {})
