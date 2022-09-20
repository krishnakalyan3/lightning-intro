

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

### API
Try out the swagger API. Add a command using `/command/add`

https://*.litng.ai/docs

### Connect

```
lightning connect 01gdd5e39n6bvx8thv9sy3p3re 
lightning add --cmd=hello
lightning disconnect
```

### Links
- [Getting Started](https://lightning.ai/lightning-docs/get_started/lightning_apps_intro.html)
- [CLI Server](https://lightning.ai/lightning-docs/workflows/build_command_line_interface/cli.html?highlight=cli)
