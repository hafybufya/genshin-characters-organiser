# GenshinCharactersOrganiser

[Trying to check if I can merge changes into main branch]

This project complied all characters that users input from Genshin. This was created and submitted for my final Fundamental of Programming Assignment Year1.



## UML DIAGRAMS

I used mermaid live editor to make a frame for my three classes:

```
mermaid
classDiagram
class Characters{
     name 
     element 
     character_star
     character_level 
     max_hp 
     base_ATK
     elemental_skill
     elemental_burst
     region
     weapon_owned
     Character.count
}

class GenshinOrganiser{  
    ttk.Style
    buttons
    labels
    entryboxes
    add_treeview()
    update_character()
    delete_character()
    sort_characters()
    clear_boxes()
    search_character()
    select_character
    add_character()
}

    GenshinOrganiser <|-- IntroPage

class IntroPage{
    labels
    buttons
    stats e.g. no* characters inputted
    graph e.g. piechart
}
```

## 📁 Project Structure

```

├── GenshinOrganiser.py
├── genshinCharacters.csv
├── requirements.txt
└── README.md
└── .circle.ci/
    └── config.yml

```


## ✅ Page 1: Home:

## Page 2:

## Page 3:



## 🛠️ Installation

Python 3.10 or newer to run python files

Python modules used: 
* pandas – reading and handling CSV files.
* matplotlib – plotting graphs.
* tkinter - creating window.
* os – Checking if files exist.

You can install required packages with:

```
pip install pandas matplotlib

```
