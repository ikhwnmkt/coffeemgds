from django.shortcuts import render
from django.http import JsonResponse
from .report import ReportManager

def report_view(request, report_type):
    manager = ReportManager()
    try:
        report = manager.get_report(report_type)
        result = report.generate()  
        return JsonResponse(result, safe=False) 
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    
# Create your views here.

