import character_selection

running = True
while running:
    character_select_event = character_selection.run()
    if character_select_event == "Quit":
        running = False
    elif character_select_event == "Next":
        import choose_locations
        choose_locations_event = choose_locations.run()
        if choose_locations_event == "Quit":
            running = False
        elif choose_locations_event == "Start":
            import spartandash
            game = spartandash.run()
            if game == "Done":
                running = False