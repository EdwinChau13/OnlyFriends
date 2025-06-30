# OnlyFriends

## Setup

**Generate CSS data:**  
Use [Mockaroo](https://www.mockaroo.com/schemas/) for sample data.

---

### 1. Create Project

```bash
django-admin startproject OnlyFriends
code .
git init
touch README.md
echo "hello" > README.md
```

---

### 2. Create Support Files

```bash
# Add these files as needed
.gitignore
settings.py
.env
```

---

### 3. Make Virtual Environment

```bash
mkvirtualenv onlyfriends
workon onlyfriends
pip freeze > requirements.txt
pip install -r requirements.txt
```

---

### 4. Create App and Folders

```bash
python manage.py startapp contacts
code .
# Create templates and static folders as needed
```

---

### 5. Push to Git

```bash
git add .
git commit -m "first commit"
git remote add origin git@github.com:EdwinChau13/OnlyFriends.git
git push -u origin master
```

---

### 6. Setup Database in pgAdmin

- Download: [pgAdmin for macOS](https://www.postgresql.org/ftp/pgadmin/pgadmin4/v9.3/macos/)
- Server: `local`
- Host: `localhost`
- Port: `5432`

#### General

```
Database: project_name
Owner: postgres
```

#### Definition

```
Tablespace: pg_default
Locale Provider: ice
```

#### Security

| Grantee   | Privileges           | Grantor  |
|-----------|----------------------|----------|
| Public    | Temporary, CONNECT   | postgres |
| postgres  | ALL                  | postgres |

---

### 7. Migrations

1. **Create migration scripts (when you change models):**
    ```bash
    python manage.py makemigrations
    ```
2. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

---

### 8. Create Admin User

```bash
python manage.py createsuperuser
# Example:
# Username: edwinchau
# Password: postgres
```

---

### Design

- **Contacts:** (add your design notes here)

---