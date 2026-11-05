import time ##Python's built-in time module, used for the pauses

passed_tests = set() ## These are sets
failed_tests = set() ## It is a collection of unique values


def pytest_runtest_logreport(report):
    test_title = report.nodeid ## Gets the test name

    if report.failed: ## If this test fails, then this block runs
        failed_tests.add(test_title) ## Adds the failed test and the title
        passed_tests.discard(test_title) ## Removes it from passed tests

    elif report.when == "call" and report.passed: ## When the test runs it will have a before, actual test running, and the tear down which would mean that the test completed, creates a report, so if there is an issue at any of these stages it should report at what stage had an issue
        passed_tests.add(test_title) ## Adds the passed test with title of the test


def show_test_statistics(): ## This will show the stats for the failed and passed tests
    passed_count = len(passed_tests) ## Counts the passed tests in a collection
    failed_count = len(failed_tests) ## counts the failed tests in a collection

    print("\nTEST RESULTS:") ## In a new line, this will print out when called
    print(f"Total tests: {passed_count + failed_count}") ## This prints both the failed and passed tests as total tests executed
    print(f"Passed tests: {passed_count}") ## This prints out the passed tests executed
    print(f"Failed tests: {failed_count}") ## This prints out the failed tests executed

    if failed_tests:
        print("\nFAILED TEST TITLES:") ## When there are failed tests, it will print the titles of the tests

        for test_title in sorted(failed_tests): ## Sorts the failed tests
            print(f"  FAILED: {test_title}") ## Shows the title of the failed test

    else:
        print("\nNo tests failed.") ## If no tests fail then this will print under the stats


def pytest_sessionfinish(session, exitstatus): ## When the last test is run when it finishes it preforms an exit status, that is when this code will run when EVERYTHING PASSES

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
        r"Pytest loves Bethany ❤️",
        r"",


        ]
        for line in fireworks: ## Meaning take one line and print it, then move onto the next line
            print(line)
            if "Bethany" in line:
                time.sleep(1.5) ## Pauses for 1.5 seconds specifically when Bethany is shown in the line

            else:
                time.sleep(0.2)
        time.sleep(2)
        show_test_statistics() ## This is call for the stats if it passes
    else: ## For if there is a failing test this celebration will happen

        for i in range(10): ## This drops the bomb emoji counting down until 1

            print("\n" * i + "                💣") ## ""\n" creates blank lines, and it creates the illusion that the bomb is falling

            time.sleep(0.1) ## The wait between frames

        print(r"""

               💥 💥 💥
            💥 💥 💥 💥 💥
         💥 💥 FAILURE 💥 💥
            💥 💥 💥 💥 💥
               💥 💥 💥

        """)
        time.sleep(2) ## Waits 2 seconds before the frame jumps
        print("\033[2J\033[H", end="") ## this is using the ANSI terminal, which clears the terminal, the first part of the string is what moves the cursor to the top left corner and it will show the boom disappearing
            ## 003 part is Python code for the escp key in the terminal, the 2J part means clear the screen, together becomes clear terminal, H means move cursor to home position
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
        show_test_statistics() ## This is called when the tests fail






