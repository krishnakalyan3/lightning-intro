

### Creating Virtual Environment

```
conda create -n addemo python=3.9
conda activate addemo
pip install -r requirements.txt
```

### Deployment

```
# Running App locally (Testing)
python -m lightning run app app.py --open-ui false

# Running App on the cloud 
python -m lightning run app app.py --cloud --open-ui false
```