import pytorch_lightning as pl
from torchvision import transforms as T
from PIL import Image
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.utils.data import Subset


class PetsDataset(Dataset):
    def __init__(self, 
                 data_dir: str = None,
                 transforms = T.Compose([T.Resize((225, 225)), T.ToTensor(), T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])):
        super().__init__()
        self.files = [i for i in data_dir.glob("*/*.jpg")]
        self.transforms = transforms
        self.target_dict = {k.name:i for i,k in enumerate(data_dir.iterdir())}
        self.inverse_target = {i:k.name for i,k in enumerate(data_dir.iterdir())}

    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        img_path  = self.files[idx]
        img = Image.open(img_path).convert("RGB")
        
        if self.transforms:
            img = np.array(img)
            img = self.transforms(image=img)['image']

        return {'image':img, 'target': self.target_dict[img_path.parent.name]}


class PetsDataModule(pl.LightningDataModule):
    def __init__(self, data_dir, batch_size, index, dset):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        (self.train_idx, self.val_idx) = index
        self.dset = dset

    def train_dataloader(self):
        train_dset = Subset(self.dset, self.train_idx)
        return DataLoader(train_dset, batch_size=self.batch_size, pin_memory=True, shuffle=True, num_workers=2)
    
    def val_dataloader(self):
        val_dset = Subset(self.dset, self.val_idx)
        return DataLoader(val_dset, batch_size=self.batch_size, num_workers=1)