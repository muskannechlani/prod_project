from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import subprocess
def index(request):
     return render(request,'index.html')

def cpu(request):
    process = subprocess.Popen('top -b -n1 | grep ^%Cpu | awk \'{print 100-$8}\'', 
    shell=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE )
    cpu_util = process.stdout.read()
  
    return HttpResponse(cpu_util)

   

def mem(request):

    process = subprocess.Popen('free | grep Mem | awk \'{print $3/$2 * 100.0}\'',
    shell=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE )
    mem_util = process.stdout.read()
    return HttpResponse(mem_util)

  

def db(request):
    #TO DO: Returns a random number that may or may not be db trend :)
    #we have to find command for this
    import random
    return HttpResponse(random.randint(20,60));
    
def maxcpu(request):
    process = subprocess.Popen('ps -eo pid,ppid,%cpu,cmd --sort=-%cpu | head -n 6 | tail -n 5', 
    shell=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE )
    arr_cpu = []
    for a in process.stdout:
        json_str = {}         
        a=a.decode("utf-8") 
        stri = a.split()
        json_str['pid'] = stri[0]
        json_str['ppid'] = stri[1]
        json_str['cpuUtilization'] = stri[2]
        json_str['name'] = stri[3]
        arr_cpu.append(json_str)
    return JsonResponse(arr_cpu,safe=False)


def maxmem(request):
    #TO DO: Return the json object in response
    #filter the command to get the required things
    process = subprocess.Popen('ps -eo pid,ppid,%mem,cmd --sort=-%mem | head -n 6 | tail -n 5', 
    shell=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE )
    arr_mem = []
    for a in process.stdout:
        json_str = {}
        a=a.decode("utf-8")
        stri = a.split();
        json_str['pid'] = stri[0]
        json_str['ppid'] = stri[1]
        json_str['memory_utilization'] = stri[2]
        json_str['name'] = stri[3]
        arr_mem.append(json_str)
    return JsonResponse(arr_mem,safe=False)