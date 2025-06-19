from autosurfer.utils.image_processor import UIElementDetector

if __name__ == "__main__":
    img_path = "../.temp/screenshots/screenshot_.jpg"
    detector = UIElementDetector(
        yolo_model_path="models/weights/v1.pt",
        yolo_conf_threshold=0.6,
        ocr_conf_threshold=0.4
    )

    detect_res = detector.detect(img_path)
    last_action = {"type": None, "description": "start"}
    prompt_payload = detector.prepare_openai_payload(
        objective="Click the Login button",
        last_action=last_action,
        detect_result=detect_res
    )

    print("------ OPENAI PAYLOAD ------")
    print(prompt_payload)
