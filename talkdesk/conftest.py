import time ## Gives access to sleep and pauses in the code

def pytest_sessionfinish(session, exitstatus): ##When the last test is run when it finishes it preforms an exit status, that is when this code will run when EVERYTHING PASSES

    if exitstatus == 0:
        ## This list allows for the code to execute one line at a time, r means raw query
        fireworks = [
        r"       .''.",
        r"     .''.      .        *''*    :_\/_:     .",
        r"     :_\/_:   _\(/_  .:.*_\/_*   : /\ :  .'.:.'.",
        r" .''.: /\ :   ./)\   ':'* /\ * :  '..'.  -=:o:=-",
        r":_\/_:'.:::.    ' *''*    * '.\'/.'_\(/_ '.':'.'",
        r": /\ : :::::     *_\/_*     -= o =- /)\    '  *",
        r"'..'  ':::'     * /\ *     .'/.\'.  '",
        r"     *            *..*         :",
        r"== == == == == == == == == == == == == == == == ==",
        r"Pytest loves Bethany ❤️",
        r"",
        r"All tests passed Ta Da!✅",
        r"== == == == == == == == == == == == == == == == ==",
        ]
        for line in fireworks: ## Meaning take one line and print it, then move onto the next line
            print(line)
            if "Bethany" in line:
                time.sleep(1.5) ##Pauses for 1.5 seconds specifically when Bethany is shown in the line
            elif"All tests passed Ta Da!" in line:
                time.sleep(2) ## Pauses for 2 seconds
            else:
                time.sleep(0.2) ## Everything else (fireworks) will run in a speed of 2.seconds
        for i in range(10): ## This drops the bomb emoji counting down until 1
            print("\n" * i + "                💣") ## ""\n" creates blank lines and it creates the illusion that the bomb is falling
            time.sleep(0.1) ## the wait between frames

        print(r"""

               💥 💥 💥
            💥 💥 💥 💥 💥
         💥 💥 BOOM! 💥 💥
            💥 💥 💥 💥 💥
               💥 💥 💥

        """)
        time.sleep(2) ## Waits 2 seconds before the frame jumps
        print("\033[2J\033[H", end="") ## this is using the ANSI terminal, which clears the terminal, teh first part of the string is what moves the cursor to the top left corner and it will show the boom disappearing
            ## 003 part is python code for the escp key in the terminal, the 2J part means clear the screen, together becomes clear terminal, H means move cursor to home position
        print("""

                      ⢱⣆⠀⠀⠀⠀⢳⠀
                ⠀⠀⠄⠀⠀⠀⠈⣿⣷⡀⠀⠀⠀⠀
                ⠀⢠⠀⠀⠀⠀⢸⣿⣿⣷⣧⠀⠀⠀
                ⠀⠀⠀⠀⡀⢠⣿⡟⣿⣿⣿⡇⠀⠀
                ⠀⠀⠀⠀⣳⣼⣿⡏⢸⣿⣿⣿⢀⠀
                ⠀⠀⠀⣰⣿⣿⡿⠁⢸⣿⣿⡟⣼⡆
                ⢰⢀⣾⣿⣿⠟⠀⠀⣾⢿⣿⣿⣿⣿
                ⢸⣿⣿⣿⡏⠀⠀⠀⠃⠸⣿⣿⣿⡿
                ⢳⣿⣿⣿⠀⠀⣄⠓⠂⠀⢹⣿⡿⡁
                ⠀⠹⣿⣿⡄⠀⣏⠈⡏⠀⢠⣿⡞⠁
                ⠀⠀⠈⠛⢿⣄⠀⠛⠃⣠⠞⠋⠀⠀
                ⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀
  ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡤⠤⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠒⠲⡤⠤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠉⠀⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠋⠀⠀⠈⠓⢾⡉⠉⠙⠒⠒⠒⠦⣄⡀⠀⠀⠀
⡤⠖⠒⠒⠋⠉⠉⠉⢩⠏⠁⠀⠀⠀⠃⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢧⡀⠀⠀⠀⠀⠀⠀⠈⢳⠀
⡇⠀⠀⠀⠀⠀⠀⡼⠁⠀⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⡆⠀⠀⠀⠀⠀⠀⠀⢹
⠀⠀⠀⠀⠀⠀⡜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡄⠀⠀⠀⠀⠀⢀⡼
⡆⠀⠀⠀⠀⢸⠇⠀⠀⠀⠀⠀⠀⠀⠛⠦⡆⡀⠃⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⣄⡖⠖⠂⠀⠀⠀⠀⠀⠀⠘⡌⠀⠀⠀⠀⣀⠖⠃⠀
⢳⡀⠀⠀⠀⡞⠀⠀⣀⣠⡤⣤⠤⣄⡀⠘⢀⢸⠀⠀⠀⠀⠀⠀⠀⠴⠀⠀⠆⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢀⣠⠖⠃⠀⠀⠀⠀
⠀⠘⠲⣄⠀⡇⡴⠋⠀⠀⠙⡆⢧⠀⠉⠧⡈⣸⠀⠀⠀⠀⠀⠀⠀⣇⠀⠀⠂⠀⠀⣠⢖⣾⡟⠉⠓⢦⡀⣷⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠙⡇⠇⠀⠀⠀⠀⢸⠀⡇⠀⠀⣹⡼⠯⠤⠤⠤⠤⠤⠤⢿⣦⠀⡼⠁⠀⠀⡏⢸⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢹⠲⣄⣀⣀⣫⣞⣁⣀⡖⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢦⡀⠸⣄⢳⡀⠀⢠⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡴⠃⠠⣄⣀⠀⠀⣠⠄⠏⠀⠀⠀⣀⡤⠖⠚⠉⠉⠓⢦⡀⠀⠀⠀⠀⠈⢯⢉⡓⠚⠛⠉⠁⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡸⠁⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠉⠀⠀⣀⣤⣤⠤⣤⣤⡀⠙⠂⠀⠀⠀⠀⢩⡀⠉⠓⠒⠋⠀⠙⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡇⠀⢨⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠧⣁⣤⠀⣴⣽⡾⠀⠀⠀⠀⠀⢀⠀⢳⡀⠀⠀⠢⡀⠀⠙⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡇⠀⢷⠀⠀⢠⢃⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⡏⠉⠁⠀⠀⠀⠀⠀⠀⠀⣇⠀⢧⠀⠀⠀⠙⠆⠀⢣⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡇⠀⢻⠀⣰⠃⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⢧⠀⠀⠀⡗⠀⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠙⡄⠀⠁⡇⠀⠀⠳⣄⠀⠀⠀⠀⠀⠀⠀⣠⣞⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⡼⠀⠀⠀⡇⠀⢀⡌⠁⢸⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠙⣆⠀⠓⡦⣤⡀⠀⠉⠉⠓⠒⡖⠉⠉⠀⠀⠀⠀⠀⠈⠓⣲⠒⠒⠋⠁⣠⠖⠋⠁⠀⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠦⣄⡉⠙⠧⠲⠆⠀⠀⠀⠓⠲⠤⠴⠤⠤⠤⠤⠞⠁⠀⠀⠀⠀⠀⠀⡰⢃⣀⠴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠒⠒⠙⠒⠦⣄⡀⠈⠛⠻⠁⠀⣀⣀⡠⠟⠒⠒⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠓⠒⠚⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

""")






