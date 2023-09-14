import os
import azure.ai.vision as sdk
from dotenv import load_dotenv

class VisionApi:
    Name = "VisionApi"

    def __init__(self, endpoint, key):
        self.endpoint = endpoint
        self.key = key
        self.service_options = sdk.VisionServiceOptions(endpoint, key)

    def AnalyzeImage(self, vision_source, analysis_options):
        # default the language to english and gender neutral caption to true
        analysis_options.language = "en"
        analysis_options.gender_neutral_caption = True
        image_analyzer = sdk.ImageAnalyzer(self.service_options, vision_source, analysis_options)
        return image_analyzer.analyze()

    def GetImageCaption(self, vision_source):
        image_analysis_options = sdk.ImageAnalysisOptions()
        image_analysis_options.features = sdk.ImageAnalysisFeature.CAPTION
        result = self.AnalyzeImage(vision_source, image_analysis_options)

        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            return result.caption.content

    def GetImageDetailedCaption(self, vision_source):
        image_analysis_options = sdk.ImageAnalysisOptions()
        image_analysis_options.features = sdk.ImageAnalysisFeature.DENSE_CAPTIONS
        result = self.AnalyzeImage(vision_source, image_analysis_options)

        if result.reason == sdk.ImageAnalysisResultReason.ANALYZED:
            return result.dense_captions

    def DetectObjects(self, vision_source):
        image_analysis_options = sdk.ImageAnalysisOptions()
        image_analysis_options.features = sdk.ImageAnalysisFeature.OBJECTS
        result = self.AnalyzeImage(vision_source, image_analysis_options)
        if result.objects is not None:
            return result.objects

# load_dotenv()

# vision = VisionApi(os.getenv("VISION_ENDPOINT"), os.getenv("VISION_KEY"))
# vision_source = sdk.VisionSource(filename="./WIN_20230913_13_46_54_Pro.jpg")
# detected_objects = vision.DetectObjects(vision_source)
# for detected_object in detected_objects:
#     print(detected_object.bounding_box)
#     print(detected_object.confidence)
#     print(detected_object.name)
