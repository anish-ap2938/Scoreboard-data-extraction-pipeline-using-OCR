import cv2

def manual_crop_scoreboard(image_path, output_path):
    """
    Crops a fixed rectangular region from the center of the image
    where the Valorant scoreboard usually appears.
    Adjust the crop boundaries to match your screen resolution.
    """
    # Read the image from the given file path.
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read {image_path}")

    height, width = img.shape[:2]

    # Crop a rectangle based on the percentages of the width and height.
    x1 = int(width * 0.20)
    x2 = int(width * 0.80)
    y1 = int(height * 0.10)
    y2 = int(height * 0.50)

    scoreboard_img = img[y1:y2, x1:x2]

    # Write the cropped image to the output path.
    cv2.imwrite(output_path, scoreboard_img)
    return output_path

if __name__ == "__main__":
    input_image = "7.png"                # The original screenshot in the same directory
    output_image = "green_cropped.png"   # Cropped scoreboard output
    manual_crop_scoreboard(input_image, output_image)
    print("Saved cropped scoreboard to:", output_image)
