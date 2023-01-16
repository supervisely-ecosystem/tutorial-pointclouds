import os
import json
from dotenv import load_dotenv
import supervisely as sly
from pathlib import Path


# File paths
# pcd_file = "src/input/pcd/000000.pcd"
# img_file = "src/input/img/000000.png"
# calib_file = "src/input/calib/000000.txt"
# label_file = "src/input/label/000000.txt"

load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

workspace_id = sly.env.workspace_id()

# Create new Supervisely project.
project = api.project.create(
    workspace_id,
    name="Point Clouds Tutorial",
    type=sly.ProjectType.POINT_CLOUDS,
    change_name_if_conflict=True,
)
print(f"Project ID: {project.id}")

# Create new Supervisely dataset.
dataset = api.dataset.create(project.id, "dataset_1")
print(f"Dataset ID: {dataset.id}")


# Upload point cloud to Supervisely platform.
pcd_file = "src/input/pcd/000000.pcd"
pcd_info = api.pointcloud.upload_path(dataset.id, name="pcd_0", path=pcd_file)
print(f'Point cloud "{pcd_info.name}" uploaded to Supervisely with ID:{pcd_info.id}')


# Upload related context image to Supervisely.
# input files:
img_file = "src/input/img/000000.png"
cam_info_file = "src/input/cam_info/000000.json"

# 0. Read cam_info with matrices (meta dict).
with open(cam_info_file, "r") as f:
    cam_info = json.load(f)

# 1. Upload an image to the Supervisely. It generates us a hash for image
img_hash = api.pointcloud.upload_related_image(img_file)
# 2. Create img_info needed for matching the image to the point cloud by its ID
img_info = {"entityId": pcd_info.id, "name": "img_0", "hash": img_hash, "meta": cam_info}
# 3. Run the API command to attach the image
api.pointcloud.add_related_images([img_info])

print("Context image has been uploaded.")


# Upload a batch of point clouds and related images
paths = ["src/input/pcd/000001.pcd", "src/input/pcd/000002.pcd"]
img_paths = ["src/input/img/000001.png", "src/input/img/000002.png"]
cam_paths = ["src/input/cam_info/000001.json", "src/input/cam_info/000002.json"]

pcd_infos = api.pointcloud.upload_paths(dataset.id, names=["pcd_1", "pcd_2"], paths=paths)
img_hashes = api.pointcloud.upload_related_images(img_paths)
img_infos = []
for i, cam_info_file in enumerate(cam_paths):
    # reading cam_info
    with open(cam_info_file, "r") as f:
        cam_info = json.load(f)
    img_info = {
        "entityId": pcd_infos[i].id,
        "name": f"img_{i}",
        "hash": img_hashes[i],
        "meta": cam_info,
    }
    img_infos.append(img_info)
result = api.pointcloud.add_related_images(img_infos)
print("Batch uploading has finished:", result)


# Get point cloud info by name
pcd_info = api.pointcloud.get_info_by_name(dataset.id, name="pcd_0")
print("Get point cloud info:")
print(pcd_info)

# Get point cloud info by id
pcd_info = api.pointcloud.get_info_by_id(pcd_info.id)
print("Point cloud name:", pcd_info.name)

# Get context image info
img_infos = api.pointcloud.get_list_related_images(pcd_info.id)
img_info = img_infos[0]
print("Get context image info:")
print(img_info)

# Get list of all point clouds in the dataset
pcd_infos = api.pointcloud.get_list(dataset.id)
print(f"Dataset contains {len(pcd_infos)} point clouds")


# Download point clouds
save_path = "src/output/pcd_0.pcd"
api.pointcloud.download_path(pcd_info.id, save_path)
print(f"Point cloud has been successfully downloaded to '{save_path}'")

# Download related context image
save_path = "src/output/img_0.png"
img_info = api.pointcloud.get_list_related_images(pcd_info.id)[0]
api.pointcloud.download_related_image(img_info["id"], save_path)
print(f"Context image has been successfully downloaded to '{save_path}'")


### Point Cloud Episodes

# Create new Supervisely project.
project = api.project.create(
    workspace_id,
    name="Point Cloud Episodes Tutorial",
    type=sly.ProjectType.POINT_CLOUD_EPISODES,
    change_name_if_conflict=True,
)
print(f"Project ID: {project.id}")

# Create new Supervisely dataset.
dataset = api.dataset.create(project.id, "dataset_1")
print(f"Dataset ID: {dataset.id}")


# Upload one point cloud to Supervisely.
# meta = {"frame": 0}  # "frame" is a required field for Episodes
# pcd_info = api.pointcloud_episode.upload_path(dataset.id, "pcd_0", "src/input/pcd/000000.pcd", meta=meta)
# print(f'Point cloud "{pcd_info.name}" (frame={meta["frame"]}) uploaded to Supervisely')


# Upload entire point clouds episode to Supervisely platform.
def read_cam_info(cam_info_file):
    with open(cam_info_file, "r") as f:
        cam_info = json.load(f)
    return cam_info


# 1. get paths
input_path = "src/input"
pcd_files = list(Path(f"{input_path}/pcd").glob("*.pcd"))
img_files = list(Path(f"{input_path}/img").glob("*.png"))
cam_info_files = Path(f"{input_path}/cam_info").glob("*.json")

# 2. get names and metas
pcd_metas = [{"frame": i} for i in range(len(pcd_files))]
img_metas = [read_cam_info(cam_info_file) for cam_info_file in cam_info_files]
pcd_names = list(map(os.path.basename, pcd_files))
img_names = list(map(os.path.basename, img_files))

# 3. upload
pcd_infos = api.pointcloud_episode.upload_paths(dataset.id, pcd_names, pcd_files, metas=pcd_metas)
img_hashes = api.pointcloud.upload_related_images(img_files)
img_infos = [
    {"entityId": pcd_infos[i].id, "name": img_names[i], "hash": img_hashes[i], "meta": img_metas[i]}
    for i in range(len(img_hashes))
]
api.pointcloud.add_related_images(img_infos)

print("Point Clouds Episode has been uploaded to Supervisely")
