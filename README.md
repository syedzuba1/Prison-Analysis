# Project Submission - Phase 3

**Prison Data Analysis Project**  
**Authors**: FNU Syed Zubair Ahmed - 50560739, Apoorv Sood - 50599568, Jainam Manish Jain-50606698 , Kalash Thakur -50560545 
**Project Name**: Predicting Crime Rates and Enhancing Resource Allocation Strategies Using Prison Data  
**Professor Name**: Prof. Chen Xu  

---

## Team Members and Questions 

| Team Member           | Question                                                                                                     | Code Location                       | Report Location                   |
|-----------------------|-------------------------------------------------------------------------------------------------------------|-------------------------------------|-------------------------------------|
| Jainam Manish Jain     | Rates of Escape and Mental Illness vs. Educational Infrastructure: Identify relationships between inmate education programs and outcomes. | `predictions/views.py` - line 149 function-predict_view_2 | page 2|
|  FNU Syed Zubair Ahmed         | Proportion of Undertrial vs. Convicted Inmates Across States and Crimes: Analyze judicial inefficiencies.    | `predictions/views.py` - line 197 function-predict_view_3 | page 5 |
| Kalash Thakur | Predicting Prison Budget Allocations: Explore historical overcapacity and expenditure data for insights.    | `predictions/views.py` - line 245 function-predict_view_4 | page 7  |
| Apoorv Sood            | Demographic Analysis of Inmate Populations: Classify inmates as undertrial or convicted by demographics.     | `predictions/views.py` - line 102 function-predict_view_1 | page 9 |

---

## Project Structure
- **README.md**: Contains project details, team member contributions, and folder structure.
- **app/**: contains django code for project.
- **exp/**: python notebook code for ML models being used.
- **requirements.txt**: Python dependencies for the project.
./
|-- Prison_Analysis_Report.pdf
|-- app/
|   |-- Prison_Analysis/
|   |   |-- README.md
|   |   |-- requirements.txt
|   |   |-- static/
|   |   |   |-- images/
|   |   |   |   |-- [image files]
|   |   |   |-- admin/
|   |   |   |   |-- [CSS, JS, and other static files]
|   |   |-- Prison_Analysis/
|   |   |   |-- settings.py
|   |   |   |-- urls.py
|   |   |-- predictions/
|   |   |   |-- models/
|   |   |   |-- templates/
|   |   |   |-- views.py
|-- exp/
|   |-- Dataset/
|   |   |-- [dataset files]
|-- requirements.txt
|-- directory_structure.txt

## Instructions to Build the App

Follow the steps below to set up and run the application locally with Django and ensure scikit-learn version 1.5.1 is installed.Make sure you have python 3.12

1. **Clone the Repository**:
   - Clone the project repository from GitHub:
     ```bash
     git clone https://github.com/apoorvso/Prison_Analysis.git
     ```
   - Navigate into the project directory:
     ```bash
     cd your-repo
     ```

2. **Create a Virtual Environment (Recommended)**:
   It's best to use a virtual environment to manage dependencies. Run the following commands:
   - For Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - For macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Required Dependencies**:
   - Install the required Python dependencies listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

4. **Ensure scikit-learn version 1.5.1**:
   - Check the currently installed version of scikit-learn:
     ```bash
     pip show scikit-learn
     ```
   - If the installed version is not 1.5.1, you can install the correct version using:
     ```bash
     pip install scikit-learn==1.5.1
     ```

5. **Run Database Migrations**:
   - Apply the database migrations to set up the database schema:
     ```bash
     python manage.py migrate
     ```

6. **Start the Django Development Server**:
   - Run the Django development server:
     ```bash
     python manage.py runserver
     ```
   - The application will be available at `http://127.0.0.1:8000/` in your browser.

7. **Access the Application**:
   - Open your browser and go to `http://127.0.0.1:8000/` to access the application locally.

---
