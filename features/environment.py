import tkinter as tk


def before_scenario(context, scenario):
    context.tk_root = tk.Tk()
    context.tk_root.withdraw()


def after_scenario(context, scenario):
    if hasattr(context, "tk_root") and context.tk_root:
        context.tk_root.destroy()
        context.tk_root = None
