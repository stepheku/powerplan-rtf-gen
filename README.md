# Powerplan RTF Generator

This set of scripts helps with generating RTF-type extracts of PowerPlans, rather than having to go into each PowerPlan from the PowerPlan tool and go to the Print/Save function

## Installation
Make sure `pip` and `venv` is installed and create a virtual environment
```
cd powerplan_rtf_gen

python -m venv venv
```

Then activate the virtual environment
```
venv\Scripts\Activate

# For Linux
source ./venv/bin/activate
```

Then install the dependencies
```
pip install -r requirements.txt
```

## Usage
When all of the dependencies are installed, run all of the queries in the `ccl_queries/` folder and save the results as CSV files in the main folder so it can be referenced later

Finally run:
```
python create_powerplan_doc.py ^
--pathways-file pathways.csv ^
--components-file components.csv ^
--order-comments-file order_comments.csv ^
--domain P0783
```