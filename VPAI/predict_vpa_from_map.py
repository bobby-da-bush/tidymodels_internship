from fastai.vision.all import *
import torch
import re

# First verify GPU is available and being used
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU device: {torch.cuda.get_device_name(0)}")
else:
    raise SystemError("This script requires GPU")

# Force fastai to use GPU
defaults.device = torch.device('cuda')

bin_labels = ["0-500k", "500k-1M", "1M-5M", "5M-10M", "10M-Inf"]
def label_func(file_path):
    match = re.search(r'_(\d+)', str(file_path))
    if match:
        value = int(match.group(1))
        if value <= 500000:
            return bin_labels[0]
        elif value <= 1000000:
            return bin_labels[1]
        elif value <= 5000000:
            return bin_labels[2]
        elif value <= 10000000:
            return bin_labels[3]
        else:
            return bin_labels[4]
    return "Unknown"

path = "parcel_maps"
files = get_image_files(path)
dls = ImageDataLoaders.from_name_func(path, files, label_func, item_tfms=Resize(256))
learn = vision_learner(dls, resnet34, metrics=error_rate)

# Verify learner is using GPU
print(f"Learner device: {learn.dls.device}")

learn.fine_tune(10, 3e-5)
learn.show_results()