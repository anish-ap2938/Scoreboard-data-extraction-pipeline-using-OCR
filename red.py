import cv2

def manual_crop_scoreboard2(image_path, output_path):
    """
    Crops a fixed rectangular region from the lower portion of the image,
    where the Valorant scoreboard's red section usually appears.
    Adjust the crop boundaries to match your screen resolution.
    """
    # Read the image from the given file path
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read {image_path}")

    height, width = img.shape[:2]

    # Define crop boundaries (adjust these percentages as needed)
    x1 = int(width * 0.20)
    x2 = int(width * 0.80)
    y1 = int(height * 0.50)
    y2 = int(height * 0.90)

    # Crop the region from y1 to y2 and x1 to x2
    scoreboard_img = img[y1:y2, x1:x2]

    # Save the cropped image to the output path
    cv2.imwrite(output_path, scoreboard_img)
    return output_path

if __name__ == "__main__":
    input_image = "7.png"                # The original screenshot in the working directory
    output_image = "red_cropped.png"       # Output file name for the cropped red scoreboard
    manual_crop_scoreboard2(input_image, output_image)
    print("Saved cropped scoreboard to:", output_image)
