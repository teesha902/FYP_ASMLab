# DeepLabCut Setup Guide

This README provides a full walkthrough for setting up and running DeepLabCut (DLC) to analyze behavioural videos.

<i>This guide is split into three parts: environment setup (macOS and GPU machines), running inference, and notes on post-processing.</i>

---
## Environment Installation & Setup Guide

This guide follows the latest DLC version as of **April 2025**, using **Python 3.10** and **DeepLabCut v3.0 (PyTorch backend)** 
<i> (already installed in Toothless) </i>

Official documentation: https://deeplabcut.github.io/DeepLabCut/docs/installation.html  
<i>Refer to this for advanced troubleshooting and the latest environment setup options.</i>

---

### Mac (M1)
Use your personal Mac for lightweight steps like **creating DLC projects**, **extracting/labeling frames**, and **post-processing small files**.

> ⚠️ Model training and full inference should **only be done on a GPU-equipped system (e.g., Toothless)**. Attempting these on a Mac may take several days and lead to overheating or crashes. This includes tasks like frame extraction and model training. 


#### 1. Install Anaconda (if not already installed)
**Miniconda3 is recommended for MacOS,** (lighter than full Anaconda) but either is fine.

Download and install from:
https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html

#### 2. Create and activate the DLC environment

1. Download the official `.yaml` file:  
   https://github.com/DeepLabCut/DeepLabCut/blob/main/conda-environments/DEEPLABCUT.yaml

2. Open terminal and navigate to the folder with the `.yaml`, then run:

```bash
conda env create -f DEEPLABCUT.yaml
conda activate DEEPLABCUT
```
This installs DLC and all required dependencies with the PyTorch backend, which is preferred on macOS.

#### 3. Launch DLC 
You can start DLC from the terminal with:

```bash
python -m deeplabcut
```

If you encounter errors related to pyqt or ffmpeg, try installing them separately (inside the conda environment):

```bash
conda install pyqt
conda install -c conda-forge ffmpeg
```

### GPU (Windows with CUDA) --> For Lab PC: Toothless

The latest DLC version should be up and running. However if you encoutner issues with version compatibilities and updates, refer to the guide below (which works for the version in April 2025). 

If updates are required, please update this guide as well.


#### 1. Install NVIDIA GPU Driver

First, install the correct **NVIDIA driver** for your GPU model: 
i. Go to the official NVIDIA driver download page: https://www.nvidia.com/Download/index.aspx
ii. Select your GPU model (check via **Device Manager > Display adapters**)
iii. Download and install the driver shown

After installation, open **Command Prompt** and type:

```bash
nvidia-smi
```
> This command should show GPU details. If you see "driver not found" or an error, your driver isn't set up properly.
    
    
#### 2. Install CUDA Toolkit (not cudnn)

i. Visit the official CUDA download page:https://developer.nvidia.com/cuda-downloads
ii. Follow the prompts to download the recommended version for Windows (default options are fine)
iii. Run the installer and complete the installation

After installing, check if it worked by running this command:

To verify CUDA after installation:
```bash
nvcc -V
```
You should see a message showing your installed CUDA version (e.g., "release 11.8").

⚠️ Note: You don’t need to install cuDNN manually — it's already included in the DeepLabCut environment you'll set up later.


#### 3. Install Anaconda for Windows
Download and install the Anaconda Distribution: https://www.anaconda.com/products/distribution#windows


#### 4. Create a Python environment
Open **Anaconda Prompt**, (not the Command Prompt) and run: 

```bash
conda create -n DEEPLABCUT python=3.10
conda activate DEEPLABCUT
```
    
#### 5. Install PyTorch with CUDA Support
Use PyTorch’s install command for your CUDA version. For CUDA 11.8:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
You can confirm GPU access with:

```bash
import torch
print(torch.cuda.is_available())  # Should return True
```
    
#### 6. Install DeepLabCut
Once PyTorch is installed, install DLC with GUI support:

```bash
pip install deeplabcut[gui]
```

#### 7. Launch DLC 
Now you can start DLC with:
```bash
python -m deeplabcut
```
      
##### With DLC up and running we can move onto the next steps...

---

## Project Workflow & Jupyter Notebooks


Depending on whether you’re starting fresh or using an existing model, follow one of the workflows below. Here, you can find step-by-step notebooks to guide both paths:

---

### A. Creating a New Project

Use the Jupyter notebook here:
[`DLC_Workflow_Guide.ipynb`](./DLC_Workflow_Guide.ipynb)

It contains:

- Creating a new DLC project
- Extracting & labeling frames
- Training a network (run on GPU only)
- Running inference

---

### B. Using an Inherited Model

Also in `DLC_Workflow_Guide.ipynb`, under **Section B**, you’ll find steps for:

- Loading an existing DLC config
- Verifying model files
- Running inference and generating labeled videos
- Generate labeled videos

---

##  Transferring Between Mac ↔ GPU PC

When switching between Mac and GPU PC (e.g., Toothless), be sure to copy the following:

| Folder/File       | Purpose |
|-------------------|---------|
| `config.yaml`     | All project metadata and paths |
| `labeled-data/` (if labelling was done)  | Manually labeled frames |
| `dlc-models/`     | Contains trained model (`pose_cfg.yaml`, snapshots, logs) | 
| `videos/`         | Input videos used for training/inference |

> ⚠️ You must recheck all paths in `config.yaml` after moving to another machine.

---

###  Post-Processing

After inference, use:
 [`Post_DLC.ipynb`](./Post_DLC.ipynb)

This notebook includes:
- Filtering low-confidence predictions
- Angle/trajectory computation
- Trial segmentation and alignment with stimulus events
- Summary metrics extraction (acceleration, trajectory, etc)
