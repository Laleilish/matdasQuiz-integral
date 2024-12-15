from django.shortcuts import render
from sympy import symbols, integrate, sympify, latex

def calculate_integral(request):
    result = None
    error = None
    steps = []

    if request.method == "POST":
        func = request.POST.get("function", "").strip()
        integral_type = request.POST.get("integral_type", "").strip()
        x = symbols('x')  # Define the symbol for integration

        if not func:
            error = "Harap masukkan fungsi yang valid."
        else:
            try:
                # Step 1: Parse the function
                expr = sympify(func)
                steps.append(f"Langkah 1: Fungsi yang akan diintegralkan adalah: \\( {latex(expr)} \\)")

                if integral_type == "definite":
                    try:
                        # Step 2: Parse and validate limits
                        lower_limit = float(request.POST.get("lower_limit", 0))
                        upper_limit = float(request.POST.get("upper_limit", 0))
                        steps.append(f"Langkah 2: Batas integral adalah: "
                                     f"\\( \\text{{Batas bawah}} = {lower_limit}, \\text{{Batas atas}} = {upper_limit} \\)")

                        # Step 3: Compute the indefinite integral
                        indefinite_integral = integrate(expr, x)
                        steps.append(f"Langkah 3: Integral tak tentu dari fungsi ini adalah: "
                                     f"\\( \\int {latex(expr)} \\, dx = {latex(indefinite_integral)} + C \\)")

                        # Step 4: Evaluate the indefinite integral at limits
                        upper_eval = round(float(indefinite_integral.subs(x, upper_limit)), 2)
                        lower_eval = round(float(indefinite_integral.subs(x, lower_limit)), 2)
                        steps.append(f"Langkah 4: Evaluasi hasil integral pada batas atas ({upper_limit}): "
                                     f"\\( {latex(indefinite_integral)} \\big|_{{x={upper_limit}}} = {upper_eval} \\)")
                        steps.append(f"Langkah 5: Evaluasi hasil integral pada batas bawah ({lower_limit}): "
                                     f"\\( {latex(indefinite_integral)} \\big|_{{x={lower_limit}}} = {lower_eval} \\)")

                        # Step 5: Subtract the evaluated values
                        result = round(upper_eval - lower_eval, 2)
                        steps.append(f"Langkah 6: Hasil integral definit dihitung dengan: "
                                     f"\\( \\int_{{{lower_limit}}}^{{{upper_limit}}} {latex(expr)} \\, dx = {upper_eval} - {lower_eval} = {result} \\)")

                    except ValueError:
                        error = "Batas integral tidak valid. Harap masukkan angka yang valid."
                    except Exception as e:
                        error = f"Terjadi kesalahan saat menghitung integral definit: {str(e)}"

                elif integral_type == "indefinite":
                    try:
                        # Step 2: Compute the indefinite integral
                        indefinite_integral = integrate(expr, x)
                        result = f"{latex(indefinite_integral)} + C"
                        steps.append(f"Langkah 2: Integral tak tentu dari fungsi ini adalah: "
                                     f"\\( \\int {latex(expr)} \\, dx = {latex(indefinite_integral)} + C \\)")

                    except Exception as e:
                        error = f"Terjadi kesalahan saat menghitung integral tak tentu: {str(e)}"

                else:
                    error = "Tipe integral yang dipilih tidak valid."

            except Exception as e:
                error = f"Terjadi kesalahan saat memproses fungsi: {str(e)}"

    return render(request, "base.html", {"result": result, "error": error, "steps": steps})
