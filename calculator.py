import tkinter as tk


class CalculatorLogic:
    @staticmethod
    def calculate(expression):
        try:
            if not expression:
                return "0"
            tokens = CalculatorLogic._tokenize(expression)
            if tokens is None:
                return "Error"
            result = CalculatorLogic._evaluate(tokens)
            if result is None:
                return "Error"
            return int(result) if float(result).is_integer() else round(result, 8)
        except ZeroDivisionError:
            return "Error"
        except (ValueError, SyntaxError, NameError):
            return "Error"
        except Exception:
            return "Error"

    @staticmethod
    def _tokenize(expression):
        tokens = []
        current = []
        for ch in expression:
            if ch.isdigit() or ch == ".":
                current.append(ch)
                continue
            if ch in "+-*/":
                if not current:
                    return None
                number = "".join(current)
                if not CalculatorLogic._is_valid_number(number):
                    return None
                tokens.append(float(number))
                tokens.append(ch)
                current = []
                continue
            return None
        if not current:
            return None
        number = "".join(current)
        if not CalculatorLogic._is_valid_number(number):
            return None
        tokens.append(float(number))
        return tokens

    @staticmethod
    def _is_valid_number(text):
        if text.count(".") > 1:
            return False
        if text.startswith(".") or text.endswith("."):
            return False
        return text.replace(".", "").isdigit()

    @staticmethod
    def _evaluate(tokens):
        values = []
        ops = []

        def apply():
            if len(values) < 2 or not ops:
                return False
            b = values.pop()
            a = values.pop()
            op = ops.pop()
            if op == "+":
                values.append(a + b)
            elif op == "-":
                values.append(a - b)
            elif op == "*":
                values.append(a * b)
            elif op == "/":
                if b == 0:
                    raise ZeroDivisionError()
                values.append(a / b)
            return True

        def prec(op):
            return 2 if op in "*/" else 1

        for token in tokens:
            if isinstance(token, float):
                values.append(token)
            else:
                while ops and prec(ops[-1]) >= prec(token):
                    if not apply():
                        return None
                ops.append(token)

        while ops:
            if not apply():
                return None
        if len(values) != 1:
            return None
        return values[0]


class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Calculator")
        self.master.geometry("360x520")
        self.master.configure(bg="#E6F3FF")

        self.expression = ""
        self.error_state = False
        self.leading_operator_ignored = False

        # Display
        self.display = tk.Entry(master, font=("Arial", 28), justify='right',
                                bg="white", fg="black", borderwidth=3, relief="solid",
                                highlightthickness=1, highlightbackground="#9E9E9E")
        self.display.grid(row=0, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
        self.display.insert(0, "0")

        # Keyboard processing
        self.master.bind('<Key>', self.on_key_press)

        # Updated list of buttons with standard symbols * and /
        buttons = [
            ('7', 1, 0, '#004C99', '#F2F2F2'), ('8', 1, 1, '#004C99', '#F2F2F2'), ('9', 1, 2, '#004C99', '#F2F2F2'),
            ('/', 1, 3, 'white', '#7A7A7A'), ('←', 1, 4, 'white', '#B0B0B0'),
            ('4', 2, 0, '#004C99', '#F2F2F2'), ('5', 2, 1, '#004C99', '#F2F2F2'), ('6', 2, 2, '#004C99', '#F2F2F2'),
            ('*', 2, 3, 'white', '#7A7A7A'),
            ('1', 3, 0, '#004C99', '#F2F2F2'), ('2', 3, 1, '#004C99', '#F2F2F2'), ('3', 3, 2, '#004C99', '#F2F2F2'),
            ('-', 3, 3, 'white', '#7A7A7A'), ('=', 3, 4, 'white', '#0059B3'),
            ('C', 4, 0, 'white', '#FF0000'), ('0', 4, 1, '#004C99', '#F2F2F2'), ('.', 4, 2, '#004C99', '#F2F2F2'),
            ('+', 4, 3, 'white', '#7A7A7A'),
        ]

        for (text, row, col, fg, bg) in buttons:
            row_span = 2 if text == '=' else 1
            btn = tk.Button(master, text=text, font=("Arial", 14, "bold"),
                            fg=fg, bg=bg, relief="solid", borderwidth=1,
                            command=lambda t=text: self.process_input(t))
            btn.grid(row=row, column=col, rowspan=row_span, padx=8, pady=8, sticky="nsew")

        for i in range(5):
            master.grid_columnconfigure(i, weight=1, minsize=60)
        for i in range(1, 5):
            master.grid_rowconfigure(i, weight=1, minsize=60)

    def on_key_press(self, event):
        key = event.char
        # Mapping of special keys
        mapping = {
            '\r': '=',  # Enter
            '\x08': '←',  # Backspace
            '\x1b': 'C',  # Escape
            ',': '.'  # Replacing a comma with a full stop
        }

        char = mapping.get(key, key)

        # Check for valid characters (including * and /)
        allowed_chars = "0123456789+-*/.C=←"
        if char in allowed_chars:
            self.process_input(char)

    def process_input(self, char):
        if self.error_state and char != 'C':
            return
        if char == 'C':
            self.expression = ""
            self.error_state = False
            self.leading_operator_ignored = False
            self.update_display("0")
        elif char == '←':
            self.expression = self.expression[:-1]
            self.update_display(self.expression if self.expression else "0")
        elif char == '=':
            if not self.expression and self.leading_operator_ignored:
                self.update_display("Error")
                self.error_state = True
                self.leading_operator_ignored = False
                return
            result = CalculatorLogic.calculate(self.expression)
            self.update_display(result)
            if result == "Error":
                self.expression = ""
                self.error_state = True
            else:
                self.expression = str(result)
        else:
            # LOGIC OF OPERATOR REPLACEMENT:
            if char in '+-*/':
                if not self.expression:
                    self.leading_operator_ignored = True
                    return
                elif self.expression[-1] in '+-*/':  # If the last character is an operator
                    self.expression = self.expression[:-1] + char  #  replace it
                else:
                    self.expression += char
            else:
                self.expression += str(char)
                self.leading_operator_ignored = False

            self.update_display(self.expression)

    def update_display(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(0, value)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
