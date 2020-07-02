
import time

import cv2

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
matplotlib.use("Agg")

try:
    from PIL import Image
except ImportError:
    import Image

class BoundingBox(object):
    """docstring for BoundingBox"""
    def __init__(self, top, left, bottom, right, grid_coord=None, label=None):
        super(BoundingBox, self).__init__()
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        if grid_coord:
            self.grid_coord = grid_coord
        if label:
            self.label = label

class BoundingBoxGrid(object):
    """docstring for BoundingBoxGrid"""
    def __init__(self):
        super(BoundingBoxGrid, self).__init__()
        self.debug_mode = True
        
    def generate_bounding_box_grid_from_image(self, image, output_file, grid_count):
        """
        Creates a grid of bounding boxes against an image
        Inputs: Path to image file || Path to output file || number of grids to divide image into || Debug mode 
        Returns: List of BoundingBox() objects which form the grid
        """
        bounding_box_grid_list = []
        image = Image.open(image)
        #print(image.size)
        my_dpi = 200.
        fig = plt.figure(
            figsize=(
                float(image.size[0]) / my_dpi, float(image.size[1]) / my_dpi), dpi=my_dpi)
        ax = fig.add_subplot(111)
        fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
        # Set the grid size
        grid_size = image.size[0] / grid_count
        loc = plticker.MultipleLocator(base=grid_size)
        ax.xaxis.set_major_locator(loc)
        ax.yaxis.set_major_locator(loc)
        # Add the grid
        ax.grid(which='major', axis='both', linestyle='-', color='b')
        # Add the image
        ax.imshow(image)
        # Get the number of x/y grid elements
        x_grids=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(grid_size)))
        y_grids=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(grid_size)))
        #print(x_grids, y_grids)
        #Loop through the grids and generate bounding boxes for each of them
        y_min = 0
        y_max = int(grid_size)
        for j in range(y_grids):
            y = grid_size / 2 + j * grid_size
            x_min = 0
            x_max = int(grid_size)
            for i in range(x_grids):
                x = grid_size / 2. + float(i) * grid_size
                ax.text(x,y,'{0},{1}'.format(j,i),color='w',ha='center',va='center')
                if i == 0:
                    box = self.generate_bounding_box(
                        'output.jpeg',
                        x_min,
                        y_min,
                        x_max,
                        y_max,
                        (j,i),
                        wait=False
                    )
                else:
                    x_min = int( x_min + grid_size)
                    x_max = int(x_max + grid_size)
                    #print(x_min, y_min, x_max, y_max)
                    box = self.generate_bounding_box(
                        'output.jpeg',
                        x_min,
                        y_min,
                        x_max,
                        y_max,
                        (j,i),
                        wait=False
                    )
                bounding_box_grid_list.append(box)
            y_min = int( y_min + grid_size)
            y_max = int( y_max + grid_size)
        if output_file:
            fig.savefig(output_file, dpi=my_dpi)
        return bounding_box_grid_list

    def generate_bounding_box(self, image, x_min, y_min, x_max, y_max, grid_coord=None, wait=True, draw=True, box_id=None):
        """
        Draws a bounding box onto an image and creates a BoundingBox() object
        Inputs: Image file || x/y min/max positions || cartesian grid coordinates || Bool for indicating wait for keypress
        Returns: A BoundinBox() object
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (0, 255, 0)
        thickness = 2
        fontScale = 1
        if draw:
            image = cv2.imread(image, 1)
            # Draw the bounding box
            x_offset = int(abs(x_max - x_min) / 2.5)
            y_offset = int(abs(y_max - y_min) / 2.5)
            x_offset = x_min + x_offset
            y_offset = y_min + y_offset
            org = (x_offset, y_offset)
            cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0), 1)
            if box_id:
                cv2.putText(image, box_id, org, font,  
                       fontScale, color, thickness, cv2.LINE_AA) 
            if self.debug_mode:
                cv2.imshow("Bounds", image)
                if wait:
                    cv2.waitKey()
        #https://stackoverflow.com/questions/25642532/opencv-pointx-y-represent-column-row-or-row-column
        return BoundingBox(-x_min, y_min, -x_max, y_max, grid_coord, box_id)

    #https://gamedev.stackexchange.com/questions/586/what-is-the-fastest-way-to-work-out-2d-bounding-box-intersection
    def do_bounding_boxes_intersect(self, box_a, box_b):
        """ 
        Tests if two bounding boxes are overlapping
        Input: Two BoundingBox() objects
        Returns: Bool 
        """
        return not (
            box_b.left > box_a.right or \
            box_b.right < box_a.left or \
            box_b.top < box_a.bottom or \
            box_b.bottom > box_a.top
        )        
