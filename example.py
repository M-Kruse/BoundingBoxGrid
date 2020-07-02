from BoundingBoxGrid import BoundingBoxGrid

print(
    """
    This example turns an image into a grid of bounding boxes 
    Various bounding boxes are created and tested against the grid bounding boxes for interesction.
    """)

test_boxes = []
b = BoundingBoxGrid()
#Get a list of bounding boxes in a grid 
bounding_grid_list = b.generate_bounding_box_grid_from_image("sample_4x4.jpeg",'output.jpeg', 4)
#Generate some test bounding boxes to compare against the grid boxes
test_boxes.append(b.generate_bounding_box('output.jpeg', 150, 125, 250, 200, box_id="A"))
test_boxes.append(b.generate_bounding_box('output.jpeg',80, 0, 200, 110, box_id="B"))
test_boxes.append(b.generate_bounding_box('output.jpeg',200, 240, 300, 300, box_id="C"))
test_boxes.append(b.generate_bounding_box('output.jpeg',0, 0, 300, 300, box_id="D"))
#Loop through the example boxes
for test_box in test_boxes:
    first = True
    #Loop through the grid boxes
    for grid_box in bounding_grid_list:
        #Test if the boxes interesect
        if b.do_bounding_boxes_intersect(test_box, grid_box):
            if first:
                print("Detected intersection for box {}".format(test_box.label))
                first = False
            print("Grid Coordinates: {}".format(grid_box.grid_coord))

    