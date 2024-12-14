from django.shortcuts import render,HttpResponse
from django.shortcuts import render
from sympy import symbols, integrate,sympify
from django.http import JsonResponse



def calculate_integral(request):
    result = None   
    error = None   
    steps = None

    if request.method == "POST":
        func = request.POST.get("function")
        integral_type = request.POST.get("integral_type")
        x = symbols('x')  # Define the symbol for integration

        try:
            # Step 1: Parse and validate the function
            expr = sympify(func)
            
            if integral_type == "definite":
                try:
                    # Step 2: Parse and validate the limits
                    lower_limit = float(request.POST.get("lower_limit"))
                    upper_limit = float(request.POST.get("upper_limit"))
                    
                    # Step 3: Compute the indefinite integral
                    indefinite_integral = integrate(expr, x)
                    
                    # Step 4: Evaluate the integral at the limits
                    upper_eval = indefinite_integral.subs(x, upper_limit)
                    lower_eval = indefinite_integral.subs(x, lower_limit)
                    result = upper_eval - lower_eval
                    
                    # Step 5: Build the step-by-step explanation
                    steps = (
                        f"Step 1: Parse the function: {func}\n"
                        f"Step 2: Compute the indefinite integral:\n"
                        f"  ∫({func}) dx = {indefinite_integral}\n"
                        f"Step 3: Evaluate at the upper limit ({upper_limit}):\n"
                        f"  F({upper_limit}) = {upper_eval}\n"
                        f"Step 4: Evaluate at the lower limit ({lower_limit}):\n"
                        f"  F({lower_limit}) = {lower_eval}\n"
                        f"Step 5: Compute the definite integral:\n"
                        f"  F({upper_limit}) - F({lower_limit}) = {result}"
                    )
                except ValueError:
                    error = "Invalid limits provided. Please enter valid numbers."
                except Exception as e:
                    error = f"Error calculating definite integral: {str(e)}"

            elif integral_type == "indefinite":
                try:
                    # Compute the indefinite integral
                    result = str(integrate(expr, x))


                   
                    steps = (
                        f"Step 1: Parse the function: {func}\n"
                        f"Step 2: Compute the indefinite integral:\n"
                        f"  ∫({func}) dx = {result} + C"  # C is the constant of integration
                    )
                except Exception as e:
                    error = f"Error calculating indefinite integral: {str(e)}"

            else:
                error = "Invalid integral type selected."

        except Exception as e:
            error = f"Error parsing the function: {str(e)}"

    return render(request, "base.html", {"result": result, "error": error, "steps": steps})











