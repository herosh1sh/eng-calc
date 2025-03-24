import tkinter as tk
from tkinter import ttk
import math
import cmath
import numpy as np
import os
import sys
from sympy import symbols, solve, simplify, expand, factor, Matrix, sqrt, sin, cos, tan, log, ln, pi, E

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#1c1c1e")
        
        
        self.current_expression = ""
        self.total_expression = ""
        self.display_val = tk.StringVar(value="0")
        self.memory = 0
        self.ans = 0
        self.angle_mode = "RAD"  
        
        
        self.create_display()
        
        
        self.create_buttons()
    
    def create_display(self):
        display_frame = tk.Frame(self.root, bg="#1c1c1e")
        display_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.small_display = tk.Label(
            display_frame, 
            text="", 
            anchor="e", 
            bg="#1c1c1e", 
            fg="#8a8a8c", 
            font=("Arial", 12)
        )
        self.small_display.pack(expand=True, fill="both")
        
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_val,
            justify="right",
            bg="#1c1c1e",
            fg="white",
            font=("Arial", 36, "bold"),
            bd=0,
            highlightthickness=1,
            highlightbackground="#333333",
            insertbackground="white"  
        )
        self.display.pack(expand=True, fill="both", pady=5)
        
        self.mode_display = tk.Label(
            display_frame, 
            text=f"Mode: {self.angle_mode}", 
            anchor="w", 
            bg="#1c1c1e", 
            fg="#8a8a8c", 
            font=("Arial", 10)
        )
        self.mode_display.pack(expand=True, fill="both")
        
    def create_buttons(self):
        buttons_frame = tk.Frame(self.root, bg="#1c1c1e")
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        
        styles = {
            "normal": {"bg": "#333333", "fg": "white", "font": ("Arial", 14)},
            "operation": {"bg": "#ff9f0a", "fg": "white", "font": ("Arial", 14)},
            "function": {"bg": "#5e5e5e", "fg": "white", "font": ("Arial", 14)},
            "special": {"bg": "#5e5e5e", "fg": "white", "font": ("Arial", 14)},
            "clear": {"bg": "#ff453a", "fg": "white", "font": ("Arial", 14)},
        }
        
        
        buttons = [
            ("sin", self.sin, "function"),
            ("cos", self.cos, "function"),
            ("tan", self.tan, "function"),
            ("π", lambda: self.add_to_expression("math.pi"), "function"),
            ("e", lambda: self.add_to_expression("math.e"), "function"),
            
            ("√", self.sqrt, "function"),
            ("^2", self.square, "function"),
            ("^", lambda: self.add_to_expression("**"), "function"),
            ("log", self.log10, "function"),
            ("ln", self.ln, "function"),
            
            ("(", lambda: self.add_to_expression("("), "special"),
            (")", lambda: self.add_to_expression(")"), "special"),
            ("DEG/RAD", self.toggle_angle_mode, "special"),
            ("M+", self.memory_add, "special"),
            ("MR", self.memory_recall, "special"),
            
            ("7", lambda: self.add_to_expression("7"), "normal"),
            ("8", lambda: self.add_to_expression("8"), "normal"),
            ("9", lambda: self.add_to_expression("9"), "normal"),
            ("DEL", self.delete, "clear"),
            ("AC", self.clear, "clear"),
            
            ("4", lambda: self.add_to_expression("4"), "normal"),
            ("5", lambda: self.add_to_expression("5"), "normal"),
            ("6", lambda: self.add_to_expression("6"), "normal"),
            ("×", lambda: self.add_to_expression("*"), "operation"),
            ("÷", lambda: self.add_to_expression("/"), "operation"),
            
            ("1", lambda: self.add_to_expression("1"), "normal"),
            ("2", lambda: self.add_to_expression("2"), "normal"),
            ("3", lambda: self.add_to_expression("3"), "normal"),
            ("+", lambda: self.add_to_expression("+"), "operation"),
            ("-", lambda: self.add_to_expression("-"), "operation"),
            
            ("0", lambda: self.add_to_expression("0"), "normal"),
            (".", lambda: self.add_to_expression("."), "normal"),
            ("Ans", self.use_answer, "special"),
            ("=", self.evaluate, "operation")
        ]
        
        
        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)
        buttons_frame.columnconfigure(2, weight=1)
        buttons_frame.columnconfigure(3, weight=1)
        buttons_frame.columnconfigure(4, weight=1)
        
        
        row, col = 0, 0
        for (text, command, style_name) in buttons:
            style = styles[style_name]
            
            
            if text == "=":
                btn = tk.Button(
                    buttons_frame, 
                    text=text, 
                    command=command,
                    bg=style["bg"], 
                    fg=style["fg"], 
                    font=style["font"],
                    borderwidth=0,
                    highlightthickness=0
                )
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            else:
                btn = tk.Button(
                    buttons_frame, 
                    text=text, 
                    command=command,
                    bg=style["bg"], 
                    fg=style["fg"], 
                    font=style["font"],
                    borderwidth=0,
                    highlightthickness=0
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                
                col += 1
                if col > 4:
                    col = 0
                    row += 1
        
        
        for i in range(7):
            buttons_frame.rowconfigure(i, weight=1)
            
        
        self.root.bind("<Key>", self.key_press)
    
    def key_press(self, event):
        """Handle keyboard inputs"""
        key = event.char
        if key.isdigit() or key in "+-*/().":
            self.add_to_expression(key)
        elif key == "\r":  
            self.evaluate()
        elif key == "\x08":  
            self.delete()
    
    def add_to_expression(self, value):
        if self.display_val.get() == "0" and value.isdigit():
            self.current_expression = value
        else:
            self.current_expression += value
        self.update_display()
    
    def evaluate(self):
        self.total_expression = self.current_expression
        try:
            
            expression = self.total_expression
            
            
            result = eval(expression)
            
            
            self.ans = result
            
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 8)
            
            self.current_expression = str(result)
            self.small_display.config(text=self.total_expression)
        except Exception as e:
            self.current_expression = "Error"
        
        self.update_display()
    
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.display_val.set("0")
        self.small_display.config(text="")
    
    def delete(self):
        self.current_expression = self.current_expression[:-1]
        if not self.current_expression:
            self.display_val.set("0")
        else:
            self.update_display()
    
    def update_display(self):
        if self.current_expression:
            self.display_val.set(self.current_expression)
        else:
            self.display_val.set("0")
        
        
        self.display.icursor(len(self.display_val.get()))
    
    def memory_add(self):
        try:
            value = eval(self.current_expression)
            self.memory += value
        except:
            pass
    
    def memory_recall(self):
        self.current_expression = str(self.memory)
        self.update_display()
    
    def use_answer(self):
        self.current_expression += str(self.ans)
        self.update_display()
    
    def sin(self):
        try:
            if self.angle_mode == "DEG":
                value = eval(self.current_expression) * math.pi / 180
            else:
                value = eval(self.current_expression)
            self.current_expression = str(math.sin(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def cos(self):
        try:
            if self.angle_mode == "DEG":
                value = eval(self.current_expression) * math.pi / 180
            else:
                value = eval(self.current_expression)
            self.current_expression = str(math.cos(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def tan(self):
        try:
            if self.angle_mode == "DEG":
                value = eval(self.current_expression) * math.pi / 180
            else:
                value = eval(self.current_expression)
            self.current_expression = str(math.tan(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def sqrt(self):
        try:
            value = eval(self.current_expression)
            self.current_expression = str(math.sqrt(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def square(self):
        try:
            value = eval(self.current_expression)
            self.current_expression = str(value ** 2)
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def log10(self):
        try:
            value = eval(self.current_expression)
            self.current_expression = str(math.log10(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def ln(self):
        try:
            value = eval(self.current_expression)
            self.current_expression = str(math.log(value))
            self.update_display()
        except:
            self.current_expression = "Error"
            self.update_display()
    
    def toggle_angle_mode(self):
        if self.angle_mode == "RAD":
            self.angle_mode = "DEG"
        else:
            self.angle_mode = "RAD"
        self.mode_display.config(text=f"Mode: {self.angle_mode}")


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()