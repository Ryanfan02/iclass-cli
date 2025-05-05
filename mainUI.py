# main.py
import asyncio
import curses
from api.auth_module import Authenticator
from api.iclass_api import TronClassAPI

def draw_menu(stdscr, selected_idx, options, title):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(1, w//2 - len(title)//2, title, curses.A_BOLD | curses.A_UNDERLINE)

    for idx, option in enumerate(options):
        x = w // 2 - 30
        y = 3 + idx
        if idx == selected_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)
    stdscr.refresh()

async def handle_course_actions(stdscr, api, course_id):
    actions = ["View Activities", "Download Files", "Submit Homework", "Back"]
    selected = 0
    while True:
        draw_menu(stdscr, selected, actions, f"Course ID: {course_id} - Actions")
        key = stdscr.getch()
        if key == curses.KEY_UP and selected > 0:
            selected -= 1
        elif key == curses.KEY_DOWN and selected < len(actions) - 1:
            selected += 1
        elif key in [curses.KEY_ENTER, ord("\n")]:
            action = actions[selected]
            if action == "View Activities":
                response = await api.get_activities(course_id)
                stdscr.clear()
                stdscr.addstr(1, 2, f"Activities for Course ID {course_id}:", curses.A_BOLD)
                y = 3
                for act in response["activities"]:
                    stdscr.addstr(y, 4, f"{act['id']}: {act['type']} - {act.get('deadline', '')}")
                    y += 1
                    if y >= curses.LINES - 2:
                        stdscr.addstr(y, 4, "-- More --")
                        stdscr.getch()
                        y = 3
                        stdscr.clear()
                stdscr.addstr(y + 1, 2, "Press any key to go back...")
                stdscr.getch()

            elif action == "Download Files":
                response = await api.get_activities(course_id)
                for act in response["activities"]:
                    for upload in act.get("uploads", []):
                        file_id = upload.get("reference_id")
                        filename = await api.download(file_id)
                        stdscr.addstr(1, 2, f"Downloaded {filename}")
                        stdscr.getch()

            elif action == "Submit Homework":
                stdscr.clear()
                curses.echo()
                stdscr.addstr(2, 2, "Enter activity ID: ")
                activity_id = int(stdscr.getstr(2, 25).decode())
                stdscr.addstr(3, 2, "Enter upload file IDs (comma-separated): ")
                upload_ids = stdscr.getstr(3, 40).decode().split(",")
                upload_ids = [int(uid.strip()) for uid in upload_ids]
                result = await api.submit_homework(activity_id, upload_ids)
                stdscr.addstr(5, 2, str(result))
                curses.noecho()
                stdscr.getch()
            elif action == "Back":
                break

async def curses_main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)

    stdscr.addstr(0, 0, "🔐 Logging in...", curses.A_BOLD)
    stdscr.refresh()

    auth = Authenticator()
    session = auth.perform_auth()
    api = TronClassAPI(session)

    result = await api.get_courses()
    courses = result.get("courses", [])
    course_options = [f"{c['id']} - {c['name']}" for c in courses]

    selected_idx = 0
    while True:
        draw_menu(stdscr, selected_idx, course_options + ["Exit"], "🎓 Select a Course")
        key = stdscr.getch()
        if key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(course_options):
            selected_idx += 1
        elif key in [curses.KEY_ENTER, ord('\n')]:
            if selected_idx == len(course_options):
                break
            selected_course = courses[selected_idx]
            await handle_course_actions(stdscr, api, selected_course["id"])

if __name__ == '__main__':
    curses.wrapper(lambda stdscr: asyncio.run(curses_main(stdscr)))
