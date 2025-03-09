import cv2
import pytesseract
from PIL import Image
import json

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

def extract_text_from_masked_image(image_path):
    """
    Preprocesses the masked image and then extracts text using Tesseract OCR.
    """
    preprocessed = preprocess_for_ocr(image_path, output_path="debug_preprocessed.png")
    pil_img = Image.fromarray(preprocessed)
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(pil_img, config=custom_config)
    return text

def is_numeric(token):
    """
    Returns True if token is numeric (ignoring commas), otherwise False.
    """
    try:
        float(token.replace(',', ''))
        return True
    except ValueError:
        return False

def parse_ocr_text(text):
    """
    Parses the OCR text to extract a dictionary where each key is a player's name
    and the value is a dictionary containing the player's KDA and CREDS.
    
    Expected OCR text format (example):
    
      NAME KDA CREDS
      Ritzy 6 2 0 n 50
      Ken Kaneki 4 1 0 5 2,650
      ROwDyyy 3 0 0 n 6,950
      Parigt 1 2 1 4,950
      MONKEKILLER69 1 2 4 n 400
      BAR
    """
    data = {}
    lines = text.strip().splitlines()
    for line in lines:
        line = line.strip()
        # Skip header or extra lines
        if not line or line.upper().startswith("EXTRACTED") or line.upper().startswith("NAME") or line.upper() == "BAR":
            continue
        
        tokens = line.split()
        first_numeric_idx = None
        for i, token in enumerate(tokens):
            if is_numeric(token):
                first_numeric_idx = i
                break
        if first_numeric_idx is None:
            continue
        
        # The player's name may span multiple tokens
        name = " ".join(tokens[:first_numeric_idx])
        
        # Collect the first three numeric tokens as KDA
        kda_tokens = []
        j = first_numeric_idx
        while j < len(tokens) and len(kda_tokens) < 3:
            if is_numeric(tokens[j]):
                kda_tokens.append(tokens[j])
            j += 1
        kda = " ".join(kda_tokens)
        
        # Assume the last token is the creds value
        creds = tokens[-1]
        
        data[name] = {"KDA": kda, "CREDS": creds}
    return data

if __name__ == "__main__":
    # Use "green_masked.png" as the input masked image file.
    input_image = "green_masked.png"
    
    # Extract OCR text from the masked image.
    ocr_text = extract_text_from_masked_image(input_image)
    print("Extracted OCR Text:\n", ocr_text)
    
    # Parse the OCR text to extract player information.
    parsed_data = parse_ocr_text(ocr_text)
    
    # Convert the parsed data to a JSON string and print it.
    json_output = json.dumps(parsed_data, indent=4)
    print("\nParsed Data in JSON format:\n", json_output)
