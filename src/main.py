import os
from dotenv import load_dotenv
import supervisely as sly


load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))

api = sly.Api()

workspace_id = sly.env.workspace_id()

# Create new Supervisely project.
project = api.project.create(workspace_id, "Point Clouds Tutorial", type=sly.ProjectType.POINT_CLOUDS, change_name_if_conflict=True)
print(f"Project ID: {project.id}")

# Create new Supervisely dataset.
dataset = api.dataset.create(project.id, "dataset_1")
print(f"Dataset ID: {dataset.id}")

# File paths
# pcd_file = "src/input/pcd/000000.pcd"
# img_file = "src/input/img/000000.png"
# calib_file = "src/input/calib/000000.txt"
# label_file = "src/input/label/000000.txt"

# Upload point cloud from local directory to Supervisely platform.
pcd_file = "src/input/pcd/000000.pcd"
pcd_info = api.pointcloud.upload_path(dataset.id, name="pcd_0", path=pcd_file)
print(f'Point cloud "{pcd_info.name}" uploaded to Supervisely with ID:{pcd_info.id}')

# Upload a related context image to Supervisely.
img_file = "src/input/img/000000.png"
img_hash = api.pointcloud.upload_related_image(img_file)
img_info = {"entityId": pcd_info.id, "name": "img0", "hash": img_hash}
result = api.pointcloud.add_related_images([img_info])
print("Context image has been uploaded.", result)


# Upload batch
paths = ["src/input/pcd/000001.pcd", "src/input/pcd/000002.pcd"]
img_paths = ["src/input/img/000001.png", "src/input/img/000002.png"]
pcd_infos = api.pointcloud.upload_paths(dataset.id, names=["pcd_1", "pcd_2"], paths=paths)
img_hashes = api.pointcloud.upload_related_images(img_paths)
img_infos = [{"entityId": pcd_infos[i].id, "name": f"img{i}", "hash": img_hashes[i]} for i in range(len(img_paths))]
result = api.pointcloud.add_related_images(img_infos)
print("Batch uploading has finihed:", result)


# Get point cloud info by name
pcd_info = api.pointcloud.get_info_by_name(dataset.id, name="pcd_0")
print(pcd_info)

# Get point cloud info by id
pcd_info = api.pointcloud.get_info_by_id(pcd_info.id)
print("Point cloud name:", pcd_info.name)

# Get image context info
img_infos = api.pointcloud.get_list_related_images(pcd_info.id)
img_info = img_infos[0]
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


# Update meta
###

# Remove
### NotImplementedError
api.pointcloud.remove(img_infos[0]["id"])
api.pointcloud.remove_batch([img_infos[0]["id"]])


# Point Cloud Episodes

# Create new Supervisely project.
# project = api.project.create(workspace_id, "Point Cloud Episodes Tutorial", type=sly.ProjectType.POINT_CLOUD_EPISODES, change_name_if_conflict=True)
# print(f"Project ID: {project.id}")

# # Create new Supervisely dataset.
# dataset = api.dataset.create(project.id, "dataset_1")
# pcd_info = api.pointcloud_episode.upload_path(dataset.id, "pcd_0", "src/input/pcd/000000.pcd")
