# TwitterAnalyzer

Application for analyzing and processing text information in tweets using Machine learning techniques.

## Recommended setup
Clone this repository

#### Python version 
`python==3.8.1`

#### Virtual environment
    conda create -n analyzer python==3.8.1
    conda activate analyzer
    
#### Install 

Run this command to install package with `setup.py`

`pip install -e .`

or install just dependencies

`pip install -r requirements.txt`

## Usage
Gui has 3 main tabs
 - Tweet request
 - Tweet filtration
 - Tweet analysis
 
 
#
#### Layers
 
```
        1. Gui
        2. Celery
        3. Tweet operator
         /               \
        /                 \
4. Database operator    4. Api
```  
 