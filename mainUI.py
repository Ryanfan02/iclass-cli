# main.py
import asyncio
import curses
import json
from api.auth_module import Authenticator
from api.iclass_api import TronClassAPI

MENU_OPTIONS = [
    "Get Todos",
    "Get Bulletins",
    "Get Courses",
    "Upload File",
    "Submit Homework",
    "Exit"
]

async def handle_selection(api, stdscr, index):
    curses.echo()
    stdscr.clear()

    if index == 0:
        result = await api.get_todos()
        stdscr.addstr(0, 0, "Todos:\n" + json.dumps(result, indent=2))
    elif index == 1:
        result = await api.get_bulletins()
        stdscr.addstr(0, 0, "Bulletins:\n" + json.dumps(result, indent=2))
    elif index == 2:
        result = await api.get_courses()
        stdscr.addstr(0, 0, "Courses:\n" + json.dumps(result, indent=2))
    elif index == 3:
        stdscr.addstr(0, 0, "Enter file path to upload: ")
        curses.curs_set(1)
        file_path = stdscr.getstr().decode()
        curses.curs_set(0)
        result = await api.upload_file(file_path)
        stdscr.addstr(2, 0, f"Upload Result: {result}")
    elif index == 4:
        stdscr.addstr(0, 0, "Enter activity ID: ")
        curses.curs_set(1)
        activity_id = int(stdscr.getstr().decode())
        stdscr.addstr(1, 0, "Enter upload file IDs (comma-separated): ")
        upload_ids = [int(i.strip()) for i in stdscr.getstr().decode().split(",")]
        curses.curs_set(0)
        result = await api.submit_homework(activity_id, upload_ids)
        stdscr.addstr(3, 0, f"Submit Result: {result}")
    elif index == 5:
        return False  # Exit

    stdscr.addstr(curses.LINES - 2, 0, "Press any key to return to menu...")
    stdscr.getch()
    return True

async def curses_main(stdscr):
    curses.curs_set(0)  # Hide cursor
    current_row = 0

    stdscr.clear()
    stdscr.addstr(0, 0, "🔐 Logging in...")
    stdscr.refresh()

    auth = Authenticator()
    session = auth.perform_auth()
    api = TronClassAPI(session)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "📚 iClass TKU - Use ↑ ↓ and Enter to select\n", curses.A_BOLD)

        for idx, option in enumerate(MENU_OPTIONS):
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(idx + 2, 2, f"> {option}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(idx + 2, 4, option)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_row = (current_row - 1) % len(MENU_OPTIONS)
        elif key == curses.KEY_DOWN:
            current_row = (current_row + 1) % len(MENU_OPTIONS)
        elif key in [curses.KEY_ENTER, 10, 13]:
            should_continue = await handle_selection(api, stdscr, current_row)
            if not should_continue:
                break

def main():
    curses.wrapper(run_curses)

def run_curses(stdscr):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    asyncio.run(curses_main(stdscr))

if __name__ == '__main__':
    main()
