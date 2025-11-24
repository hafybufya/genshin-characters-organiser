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

        #Stylising tkinter window
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Allows more customisation
        self.style.configure("Treeview",  # Neuvillette's colour pallette from Genshin
                           background= colour_1,
                           foreground= colour_2,
                           fieldbackground = colour_1,
                           font=("Arial", 12, "bold") # This is the size of the treeview elements                    
                             )  
        self.style.map('Treeview',
                      background=[('selected', '#2852B3')]) # Changes the color of selected text to #2852B3 (blue)
                                #even hotter button stuff
        self.style.configure(
            "Custom.TButton", #placing this style in all ttk buttons customises them like this 
            font=("Arial", 14, "bold"),
            foreground="#F6F8F9",  #button text color
            background="#253365",  #background button color
    )
        # Pages stuff #all pages set as a frame so i could then set a color because i couldnt change the color of the window since it would keep following my evil mac settings
        self.page1 = tk.Frame(self.genshin_window, bg = colour_2) 
        self.page2 = tk.Frame(self.genshin_window, bg = colour_2)
        self.page3 = tk.Frame(self.genshin_window, bg = colour_2)

        self.frame_page_1buttons = ttk.Frame(self.page1) #frame for my page 1 buttons
        self.frame_page_1buttons.pack(side=BOTTOM, pady = 15)
        self.frame_page_2buttons = ttk.Frame(self.page2) #frame for my page 2 buttons
        self.frame_page_2buttons.pack(side=BOTTOM, pady = 15)
        self.frame_page_3buttons = ttk.Frame(self.page3) #frame for my page tres buttons
        self.frame_page_3buttons.pack(side=BOTTOM, pady = 15)

        #using grids inside of a frame thats been packed is my fave cheeky thing
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

        #TITLES FOR PAGE 2 AND 3
        self.page2_title = tk.Label(self.page2, text="SORT CHARACTERS", bg=colour_2 , font=("Ariel",30, "bold"))
        self.page2_title.pack(side= TOP)
        self.page2_search= tk.Label(self.page2, text= "You can search for: Name, Element, Star, Region and Weapon ;)",font=("Ariel",14, "bold"), bg=colour_2)
        self.page2_search.pack(side=TOP)
        self.page2_advice= tk.Label(self.page2, text= "Press 'Search' with the search box empty to get all characters",font=("Ariel",14, "bold"), bg=colour_2)
        self.page2_advice.pack(side=TOP)

        self.page3_title = tk.Label(self.page3, text="EDIT CHARACTERS", font=("Ariel",30, "bold"), bg=colour_2)
        self.page3_title.pack(side= TOP)
        self.info_label= tk.Label(self.page3, text= "To view edits on page 2, close the window and reopen :D",font=("Ariel",14, "bold"), bg=colour_2)
        self.info_label.pack(side=TOP)

        #This is a place holder ish error message for when boxes are empty for certain buttons
        self.error_label_2 = tk.Label(self.page2, text="", font=("Ariel",15, "bold"), bg=colour_2 , fg=colour_1 )
        self.error_label_2.pack(side=BOTTOM)

        self.error_label_3 = tk.Label(self.page3, text="", font=("Ariel",15, "bold"), bg=colour_2 , fg=colour_1 )
        self.error_label_3.pack(side=BOTTOM)

        #frame for editting entry boxes
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

        #cutsey frame for character edits button stuff yurrr
        self.frame_buttons = ttk.Frame(self.page3)
        self.frame_buttons.pack(side=BOTTOM, pady = 20)
       
        self.delete_button = ttk.Button(self.frame_buttons, text="Delete", command=self.delete_character, style= 'Custom.TButton')
        self.delete_button.grid(row= 0, column=3)#delete button

        self.add_button = ttk.Button(self.frame_buttons, text="Add", command=self.add_character, style= 'Custom.TButton')
        self.add_button.grid(row =0, column = 2)#add character button

        self.select_button = ttk.Button(self.frame_buttons, text="Select record", command=self.select_character, style= 'Custom.TButton')
        self.select_button.grid(row = 0 , column = 0)#select button

        self.clear_button = ttk.Button(self.frame_buttons, text="Clear Boxes", command=self.clear_boxes, style= 'Custom.TButton')
        self.clear_button.grid(row = 0 , column = 1) #clear button

        self.update_button = ttk.Button(self.frame_buttons, text="Update record", command=self.update_character, style= 'Custom.TButton')
        self.update_button.grid(row = 0, column = 4)# update button
        
        self.search_button = ttk.Button(self.page2, text="Search", command=self.search_character, style= 'Custom.TButton')
        self.search_button.pack(side=BOTTOM)#search button 
       
        self.search_entry = Entry(self.page2, width=35, bg=colour_3, font=18)
        self.search_entry.pack(side=BOTTOM) #search button entry box yurrr

        #INTERACTIVE PAGE 2 TINGS
        self.sort_button = ttk.Button(self.page2, width=20, text="Sort", command=self.sort_characters, style= 'Custom.TButton')
        self.sort_button.pack(side=TOP , anchor =E)  #sort button

        #dropdown menu
        self.option = StringVar(self.page2)
        self.dropdown_choices = ["--", "Name", "Level",'HP', "ATK"] #super leng options
        self.option.set(self.dropdown_choices[0]) #automatically on "--"
        self.dropdown = OptionMenu(self.page2, self.option, *self.dropdown_choices)
        self.dropdown.pack(side=TOP ,anchor = W) #anchored top left (idk my NESW)
        self.dropdown.config(width = 8)
        
        #Adds treeview to both pages
        #different treeviews for diff pages makes it easier so i can have them for diff things
        self.tree_page2=self.add_treeview(self.page2)  #treeview here for searching and sorting and sorting
        self.tree_page3= self.add_treeview(self.page3) #treeview here for edittig csv file

    def add_treeview(self, page):
        """Add the Treeview to a given page in this case only 2 and 3"""
        
        TableMargin = Frame(page, width=500)
        TableMargin.pack(side=TOP)

        self.tree = ttk.Treeview(
            TableMargin,
            columns=("Name", "Element", "Character Star", "Character Level", "Max HP", "Base ATK", "Elemental Skill", "Elemental Burst", "Region", "Weapon"),
            height=400,
            selectmode="extended",
        )
        with open('genshinCharacters.csv') as characters:
            read_csv = csv.DictReader(characters, delimiter=',')
            for row in read_csv:
                #rows passed as a tuple into values which will populate the treeview
                self.tree.insert("", "end", values= (row['Name'], row['Element'], row['Character Star'], row["Character Level"], row["Max HP"],
                          row["Base ATK"], row["Elemental Skill"], row["Elemental Burst"], row["Region"], row["Weapon"]))

        self.tree.heading("Name", text="Name", anchor="c")
        self.tree.heading("Element", text="Element", anchor="c")
        self.tree.heading("Character Star", text="Star", anchor="c")
        self.tree.heading("Character Level", text="Level", anchor="c")
        self.tree.heading("Max HP", text="HP", anchor="c")
        self.tree.heading("Base ATK", text="Base ATK", anchor="c")
        self.tree.heading("Elemental Skill", text="Skill", anchor="c")
        self.tree.heading("Elemental Burst", text="Burst", anchor="c")
        self.tree.heading("Region", text="Region", anchor="c")
        self.tree.heading("Weapon", text="Weapon", anchor="c")
        #treeview column properties
        self.tree.column("#0", stretch=NO, minwidth=15, width=0, anchor="c") #ghost column ignore
        self.tree.column("#1", stretch=NO, minwidth=15, width=90, anchor="c")
        self.tree.column("#2", stretch=NO, minwidth=15, width=70, anchor="c")
        self.tree.column("#3", stretch=NO, minwidth=15, width=50, anchor="c")
        self.tree.column("#4", stretch=NO, minwidth=15, width=50, anchor="c")
        self.tree.column("#5", stretch=NO, minwidth=15, width=60, anchor="c")
        self.tree.column("#6", stretch=NO, minwidth=15, width=70, anchor="c")
        self.tree.column("#7", stretch=NO, minwidth=15, width=150, anchor="c")
        self.tree.column("#8", stretch=NO, minwidth=15, width=200, anchor="c")
        self.tree.column("#9", stretch=NO, minwidth=15, width=100, anchor="c")
        self.tree.column("#10", stretch=NO, minwidth=15, width=75, anchor="c")
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
# FUNCTION: update character data
# ---------------------------------------------------------------------

    def update_character(self):
        """Connected to the update button and it pastes the data user has selected so it can be updated"""  
      
       # --- List of character trait lists ---
        character_traits = [
        self.name_entry, self.element_entry, self.star_entry, self.level_entry,
        self.hp_entry, self.atk_entry, self.skill_entry, self.burst_entry,
        self.region_entry, self.weapon_entry
    ] 
        # For validating numeric fields
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
        self.page3.after(3000, lambda: self.error_label_3.config(text="")) #error shown for only 3 seconds before dissappearing as text is reset to nothing


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



    def clear_boxes(self):
        #deletes all entry box data
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry, self.burst_entry,self.region_entry, self.weapon_entry )
        for options in tree_entryboxes: #iterates # loop knowledge ate
            options.delete(0, END)
       
    def search_character(self):
        #clears current rows in the treeview
        for row in self.tree_page2.get_children():
            self.tree_page2.delete(row)
            found= False #defined outside da loop 
        query = self.search_entry.get().lower()#get the search query which is in the search entry box and lower cases it 
        #reads the CSV and filters rows based on the query dun dun dunnnnn
        #opens character.csv file
        with open('genshinCharacters.csv') as characters:
            character_selected = csv.DictReader(characters, delimiter=',')
            for row in character_selected: 
                #checks if the query matches in certain rows and then appends to empty treeview
                #didnt include burst or skill coz literally no one would ever search by that
                if query in row['Name'].lower() or query in row['Element'].lower() or query in row['Character Star'].lower() or query in row['Region'].lower() or query in row['Weapon'].lower():
                    self.tree_page2.insert("", 0, values=(
                        row['Name'], row['Element'], row['Character Star'], row['Character Level'], row['Max HP'], row['Base ATK'], row['Elemental Skill'], row['Elemental Burst'], row["Region"], row["Weapon"]
                    ))
                    found=True #set found as true if query found
            if not found:
               self.error_label_2.config(text="DOES NOT EXIST.")
               self.page2.after(3000, lambda: self.error_label_2.config(text=""))


    def select_character(self):
        #clear entry boxes
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry, self.burst_entry,self.region_entry, self.weapon_entry )
        for options in tree_entryboxes:
            options.delete(0, END)
        selected = self.tree.focus() #tells u whats focused or currently pressed on shows up as pink on my mac
        #grabs values associated with record
        #values is a tuple of the selected row dun da dunnn
        values = self.tree.item(selected, 'values') #id (a number e.g. 1 for Traveller) and associated values
        self.name_entry.insert(0, values[0]) #0 because i want to insert my king into the 0th position of the entry box
        self.element_entry.insert(0, values[1])
        self.star_entry.insert(0, values[2])
        self.level_entry.insert(0, values[3])
        self.hp_entry.insert(0, values[4])
        self.atk_entry.insert(0, values[5])
        self.skill_entry.insert(0, values[6])
        self.burst_entry.insert(0, values[7])
        self.region_entry.insert(0, values[8])
        self.weapon_entry.insert(0, values[9])

    def add_character(self): #need this to show up on treeview too on page 2 maybe message to user to reload page to show addec charater to masterlist
        if not (self.name_entry.get() and self.element_entry.get() and self.star_entry.get() and self.level_entry.get() and self.hp_entry.get() and self.atk_entry.get() and self.skill_entry.get() and self.burst_entry.get() and self.region_entry.get() and self.weapon_entry.get()):
            # Check if all fields are filled #If any field is empty, show an error message and return
            self.error_label_3.config(text="Please fill all fields!!.")
            self.page3.after(3000, lambda: self.error_label_3.config(text="")) #error shown for only 3 seconds before dissappearing as text is reset to nothing
            return  #stop the function from running
          
        if not (self.star_entry.get().isdigit() and self.level_entry.get().isdigit() and self.hp_entry.get().isdigit() and self.atk_entry.get().isdigit()):
            self.error_label_3.config(text="'Star', 'Level' , 'Max HP' and 'Base ATK' should all be numbers.") #validation and makes sure number boxes have only numbers in them
            self.page3.after(4000, lambda: self.error_label_3.config(text="")) #error shown for only 4 seconds before dissappearing as text is reset to nothing
            return  #stop the function from running
        
        self.tree.insert(parent='', index='end', text='',values= (self.name_entry.get(), self.element_entry.get(), self.star_entry.get(), self.level_entry.get(), self.hp_entry.get(), self.atk_entry.get(), self.skill_entry.get(), self.burst_entry.get(), self.region_entry.get(), self.weapon_entry.get())) #added to the end
        #deletes all entry box data
        tree_entryboxes = (self.name_entry,self.element_entry, self.star_entry, self.level_entry,
                   self.hp_entry,self.atk_entry,self.skill_entry, self.burst_entry, self.burst_entry,self.region_entry, self.weapon_entry )
        for options in tree_entryboxes:
            options.delete(0, END)
        column_a_list = [] #this is the name column
        column_b_list = []
        column_c_list = []
        column_d_list = []
        column_e_list = []
        column_f_list = []
        column_g_list = []
        column_h_list = []
        column_i_list = []
        column_j_list = [] #finally this is thw weapon column

        for child in self.tree.get_children():
            column_a_list.append(self.tree.item(child)["values"][0])  #counts from name column not the ghost column         
            column_b_list.append(self.tree.item(child)["values"][1])  
            column_c_list.append(self.tree.item(child)["values"][2])  
            column_d_list.append(self.tree.item(child)["values"][3])
            column_e_list.append(self.tree.item(child)["values"][4])            
            column_f_list.append(self.tree.item(child)["values"][5])  
            column_g_list.append(self.tree.item(child)["values"][6])  
            column_h_list.append(self.tree.item(child)["values"][7]) 
            column_i_list.append(self.tree.item(child)["values"][8])            
            column_j_list.append(self.tree.item(child)["values"][9])  #again this is the weapon column
        
        #putting values into a dictionairy with the headings as the key and the rows containing data from the rows as the values
        full_treeview_data_dict = {'Name': column_a_list, 'Element': column_b_list, 'Character Star': column_c_list, 'Character Level': column_d_list, "Max HP":column_e_list, "Base ATK": column_f_list, "Elemental Skill": column_g_list, "Elemental Burst": column_h_list, "Region":column_i_list, "Weapon": column_j_list}
        treeview_df = pd.DataFrame.from_dict(full_treeview_data_dict)
        treeview_df.to_csv("genshinCharacters.csv", index = False)
        self.error_label_3.config(text="CHARACTER ADDED")
        self.page3.after(3000, lambda: self.error_label_3.config(text="")) #error shown for only 3 secondsssss before dissappearing as text is reset to nothing
        
