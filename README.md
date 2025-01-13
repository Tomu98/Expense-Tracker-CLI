# Expense Tracker CLI


This project is a command line application I developed for personal expense management.
You can record, update, delete and visualize your expenses, either in a detailed list or in summaries, as well as generate summaries to help you organize your finances.
In addition, you can set budgets to control your expenses and export the data in CSV, JSON and even Excel format.


This is another project that I was inspired by an idea from [roadmap.sh](https://roadmap.sh), a platform that offers roadmaps, best practices, projects and community-created resources to help people grow in their technology careers.


Specific inspiration for this project comes from the following link: [Expense Tracker CLI in roadmap.sh](https://roadmap.sh/projects/expense-tracker)


<img alt="Static Badge" src="https://img.shields.io/badge/Version-1.0.0-yellowgreen?style=for-the-badge">


<br>


## Installation


1. Clone this repository:

   ```bash
   git clone https://github.com/Tomu98/Expense-Tracker-CLI.git
   ```

2. Within the project directory, create and activate a virtual environment:

   ```bash
   python -m venv .venv        # Create a virtual environment
   source .venv/bin/activate   # Activate the environment in Linux/MacOS
   .venv\Scripts\activate      # Activate the environment in Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```


<br>


## How to use it

To use the Expense Tracker CLI, run the following command:

   ```bash
   python -m src/cli <command> [options]
   ```

Here are the available commands and their options:
- Add expense: `python -m src/cli add --amount <amount> --category <category> [--date <YYYY-MM-DD>] [--description <description>]`
- Delete expense: `python -m src/cli delete [--id <id>] [--all]`
- Update expense: `python -m src/cli update --id <id> [--date <YYYY-MM-DD>] [--amount <amount>] [--category <category>] [--description <description>]`
- Summary of expenses: `python -m src/cli summary [--date <YYYY-MM>] [--category <category>]`
- List expenses: `python -m src/cli list [--category <category>] [--from <YYYY-MM-DD>] [--to <YYYY-MM-DD>] [--min <amount>] [--max <amount>]`
- Set budget: `python -m src/cli set-budget --amount <amount> --date <YYYY-MM>`
- Delete budget: `python -m src/cli delete-budget --date <YYYY-MM>`
- View budget: `python -m src/cli view-budget [--current] [--all] [--date <YYYY-MM>]`
- Export expenses: `python -m src/cli export --output <filename> [--date <YYYY-MM>] [--category <category>] [--include-budget]`

For example, to add a new expense:

   ```bash
   python -m src/cli add --amount 50.75 --category Groceries --description "Weekly groceries"
   ```


<br>


## Feedback & Contributions

This is my second CLI project, and I welcome any comments or contributions. If you find bugs or have suggestions to help me, feel free to open an issue or send a pull request, it will help me a lot to improve as a developer.


<br>


### **Thanks for stopping by and taking a look at the project. 🤍**
