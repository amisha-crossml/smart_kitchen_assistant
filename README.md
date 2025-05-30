
# 🧠 SmartKitchenAssistant Crew

Welcome to the **SmartKitchenAssistant Crew** — AI-powered culinary companion, built using [crewAI](https://crewai.com). This project brings together a team of intelligent agents to make cooking easier, smarter, and more personalized.

---

## 🚀 Features

- 🧑‍🍳 **Recipe Suggestions** tailored to user preferences, dietary needs, and available ingredients.
- 🎥 **YouTube Recommendations** for those who prefer to learn through visual step-by-step tutorials.
- 🥫 **Ingredient Listings** with accurate measurements, substitutions, and pantry advice.
- 🔧 **Kitchen Emergency Help** to troubleshoot common cooking mistakes like over-salting, burning, or texture issues.

---

## 📦 Installation

Ensure you’re using **Python >=3.10 and <3.13**.

1. Install `uv` (a faster Python package manager):
   ```bash
   pip install uv
   ```

2. Use `uv` to install `crewai`:
   ```bash
   uv tool install crewai
   ```

### Customizing Agents and Tasks

1. Define and update agents in: `src/smart_kitchen_assistant/config/agents.yaml`

2. Define tasks and workflows in: `src/smart_kitchen_assistant/config/tasks.yaml`

3. Add custom logic, tools, or agent arguments in: `src/smart_kitchen_assistant/crew.py`

4. Modify input handling and CLI/UI logic in: `src/smart_kitchen_assistant/app.py`

---

## 🏃‍♀️ Running the Project

Start the SmartKitchenAssistant Crew with:

```bash
flask run
```

This command spins up your crew of intelligent agents and initiates the task flow based on user input.

---

## 🧑‍💼 Agent Overview

1. **Cooking Manager** -> Manages agent roles like recipes and recipes video 
2. **Recipe Agent** -> Suggests recipes based on preferences and available ingredients 
3. **YouTube Agent** -> Finds YouTube link relevant recipes.
4. **Kitchen Support Manager** -> Manages support roles like ingredients and emergencies 
5. **Ingredient Agent** -> Lists ingredients and suggests alternatives 
6. **Kitchen Emergency Expert** -> Helps fix common cooking issues in real time 

---