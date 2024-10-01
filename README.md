# 13-14-devops-bootcamp__python_automation
coming up

<b><u>The course examples are:</u></b>
1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs

<b><u>The exercise projects are:</u></b>

## Setup

### 1. Pull SCM

Pull the repository locally by running
```bash
git clone https://github.com/hangrybear666/13-14-devops-bootcamp__python_automation.git
```
### 2. Install python3 on your development machine

For debian 12 it is already preinstalled.

## Usage (course examples)

<details closed>
<summary><b>1. Simple Python scripts for parsing cli user inputs, manipulating xlsx files and interacting with REST APIs</b></summary>

#### a. Enter venv and install dependencies
```bash
python3 -m venv $HOME/.venv
source $HOME/.venv/bin/activate
cd 01-python-basics/
pip install -r requirements.txt
```

#### b. Execute basic demo modules
```bash
python src/countdown.py
python src/csv-manipulation.py
python src/http-requests.py
```

#### c. Freeeze dependencies in requirements file in case you made any changes and exit venv

```bash
cd 01-python-basics/
pip freeze > requirements.txt
deactivate
```

</details>

-----