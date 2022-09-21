#!/usr/bin/env python3


import os
import pytorch_lightning as pl
from pytorch_lightning.callbacks import RichProgressBar
from pathlib import Path
from datetime import datetime
from pets.pets_datamodule import PetsDataset, PetsDataModule
from pets.pets_model import LitClassifier
from pets.pets_utils import is_valid, augmentation


# Download data
os.system(f"kaggle datasets download jessicali9530/stanford-dogs-dataset -p . --unzip")

ROOT = Path("images/Images/")

if __name__ == "__main__":
    # Dataset
    dset = PetsDataset(data_dir=ROOT, transforms=augmentation)
    index = is_valid(dset.files, dset.target_dict)
    
    # DataModule
    pets = PetsDataModule(ROOT, 64, index, dset)
    
    # Model
    model = LitClassifier(learning_rate=0.001)
    
    # Trainer
    trainer = pl.Trainer(max_epochs=5, 
                     accelerator='auto',
                     devices=1, 
                     precision=16,
                     enable_progress_bar=True,
                     callbacks=[RichProgressBar()])
    # Fit
    trainer.fit(model, pets)
