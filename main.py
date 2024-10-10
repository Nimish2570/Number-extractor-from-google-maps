import tkinter as tk
from tkinter import messagebox
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import time
import re

# Define hacker-like colors
BG_COLOR = "#000000"  # black
FG_COLOR = "#00FF00"  # green
ENTRY_BG = "#222222"  # dark gray
ENTRY_FG = "#00FF00"  # green
BUTTON_BG = "#111111"  # darker gray
BUTTON_FG = "#00FF00"  # green
DANGER_COLOR = "#FF0000"  # red

def display_search_box():
    search_frame = tk.Frame(root, bg=BG_COLOR)
    search_frame.pack(pady=20)

    # Search Keyword Label and Entry
    search_label = tk.Label(search_frame, text="Enter Search Keyword:", bg=BG_COLOR, fg=FG_COLOR, font=("Courier", 12))
    search_label.pack(pady=5)

    global search_entry
    search_entry = tk.Entry(search_frame, bg=ENTRY_BG, fg=ENTRY_FG, font=("Courier", 12))
    search_entry.pack(pady=5)

    # Minimum Number of Results Label and Entry
    min_results_label = tk.Label(search_frame, text="Minimum Number of Results:", bg=BG_COLOR, fg=FG_COLOR, font=("Courier", 12))
    min_results_label.pack(pady=5)

    global min_results_entry
    min_results_entry = tk.Entry(search_frame, bg=ENTRY_BG, fg=ENTRY_FG, font=("Courier", 12))
    min_results_entry.pack(pady=5)

    # Generate CSV Button
    generate_button = tk.Button(search_frame, text="Generate CSV", command=generate_csv, bg=BUTTON_BG, fg=BUTTON_FG, font=("Courier", 12))
    generate_button.pack(pady=10)

def generate_csv():
    search_keyword = search_entry.get()
    num_results = int(min_results_entry.get())

    if num_results < 1:
        messagebox.showerror("Invalid Input", "Minimum number of results should be at least 1")
        return
    if len(search_keyword) == 0:
        messagebox.showerror("Invalid Input", "Search keyword cannot be empty")
        return
    if num_results > 500:
        messagebox.showerror("Invalid Input", "Maximum number of results is 500")
        return

    def checkPhone(phone):
        # remove blank spaces
        pattern = r'^[0-9\s]+$'
        # Use re.match() to check if the input string matches the pattern
        return bool(re.match(pattern, phone))

    def format_phone(phone):
        phone = phone.replace(' ', '')
        while phone.startswith('0'):
            phone = phone[1:]
        return phone

    def run(playwright, search_keyword, num_results):
        # Launch the browser
        browser = playwright.chromium.launch(headless=False)
        # Open a new browser page
        page = browser.new_page()
        # Navigate to Google Maps
        page.goto("https://www.google.com/maps")

        # Wait for the page to fully load
        page.wait_for_load_state("networkidle")

        # Wait for the search box to be available using id 'searchboxinput'
        search_box = page.wait_for_selector("#searchboxinput", timeout=10000)
        
        if search_box:
            # Fill the search box and submit
            search_box.fill(search_keyword)
            search_box.press("Enter")
        else:
            print("Search box not found")
            browser.close()
            return []

        # Wait for search results to load
        time.sleep(3)
        
        # Click on the first result's div if it's loaded
        div = page.query_selector(".L1xEbb")
        if div:
            div.click()
        else:
            print("First result div not found")
        
        # Scroll to load more results
        for _ in range(num_results // 2):  # Assuming each scroll loads 10 results
            page.keyboard.press("PageDown")
            time.sleep(1)

        results = []
        divs = page.query_selector_all('div.Nv2PK')

        for div in divs:
            if num_results == -1:
                break
            div.click()
            time.sleep(1)
            popup_content = page.content()
            popup_soup = BeautifulSoup(popup_content, 'html.parser')
            name_tag = popup_soup.find('h1', class_='DUwDvf lfPIob')
            info_tags = page.query_selector_all('div.Io6YTe')

            name = name_tag.get_text() if name_tag else 'No name found'
            phone = 'No phone number found'

            for info_tag in info_tags:
                if checkPhone(info_tag.inner_text()):
                    phone = info_tag.inner_text()
                    num_results -= 1
                    break
            if checkPhone(phone):
                phone = format_phone(phone)
                results.append({'Phone': phone, 'Name': name})

        browser.close()
        return results

    with sync_playwright() as playwright:
        results = run(playwright, search_keyword, num_results)

    # Clean search keyword to use it in the file name
    filename = re.sub(r'\W+', '', search_keyword)  # Remove non-alphanumeric characters
    # Write data to CSV file, including the search keyword in the file name
    with open(f'{filename}_search_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Phone', 'Name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()  # Write header
        for result in results:
            writer.writerow(result)
    
    messagebox.showinfo("CSV Generated", "The CSV file has been generated successfully.")

# Create the main window
root = tk.Tk()
root.title("WhatsApp Bot")
root.geometry("900x600")  
root.config(bg=BG_COLOR)

# Display search box directly
display_search_box()

# Run the Tkinter event loop
root.mainloop()
