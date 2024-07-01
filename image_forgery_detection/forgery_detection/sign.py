import cv2
import numpy as np
from PIL import Image
class FeatureMatching:
    def __init__(self, image1_data, image2_data):
        self.img1 = cv2.imdecode(np.frombuffer(image1_data, np.uint8), cv2.IMREAD_COLOR)
        self.img2 = cv2.imdecode(np.frombuffer(image2_data, np.uint8), cv2.IMREAD_COLOR)

    def preprocess_images(self):
        self.img1 = cv2.cvtColor(self.img1, cv2.COLOR_BGR2GRAY)
        self.img1 = cv2.resize(self.img1, (800, 600))
        self.img2 = cv2.cvtColor(self.img2, cv2.COLOR_BGR2GRAY)
        self.img2 = cv2.resize(self.img2, (800, 600))

    def find_features(self):
        self.sift = cv2.SIFT_create(nfeatures=500, nOctaveLayers=5, contrastThreshold=0.09, edgeThreshold=11, sigma=1.8)
        self.kp1, self.des1 = self.sift.detectAndCompute(self.img1, None)
        self.kp2, self.des2 = self.sift.detectAndCompute(self.img2, None)

    def match_features(self):
        bf = cv2.BFMatcher()
        self.matches = bf.knnMatch(self.des1, self.des2, k=3)

    def filter_matches(self):
        self.good_matches = []
        for match_list in self.matches:
            m, n = match_list[:2]
            if m.distance < 0.75 * n.distance:
                self.good_matches.append([m])

    def calculate_match_percentage(self):
        self.match_percentage = len(self.good_matches) / len(self.kp1) * 100

    def check_authenticity(self):

        if self.match_percentage < 13.5:
            result="Forged"
        else:
            result="Original"

        return result

    def draw_matches(self):
        img_matches = cv2.drawMatchesKnn(self.img1, self.kp1, self.img2, self.kp2, self.good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        img_matches = Image.fromarray(img_matches)
        img_matches.save("D:\\RPOOPFINAL\\image_forgery_detection\\forgery_detection\\static\\forgery_detection\\img\\matched.jpg")


# if __name__ == "__main__":
#     image1_path = r"D:\final_year_project\data\genuine\005005_000.png"
#     image2_path = r"D:\final_year_project\data\genuine\005005_000.png"

#     feature_matching = FeatureMatching(image1_path, image2_path)
#     feature_matching.preprocess_images()
#     feature_matching.find_features()
#     feature_matching.match_features()
#     feature_matching.filter_matches()
#     feature_matching.calculate_match_percentage()
#     print(f"Length of Matches: {len(feature_matching.matches)}")
#     print(f"Percentage of match: {feature_matching.match_percentage:.2f}%")
#     print(f"Length of good matches: {len(feature_matching.good_matches)}")
#     feature_matching.check_authenticity()
#     feature_matching.draw_matches()