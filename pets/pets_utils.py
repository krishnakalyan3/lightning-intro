import albumentations as A
from albumentations.pytorch import ToTensorV2

def is_valid(files, target_dict, split_pct = .2):
    split_class = {j:0 for j in target_dict}
    train_idx = []
    val_idx = []
    
    # Calculate number of images perclass
    for i in files:
        class_name = i.parent.name
        split_class[class_name] += 1
    
    # Calculate percentage
    for i in split_class:
        split_class[i] = int(split_class[i]*split_pct)
    
    for idx, i in enumerate(files):
        class_name = i.parent.name
        
        if split_class[class_name] == 0:
            train_idx.append(idx)
        else:
            val_idx.append(idx)
            split_class[class_name] -= 1
    
    return train_idx, val_idx

augmentation = A.Compose([
            A.Resize(225, 225),
            A.HorizontalFlip(0.5),
            A.VerticalFlip(),
            A.RandomRotate90(),
            A.Rotate(10),
            A.ColorJitter(0.2,0.2,0,0),
            A.Normalize(),
            ToTensorV2(p=1.0),
        ], p=1.0)
