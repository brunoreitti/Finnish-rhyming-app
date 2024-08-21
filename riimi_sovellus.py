import tkinter as tk
from tkinter import font

# Ladataan sanat tiedostosta
with open('C:\\Users\\bruno\\Desktop\\kaikkisanat.txt', 'r', encoding='utf-8') as file:
    suomen_sanat = [line.strip().lower() for line in file.readlines()]

def find_matching_words(input_word):
    input_word = input_word.lower()
    matching_words = []
    
    for sana in suomen_sanat:
        match_length = 0
        # Tutkitaan loppuosa ja kuinka monta kirjainta täsmää alkuosaan nähden
        for i in range(1, len(input_word) + 1):
            if sana.endswith(input_word[-i:]):
                match_length = i
            else:
                break
        
        if match_length > 0:
            matching_words.append((match_length, sana))
    
    # Järjestetään sanat täsmäävän pituuden mukaan, laskevassa järjestyksessä
    matching_words.sort(reverse=True, key=lambda x: x[0])
    
    return matching_words

def on_text_change(event):
    input_text = text_input.get("1.0", tk.END).strip()
    matching_words = find_matching_words(input_text)
    text_output.config(state=tk.NORMAL)
    text_output.delete("1.0", tk.END)
    
    # Insert words with color coding based on match length
    for match_length, sana in matching_words:
        if match_length == len(input_text):
            color_tag = "exact_match"
        elif match_length > len(input_text) * 0.75:
            color_tag = "high_match"
        elif match_length > len(input_text) * 0.5:
            color_tag = "medium_match"
        else:
            color_tag = "low_match"
        
        text_output.insert(tk.END, sana + "\n", color_tag)
    
    text_output.config(state=tk.DISABLED)

# Luodaan pääikkuna
root = tk.Tk()
root.title("Suomen Sanasto Rimausjärjestelmä")

# Tekstikenttä käyttäjän syötteelle
text_input = tk.Text(root, height=5, width=50)
text_input.pack(pady=10)

# Frame to hold the text_output and scrollbar
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

# Lukukenttä tuloksille
text_output = tk.Text(output_frame, height=20, width=50)
text_output.pack(side=tk.LEFT)

# Scrollbar for the text_output
scrollbar = tk.Scrollbar(output_frame, command=text_output.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the text_output to use the scrollbar
text_output.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

# Define color tags
text_output.tag_configure("exact_match", foreground="green")
text_output.tag_configure("high_match", foreground="yellowgreen")
text_output.tag_configure("medium_match", foreground="orange")
text_output.tag_configure("low_match", foreground="red")

# Sitotaan syötekentän muutostapahtuma
text_input.bind("<KeyRelease>", on_text_change)

# Käynnistetään GUI
root.mainloop()
