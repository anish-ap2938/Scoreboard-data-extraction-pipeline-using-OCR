import cv2
import pytesseract
from PIL import Image

def preprocess_for_ocr(image_path, output_path=None):
    """
    Preprocesses the image to improve OCR accuracy:
      1. Converts the image to grayscale.
      2. Resizes the image (scales up by 2x).
      3. Applies a binary threshold for high contrast.
    Optionally saves the preprocessed image for inspection.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read {image_path}")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize image to enlarge text
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    # Apply binary threshold to sharpen contrast
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    if output_path:
        cv2.imwrite(output_path, thresh)
    
    return thresh

def crop_region(image, x1, y1, x2, y2):
    """
    Returns a cropped region of the image from (x1, y1) to (x2, y2).
    Coordinates must match the positions on debug_preprocessed.png.
    """
    return image[y1:y2, x1:x2]

def extract_text_from_region(region):
    """
    Uses Tesseract OCR on the provided image region (NumPy array)
    and returns the extracted text as a string.
    """
    pil_img = Image.fromarray(region)
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=config)
    return text

def main():
    # 1. Define your input masked image file
    input_image = "green_masked.png"
    
    # 2. Preprocess to create the debug image
    preprocessed = preprocess_for_ocr(input_image, output_path="debug_preprocessed.png")
    
    # 3. Read the debug_preprocessed image for cropping
    debug_img = cv2.imread("debug_preprocessed.png", cv2.IMREAD_GRAYSCALE)
    if debug_img is None:
        raise FileNotFoundError("Could not read debug_preprocessed.png")
    
    # 4. Define bounding box coordinates (x1, y1, x2, y2) for each column.
    #    Replace these placeholders with your measured values from GIMP.
    name_col_coords  = (483, 398, 882, 792)  # Adjust these values!
    kda_col_coords   = (1080, 398, 1349, 800)  # Adjust these values!
    creds_col_coords = (1626, 402, 1823, 806)  # Adjust these values!
    
    # 5. Crop the regions for each column
    name_region  = crop_region(debug_img, *name_col_coords)
    kda_region   = crop_region(debug_img, *kda_col_coords)
    creds_region = crop_region(debug_img, *creds_col_coords)
    
    # 6. Extract OCR text from each region
    name_text  = extract_text_from_region(name_region)
    kda_text   = extract_text_from_region(kda_region)
    creds_text = extract_text_from_region(creds_region)
    
    # 7. Print OCR outputs for each column
    print("Name Column OCR Output:\n", name_text)
    print("KDA Column OCR Output:\n", kda_text)
    print("CREDS Column OCR Output:\n", creds_text)

if __name__ == "__main__":
    main()
