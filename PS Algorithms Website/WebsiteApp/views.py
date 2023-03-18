from django.shortcuts import render, HttpResponse
# Create your views here.

no_of_processes=None

def home(request):
    return render(request, 'index.html')

def about(request):
    return HttpResponse('This is about page')

def SRTF(request):
    from WebsiteApp.calcy import Calcy
    if request.method == 'POST':
        if request.POST.get('no_of_processes'):
            global no_of_processes
            no_of_processes=int(request.POST['no_of_processes'])
            context={'no_of_processes' : range(1, no_of_processes+1)}
            return render(request, 'SRTF.html', context)
        else:
            obj=Calcy(no_of_processes, {}, [], [])
            input_data={}
            input_data.update({'process_input' : request.POST.getlist('process_input')})
            input_data['process_input']=[int(x) for x in input_data['process_input']]
            obj.take_input(input_data)
            obj.processor('srtf')
            avg_wait_time, avg_turn_time=obj.output()
            obj.completion_time_calc()
            data=obj.datastore
            context={'no_of_processes' : range(1,no_of_processes+1), 'output' : [avg_wait_time, avg_turn_time], 'process_data' : data}
            return render(request, 'SRTF_done.html', context)
    else:
        return render(request, 'SRTF.html')

