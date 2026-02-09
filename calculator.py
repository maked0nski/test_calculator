import tkinter as tk
# ============================================================
# 1) Clear calculator logic (without GUI)
# ============================================================
class CalculatorLogic:
    @staticmethod
    def calculate(expression):
        """
        The main public entry point for calculating.

        INPUT:
          expression: str (for example "12.5+3*2")

        OUTPUT:
          - "0" if the string is empty
          - "Error" if the input is incorrect
          - number (int or float rounded to 8 digits)
        """
        try:
            # 1) Empty input -> display "0"
            if not expression:
                return "0"
            # 2) Split the string into tokens (numbers + operators)
            tokens = CalculatorLogic._tokenize(expression)
            # If something rong with split -> error
            if tokens is None:
                return "Error"
            # 3) Calculate tokens with priority */ over +-
            result = CalculatorLogic._evaluate(tokens)
            # If something wrong during the calculating -> Error
            if result is None:
                return "Error"
            # 4) Formatting the result:
            #    - if result is integer (example  5.0) -> return int(5)
            #    - else round to 8 digits (to control float errors)
            return int(result) if float(result).is_integer() else round(result, 8)
        except ZeroDivisionError:
            # If division by 0 -> Error
            return "Error"
        except (ValueError, SyntaxError, NameError):
            # If typical parsing/calculation errors -> Error
            return "Error"
        except Exception:
            # Any other unexpected crash -> Error
            return "Error"

    # ------------------------------------------------------------
    # 1.1) Parse string into number and operator:
    #       "12.5+3*2" -> [12.5, '+', 3.0, '*', 2.0]
    # ------------------------------------------------------------

    @staticmethod
    def _tokenize(expression):
        """
        Split the string into tokens:
            - numbers (float)
            - operators "+-*/"

        Rules:
          - the number can contain a maximum of one point
          - The point cannot be first or last character (".5" or "5." -> not allowed)
          - the operator cannot be first
          - two operators in a row are NOT allowed
        """
        tokens = []
        current = []   # temporarily accumulate characters of the current number

        for ch in expression:
            # If digit or point is part of a number
            if ch.isdigit() or ch == ".":
                current.append(ch)
                continue
            # If next operator — complete the previous number and add the operator
            if ch in "+-*/":
                # If before operator no number, the expression is incorrect.
                # Examples: "+5", "5++2" (the second + will see current as empty)
                if not current:
                    return None
                number = "".join(current)

                # Validation number format (points/digits)
                if not CalculatorLogic._is_valid_number(number):
                    return None

                # Add a number and operator to the token list
                tokens.append(float(number))
                tokens.append(ch)

                # Clean the storage for the next number
                current = []
                continue

            # Any other characters (letters, spaces, etc.) are not allowed.
            return None

        # At the end of the loop, check if finished with number and NOT an operator
        if not current:
            # example: "5+"
            return None
        number = "".join(current)

        # Validation number format (points/digits)
        if not CalculatorLogic._is_valid_number(number):
            return None

        tokens.append(float(number))
        return tokens

    # ------------------------------------------------------------
    # 1.2) Checking text. Mast be valid number with a decimal point
    # ------------------------------------------------------------
    @staticmethod
    def _is_valid_number(text):
        """
        Allowed:
          "12"
          "12.34"

        Not allowed:
          "12..3" (2 points)
          ".5"    (point in the beginning)
          "5."    (point in the end)
          "1a" (letters)
        """
        if text.count(".") > 1:
            return False
        if text.startswith(".") or text.endswith("."):
            return False

        # After removing the point, only numbers should remain.
        return text.replace(".", "").isdigit()

    # ------------------------------------------------------------
    # 1.3) Evaluate: calculations with priorities (*/ > +-)
    # implemented with two stacks: values and ops
    # ------------------------------------------------------------
    @staticmethod
    def _evaluate(tokens):
        """
        Calculates a list of tokens, with operator priorities.

        Example:
            [2.0, '+', 3.0, '*', 4.0] -> 14.0

        Algorithm:
            - values: stack of numbers
            - ops:    stack of operators
            - when a new operator arrives, apply all operators with higher or
                equal priority from the ops stack
        """
        values = []
        ops = []

        def apply():
            """
            Take the operation from stack and use with the last two numbers.
            If there is not enough data, return False.
            """
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
            """
            Operator priority:
                * or /  ->  2
                + or -  ->  1
            """
            return 2 if op in "*/" else 1

        for token in tokens:
            # IF Number -> put it in values stack
            if isinstance(token, float):
                values.append(token)

            # IF Operator -> before putting it in ops,
            # use previous operators with higher or equal priority
            else:
                while ops and prec(ops[-1]) >= prec(token):
                    if not apply():
                        return None
                ops.append(token)

        # After passing the tokens, we use the rest of the operators
        while ops:
            if not apply():
                return None

        # At the end, should be one value (result) left.
        if len(values) != 1:
            return None
        return values[0]



