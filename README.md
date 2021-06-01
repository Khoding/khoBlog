# khoBlog

If you want to use for yourself:
1. Clone this repository
2. Create a database called khoBlog in localhost (using wamp or xampp, you need mysql timezones if you don't have them, and you need to use this collation `utf8mb4_unicode_520_ci`)
3. `pip install -r requirements.txt` in a venv
4. Copy and paste `.env.example` and fill it with the data you want (and need) and call it `.env`
5. `python manage.py makemigrations`
6. `python manage.py migrate`
7. `python manage.py createsuperuser`
8. You'll then have to either have already set up an email verification in `.env` or change the value manually in phpmyadmin or whatever you use to see your database.
9. And I believe I'm not missing anything, if it crashes, check Django's Documentation, btw you're expected to know how to use Django and Python before using this for yourself, I will not debug your issues, so feel free to not ask me for help unless you're absolutely certain the problem comes from me (which would probably mean that my website is down while you're trying)
10. Also please Idc if you use it fully in production but gimme credits and don't just copy my content, and I'm not responsible of any problems you encounter.
