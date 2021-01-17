#!/home/kyle/PycharmProjects/background-changer/venv/bin/python

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


def image_to_array(path):
    """ Turn an image into a numpy array

    Args:
        path: a string of the path to the image

    Returns:
        a numpy array of the image
    """

    image = Image.open(path)
    return np.array(image, dtype=np.float64) / 255


def get_image_dimensions(image):
    """ Get the dimensions of the image

    Args:
        image: an array of the image

    Returns:
        the height, width, and number of channels
    """

    return image.shape[0], image.shape[1], image.shape[2]


def stack_image(image, width, height, channels):
    """ Flatten the image so that all pixels are stacked

    Args:
        image: an array of the image
        width: the image width
        height: the image height
        channels: the number of color channels used in the image

    Returns:
        a numpy array of the stacked image
    """

    flattened_image = np.reshape(image, (width*height, channels))
    return flattened_image


def fit_image(image, n_colors):
    """ Get the primary colors of the image

    Args:
        image: a numpy array of the image
        n_colors: the number of colors (clusters) to find

    Returns:
        a kmeans fit of the image
    """

    return KMeans(n_clusters=n_colors, random_state=0).fit(image)


def plot_primary_colors(colors, save_location, name='kmeans_colors.png'):
    """ Plot the primary colors of the image to see how they look

    Args:
        colors: a numpy array of the rgb values
        save_location: a string of the folder where to save these images
        name: a string of what to call the file

    Returns:
        nothing
    """

    # Crate the subplots
    fig, ax = plt.subplots(1, 1)

    # Make the grid and the grid fill. The grid fill is a dummy varaible needed for pcolormesh
    x, y = np.meshgrid(np.linspace(0, len(colors), len(colors)+1), np.linspace(0, 1, 2))
    fill = np.ones((1, len(colors)))

    # Do the plotting, setting the colors of each square equal to the input colors
    img = ax.pcolormesh(x, y, fill, color=colors, linewidth=0, edgecolors='none')
    img.set_array(None)
    ax.set_xticks([])
    ax.set_yticks([])

    # Make the squares... square. Default is the whole image is a square
    plt.gca().set_aspect('equal')

    # Save the figure
    plt.savefig(save_location + name)


def unstack_image(image, width, height):
    """ Turn a stacked image into the original image shape

    Args:
        image: a numpy array of the image
        width: the original image width
        height: the original image height

    Returns:
        a numpy array of the original image shape
    """

    return np.reshape(image, (height, width))


def make_watercolor_array(image, colors):
    """ Turn an image into a watercolor-style image

    Args:
        image: an NxM numpy array of the image and the indices that correspond to each color
        colors: the colors corresponding to the image

    Returns:
        an NxMx3 numpy array of the watercolor image
    """

    # Make an array of the same size as the image but with 3 color channels
    expanded_array = np.zeros((image.shape[0], image.shape[1], 3))

    # Put the rgb values into the array instead of just which components correspond to which color
    for component in range(len(colors)):
        color_index = np.where(image == component)
        expanded_array[color_index[0], color_index[1], :] = colors[component]

    return expanded_array


def plot_watercolor(width, height, dpi, watercolors, save_location, name):
    """ Plot the watercolor image

    Args:
        width: the image width
        height: the image height
        dpi: the image dpi
        watercolors: the colors to use in the image
        save_location: a string of where to save the image
        name: a string of what to save this file to

    Returns:
        nothing
    """

    # Setup the plot to expand to the entire screen
    plt.figure(figsize=(width / dpi, height / dpi))
    ax = plt.axes([0, 0, 1, 1], frame_on=False)

    # Plot the stuffs
    x, y = np.meshgrid(np.linspace(0, width, width+1), np.linspace(0, height, height+1))
    fill = np.ones((height, width))

    # Do the plotting, setting the colors of each square equal to the input colors
    img = ax.pcolormesh(x, y, fill, color=watercolors, linewidth=0, edgecolors='none')
    img.set_array(None)
    ax.set_xticks([])
    ax.set_yticks([])

    # Make the squares... square. Default is the whole image is a square
    plt.gca().set_aspect('equal')

    # Save the figure
    plt.savefig(save_location + name, dpi=dpi, pad=0)


def make_figure_name(original_image_path, n_colors=''):
    """ Make the string of the figure name

    Args:
        original_image_path: a string of the path to the original image
        n_colors: the number of colors to use

    Returns:
        a string of the new image name
    """

    # Get the original name of the picture
    picture = original_image_path.split('/')[-1]

    # Make the new image a .png because matplotlib can only handle .png format for images
    name = picture.split('.')[0]

    # If the user wants, specify the number of colors used in creating the image
    if n_colors:
        n_colors = '-{}colors'.format(n_colors)
    new_name = '{}_watercolor{}.png'.format(name, n_colors)

    return new_name


if __name__ == '__main__':
    # Set all varaibles relevant to the user's computer
    img_path = '/home/kyle/Pictures/desktop_backgrounds/summer_test.jpg'
    watercolor_save_location = '/home/kyle/Pictures/watercolor_backgrounds/'
    my_dpi = 96
    number_colors = 20

    # Pre-process the image, turning it into an N*Mx3 array
    image_array = image_to_array(img_path)
    img_height, img_width, img_channels = get_image_dimensions(image_array)
    stacked_image = np.flipud(stack_image(image_array, img_width, img_height, img_channels))

    # Use kmeans to get the primary colors of the image
    kmeans = fit_image(stacked_image, number_colors)
    kmeans_colors = kmeans.cluster_centers_
    clustered_pixels = kmeans.predict(stacked_image)
    # If you want, plot up the primary colors
    #plot_primary_colors(kmeans_colors, watercolor_save_location)

    # Reconstruct the image
    clustered_image = unstack_image(clustered_pixels, img_width, img_height)
    watercolor = np.fliplr(make_watercolor_array(clustered_image, kmeans_colors))
    watercolor = stack_image(watercolor, img_height, img_width, img_channels)

    # And plot it
    watercolor_name = make_figure_name(img_path, number_colors)
    plot_watercolor(img_width, img_height, my_dpi, watercolor, watercolor_save_location, watercolor_name)
