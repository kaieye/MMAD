import os
import shutil
import matplotlib
import matplotlib.pyplot as plt
import nibabel as nib
from glob import glob
import numpy as np
from tqdm import tqdm
matplotlib.use('Agg')

def get_all_files_in_directory(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files
def move_files_to_destination(files, destination_directory):
    for file_path in files:
        destination_path = os.path.join(destination_directory, os.path.basename(file_path))
        shutil.move(file_path, destination_path)

def delete_all_subfolders(folder_path):
    try:
        subfolders = [f.path for f in os.scandir(folder_path) if f.is_dir()]
        for subfolder in subfolders:
            shutil.rmtree(subfolder)
        print('sucess!')
    except Exception as e:
        print(f"failed: {e}")

def normalize(data):
    data = data / np.mean(data)
    data = np.clip(data, 0, 8)
    return data

def show_scan(data, filename,target):
    image_name = filename.replace('npy', 'jpg')
    vmin, vmax = 0, 8
    cmap = 'viridis'
    plt.subplot(1, 3, 1)
    img = plt.imshow(data[100, :, :], vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar(img, fraction=0.07)
    plt.title('Sagittal Slice')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    plt.subplot(1, 3, 2)
    img = plt.imshow(data[:, 100, :], vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar(img, fraction=0.07)
    plt.title('Coronal Slice')
    plt.xlabel('X')
    plt.ylabel('Z')
    
    plt.subplot(1, 3, 3)
    img = plt.imshow(data[:, :, 100], vmin=vmin, vmax=vmax, cmap=cmap)
    plt.colorbar(img, fraction=0.05)
    plt.title('Axial Slice')
    plt.xlabel('Y')
    plt.ylabel('Z')
    
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.7)

    plt.savefig(target+image_name)
    plt.close()


directory_path = "/gemini/code/ADNI/"
target_path = "/gemini/code/ADNI/"
npy_target = "/gemini/code/ADNInpy/"


all_files_in_directory = get_all_files_in_directory(directory_path)
move_files_to_destination(all_files_in_directory, target_path)
if directory_path==target_path:
    delete_all_subfolders(directory_path)

if not os.path.exists(npy_target):
    os.mkdir(npy_target)

fileList = glob(target_path+'*.nii')

for file in tqdm(fileList):
    data = np.asanyarray(nib.load(file).dataobj)
    filename = file.split('/')[-1].replace('.nii', '.npy')
    data = normalize(data)
    np.save(npy_target+filename, data)
    show_scan(data, filename,npy_target)
