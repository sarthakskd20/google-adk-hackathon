Step 1: Download the ZIP file
Step 2: Go to the fplder where you have extracted the ZIP file
Step 3: Open command prompt/powershell there & first execute the command
        python -m venv .venv
Step 4: As soon as you create a virtual environment, you will see a .venv file.
Step 5: Use this command to activate your virtual environment in your terminal
       # Windows CMD: .venv\Scripts\activate.bat
       # Windows PowerShell: .venv\Scripts\Activate.ps1
Step 6: As soon as your virtual enviornment gets activated use
      pip install -r requirements.txt
And wait till all the modules get installed. Till then you can create a .env file and the content from .env.example file and paste it in the .env file. [Make sure you use your api key]
Step 7: After completing all the above steps, use this command.
    python main.py
Step 8: Your agent will get executed with a proper UI

Thank you.
