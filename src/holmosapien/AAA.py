import boto3
import crypt

class AAA:
    ddb = None

    def __init__(self):
        self.ddb = boto3.resource('dynamodb', region_name = 'us-east-1')

    def verifyUser(self, email, providedPassword):
        table = self.ddb.Table('Users')

        request = {
            'TableName' : 'Users',
            'Key'       : { 'email' : email }
        }

        user     = table.get_item(**request)
        password = user['Item']['password']

        if crypt.crypt(providedPassword, password) == password:
            out = {
                'email'   : user['Item']['email'],
                'api_key' : user['Item']['api_key']
            }

            return out

        return None

    def getUserFromToken(self, apiKey):
        table = self.ddb.Table('Users')

        request = {
            'TableName'                 : 'Users',
            'IndexName'                 : 'api_key-index',
            'KeyConditionExpression'    : 'api_key = :apiKey',
            'ExpressionAttributeValues' : { ':apiKey' : apiKey }
        }

        users = table.query(**request)

        for user in users['Items']:
            return user['email']

        return None

    def getOrganizations(self, email):
        table = self.ddb.Table('OrganizationMemberships')

        request = {
            'TableName'                 : 'OrganizationMemberships',
            'KeyConditionExpression'    : 'email = :email',
            'ExpressionAttributeValues' : { ':email' : email }
        }

        organizations = table.query(**request)

        out = []

        for organization in organizations['Items']:
            organizationId = organization['organization_id']

            org = self.getOrganization(organizationId)

            if 'default' in organization:
                org['default'] = 1

            out.append(org)

        return out

    def getOrganization(self, organizationId):
        table = self.ddb.Table('Organizations')

        request = {
            'TableName' : 'Organizations',
            'Key'       : { 'organization_id' : organizationId }
        }

        organization = table.get_item(**request)

        return organization['Item']
