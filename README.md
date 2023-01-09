# Basic operations with Point Clouds

## Introduction

In this tutorial we will focus on working with Point Clouds using Supervisely SDK.

You will learn how to:

1. [Upload point clouds from local directory to Supervisely](#Upload-point-clouds-from-local-directory-to-Supervisely)
2. [Get information about Point Clouds and image contexts](#Get-information-about-Point-Clouds-and-image-contexts)
3. [Download point clouds and image contexts to local directory](#Download-point-clouds-and-image-contexts-to-local-directory)
6. [get and update image metadata](#get-and-update-image-metadata)
7. [remove images from Supervisely.](#remove-images-from-supervisely)

📗 Everything you need to reproduce [this tutorial is on GitHub](https://github.com/supervisely-ecosystem/tutorial-pointclouds): source code and demo data.

## How to debug this tutorial

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](../basics-of-authentication.md)

**Step 2.** Clone [repository](https://github.com/supervisely-ecosystem/tutorial-pointclouds) with source code and demo data and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

```
git clone https://github.com/supervisely-ecosystem/tutorial-pointclouds.git

cd tutorial-pointclouds

./create_venv.sh
```

**Step 3.** Open repository directory in Visual Studio Code.

```
code -r .
```

**Step 4.** Change workspace ID in `local.env` file by copying the ID from the context menu of the workspace.

```
context.workspaceId=654 # ⬅️ change value
```

<figure><img src="https://user-images.githubusercontent.com/79905215/209327856-e47fb82b-c207-48fc-bb36-1fe795d45f6f.png" alt=""><figcaption></figcaption></figure>

**Step 5.** Start debugging `src/main.py`.

### Import libraries

```python
import os
from dotenv import load_dotenv
import supervisely as sly
```

### Init API client

First, we load environment variables with credentials and init API for communicating with Supervisely Instance.

```python
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()
```

### Get variables from environment

In this tutorial, you will need an workspace ID that you can get from environment variables. [Learn more here](../environment-variables.md#workspace_id)

```python
workspace_id = sly.env.workspace_id()
```

## Create new project and dataset

Create new project.

**Source code:**

```python
project = api.project.create(workspace_id, name="Point Clouds Tutorial", type=sly.ProjectType.POINT_CLOUDS, change_name_if_conflict=True)

print(f"Project ID: {project.id}")
```

**Output:**

```python
# Project ID: 15599
```

Create new dataset.

**Source code:**

```python
dataset = api.dataset.create(project.id, name="dataset_1")

print(f"Dataset ID: {dataset.id}")
```

**Output:**

```python
# Dataset ID: 53465
```

## Upload point clouds from local directory to Supervisely

### Upload single point cloud.

**Source code:**

```python
pcd_file = "src/input/pcd/000000.pcd"
pcd_info = api.pointcloud.upload_path(dataset.id, name="pcd_0", path=pcd_file)
print(f'Point cloud "{pcd_info.name}" uploaded to Supervisely with ID:{pcd_info.id}')
```

**Output:**

```python
# Point cloud "pcd_0" uploaded to Supervisely platform with ID:17539453
```

<figure><img src="https://user-images.githubusercontent.com/79905215/209367792-2bd43e87-453f-4cba-9f41-9648a964658d.png" alt=""><figcaption></figcaption></figure>

### Upload context image to Supervisely.

**Source code:**

```python
img_file = "src/input/img/000000.png"
img_hash = api.pointcloud.upload_related_image(img_file)
img_info = {"entityId": pcd_info.id, "name": "img0", "hash": img_hash}
result = api.pointcloud.add_related_images([img_info])
print("Image context has uploaded.", result)
```

**Output:**

```python
# Image context has uploaded. {'success': True}
```

### Upload list of point clouds and iamge contexts.

✅ Supervisely API allows uploading multiple point clouds in a single request. The code sample below sends fewer requests and it leads to a significant speed-up of our original code.

**Source code:**

```python
paths = ["src/input/pcd/000001.pcd", "src/input/pcd/000002.pcd"]
img_paths = ["src/input/img/000001.png", "src/input/img/000002.png"]

pcd_infos = api.pointcloud.upload_paths(dataset.id, names=["pcd_1", "pcd_2"], paths=paths)
img_hashes = api.pointcloud.upload_related_images(img_paths)
img_infos = [{"entityId": pcd_infos[i].id, "name": f"img{i}", "hash": img_hashes[i]} for i in range(len(img_paths))]
result = api.pointcloud.add_related_images(img_infos)
print("Batch uploading has finihed:", result)
```

**Output:**

```python
# Batch uploading has finihed: {'success': True}
```

<figure><img src="https://user-images.githubusercontent.com/79905215/209367771-ff6d5852-f153-4529-9092-f58bcb45a3cc.png" alt=""><figcaption></figcaption></figure>


## Get information about Point Clouds and image contexts

### By point cloud's name

Get information about point cloud from Supervisely by name.

**Source code:**

```python
pcd_info = api.pointcloud.get_info_by_name(dataset.id, name="pcd_0")
print(pcd_info)
```

**Output:**

```python
PointcloudInfo(
    id=17553684,
    frame=None,
    description="",
    name="pcd_0",
    team_id=440,
    workspace_id=662,
    project_id=16108,
    dataset_id=54365,
    link=None,
    hash="rxl9ioCcNobe1z7q1dA6idsebCM77G0wlrZd1Be28ng=",
    path_original="/h5un6l2bnaz1vj8a9qgms4-public/point_clouds/f/x/kC/5JwCwSNouz7u3sNVDWOIURf44HRAridOKsf3lDGjo9bEHcj22gCejQIULbZHblG9Ns6GWD4Vmc3I0KdBagpmZKovKikN50Ij7utyw5aUaCTtM10sLiX4BVqPRssx.pcd",
    cloud_mime="image/pcd",
    figures_count=0,
    objects_count=0,
    tags=[],
    meta={},
    created_at="2023-01-08T07:15:50.332Z",
    updated_at="2023-01-08T07:15:50.332Z",
)
```

### By point cloud's ID

You can also get information about image from Supervisely by id.

**Source code:**

```python
pcd_info = api.pointcloud.get_info_by_id(pcd_info.id)
print("Point cloud name -", pcd_info.name)
```

**Output:**

```python
# Point cloud name - pcd_0
```

### Get information about image contexts

Get information about related image contexts, for example it can be a photo from front/back cameras of vehicle.

**Source code:**

```python
img_infos = api.pointcloud.get_list_related_images(pcd_info.id)
img_info = img_infos[0]
print(img_info)
```

**Output:**

```python
{'pathOriginal': '/h5un6l2bnaz1vj8a9qgms4-public/images/original/S/j/hJ/PwhtY7x4zRQ5jvNETPgFMtjJ9bDOMkjJelovMYLJJL2wxsGS9dvSjQC428ORi2qIFYg4u1gbiN7DsRIfO3JVBEt0xRgNc0vm3n2DTv8UiV9HXoaCp0Fy4IoObKMg.png',
 'id': 473302,
 'entityId': 17557533,
 'createdAt': '2023-01-09T08:50:33.225Z',
 'updatedAt': '2023-01-09T08:50:33.225Z',
 'meta': {'deviceId': 'cam_2'},
 'fileMeta': {'mime': 'image/png',
  'size': 893783,
  'width': 1224,
  'height': 370},
 'hash': 'vxA+emfDNUkFP9P6oitMB5Q0rMlnskmV2jvcf47OjGU=',
 'link': None,
 'preview': '/previews/q/ext:jpeg/resize:fill:50:0:0/q:50/plain/h5un6l2bnaz1vj8a9qgms4-public/images/original/S/j/hJ/PwhtY7x4zRQ5jvNETPgFMtjJ9bDOMkjJelovMYLJJL2wxsGS9dvSjQC428ORi2qIFYg4u1gbiN7DsRIfO3JVBEt0xRgNc0vm3n2DTv8UiV9HXoaCp0Fy4IoObKMg.png',
 'fullStorageUrl': 'https://dev.supervise.ly/h5un6l2bnaz1vj8a9qgms4-public/images/original/S/j/hJ/PwhtY7x4zRQ5jvNETPgFMtjJ9bDOMkjJelovMYLJJL2wxsGS9dvSjQC428ORi2qIFYg4u1gbiN7DsRIfO3JVBEt0xRgNc0vm3n2DTv8UiV9HXoaCp0Fy4IoObKMg.png',
 'name': 'img00'}
```


### Get list of all point clouds in the dataset.

You can list all point clouds in the dataset.

**Source code:**

```python
pcd_infos = api.pointcloud.get_list(dataset.id)
print(f"Dataset contains {len(pcd_infos)} point clouds")
```

**Output:**

```python
# The dataset contains 3 point clouds
```


## Download point clouds and image contexts to local directory

### Single point cloud

Download point cloud from Supervisely to local directory by id.

**Source code:**

```python
save_path = "src/output/pcd_0.pcd"
api.pointcloud.download_path(pcd_info.id, save_path)
print(f"Point cloud has been successfully downloaded to '{save_path}'")
```

**Output:**

```python
# Point cloud has been successfully downloaded to 'src/output/pcd_0.pcd'
```

### Single related image context

Download a related image context from Supervisely to local directory by image id.

**Source code:**

```python
save_path = "src/output/img_0.png"
img_info = api.pointcloud.get_list_related_images(pcd_info.id)[0]
api.pointcloud.download_related_image(img_info["id"], save_path)
print(f"Image context has been successfully downloaded to '{save_path}'")
```

**Output:**

```python
# Image context has been successfully downloaded to 'src/output/img_0.png'
```
