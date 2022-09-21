import torch
from torchmetrics import Accuracy, F1Score, MetricCollection
from torch.optim.lr_scheduler import ReduceLROnPlateau

import pytorch_lightning as pl
import torch.nn as nn
import timm


CLASSES = 120


class LitModel(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b0_ns', pretrained=True):
        super().__init__()
        self.model = timm.create_model(model_name, pretrained=pretrained)
        
        for param in self.model.parameters():
            param.requires_grad = False
        
        in_features = self.model.get_classifier().in_features
        self.model.classifier = nn.Sequential(
            nn.Linear(in_features, in_features),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(in_features, CLASSES)
        )

    def forward(self, x):
        return self.model(x)


class LitClassifier(pl.LightningModule):
    def __init__(self, learning_rate):
        super().__init__()
        self.criterion = nn.CrossEntropyLoss()
        metrics = MetricCollection([Accuracy(multiclass=True), F1Score(multiclass=True)])
        self.train_metrics = metrics.clone(prefix='train_')
        self.valid_metrics = metrics.clone(prefix='val_')
        self.learning_rate = learning_rate
        self.model = LitModel()
        self.save_hyperparameters()
        
    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        x = batch['image']
        y = batch['target']
        y_hat = self.model(x)

        loss = self.criterion(y_hat, y)
        output = self.train_metrics(y_hat, y)
        
        logs = {'train_loss': loss, 'train_metrics': output}

        self.log_dict(
            logs,
            on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return loss
    
    def validation_step(self, batch, batch_idx):
        x, y = batch
        x = batch['image']
        y = batch['target']
        y_hat = self.model(x)

        loss = self.criterion(y_hat, y)
        output = self.valid_metrics(y_hat, y)

        logs = {'val_loss': loss, 'val_metrics': output}
        
        self.log_dict(
            logs,
            on_step=False, on_epoch=True, prog_bar=True, logger=True
        )
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=(self.learning_rate))
        scheduler = ReduceLROnPlateau(optimizer, 'min', patience = 3)
        return {"optimizer": optimizer, "lr_scheduler": {"scheduler": scheduler, "monitor": "val_loss"}}
