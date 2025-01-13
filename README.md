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
   python src/cli.py <command> [options]
   ```

Use the `--help` option to learn about available commands and their usage:

   ```bash
   python src/cli.py --help
   python src/cli.py <command> --help
   ```

<br>

Here are the available commands and their options:

- ***add:***<br>
  `--amount`: Required. The amount of the expense.<br>
  `--category`: Required. The category of the expense.<br>
  `--date`: Optional. The date of the expense (YYYY-MM-DD). Defaults to today's date if not provided.<br>
  `--description`: Optional. A description of the expense.<br>

     ```bash
     python src/cli.py add --amount 10 --category Leisure --description "Buying Project Zomboid :D"
     ```

- ***delete:***<br>
  `--id`: Required. The ID of the expense to delete.<br>
  `--all`: Optional. Delete all expenses.<br>

     ```bash
     python src/cli.py delete --id 2
     ```

- ***update:***<br>
  `--id`: Required. The ID of the expense to update.<br>
  `--date`: Optional. The new date of the expense (YYYY-MM-DD).<br>
  `--amount`: Optional. The new amount of the expense.<br>
  `--category`: Optional. The new category of the expense.<br>
  `--description`: Optional. The new description of the expense.<br>

     ```bash
     python src/cli.py update --id 1 --amount 20 --description "A gift for my mom <3"
     ```

- ***summary:***<br>
  `--date`: Optional. Filter expenses by date (YYYY-MM).<br>
  `--category`: Optional. Filter expenses by category.<br>

     ```bash
     python src/cli.py summary --date 2025-01 --category Others
     ```

- ***list:***<br>
  `--category`: Optional. Filter by expense category.<br>
  `--from`: Optional. Filter expenses from this date onwards (YYYY-MM-DD).<br>
  `--to`: Optional. Filter expenses up to this date (YYYY-MM-DD).<br>
  `--min`: Optional. Show expenses above or equal to this amount.<br>
  `--max`: Optional. Show expenses below or equal to this amount.<br>

     ```bash
     python src/cli.py list --from 2025-01-13 --to 2024-12-20 --min 20
     ```

- ***set-budget:***<br>
  `--amount`: Required. The amount for the budget.<br>
  `--date`: Required. The date for the budget (YYYY-MM).<br>

     ```bash
     python src/cli.py set-budget --amount 1000 --date 2025-01
     ```

- ***delete-budget:***<br>
  `--date`: Required. The date for the budget (YYYY-MM).<br>

     ```bash
     python src/cli.py delete-budget --date 2024-12
     ```

- ***view-budget:***<br>
  `--current`: Optional. Show the current month's budget.<br>
  `--all`: Optional. Show all budgets.<br>
  `--date`: Optional. Show the budget for a specific month or year (YYYY-MM).<br>

     ```bash
     python src/cli.py view-budget --all
     ```

- ***export:***<br>
  `--output`: Required. The name of the exported file.<br>
  `--date`: Optional. Filter expenses by date (YYYY-MM).<br>
  `--category`: Optional. Filter expenses by category.<br>
  `--include-budget`: Optional. Include budget information in the export.<br>

     ```bash
     python src/cli.py export --output expenses_2025_01.xlsx --date 2025-01 --include-budget
     ```


<br>


## Feedback & Contributions

This is my second CLI project, and I welcome any comments or contributions. If you find bugs or have suggestions to help me, feel free to open an issue or send a pull request, it will help me a lot to improve as a developer.


<br>


### **Thanks for stopping by and taking a look at the project. 🤍**
