import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Hardcoded exchange rates with symbols (base USD)
exchange_rates = {
    'USD': {'rate': 1.0, 'symbol': '$'},
    'EUR': {'rate': 0.85, 'symbol': '€'},
    'GBP': {'rate': 0.73, 'symbol': '£'},
    'JPY': {'rate': 110.0, 'symbol': '¥'},
    'CAD': {'rate': 1.25, 'symbol': 'C$'},
    'INR': {'rate': 83.5, 'symbol': '₹'},
    'AUD': {'rate': 1.52, 'symbol': 'A$'}
}

def convert_currency(event=None):
    print("DEBUG: Convert button clicked or Enter pressed")
    try:
        amount_str = amount_entry.get().strip()
        for char in ['$', '€', '£', '₹', ',', 'C$', 'A$']:
            amount_str = amount_str.replace(char, '')
            
        if not amount_str:
            result_label.config(text="Enter an amount", fg="#ff6b6b")
            rate_label.config(text="")
            return
            
        amount = float(amount_str)
        from_curr = from_var.get()
        to_curr = to_var.get()

        # Calculation
        amount_in_usd = amount / exchange_rates[from_curr]['rate']
        converted = amount_in_usd * exchange_rates[to_curr]['rate']

        from_sym = exchange_rates[from_curr]['symbol']
        to_sym = exchange_rates[to_curr]['symbol']

        result_text = f"{from_sym}{amount:,.2f} = {to_sym}{converted:,.2f}"
        print(f"DEBUG: Result -> {result_text}")
        
        # Update UI
        result_label.config(text=result_text, fg="#00ff99")
        
        single_rate = (1 / exchange_rates[from_curr]['rate']) * exchange_rates[to_curr]['rate']
        rate_label.config(text=f"1 {from_curr} = {single_rate:.4f} {to_curr}")
        
        root.update_idletasks()

    except Exception as e:
        print(f"DEBUG: Error -> {e}")
        result_label.config(text="Invalid Input", fg="#ff6b6b")
        rate_label.config(text="")

def swap_currencies():
    f, t = from_var.get(), to_var.get()
    from_var.set(t)
    to_var.set(f)
    print(f"DEBUG: Swapped to {t} -> {f}")
    convert_currency()

# --- THEME ---
DARK_BG = "#0f0f17"
CARD_BG = "#181825"
TEXT_FG = "#cdd6f4"
ACCENT = "#cba6f7"
INPUT_BG = "#313244"

root = tk.Tk()
root.title("Currency Pro")
root.geometry("450x580")
root.configure(bg=DARK_BG)

# Initialize Variables Early
from_var = tk.StringVar(value="USD")
to_var = tk.StringVar(value="INR")

style = ttk.Style()
style.theme_use('clam')
style.configure("Card.TFrame", background=CARD_BG)
style.configure("TLabel", background=CARD_BG, foreground=TEXT_FG, font=("Segoe UI", 10))
style.configure("Title.TLabel", font=("Segoe UI", 20, "bold"), foreground=ACCENT)

# Main App Container
container = ttk.Frame(root, padding=25, style="Card.TFrame")
container.place(relx=0.5, rely=0.5, anchor="center", width=400, height=520)

# 1. ICON
try:
    icon_path = r"C:\Users\ashwi\.gemini\antigravity\brain\18955bc7-af7c-4ed7-8abc-75c43701febc\currency_icon_modern_1778838948552.png"
    img = Image.open(icon_path)
    img = img.resize((110, 110), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(img)
    icon_lbl = tk.Label(container, image=icon_photo, bg=CARD_BG)
    icon_lbl.image = icon_photo
    icon_lbl.pack(pady=(5, 5))
except Exception as e:
    pass

# 2. HEADER
ttk.Label(container, text="Exchange Pro", style="Title.TLabel").pack()
ttk.Label(container, text="Precise Global Conversions", font=("Segoe UI", 10), foreground="#7f849c").pack(pady=(0, 15))

# 3. INPUT CARD
input_card = tk.Frame(container, bg=INPUT_BG, padx=20, pady=15)
input_card.pack(fill="x", pady=10)

ttk.Label(input_card, text="AMOUNT TO CONVERT", background=INPUT_BG, font=("Segoe UI", 8, "bold"), foreground=ACCENT).pack(anchor="w")
amount_entry = tk.Entry(input_card, bg=INPUT_BG, fg="white", insertbackground=ACCENT, 
                        font=("Segoe UI", 22, "bold"), border=0, justify="center")
amount_entry.pack(fill="x", pady=5)
amount_entry.insert(0, "100")
amount_entry.focus()

# 4. SELECTORS
select_frame = tk.Frame(container, bg=CARD_BG)
select_frame.pack(fill="x", pady=15)

currency_list = list(exchange_rates.keys())

from_cb = ttk.Combobox(select_frame, textvariable=from_var, values=currency_list, state="readonly", width=10, font=("Segoe UI", 12))
from_cb.grid(row=0, column=0)

swap_btn = tk.Button(select_frame, text="⇌", command=swap_currencies, bg=ACCENT, fg=DARK_BG, 
                     font=("Segoe UI", 16, "bold"), border=0, cursor="hand2", padx=12, activebackground="#b4befe")
swap_btn.grid(row=0, column=1, padx=10)

to_cb = ttk.Combobox(select_frame, textvariable=to_var, values=currency_list, state="readonly", width=10, font=("Segoe UI", 12))
to_cb.grid(row=0, column=2)

select_frame.columnconfigure(0, weight=1)
select_frame.columnconfigure(2, weight=1)

# 5. BUTTON (Switched back to tk.Button for more reliable event handling)
convert_btn = tk.Button(container, text="Convert Now", command=convert_currency, bg=ACCENT, fg=DARK_BG,
                       font=("Segoe UI", 12, "bold"), pady=12, border=0, cursor="hand2", activebackground="#b4befe")
convert_btn.pack(fill="x", pady=15)

# 6. RESULTS
result_label = tk.Label(container, text="", font=("Segoe UI", 20, "bold"), 
                        background=CARD_BG, fg="#00ff99", wraplength=350, justify="center")
result_label.pack(pady=(10, 0))

rate_label = tk.Label(container, text="", font=("Segoe UI", 10), 
                      foreground="#9399b2", background=CARD_BG)
rate_label.pack(pady=(2, 10))

# Run initial conversion
convert_currency()

root.bind('<Return>', convert_currency)
root.mainloop()
