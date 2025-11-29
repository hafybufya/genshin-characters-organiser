# ---------------------------------------------------------------------
# IMPORTED FUNCTIONS USED IN PROGRAM
# ---------------------------------------------------------------------

import csv
import tkinter as tk
from tkinter import *
from tkinter import ttk 
import pandas as pd
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # Used for the piechart
from matplotlib.figure import Figure # Also used for the figure creation

# ---------------------------------------------------------------------
# Defined colours used in program
#  -> make colour scheme easier to change
# -> currently Neuvillette's colour pallette
# ---------------------------------------------------------------------

colour_1 =  "#222437" 
colour_2 = "#7FB1CE"
colour_3= "#2c77d8"

# ---------------------------------------------------------------------
# CLASS: character data 
# ---------------------------------------------------------------------

class Character: # Character class to hold character data and create CSV
    characters = [] # Empty list to hold chars
    character_count = 0 # Counter for total number of characters
 
    def __init__(self, name, element, character_star, character_level, max_hp, base_ATK, elemental_skill, elemental_burst, region, weapon_owned):
        self.name = name
        self.element = element
        self.character_star = character_star
        self.character_level = character_level
        self.max_hp = max_hp
        self.base_ATK = base_ATK
        self.elemental_skill = elemental_skill
        self.elemental_burst = elemental_burst
        self.region = region
        self.weapon_owned = weapon_owned
        Character.characters.append(self) # New characaters appended to genshinOrganiser.csv

    @staticmethod 
    def make_characters_csv(): 
        """makes a CSV file called genshinCharacters.csv if one does not already exist in the cwd"""  
        if not os.path.exists('genshinCharacters.csv'):
            character_data = [{"Name": character.name, "Element": character.element, "Character Star": character.character_star,
                               "Character Level": character.character_level, "Max HP": character.max_hp, "Base ATK": character.base_ATK,
                               "Elemental Skill": character.elemental_skill, "Elemental Burst": character.elemental_burst,
                               "Region": character.region, "Weapon": character.weapon_owned} for character in Character.characters]
            character_table = pd.DataFrame(character_data) #convereted from a dictionairy to a pd data frame
            character_table.to_csv('genshinCharacters.csv') #then a pd data frame to  csv   
        return pd.read_csv('genshinCharacters.csv') #returns the resultant so it can be used if necessay    

# ---------------------------------------------------------------------
# CLASS: Window of genshin data
# ---------------------------------------------------------------------

# GenshinSorter class with treeview stuff yahhh baby

