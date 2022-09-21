### Creating Virtual Environment
This is a demo lightning app that gradually shows us how to build lightning applications step by step.

```
conda create -n addemo python=3.9
conda activate addemo
pip install -r requirements.txt
```

### Deployment
Lightning apps can be tested locally or on the cloud. In this repository we have two applications (`app.py` and `ml.py`). 

```
# Running App locally (Testing)
python -m lightning run app app.py --open-ui false

# Running App on the cloud 
lightning run app app.py --cloud --open-ui false
```

### Usage
Try out the swagger (https://*.litng.ai/docs) API. Add a command using `/command/add`. `cmd` with string `start` will create a new work and `stop` will stop the existing work.

```
lightning list apps
lightning connect app_name 
lightning add --cmd=hello

lightning add --cmd=start
lightning add --cmd=stop
lightning disconnect
```

### Deploying ML Pipeline
In this application we will use `CLI commands` to train a model followed by creating a Gradio application. Gradio model downloads the model weights from Weights and Biases.

```
lightning run app ml.py --cloud --open-ui false --env WANDB_API_KEY=$WANDB_API_KEY \
--env KAGGLE_USERNAME=$KAGGLE_USERNAME --env KAGGLE_KEY=$KAGGLE_KEY \
--name ml

lightning list apps
lightning connect ml

# Train pipeline
lightning av --cmd=train

# Gradio pipeline
lightning av --cmd=deploy

# Stop pipeline
lightning av --cmd=stop

lightning disconnect
```

### Related Links
- [Getting Started](https://lightning.ai/lightning-docs/get_started/lightning_apps_intro.html)
- [CLI](https://lightning.ai/lightning-docs/glossary/command_lines/command_lines.html)
- [CLI Server](https://lightning.ai/lightning-docs/workflows/build_command_line_interface/cli.html)
- [Training Script](https://github.com/Lightning-AI/lightning-hpo/blob/master/examples/scripts/train.py)
