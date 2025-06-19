## 🚀 Installation Instructions

Follow these steps to set up and run the project locally:

### 📦 Step 1: Download the Repository

* Click on the green `Code` button at the top of the repository page.
* Select **Download ZIP** and extract it to your desired location.

### 📂 Step 2: Navigate to the Project Directory

```bash
cd path/to/extracted/folder
```

### 🐍 Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

> This will create a `.venv` folder containing your isolated Python environment.

### ⚡ Step 4: Activate the Virtual Environment

* **For Windows CMD**:

  ```bash
  .venv\Scripts\activate.bat
  ```
* **For Windows PowerShell**:

  ```powershell
  .venv\Scripts\Activate.ps1
  ```

### 📥 Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Step 6: Set Up Environment Variables

* Create a `.env` file in the root folder.
* Copy contents from `.env.example` into `.env`.
* Make sure to insert your own **API key(s)** where required.

### ▶️ Step 7: Run the Application

```bash
python main.py
```

Once this is done, your agent will start and launch with the proper user interface. You're ready to go! 🎉