# ============================================================
# 2) GUI ON TKINTER
#    - display
#    - buttons
#    - keyboard handling
#    - input rules at the UI level
# ============================================================
class CalculatorGUI:
    def __init__(self, master):
        self.master = master

        # Window settings
        self.master.title("Calculator")
        self.master.geometry("360x520")
        self.master.configure(bg="#E6F3FF")

        # Current expression that the user is typing
        self.expression = ""

        # Flag that the first symbol was an operator and we ignored it.
        # This is required for the "leading operator ignored" feature, and then show Error on "=".
        self.leading_operator_ignored = False

        # Error status:
        # if Error is received — block input until C is pressed
        self.error_state = False
        #self.leading_operator_ignored = False


        # -------------------
        # DISPLAY (input field)
        # -------------------
        self.display = tk.Entry(master, font=("Arial", 28), justify='right',
                                bg="white", fg="black", borderwidth=3, relief="solid",
                                highlightthickness=1, highlightbackground="#9E9E9E")
        self.display.grid(row=0, column=0, columnspan=5, padx=20, pady=20, sticky="nsew")
        self.display.insert(0, "0")

        # -------------------
        # Keyboard handling:
        # any key -> on_key_press()
        # -------------------
        self.master.bind('<Key>', self.on_key_press)

        # -------------------
        # List of buttons:
        # (text, row, column, text colour, background colour)
        # -------------------
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

        # Creating buttons in a loop
        for (text, row, col, fg, bg) in buttons:
            # "=" made high button (rowspan=2), others are standard
            row_span = 2 if text == '=' else 1

            btn = tk.Button(master, text=text, font=("Arial", 14, "bold"),
                            fg=fg, bg=bg, relief="solid", borderwidth=1,
                            # lambda t=text — records the current value of text
                            # else, all buttons would pass the last text from the list
                            command=lambda t=text: self.process_input(t))
            btn.grid(row=row, column=col, rowspan=row_span, padx=8, pady=8, sticky="nsew")

        # Grid stretching (adaptability)
        for i in range(5):
            master.grid_columnconfigure(i, weight=1, minsize=60)
        for i in range(1, 5):
            master.grid_rowconfigure(i, weight=1, minsize=60)

    # ============================================================
    # 2.1) Keyboard processing
    # ============================================================
    def on_key_press(self, event):
        """
        event.char:
            - regular keys return a character (e.g. "1", "+")
            - Enter, Backspace, Escape have special codes
        """
        key = event.char
        # Mapping special keys to "logical" calculator buttons
        mapping = {
            '\r': '=',      # Enter
            '\x08': '←',    # Backspace
            '\x1b': 'C',    # Escape
            ',': '.'        # Replacing a comma with a full stop
        }

        # If key is in mapping, we take the mapped symbol, else key
        char = mapping.get(key, key)

        # Check for valid characters (including * and /)
        allowed_chars = "0123456789+-*/.C=←"
        # If symbol is allowed, we process it the same way as pressing a button.
        if char in allowed_chars:
            self.process_input(char)

    # ============================================================
    # 2.2) Main input "controller"
    # ============================================================
    def process_input(self, char):
        """
        Accept one "symbol" (button or key) and updates:
            - self.expression
            - display
            - error_state / leading_operator_ignored states
        """
        if self.error_state and char != 'C':
            return
        # -------------------
        # C (Clear)
        # -------------------
        if char == 'C':
            self.expression = ""
            self.error_state = False
            self.leading_operator_ignored = False
            self.update_display("0")

        # -------------------
        # ← (Backspace)
        # -------------------
        elif char == '←':
            self.expression = self.expression[:-1]
            self.update_display(self.expression if self.expression else "0")

        # -------------------
        # = (Calculate)
        # -------------------
        elif char == '=':
            # If user start with operator (we ignored it),
            # and then didn't enter anything, but pressed "=" -> Error
            if not self.expression and self.leading_operator_ignored:
                self.update_display("Error")
                self.error_state = True
                self.leading_operator_ignored = False
                return

            # Calling clear logic
            result = CalculatorLogic.calculate(self.expression)
            self.update_display(result)

            # If Error — clear expression and block to C
            if result == "Error":
                self.expression = ""
                self.error_state = True
            else:
                # If successful, we allow you to continue counting "from the result."
                self.expression = str(result)

        # -------------------
        # Any other characters: numbers, full stop, operators
        # -------------------
        else:
            # LOGIC OF OPERATOR REPLACEMENT:
            #   1) The operator cannot be entered first: "+5" — ignore "+"
            #      but set the leading_operator_ignored flag
            #   2) If the operator comes after the operator — replace the last operator
            #      example: "5++5" -> "5+5"
            # -----
            if char in '+-*/':
                if not self.expression:
                    # operator at the beginning — do not add
                    self.leading_operator_ignored = True
                    return

                # if two operators in a row -> replace the previous one
                elif self.expression[-1] in '+-*/':
                    self.expression = self.expression[:-1] + char
                else:
                    self.expression += char
            else:
                # numbers / dot:
                # simply add the symbol
                self.expression += str(char)

                # if a number was entered after the ignored operator, we reset the flag
                self.leading_operator_ignored = False

            self.update_display(self.expression)


    # ============================================================
    # 2.3) Display refresh
    # ============================================================
    def update_display(self, value):
        self.display.delete(0, tk.END)
        self.display.insert(0, value)

# ============================================================
# 3) Entry point
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
