from flask_restful import Resource
import os
from flask import Response
from Models.Account import Account

from Resources.ApiResource import ApiResource

class AccountResource(ApiResource):
    def get(self):
        message = ApiResource.check_authorization(self)
        if (message != None):
            return message, 401

        print("accountresource")
        accountName=self.email
        #move it to login
        account =Account(self.uri,self.user,self.password)
        accountExists=account.checkIfAccountCreated(accountName)
        print(accountExists);
        if (accountExists==False):
            account.create(accountName)
            account.close()
            return Response("Account created")


        return  Response("Account already existed")