class IntroPage(GenshinSorter): #inheritance yurrrrrrrrrrrrrrrr
    def __init__(self, genshin_window):
        super().__init__(genshin_window)
        #title and label fo rpage 1
        self.page1_title = tk.Label(self.page1, text="HAFSA'S GENSHIN ORGANISER", font=('Arial', 30, "bold"),bg=colour_2)
        self.page1_title.pack(side= TOP, pady=20, expand=True)
        self.theme_label = tk.Label(self.page1, text="Current Theme: Neuvillette", font=('Arial', 16),bg=colour_2)
        self.theme_label.pack(side= BOTTOM, pady=20, expand=True)
        #Character count #extraStats too good
        self.character_count_label = tk.Label(self.page1, text= f"TOTAL CHARACTER COUNT: {Character.character_count}" , font=('Arial', 15, "bold"), bg=colour_2) 
        self.character_count_label.pack(pady=20)
        #cheeky plot for elements on the homepage oui oui
        character_df =Character.make_characters_csv()  #finally get to use the csv i called yurrrrr
        #elementcounts checks the number of times something comes up in the csv
        element_counts = character_df['Element'].value_counts() #chose elements since theyre my fave cheeky attribute
        element_index = element_counts.index.tolist()  #converts both to a list
        element_count = element_counts.values.tolist() 
        frameChart = tk.Frame(self.page1) #puts the graph on page 1
        frameChart.pack()
        #creates the matplotlib figure and axes
        fig = Figure(figsize=(4,4))  #sets the figure size
        ax = fig.add_subplot(111)  #add a subplot
        fig.patch.set_facecolor(colour_2)  #set the background of the figure to the lightblue ting
        #plots the pie chart
        ax.pie(element_count, labels=element_index, autopct='%0.0f%%', startangle=180)
        element_chart = FigureCanvasTkAgg(fig, frameChart)#embeds the figure into tkinter 
        element_chart.get_tk_widget().pack(anchor="center") 


if __name__ == "__main__":
    # Creates CSV if genshinCharacaters.csv doesnt exist
    characters = [ 
        Character("Traveller", "Anemo", 4,1, 911, 17, "Gale Blade", "Dandelion Breeze", "Mondstadt", "Sword"),
        Character("Kaeya", "Cyro", 4, 1,975, 18, "Frostgnaw", "Glacial Waltz", "Mondstadt", "Sword"),
        Character("Amber", "Pyro", 4, 1, 793, 18, "Explosive Puppet", "Fiery Rain", "Mondstadt", "Bow"),
        Character("Neuvillette", "Hydro", 5, 1, 900, 20, "O Tears, I Shall Repay", "O Tides, I Have Returned", "Fontaine", "Catalyst")
    ]


    Character.make_characters_csv() #needed to  be called like so important esp if no character.csv file exists for the first call of the program
    Character.character_count = len(pd.read_csv('genshinCharacters.csv')) #calculating the length of the csv file to see the total character count
    genshin_window = tk.Tk() #main  app so crazy i can call this an app yurr
    intro_page = IntroPage(genshin_window)  #using IntroPage instead of GenshinSorter 
    intro_page.show_page(intro_page.page1) #shows the first page initially
    genshin_window.mainloop() #runs the application
