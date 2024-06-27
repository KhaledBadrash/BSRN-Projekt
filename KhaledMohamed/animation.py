def gewinner_screen(parent, personal_name):
    win_root = ttk.TTkWindow(parent=parent, title="Gewinner", border=True, pos=(35, 5), size=(30, 10))
    win_root.raiseWidget()
    log_win(personal_name)  # Loggen des Gewinnereignisses
    win_root.show()

    name_root = ttk.TTkWindow(parent=parent, title=f"{personal_name} ist der Gewinner!", border=True, pos=(35, 20), size=(30, 10))
    name_root.raiseWidget()
    name_root.show()

    # Animation: Change the title color repeatedly
    def animate_title():
        colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN, ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
        index = 0
        while True:
            win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
            name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
            index += 1
            time.sleep(0.5)
            parent.update()

    # Start the animation in a separate thread to keep the GUI responsive
    import threading
    animation_thread = threading.Thread(target=animate_title, daemon=True)
    animation_thread.start()
