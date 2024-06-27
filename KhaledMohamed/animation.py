def animate_title():
    colors = [ttk.TTkColor.RST, ttk.TTkColor.BOLD, ttk.TTkColor.UNDERLINE, ttk.TTkColor.RED, ttk.TTkColor.GREEN,
              ttk.TTkColor.YELLOW, ttk.TTkColor.BLUE, ttk.TTkColor.MAGENTA, ttk.TTkColor.CYAN, ttk.TTkColor.WHITE]
    index = 0
    while True:
        win_root.setTitle(f"{colors[index % len(colors)]}Gewinner")
        name_root.setTitle(f"{colors[index % len(colors)]}{personal_name} ist der Gewinner!")
        index += 1
        time.sleep(0.5)
        parent.update()


import threading

animation_thread = threading.Thread(target=animate_title, daemon=True)
animation_thread.start()