class GenshinSorter:
    def __init__(self, genshin_window):
        self.genshin_window = genshin_window 
        self.genshin_window.title("Genshin Organiser") 
        self.genshin_window.geometry("%dx%d+%d+%d" % (1300, 750, 100, 50)) # Width, height, xoffset, yoffset
        self.genshin_window.resizable(True, True) # Both width and height can be resized

        # --- Stylising tkinter window ---
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Allows more customisation
        self.style.configure("Treeview", 
                           background= colour_1,
                           foreground= colour_2,
                           fieldbackground = colour_1,
                           font=("Arial", 12, "bold") # This is the size of the treeview elements                    
                             )  
        self.style.map('Treeview',
                      background=[('selected', '#2852B3')]) # Changes the color of selected text to #2852B3 (blue)
                                #even hotter button stuff
        self.style.configure(
            "Custom.TButton", # Placing this style in all ttk buttons customises them like this 
            font=("Arial", 14, "bold"),
            foreground="#F6F8F9",  # Button text color
            background="#253365",  # Background button color
    )
        # --- Pages ---

        # All pages set as a frame to allow setting bg colour
        self.page1 = tk.Frame(self.genshin_window, bg = colour_2) 
        self.page2 = tk.Frame(self.genshin_window, bg = colour_2)
        self.page3 = tk.Frame(self.genshin_window, bg = colour_2)

        # --- Frame for all buttons ---
        self.frame_page_1buttons = ttk.Frame(self.page1) # Page 1 buttons
        self.frame_page_1buttons.pack(side=BOTTOM, pady = 15)
        self.frame_page_2buttons = ttk.Frame(self.page2) # Page 2 buttons
        self.frame_page_2buttons.pack(side=BOTTOM, pady = 15)
        self.frame_page_3buttons = ttk.Frame(self.page3) # Page 3 buttons
        self.frame_page_3buttons.pack(side=BOTTOM, pady = 15)

        # --- Using grids inside of a frame ---
        self.page1_to_page2 = ttk.Button(self.frame_page_1buttons, text="Show Page 2", command=lambda: self.show_page(self.page2),style= 'Custom.TButton')
        self.page1_to_page2.grid(row = 0, column = 0) 
        self.page1_to_page3 = ttk.Button(self.frame_page_1buttons, text="Show Page 3", command=lambda: self.show_page(self.page3),style= 'Custom.TButton')
        self.page1_to_page3.grid(row = 0, column = 1)

        self.page2_to_page3 = ttk.Button(self.frame_page_2buttons, text="Show Page 3", command=lambda: self.show_page(self.page3),style= 'Custom.TButton')
        self.page2_to_page3.grid(row = 0, column = 1)
        self.page2_to_page1 = ttk.Button(self.frame_page_2buttons, text="Show Page 1", command=lambda: self.show_page(self.page1),style= 'Custom.TButton')
        self.page2_to_page1.grid(row = 0, column = 0)

        self.page3_to_page2 = ttk.Button(self.frame_page_3buttons, text="Show Page 2", command=lambda: self.show_page(self.page2), style= 'Custom.TButton')
        self.page3_to_page2.grid(row = 0, column = 1)
        self.page3_to_page_1 = ttk.Button(self.frame_page_3buttons, text="Show Page 1", command=lambda: self.show_page(self.page1), style= 'Custom.TButton')
        self.page3_to_page_1.grid(row = 0, column = 0)

        # --- Title for pages 2 and 3 ---

        # --- Page 2 ---
        self.page2_title = tk.Label(self.page2, text="SORT CHARACTERS", bg=colour_2 , font=("Ariel",30, "bold"))
        self.page2_title.pack(side= TOP)
        self.page2_search= tk.Label(self.page2, text= "You can search for: Name, Element, Star, Region and Weapon ;)",font=("Ariel",14, "bold"), bg=colour_2)
        self.page2_search.pack(side=TOP)
        self.page2_advice= tk.Label(self.page2, text= "Press 'Search' with the search box empty to get all characters",font=("Ariel",14, "bold"), bg=colour_2)
        self.page2_advice.pack(side=TOP)

        # --- Page 3 ---
        self.page3_title = tk.Label(self.page3, text="EDIT CHARACTERS", font=("Ariel",30, "bold"), bg=colour_2)
        self.page3_title.pack(side= TOP)
        self.info_label= tk.Label(self.page3, text= "To view edits on page 2, close the window and reopen :D",font=("Ariel",14, "bold"), bg=colour_2)
        self.info_label.pack(side=TOP)

        # --- Placeholder error message for when boxes are empty for certain buttons ---
        self.error_label_2 = tk.Label(self.page2, text="", font=("Ariel",15, "bold"), bg=colour_2 , fg=colour_1 )
        self.error_label_2.pack(side=BOTTOM)

        self.error_label_3 = tk.Label(self.page3, text="", font=("Ariel",15, "bold"), bg=colour_2 , fg=colour_1 )
        self.error_label_3.pack(side=BOTTOM)

        # --- Frame for editting entry boxes ---
        self.frame_editting = tk.Frame(self.page3, bg=colour_2)
        self.frame_editting.pack(side=BOTTOM)
 
        self.name_label = Label(self.frame_editting, text="Name:", font=20, bg=colour_2 )#name box
        self.name_label.grid(row=0, column=0)
        self.name_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.name_entry.grid(row=1, column=0)
        
        self.element_label = Label(self.frame_editting, text="Element:", font=20, bg=colour_2)#element box
        self.element_label.grid(row=0, column=1)
        self.element_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.element_entry.grid(row=1, column=1)

        self.star_label = Label(self.frame_editting, text="Star:", font=20, bg=colour_2)#star box
        self.star_label.grid(row=0, column=2)
        self.star_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.star_entry.grid(row=1, column=2)

        self.level_label = Label(self.frame_editting, text="Level:", font=20, bg=colour_2)#level box
        self.level_label.grid(row=0, column=3)
        self.level_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.level_entry.grid(row=1, column=3)

        self.hp_label = Label(self.frame_editting, text="HP:", font=20, bg=colour_2)#HP box
        self.hp_label.grid(row=0, column=4)
        self.hp_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.hp_entry.grid(row=1, column=4)

        self.atk_label = Label(self.frame_editting, text="Base ATK:", font=20, bg=colour_2)#aTK box
        self.atk_label.grid(row=0, column=5)
        self.atk_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.atk_entry.grid(row=1, column=5)

        self.skill_label = Label(self.frame_editting, text="Skill:", font=20, bg=colour_2)#skill box
        self.skill_label.grid(row=0, column=6)
        self.skill_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.skill_entry.grid(row=1, column=6)

        self.burst_label = Label(self.frame_editting, text="Burst", font=20, bg=colour_2)#burst box
        self.burst_label.grid(row=0, column=7)
        self.burst_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.burst_entry.grid(row=1, column=7)

        self.region_label = Label(self.frame_editting, text="Region:", font=20, bg=colour_2)#region box
        self.region_label.grid(row=0, column=8)
        self.region_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.region_entry.grid(row=1, column=8)

        self.weapon_label = Label(self.frame_editting, text="Weapon", font=20, bg=colour_2) #weapon box
        self.weapon_label.grid(row=0, column=9)
        self.weapon_entry = Entry(self.frame_editting, font=20, width=10, bg=colour_3)
        self.weapon_entry.grid(row=1, column=9)

        #--- Frame for character edits buttons ---
        self.frame_buttons = ttk.Frame(self.page3)
        self.frame_buttons.pack(side=BOTTOM, pady = 20)
       
        #--- Delete button ---
        self.delete_button = ttk.Button(self.frame_buttons, text="Delete", command=self.delete_character, style= 'Custom.TButton')
        self.delete_button.grid(row= 0, column=3)

        #--- Add character button ---
        self.add_button = ttk.Button(self.frame_buttons, text="Add", command=self.add_character, style= 'Custom.TButton')
        self.add_button.grid(row =0, column = 2)

        #--- Select button ---
        self.select_button = ttk.Button(self.frame_buttons, text="Select record", command=self.select_character, style= 'Custom.TButton')
        self.select_button.grid(row = 0 , column = 0)

        #--- Clear button ---
        self.clear_button = ttk.Button(self.frame_buttons, text="Clear Boxes", command=self.clear_boxes, style= 'Custom.TButton')
        self.clear_button.grid(row = 0 , column = 1) 

        #--- Update button ---
        self.update_button = ttk.Button(self.frame_buttons, text="Update record", command=self.update_character, style= 'Custom.TButton')
        self.update_button.grid(row = 0, column = 4)
        
        #--- Search button ---
        self.search_button = ttk.Button(self.page2, text="Search", command=self.search_character, style= 'Custom.TButton')
        self.search_button.pack(side=BOTTOM)
       
        #--- Search button entry box ---
        self.search_entry = Entry(self.page2, width=35, bg=colour_3, font=18)
        self.search_entry.pack(side=BOTTOM)

        #--- Interactive page 2 elements---

        #--- Sort button ---
        self.sort_button = ttk.Button(self.page2, width=20, text="Sort", command=self.sort_characters, style= 'Custom.TButton')
        self.sort_button.pack(side=TOP , anchor =E) 

         #--- Drop down menu ---
        self.option = StringVar(self.page2)

        #--- Dropdown menu options ---
        self.dropdown_choices = ["--", "Name", "Level",'HP', "ATK"]
        self.option.set(self.dropdown_choices[0]) # Automatically on "--"
        self.dropdown = OptionMenu(self.page2, self.option, *self.dropdown_choices)
        self.dropdown.pack(side=TOP ,anchor = W) # Anchored top left 
        self.dropdown.config(width = 8)
        
        #--- Add treeview for both pages ---
        # Different treeviews for each pages makes it easier -> serve different purposes

        #--- Treeview here for searching and sorting ---
        self.tree_page2=self.add_treeview(self.page2)

        #--- Treeview here for editting csv file ---
        self.tree_page3= self.add_treeview(self.page3)

    # ---------------------------------------------------------------------
    # FUNCTION: Add treeview 
    # ---------------------------------------------------------------------

    def add_treeview(self, page):
        """Add the Treeview to a given page in this case only 2 and 3"""
        
        TableMargin = Frame(page, width=500)
        TableMargin.pack(side=TOP)

        # Column definitions
        columns = [
            ("Name", 90),
            ("Element", 70),
            ("Character Star", 50),
            ("Character Level", 50),
            ("Max HP", 60),
            ("Base ATK", 70),
            ("Elemental Skill", 150),
            ("Elemental Burst", 200),
            ("Region", 100),
            ("Weapon", 75),
        ]

        # Extract only names for the treeview config
        column_names = [c[0] for c in columns]


        self.tree = ttk.Treeview(
            TableMargin,
            columns=("Name", "Element", "Character Star", "Character Level", "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst", "Region", "Weapon"),
            height=400,
            selectmode="extended",
        )

        # --- Load CSV rows ---
        with open("genshinCharacters.csv") as f:
            # Rows passed as a tuple into values which will populate the treeview
            for row in csv.DictReader(f):
                self.tree.insert("", "end", values=[row[col] for col in column_names])

        # --- Configure headings and column widths in one loop ---
        self.tree.column("#0", width=0, stretch=NO)  # Ghost column
        for i, (name, width) in enumerate(columns, start=1):
            self.tree.heading(name, text=name.split()[-1] if name != "Name" else "Name", anchor="c")
            self.tree.column(f"#{i}", width=width, stretch=NO, anchor="c")

        self.tree.pack() 
        return self.tree

    def show_page(self, page):
        """Show a specific page this is the function thats used to change pages connected to switch page buttons"""
        #hide all pages
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack_forget()
        #packs the selected page to fill the whole window
        page.pack(fill="both", expand=True)

    # ---------------------------------------------------------------------
    # FUNCTION: Update character data
    # ---------------------------------------------------------------------

    def update_character(self):
        """Connected to the update button and it pastes the data user has selected so it can be updated"""  
      
       # --- List of character trait lists ---
        character_traits = [
        self.name_entry, self.element_entry, self.star_entry, self.level_entry,
        self.hp_entry, self.atk_entry, self.skill_entry, self.burst_entry,
        self.region_entry, self.weapon_entry
    ] 
        # --- List of numeric character trait lists ---
        numeric_traits = [self.star_entry, self.level_entry, self.hp_entry, self.atk_entry]
        
        # --- Validate empty fields --- 
        if any(not trait.get() for trait in character_traits):

            #If any field is empty, show an error message and return
            self.error_label_3.config(text="Please fill all fields!!.")
            self.page3.after(3000, lambda: self.error_label_3.config(text=""))
            return # Stop the function from running

        # --- Validate numeric fields ---
        if any(not trait.get().isdigit() for trait in numeric_traits):
            self.error_label_3.config(text="'Star', 'Level', 'Max HP' and 'Base ATK' should all be numbers.")
            # Error shown for only 4 seconds before dissappearing as text is reset to nothing
            self.page3.after(4000, lambda: self.error_label_3.config(text="")) 
            return  # Stop the function from running

        # --- Update the selected row ---
        selected = self.tree.focus() # Focus is what the mouse has touched and is illuminated
        self.tree.item(selected, text="", values=(self.name_entry.get(), self.element_entry.get(), self.star_entry.get(), self.level_entry.get(), self.hp_entry.get(), self.atk_entry.get(), self.skill_entry.get(), self.burst_entry.get(), self.region_entry.get(), self.weapon_entry.get()))

        values = [traits.get() for traits in character_traits]
        self.tree.item(selected, text="", values=values)

        # --- Clear the entry boxes ---
        for traits in character_traits:
           traits.delete(0, END)

        # --- Extract all rows from treeview in one loop ---
        headings = ["Name", "Element", "Character Star", "Character Level",
                    "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst",
                    "Region", "Weapon"]
            
        # --- Dictionary built using list comprehensions ---
        full_treeview_data_dict = {
            headings[i]: [self.tree.item(child)["values"][i] for child in self.tree.get_children()]
            for i in range(len(headings))
        }

        # --- Save to CSV ---
        treeview_df = pd.DataFrame.from_dict(full_treeview_data_dict)
        treeview_df.to_csv("genshinCharacters.csv", index = False)
  
        # --- Success message ---
        self.error_label_3.config(text="RECORD UPDATED.")
        self.page3.after(3000, lambda: self.error_label_3.config(text=""))

    # ---------------------------------------------------------------------
    # FUNCTION: Delete character data
    # ---------------------------------------------------------------------

    def delete_character(self):
        
        self.tree.delete(self.tree.selection()[0])
        # --- Extract all rows from treeview in one loop ---
        headings = ["Name", "Element", "Character Star", "Character Level",
                    "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst",
                    "Region", "Weapon"]
        
        # --- Dictionary built using list comprehensions ---
        full_treeview_data_dict = {
            headings[i]: [self.tree.item(child)["values"][i] for child in self.tree.get_children()]
            for i in range(len(headings))
        }
     
        # --- Save to CSV ---
        treeview_df = pd.DataFrame.from_dict(full_treeview_data_dict)
        treeview_df.to_csv("genshinCharacters.csv", index = False)

        # --- Feedback message ---
        self.error_label_3.config(text="CHARACTER DELETED")
        # Error shown for only 3 seconds before dissappearing as text is reset to nothing 
        self.page3.after(3000, lambda: self.error_label_3.config(text=""))

    # ---------------------------------------------------------------------
    # FUNCTION: Sort character data
    # ---------------------------------------------------------------------

    def sort_characters(self):
        
        # --- Extract all rows from treeview in one loop ---
        headings = ["Name", "Element", "Character Star", "Character Level",
                    "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst",
                    "Region", "Weapon"]
        
        # --- Dictionary built using list comprehensions ---
        full_treeview_data_dict = {
            headings[i]: [self.tree.item(child)["values"][i] for child in self.tree.get_children()]
            for i in range(len(headings))
        }

       # --- Create DataFrame ---
        treeview_df = pd.DataFrame.from_dict(full_treeview_data_dict)

        unsorted_characters = treeview_df
        
        sorted_characters = unsorted_characters  # Default to unsorted if no option is selected
       
       # --- Applies sorting ---  
        if self.option.get() == "--": # Default
            sorted_characters = unsorted_characters  # No sorting if the default option is selected
        if self.option.get() == "Name":
            sorted_characters = unsorted_characters.sort_values(by=["Name"], ascending=True)
        elif self.option.get() == "Level":
            sorted_characters = unsorted_characters.sort_values(by=["Character Level"], ascending=False)
        elif self.option.get() == "HP":
            sorted_characters = unsorted_characters.sort_values(by=["Max HP"], ascending=False)
        elif self.option.get() == "ATK":
            sorted_characters = unsorted_characters.sort_values(by=["Base ATK"], ascending=False)
     
        # --- Refill the treeview with sorted data ---  
        for row in self.tree_page2.get_children(): # Empties the treeview 
            self.tree_page2.delete(row)
        for _, row in sorted_characters.iterrows():
            self.tree_page2.insert("", "end", values=[row[col] for col in headings])

    # ---------------------------------------------------------------------
    # FUNCTION: Clear boxes
    # ---------------------------------------------------------------------

    def clear_boxes(self):
        # --- Lists all entry box data --- 
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry, self.burst_entry,self.region_entry, self.weapon_entry )
         # --- Deletes all entry box data --- 
        for options in tree_entryboxes:
            options.delete(0, END)

    # ---------------------------------------------------------------------
    # FUNCTION: Search character data
    # ---------------------------------------------------------------------

    def search_character(self):

        # --- Clears current rows in the treeview --- 
        for row in self.tree_page2.get_children():
            self.tree_page2.delete(row)
            found= False # Defined outside the loop 

        # --- Get the search query and converts to lowercase ---
        query = self.search_entry.get().lower()

        # --- Treeview columns ---
        columns = [
            "Name", "Element", "Character Star", "Character Level",
            "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst",
            "Region", "Weapon"
        ]

        # --- Searchable columns ---
        searchable = ["Name", "Element", "Character Star", "Region", "Weapon"]

        # --- Reads the CSV and filters rows based on the query ---
        with open('genshinCharacters.csv') as characters:  # Opens character.csv file
            character_selected = csv.DictReader(characters, delimiter=',')
          
            # --- Checks if the query matches in certain rows and then appends to empty treeview ---
            for row in character_selected: 
                
                # --- Check if query matches ANY searchable column ---
                if any(query in row[col].lower() for col in searchable):
                    self.tree_page2.insert("", 0, values=[row[c] for c in columns])
                    found=True # Set found as true if query found

            # --- No match ---
            if not found:
               self.error_label_2.config(text="DOES NOT EXIST.")
               self.page2.after(3000, lambda: self.error_label_2.config(text=""))

    # ---------------------------------------------------------------------
    # FUNCTION: Select character data
    # ---------------------------------------------------------------------

    def select_character(self):
       # --- Lists all entry box data --- 
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry,self.region_entry, self.weapon_entry )
      
        # --- Deletes all entry box data --- 
        for options in tree_entryboxes:
            options.delete(0, END)

        # --- Get selected row --- 
        selected = self.tree.focus() # Focus = whats currently pressed on
        values = self.tree.item(selected, "values") # Grabs values associated with record

        # --- Fill entry boxes using a loop ---
        for entry, value in zip(tree_entryboxes, values):
            entry.insert(0, value)

    # ---------------------------------------------------------------------
    # FUNCTION: Add character data
    # ---------------------------------------------------------------------

    def add_character(self):

        # --- Lists all entry box data --- 
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry,self.region_entry, self.weapon_entry )
        
        # --- Lists all numeric entry box data --- 
        numeric_traits = [self.star_entry, self.level_entry, self.hp_entry, self.atk_entry]
        
        values = [tree_entrybox.get() for tree_entrybox in tree_entryboxes]

        # --- Validation to ensure all fields are filled ---
        if any(v == "" for v in values): # Check if all fields are filled 
            self.error_label_3.config(text="Please fill all fields!!.") #If any field is empty, show an error message and return
            self.page3.after(3000, lambda: self.error_label_3.config(text=""))  # Error shown for only 3 seconds before dissappearing as text is reset to nothing
            return  # Stop the function from running 

        # --- Validation to ensure numeric fields are numeric ---
        numeric_values = [entry.get() for entry in numeric_traits]
        if any(not nv.isdigit() for nv in numeric_values):
            self.error_label_3.config(text="'Star', 'Level' , 'Max HP' and 'Base ATK' should all be numbers.") 
            self.page3.after(3000, lambda: self.error_label_3.config(text="")) # Error shown for only 3 seconds before dissappearing as text is reset to nothing
            return   #Stop the function from running
        
        self.tree.insert("", "end", values=values)
    
        # --- Deletes all entry box data --- 
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry,  self.burst_entry,self.region_entry, self.weapon_entry )
        for options in tree_entryboxes:
            options.delete(0, END)

        # --- Export updated CSV ---
        all_rows = [self.tree.item(child)["values"] for child in self.tree.get_children()]
        treeview_df = pd.DataFrame(all_rows, columns=[
            "Name", "Element", "Character Star", "Character Level",
            "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst",
            "Region", "Weapon"
        ])
        treeview_df.to_csv("genshinCharacters.csv", index = False)

        # --- Sucess message ---
        self.error_label_3.config(text="CHARACTER ADDED")
        self.page3.after(3000, lambda: self.error_label_3.config(text="")) #error shown for only 3 secondsssss before dissappearing as text is reset to nothing


