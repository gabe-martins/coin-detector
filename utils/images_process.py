from PIL import Image
import os

def resize_images(source_dir, size):
    """
    Resizes all images in the given source directory to the specified size
    and saves the resized images in a new directory called 'resized' within
    the source directory.

    Args:
    - source_dir (str): Path to the directory containing the original images.
    - size (tuple): A tuple of integers representing the desired size of the 
                    resized images in the format (width, height).

    Returns:
    - None
    """

    # Define the destination directory
    dest_dir = f'{source_dir}/resized'

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over all files in the source directory
    for filename in os.listdir(source_dir):
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            # Open the image
            image = Image.open(os.path.join(source_dir, filename))

            # Resize the image
            resized_image = image.resize(size)

            # Save the resized image to the destination directory
            dest_path = os.path.join(dest_dir, filename)
            resized_image.save(dest_path)

def rename_files_with_prefix(directory, prefix):
    """
    Renames all .jpg files in the specified directory with the desired prefix and a
    sequential number. The function renames the files in place.

    Args:
    - directory (str): The path to the directory containing the files to be renamed.
    - prefix (str): The prefix to be added to the new file names.

    Returns:
    - None
    """

    counter = 0

    # iterate over all files in the directory
    for filename in os.listdir(directory):
        # check if the file is a regular file
        if os.path.isfile(os.path.join(directory, filename)):
            # check if the file has the .jpg extension
            extension = os.path.splitext(filename)[1]
            if extension.lower() == '.jpg':
                # construct the new filename with the prefix and sequential number
                new_filename = f"{prefix}{counter}.jpg"
                # rename the file with the new filename
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
                # increment the counter for the next file
                counter += 1

#resize_images(source_dir=f'../images/dataset/50', size=(224, 224))
rename_files_with_prefix(directory=f'../images/dataset/50/resized', prefix='')
