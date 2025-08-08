from PIL import Image, ImageEnhance
import cv2
import numpy as np

def auto_enhance_image(input_path: str, output_path: str):
    # Load image with OpenCV
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Cannot load image: {input_path}")

    # Convert to LAB color space for luminance processing
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to L channel to improve contrast adaptively
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl = clahe.apply(l)

    # Merge enhanced L channel back with A and B channels
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_img = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Convert back to PIL Image for further enhancements
    pil_img = Image.fromarray(cv2.cvtColor(enhanced_img, cv2.COLOR_BGR2RGB))

    # Enhance Sharpness
    sharpener = ImageEnhance.Sharpness(pil_img)
    pil_img = sharpener.enhance(1.5)  # 1.0 = original, >1 sharpen

    # Enhance Color
    color_enhancer = ImageEnhance.Color(pil_img)
    pil_img = color_enhancer.enhance(1.2)  # 1.0 = original, >1 more color

    # Enhance Brightness
    brightness_enhancer = ImageEnhance.Brightness(pil_img)
    pil_img = brightness_enhancer.enhance(1.1)  # slight brighten

    # Save enhanced image
    pil_img.save(output_path)
    print(f"Enhanced image saved to: {output_path}")

if __name__ == "__main__":
    input_file = "/mnt/data/84E02478-AD7D-46DC-AE7E-0B5834F33FB8.jpeg"  # Your uploaded image path
    output_file = "/mnt/data/enhanced_image.jpeg"
    auto_enhance_image(input_file, output_file)

