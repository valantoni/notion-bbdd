# How to set up Notion as Database #

Documentation: https://developers.notion.com/docs/getting-started

Step1: Create a new integration

Step 2: Create a new page in notion with a table

Step 3: Invite the integration to the database (table in step2) -> Add conection -> choose integration -> https://developers.notion.com/docs/create-a-notion-integration

Step 4: Copy the link of the database and copy the id table in that link

# Steps to run the script #

### 1. Clone the repo

```bash
git clone https://github.com/valantoni/notion-bbdd

```

The `.` will clone it to the current directory so make sure you are inside your project folder first.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a .env file and set your credentials(notion_api_token and table_id)

```bash
echo. > .env
```

### Run the script to test it

```bash
python notion.py
```

## 👀 Want to learn more?

[Developers community](https://t.me/devhispanos) or follow me on [Youtube](https://www.youtube.com/@tonidev_/).

## DO NOT FORGET TO START ⭐ THE REPO