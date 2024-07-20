import cv2

class PlazaEnv():
    def __init__(self, map_filepath):

        self.map_filepath = map_filepath

        self.map_image = cv2.imread(self.map_filepath, cv2.IMREAD_GRAYSCALE)
        self.map_image_3channel = cv2.cvtColor(self.map_image, cv2.COLOR_GRAY2BGR)
        _, self.binary_map = cv2.threshold(self.map_image, 128, 255, cv2.THRESH_BINARY)
        self.map_data = (self.binary_map // 255).astype(int)  # Convert to binary map

        self.map_height, self.map_width = self.map_data.shape
