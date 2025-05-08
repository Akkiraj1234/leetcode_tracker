# LeetCode Tracker

A terminal-based app to track and analyze your LeetCode progress. Designed with modularity and scalability in mind, this app is built to grow with your needs.

## Features
- **Daily Progress Tracking**: Log solved questions with details like difficulty, tags, and time taken.
- **Insights**: Identify weak areas and get personalized recommendations.
- **Spaced Repetition**: Reinforce learning by revisiting weak areas.
- **Modular Design**: Each component (validation, database, UI) is separated for easy maintenance and scalability.

## Code Structure
- `validators.py`: Handles validation of JSON files and SQLite database schemas.
- `initapp.py`: Initializes the app, ensuring required files and directories are present.
- `utils.py`: Contains reusable utility functions.
- `ui/`: Contains terminal-based user interface code using `cursed`.

## Why Modularity Matters
This app is designed to be easily extendable. For example:
- Adding a new feature like "Weekly Summaries" only requires adding a new function in `validators.py` and updating the UI in `ui/`.
- Schema changes are handled gracefully with validation and migration logic.

## How to Run
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the app: `python src/LeetSolver/main.py`.

## Future Plans
- Add cloud syncing.
- Implement gamification features like streaks and achievements.
- Add visualizations for progress tracking.