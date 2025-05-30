# Literature Analyzer

A tool to read and analyze research papers.
Latest update added a new feature allows users to perform an in-depth analysis of any pdf document using LLMs from Google. The users could then have follow-up discussion with the LLM to dissect the information found in the target pdf file.

## [Installation](#installation)
  - If you clone this repository to your local machine, make sure to adjust the icon path, found in the main_application.spec before building the application. Else, the installer would encounter error during the packaging process.
  ```markdown
  icon='E:\\Projects\\Applications\\LiteraturatureAnalyzer\\programs\\assets\\icon.png'
  ``` 
  - Make sure the terminal in your IDE is at the root location of your project directory.
  - Ensure pyinstaller already exist in your virtual environment.
  - Run the following command in the terminal.
  ```markdown
  pyinstaller main_application.spec
  ```
  - The output executable program could then be found in the "dist" folder in the root directory.
## [Usage](#usage)
  - Perform installation and run the Literature_Analyzer.exe to start the program. 
  - OR Run the gui_2.py to start the program
  - OR Run the following commands on your terminal (make sure the terminal is at the root location of your project)
  ```markdown
  cd programs
  python gui_2.py
  ```
## [Disclaimer](#disclaimer)
  - **"Gemini is not an all-knowing entity!"** - The results provided by Google Gemini may **not always contain correct** information.
  - **"Skepticism is crucial!"** - **Always** doublecheck the analysis returned by Google Gemini by manually comparing the given claims, quotes and statements against the actual information found in the target document.
  - **"Don't be a lazy-phoque""** - **Do not**, and I can't stress this hard enough, blindly copy the answer from Google Gemini and directly paste them into your own works! Instead try to use them as supporting data to reach your own conclusion.
  - ![A lazy phoque](programs/assets/lazyphoque.jpg)
## [Contact](#contact)
  - Nguyen Son Hoang - Development and Design - sonhoangn@yahoo.com
  - Le Thi Dieu Ly - Testing and providing feedback - dieulylt@gmail.com
  
  

