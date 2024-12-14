from django.shortcuts import render
from sympy import symbols, integrate, sympify

def calculate_integral(request):
    result = None
    error = None
    steps = None

    if request.method == "POST":
        func = request.POST.get("function")
        integral_type = request.POST.get("integral_type")
        lower_limit = request.POST.get("lower_limit", None)
        upper_limit = request.POST.get("upper_limit", None)
        variable = request.POST.get("variable", "x")  # Default variable is 'x'

        try:
            # Define the variable for integration
            x = symbols(variable)

            # Parse the input function
            expr = sympify(func)

            if integral_type == "definite":
                if lower_limit and upper_limit:
                    try:
                        lower_limit = float(lower_limit)
                        upper_limit = float(upper_limit)

                        # Compute the indefinite integral
                        indefinite_result = integrate(expr, x)

                        # Substitute the limits
                        upper_sub = indefinite_result.subs(x, upper_limit)
                        lower_sub = indefinite_result.subs(x, lower_limit)

                        # Compute the definite result
                        result = upper_sub - lower_sub

                        # Mathematical steps only
                        steps = (
                            f"Step 1: Compute the indefinite integral:\n"
                            f"  ∫({func}) dx = {indefinite_result} + C\n\n"
                            f"Step 2: Substitute the limits into the result:\n"
                            f"  Upper limit ({upper_limit}): {indefinite_result} = {upper_sub}\n"
                            f"  Lower limit ({lower_limit}): {indefinite_result} = {lower_sub}\n\n"
                            f"Step 3: Calculate the definite integral:\n"
                            f"  {upper_sub} - {lower_sub} = {result}\n"
                        )

                    except ValueError:
                        error = "Invalid limits provided. Please enter valid numbers."
                    except Exception as e:
                        error = f"Error calculating definite integral: {str(e)}"
                else:
                    error = "Both lower and upper limits must be provided for definite integrals."

            elif integral_type == "indefinite":
                try:
                    # Identify the rule used for integration
                    steps = "Step 1: Identify the function and its structure.\n"
                    steps += f"  The given function is: {func}\n\n"

                    # Apply the rule for indefinite integral
                    result = integrate(expr, x)
                    result_c = f"{result} + C"
                    steps += "Step 2: Apply the integration rules:\n"

                    # Add details of integration rules
                    if expr.is_polynomial(x):
                        steps += "  Rule: ∫x^n dx = x^(n+1)/(n+1), for n ≠ -1\n"
                    elif expr.has(symbols("sin"), symbols("cos")):
                        steps += "  Rule: ∫sin(x) dx = -cos(x), ∫cos(x) dx = sin(x)\n"
                    elif expr.has(symbols("exp")):
                        steps += "  Rule: ∫e^x dx = e^x\n"
                    elif expr.has(symbols("ln")):
                        steps += "  Rule: ∫ln(x) dx requires integration by parts.\n"
                    else:
                        steps += "  Rule: Use standard integration techniques.\n\n"

                    # Show the indefinite integral result
                    steps += "Step 3: Write the result as an indefinite integral:\n"
                    steps += f"  ∫({func}) dx = {result} + C\n"  # Ensure the "+ C" is included

                    result = result_c
                    
                except Exception as e:
                    error = f"Error calculating indefinite integral: {str(e)}"
            else:
                error = "Invalid integral type selected."

        except Exception as e:
            error = f"Error parsing the function: {str(e)}"

    context = {"result": result or "", "error": error or "", "steps": steps or ""}
    return render(request, "base.html", context)
