# Scoreboard-data-extraction-pipeline-using-OCR
# Valorant Scoreboard OCR and Data Extraction

This repository contains scripts for extracting, processing, and parsing the scoreboard from Valorant game screenshots. The project leverages computer vision techniques with OpenCV and optical character recognition (OCR) using Tesseract to extract in-game statistics such as player names, KDA, and CREDS.

## Project Overview

The project is designed to work with Valorant scoreboard screenshots. It consists of three main stages:

1. **Cropping the Scoreboard Sections:**
   - **Red Section:**  
     The `red.py` script crops a specific rectangular region from the lower part of the screenshot, typically capturing the red scoreboard area.
   - **Green Section:**  
     The `green.py` script crops a rectangular region from the upper part of the screenshot where the green scoreboard appears.

2. **Masking Unwanted Data:**
   - **Green Section Masking:**  
     The `greenmask.py` script processes the cropped green scoreboard image by blacking out specific columns that contain extraneous data. This step refines the image for improved OCR performance.

3. **OCR and Data Parsing:**
   - **Preprocessing & Extraction:**  
     The `green_final.py` script preprocesses the masked image (converting it to grayscale, resizing, and thresholding) to enhance OCR accuracy. It then uses Tesseract to extract text from the processed image.
   - **Parsing OCR Results:**  
     Extracted text is parsed to obtain structured information (player names, KDA, and CREDS) and output in JSON format.

## Project Structure

- `7.png`  
  A sample image that is a Valorant scoreboard screenshot.
  
- `red.py`  
  Crops the red section from the lower portion of the screenshot and saves it as `red_cropped.png`.

- `green.py`  
  Crops the green section from the upper portion of the screenshot and saves it as `green_cropped.png`.

- `greenmask.py`  
  Masks unwanted columns in `green_cropped.png` to produce a cleaner image (`green_masked.png`) for OCR processing.

- `green_final.py`  
  Preprocesses the masked image, extracts text using Tesseract OCR, and parses the text into a structured JSON format representing the scoreboard data.

## Dependencies

Ensure you have the following installed:
- Python 3.x
- OpenCV (`opencv-python`)
- Tesseract OCR and the `pytesseract` package
- Pillow (`PIL`)

Install the Python packages using pip:

```bash
pip install opencv-python pytesseract pillow
