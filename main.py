# main.py
import asyncio
from api.auth_module import Authenticator
from api.iclass_api import TronClassAPI
from texttable import Texttable
from bs4 import BeautifulSoup

async def main():
    print("🔐 Logging in...")
    auth = Authenticator()
    session = auth.perform_auth()

    api = TronClassAPI(session)

    while True:
        print("\n📚 iClass TKU API Menu")
        print("1. Get Todos")
        print("2. Get Bulletins")
        print("3. Get Courses")
        print("4. Upload File")
        print("5. Submit Homework")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            result = await api.get_todos()
            print("\n✅ Todos:")
            print(result)

        elif choice == "2":
            result = await api.get_bulletins()
            t = Texttable()
            t.set_cols_width([23, 15, 25, 50])
            # Add header row
            t.add_row(['Title', 'CreatedBy','Created At','Content'])

            # Filter data and add to table
            for bulletin in result['bulletins']:
                title = bulletin.get('title', '')
                created_by_name = bulletin['created_by'].get('name', '')
                html_content = bulletin.get('content', '')
                created_at = bulletin.get('created_at', '')    
                # Add row to table
                html_content 
                soup = BeautifulSoup(html_content, 'html.parser')
                content = soup.get_text()
                t.add_row([title, created_by_name,created_at,content])
            print("\n📢 Bulletins:")
            print(t.draw())

        elif choice == "3":
            result = await api.get_courses()
            print("\n🎓 Courses:")
            table = Texttable()
            table.header(['ID', '名稱', '學分', '教師'])

            # Loop through the courses and extract the needed fields
            for course in result.get('courses', []):
                course_id = course.get('id')
                course_name = course.get('name')
                credit = course.get('credit')
                instructors = ', '.join(instr.get('name') for instr in course.get('instructors', []))
                table.add_row([course_id, course_name, credit, instructors])
            print(table.draw())
        elif choice == "4":
            file_path = input("Enter the file path to upload: ").strip()
            upload_id = await api.upload_file(file_path)
            print(f"\n📁 Uploaded file ID: {upload_id}")

        elif choice == "5":
            try:
                activity_id = int(input("Enter activity ID: "))
                upload_ids = input("Enter upload file IDs (comma-separated): ")
                upload_ids = [int(i.strip()) for i in upload_ids.split(",") if i.strip()]
                result = await api.submit_homework(activity_id, upload_ids)
                print("\n📨 Submission Result:")
                print(result)
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid option. Please choose a number between 1 and 6.")

if __name__ == '__main__':
    asyncio.run(main())
