# How to create a local conda environment

Create a new conda environment using the following commands:

```cli
conda create -n langsmith Python=3.9
conda activate langsmith
```

(Optional) If you would like to do experimentation in Jupyter, use the following commands to extend just created environment:

```cli
conda install ipykernel
python -m ipykernel install --user --name langsmith --display-name "Python (langsmith)"
conda install jupyter
```

Install required packages:

```cli
pip install --upgrade -r requirements.txt
```