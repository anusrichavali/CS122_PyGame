import character_selection
from pathlib import Path

#creates high_score.txt if it doesn't exist and sets high score to 0
try:
    with open("saved_states/high_score.txt", "x") as file:
        file.write("0")
except:
    pass
    
#main loop that handles gameflow and connects separate pages
running = True
while running:
    #runs character selection
    character_select_event = character_selection.run()
    if character_select_event == "Quit":
        running = False
    #connects location page
    elif character_select_event == "Next":
        #handles location page
        import choose_locations
        choose_locations_event = choose_locations.run()
        if choose_locations_event == "Quit":
            running = False
        #connects game page
        elif choose_locations_event == "Start":
            running = False
            import spartandash
            game = spartandash.run()
            if game == "Done":
                running = False
            
