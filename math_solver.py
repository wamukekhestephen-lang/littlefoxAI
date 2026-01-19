import sympy as sp
from sympy import symbols, solve, simplify, diff, integrate, limit
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import re

class MathSolver:
    def __init__(self):
        self.transformations = (standard_transformations + (implicit_multiplication_application,))
    
    def detect_math_problem(self, text):
        """Detect if text contains a math problem"""
        math_keywords = [
            'solve', 'equation', 'derivative', 'integrate', 'limit', 'simplify',
            'factor', 'expand', 'calculus', 'algebra', 'geometry', 'matrix',
            'determinant', 'eigenvalue', 'polynomial', 'root', 'quadratic',
            'linear', 'system', 'differential', 'inequality', 'inequality',
            '=', 'dx', 'dy', '∫', '∑', 'sin', 'cos', 'tan', 'log', 'sqrt'
        ]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in math_keywords)
    
    def solve_algebraic_equation(self, equation_str):
        """Solve algebraic equations"""
        try:
            # Parse the equation
            equation = parse_expr(equation_str, transformations=self.transformations)
            x = symbols('x')
            solutions = solve(equation, x)
            
            if not solutions:
                return "No solutions found."
            
            result = f"Solutions: {solutions}\n"
            if len(solutions) == 1:
                result = f"Solution: {solutions[0]}"
            
            return result
        except Exception as e:
            return f"Error solving equation: {str(e)}"
    
    def compute_derivative(self, expr_str, variable='x'):
        """Compute derivative of an expression"""
        try:
            x = symbols(variable)
            expr = parse_expr(expr_str, transformations=self.transformations)
            derivative = diff(expr, x)
            simplified = simplify(derivative)
            return f"d/d{variable}({expr_str}) = {simplified}"
        except Exception as e:
            return f"Error computing derivative: {str(e)}"
    
    def compute_integral(self, expr_str, variable='x'):
        """Compute indefinite integral of an expression"""
        try:
            x = symbols(variable)
            expr = parse_expr(expr_str, transformations=self.transformations)
            integral = integrate(expr, x)
            return f"∫({expr_str})d{variable} = {integral} + C"
        except Exception as e:
            return f"Error computing integral: {str(e)}"
    
    def compute_limit(self, expr_str, variable='x', point='0'):
        """Compute limit of an expression"""
        try:
            x = symbols(variable)
            expr = parse_expr(expr_str, transformations=self.transformations)
            point_val = parse_expr(point, transformations=self.transformations)
            limit_val = limit(expr, x, point_val)
            return f"lim (x→{point}) {expr_str} = {limit_val}"
        except Exception as e:
            return f"Error computing limit: {str(e)}"
    
    def simplify_expression(self, expr_str):
        """Simplify a mathematical expression"""
        try:
            expr = parse_expr(expr_str, transformations=self.transformations)
            simplified = simplify(expr)
            return f"Simplified: {simplified}"
        except Exception as e:
            return f"Error simplifying: {str(e)}"
    
    def factor_expression(self, expr_str):
        """Factor a polynomial expression"""
        try:
            expr = parse_expr(expr_str, transformations=self.transformations)
            factored = sp.factor(expr)
            return f"Factored form: {factored}"
        except Exception as e:
            return f"Error factoring: {str(e)}"
    
    def expand_expression(self, expr_str):
        """Expand a polynomial expression"""
        try:
            expr = parse_expr(expr_str, transformations=self.transformations)
            expanded = sp.expand(expr)
            return f"Expanded form: {expanded}"
        except Exception as e:
            return f"Error expanding: {str(e)}"
    
    def solve_system_equations(self, equations, variables='x,y'):
        """Solve system of equations"""
        try:
            var_list = [symbols(v.strip()) for v in variables.split(',')]
            eq_list = [parse_expr(eq.strip(), transformations=self.transformations) for eq in equations]
            solutions = solve(eq_list, var_list)
            return f"Solutions: {solutions}"
        except Exception as e:
            return f"Error solving system: {str(e)}"
    
    def process_math_problem(self, user_input):
        """Main method to process math problems and return solution"""
        result = "MATHEMATICAL SOLUTION:\n" + "="*50 + "\n"
        
        # Detect operation type from user input
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['solve', 'equation']):
            # Extract equation (simple heuristic)
            equation = user_input.split('=')[1] if '=' in user_input else user_input
            result += self.solve_algebraic_equation(equation)
        
        elif any(word in user_lower for word in ['derivative', 'd/dx', "d'"]):
            expr = user_input.replace('derivative of', '').replace("d'", '').strip()
            result += self.compute_derivative(expr)
        
        elif any(word in user_lower for word in ['integral', '∫', 'integrate']):
            expr = user_input.replace('integral of', '').replace('∫', '').strip()
            result += self.compute_integral(expr)
        
        elif any(word in user_lower for word in ['limit', 'lim']):
            result += self.compute_limit(user_input)
        
        elif any(word in user_lower for word in ['simplify', 'simplification']):
            expr = user_input.replace('simplify', '').strip()
            result += self.simplify_expression(expr)
        
        elif any(word in user_lower for word in ['factor', 'factorize']):
            expr = user_input.replace('factor', '').strip()
            result += self.factor_expression(expr)
        
        elif any(word in user_lower for word in ['expand']):
            expr = user_input.replace('expand', '').strip()
            result += self.expand_expression(expr)
        
        else:
            result += self.simplify_expression(user_input)
        
        return result

# Initialize solver
math_solver = MathSolver()