# ---------------------------------------------------------------------
# CLASS: First page of program
# ---------------------------------------------------------------------

class IntroPage(GenshinSorter): # Inheritance
    def __init__(self, genshin_window):
        super().__init__(genshin_window)
        # --- Title and label of page 1 ---
        self.page1_title = tk.Label(self.page1, text="HAFSA'S GENSHIN ORGANISER", font=('Arial', 30, "bold"),bg=colour_2)
        self.page1_title.pack(side= TOP, pady=20, expand=True)
        self.theme_label = tk.Label(self.page1, text="Current Theme: Neuvillette", font=('Arial', 16),bg=colour_2)
        self.theme_label.pack(side= BOTTOM, pady=20, expand=True)

        # --- Character count label ---
        self.character_count_label = tk.Label(self.page1, text= f"TOTAL CHARACTER COUNT: {Character.character_count}" , font=('Arial', 15, "bold"), bg=colour_2) 
        self.character_count_label.pack(pady=20)
        
        # --- Plot for elements on the homepage ---
        character_df =Character.make_characters_csv() 

        # --- Element counts checks the number of times something comes up in the csv ---
        element_counts = character_df['Element'].value_counts() 
        element_index = element_counts.index.tolist()  # Converts both to a list
        element_count = element_counts.values.tolist() 

        # --- Puts the graph on page 1 ---
        frameChart = tk.Frame(self.page1) 
        frameChart.pack()

        # --- Creates the matplotlib figure and axes ---
        fig = Figure(figsize=(4,4))  # Sets the figure size
        ax = fig.add_subplot(111)  # Add a subplot

        # --- Set the background of the figure to colour 2 ---
        fig.patch.set_facecolor(colour_2) 
        
        # --- Plots the pie chart ---
        ax.pie(element_count, labels=element_index, autopct='%0.0f%%', startangle=180)
        element_chart = FigureCanvasTkAgg(fig, frameChart)# Embeds the figure into tkinter 
        element_chart.get_tk_widget().pack(anchor="center") 


if __name__ == "__main__":

    # --- Creates CSV if genshinCharacaters.csv doesnt exist ---
    characters = [ 
        Character("Traveller", "Anemo", 4,1, 911, 17, "Gale Blade", "Dandelion Breeze", "Mondstadt", "Sword"),
        Character("Kaeya", "Cyro", 4, 1,975, 18, "Frostgnaw", "Glacial Waltz", "Mondstadt", "Sword"),
        Character("Amber", "Pyro", 4, 1, 793, 18, "Explosive Puppet", "Fiery Rain", "Mondstadt", "Bow"),
        Character("Neuvillette", "Hydro", 5, 1, 900, 20, "O Tears, I Shall Repay", "O Tides, I Have Returned", "Fontaine", "Catalyst")
    ]

    # --- If no character csv exists --
    Character.make_characters_csv() 
    # --- Calculating the length of the csv file to see the total character count --
    Character.character_count = len(pd.read_csv('genshinCharacters.csv')) 
 
    # --- Main app --    
    genshin_window = tk.Tk() 
    # --- Shows the first page initially -- 
    intro_page = IntroPage(genshin_window)  
    # --- Runs the application -- 
    intro_page.show_page(intro_page.page1) 
    genshin_window.mainloop()

