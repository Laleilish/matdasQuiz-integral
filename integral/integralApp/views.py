from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from sympy import symbols, integrate,sympify
from django.http import JsonResponse

# Create your views here.
def calculate_integral(request):
    result = None   
    error = None   

    if request.method == "POST":
        func = request.POST.get("function")
        try:
            lower_limit = float(request.POST.get("lower_limit"))
            upper_limit = float(request.POST.get("upper_limit"))
        except ValueError:
            error = "Invalid limits provided. Please enter valid numbers."
            return render(request, "base.html", {"result": result, "error": error})

        x = symbols('x')

        try:
            expr = sympify(func)  
            result = integrate(expr, (x, lower_limit, upper_limit))

        except Exception as e:
            error = f"Error: {str(e)}"  

    return render(request, "base.html", {"result": result, "error": error})