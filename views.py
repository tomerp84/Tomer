from django.http import HttpResponse, HttpResponseBadRequest
import json

from django.views import View
from .models import Networks,Devices,Throughputs
from django.db.models import Avg


class Netwrok(View):
    def get(self, request, *args, **kwargs):
        res = {}
        try:
            network = Networks.objects.get(network_id=request.GET['id'])
        except:
            return HttpResponse(status=404)
        devices = Devices.objects.filter(network=network)
        th = Throughputs.objects.filter(device__in=devices)
        avg_throughput = Throughputs.objects.filter(device__in=devices).aggregate(Avg('throughput'))
        avg_throughput = avg_throughput.get("throughput__avg")
        res["id"] = network.network_id
        res["auth"] = network.auth       
        res["devices"]=[device.device_id for device in devices]
        res["avg_throughput"]= avg_throughput
        res = json.dumps(res)
        return HttpResponse(res)

class Connect(View):
    def put(self, request, *args, **kwargs):
        json_params = json.loads(request.body)
        device_id = json_params.get("device_id")
        network_id = json_params.get("network_id")
        auth = json_params.get("auth")
        network = Networks.get_or_create(network_id, auth)
        if not network:
            return HttpResponseBadRequest("Invalid JSON")
        devices = Devices.objects.filter(device_id=device_id)
        if devices:
            return HttpResponseBadRequest("Device already reported")
        
        device = Devices(device_id=device_id,network=network)
        device.save()
        return HttpResponse("done")

class Report(View):
    def post(self, request, *args, **kwargs):
        json_params = json.loads(request.body)
        device_id = json_params.get("device_id")
        network_id = json_params.get("network_id")
        throughput = json_params.get("throughput")
        devices = Devices.objects.filter(device_id=device_id)
        if not devices or devices[0].network.network_id != network_id:
            return HttpResponseBadRequest("Invalid JSON")
        device = devices[0]
        throughput = Throughputs(device=device,throughput=throughput)
        throughput.save()
        
        return HttpResponse("done")

    