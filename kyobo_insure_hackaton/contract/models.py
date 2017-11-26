from django.db import models


# Create your models here.
class ContractLog(models.Model):
    name = models.CharField(max_length=32)
    contract_addr = models.CharField(max_length=64)

    def __str__(self):
        return "<%s - %s>" % (self.name, self.contract_addr)
