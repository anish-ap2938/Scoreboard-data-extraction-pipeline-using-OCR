import cv2

def remove_unwanted_columns(image_path, output_path):
    """
    Reads the scoreboard image, blacks out specific columns, 
    then saves the modified image to output_path.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read {image_path}")

    height, width = img.shape[:2]
    print(f"Original Image Dimensions: width={width}, height={height}")

    # New coordinates for columns to mask:
    # (188, 254), (427, 549), (670, 820), (910, 963)
    columns_to_remove = [
        (188, 254),
        (427, 549),
        (670, 820),
        (910, 963)
    ]

    # Draw a black rectangle over each unwanted column
    for (x1, x2) in columns_to_remove:
        x1 = max(0, x1)
        x2 = min(width, x2)
        cv2.rectangle(img, (x1, 0), (x2, height), (0, 0, 0), -1)

    cv2.imwrite(output_path, img)
    print(f"Masked image saved to: {output_path}")

if __name__ == "__main__":
    input_file = "green_cropped.png"   # your input file (rename as needed)
    output_file = "green_masked.png"   # output file with a small name
    remove_unwanted_columns(input_file, output_file)
