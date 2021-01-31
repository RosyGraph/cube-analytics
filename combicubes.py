import csv
import os
import datetime
from canalytics import get_cube_list

cube_list_filenames = os.listdir("./cube_lists")

cube_lists = [
    get_cube_list(os.path.join("cube_lists", filename))
    for filename in cube_list_filenames
]

for c in cube_lists[1:]:
    cube_lists[0].update(c)

cube_list = cube_lists[0]
print(cube_list)
current_date = str(datetime.datetime.now()).split()[0]
new_cube_list_filename = "cube-list_comprehensive_" + current_date + ".csv"
qualified_cubelist_path = os.path.join("cube_lists", new_cube_list_filename)

with open(qualified_cubelist_path, "w") as f:
    csv_writer = csv.writer(f)
    for k, v in cube_list.items():
        csv_writer.writerow([k, v])
