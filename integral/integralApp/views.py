from django.shortcuts import render, HttpResponse
from sympy import symbols, integrate, sympify, latex
from django.http import JsonResponse

def calculate_integral(request):
    result = None
    error = None
    steps = []

    if request.method == "POST":
        func = request.POST.get("function")
        integral_type = request.POST.get("integral_type")
        x = symbols('x')  # Define the symbol for integration

        try:
            # Step 1: Parse and validate the function
            expr = sympify(func)
            
            if integral_type == "definite":
                try:
                    # Step 1: Parse and validate the limits
                    lower_limit = float(request.POST.get("lower_limit"))
                    upper_limit = float(request.POST.get("upper_limit"))
                    steps.append(f"\\text{{Sederhanakan fungsi: }} {latex(expr)}")
                    
                    # Step 2: Compute the indefinite integral
                    indefinite_integral = integrate(expr, x)
                    steps.append(f"\\text{{Hitung integral definit: }} \\int {latex(expr)} \\, dx = {latex(indefinite_integral)}")
                    
                    # Step 3: Evaluate the integral at the limits
                    upper_eval = round(float(indefinite_integral.subs(x, upper_limit)),2)
                    lower_eval = round(float(indefinite_integral.subs(x, lower_limit)),2)
                    result = round(upper_eval - lower_eval,2)
                    steps.append(f"\\text{{Hitung untuk batas atas }} ({latex(upper_limit)}): {latex(upper_eval)}")
                    steps.append(f"\\text{{Hitung untuk batas bawah }} ({latex(lower_limit)}): {latex(lower_eval)}")
                    steps.append(f"\\text{{Kurangi hasil dari batas atas dengan batas bawah: }} {latex(result)}") 
                    
                    # steps = (
                    #     f"\\text{{Step 1: Sederhanakan fungsi: }} {latex(expr)} \\\\ "
                    #     f"\\text{{Step 2: Hitung integral definit: }} \\\\ "
                    #     f"\\int {latex(expr)} \\, dx = {latex(indefinite_integral)} \\\\ "
                    #     f"\\text{{Step 3: Hitung untuk batas atas }} ({latex(upper_limit)}): {latex(upper_eval)} \\\\ "
                    #     f"\\text{{Step 4: Hitung untuk batas bawah }} ({latex(lower_limit)}): {latex(lower_eval)} \\\\ "
                    #     f"\\text{{Step 5: Tambahkan kedua batasan integral tersebut: }} {latex(result)}"
                    # )
                    
                except ValueError:
                    error = "Invalid limits provided. Please enter valid numbers."
                except Exception as e:
                    error = f"Error calculating definite integral: {str(e)}"

            elif integral_type == "indefinite":
                try:
                    # Step 1: Compute the indefinite integral
                    indefinite_integral = integrate(expr, x)
                    result = f"{latex(indefinite_integral)} + C"
                    steps.append(f"\\text{{Sederhanakan fungsi: }} {latex(expr)}")
                    steps.append(f"\\text{{Hitung integral tak tentu: }} \\int {latex(expr)} \\, dx = {result}")

                    
                    # steps = (
                    #     f"\\text{{Step 1: Sederhanakan fungsi: }} {latex(expr)} \\\\ "
                    #     f"\\text{{Step 2: Compute the indefinite integral: }} \\\\ "
                    #     f"\\int {latex(expr)} \\, dx = {result}"
                    # )
                except Exception as e:
                    error = f"Error calculating indefinite integral: {str(e)}"

            else:
                error = "Invalid integral type selected."

        except Exception as e:
            error = f"Error parsing the function: {str(e)}"

    return render(request, "base.html", {"result": result, "error": error, "steps": steps})