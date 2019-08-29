from django.db import models
from datetime import datetime


class Networks(models.Model):
    AUTH_TYPES=((u'wpa', u'wpa'),
            (u'publish', u'publish'),
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    network_id =  models.CharField(max_length=64)
    auth = models.CharField(max_length=1, choices=AUTH_TYPES)

    @classmethod
    def get_or_create(cls, network_id, auth):
        networks = cls.objects.filter(network_id=network_id)
        if len(networks) == 0:
            try:
                network = cls(network_id  = network_id,
                              auth = auth,
                              )
                network.save()
            except:
                network = None
        else:
            network = networks[0]
        return network
        
class Devices(models.Model):
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    device_id =  models.CharField(max_length=64)
    network = models.ForeignKey(Networks,on_delete=models.CASCADE,)
    
    

class Throughputs(models.Model):
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    device = models.ForeignKey(Devices,on_delete=models.CASCADE,)
    throughput =  models.PositiveIntegerField(default=0)