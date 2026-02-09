import tkinter as tk


def before_scenario(context, scenario):
    """
    Called BEFORE each Scenario.
        - Create tk_root for creating/working with GUI elements.
        - withdraw() hides the window for test.
    """
    context.tk_root = tk.Tk()
    context.tk_root.withdraw()


def after_scenario(context, scenario):
    """
        Called AFTER each Scenario.
            - Cleaning up Tkinter resources after the script
            - Avoiding memory leaks/freezes
            - For clean start every scenario

        The "hasattr" check is needed to avoid crashing if tk_root has not been created.
        """
    if hasattr(context, "tk_root") and context.tk_root:
        context.tk_root.destroy()
        context.tk_root = None
