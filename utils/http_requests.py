import requests
import os
import logging
from . import decorators

PUBLIC_REMOVE : str = "JbVVYbErXnKxZdz2ryDjzXnN"
REMOVE_URL : str =  'https://api.remove.bg/v1.0/removebg'
REMOVE_HEADERS : dict = {'X-Api-Key': PUBLIC_REMOVE}
DOWNLOAD_FOLDER = "./download"

CUTOUT_PRO_PUBLIC =  "38ffa8065ae14259b46ec4bbcf8f1c95"
CUTOUT_PRO_ENHANCE_URL = "https://www.cutout.pro/api/v1/matting?mattingType=18"
CUTOUT_PRO_HEADER : dict = {"APIKEY" : CUTOUT_PRO_PUBLIC}


@decorators.log(message="HTTP POST IMAGE POSTING")
def post_image(image_path: str, url: str, headers: dict,key="image_file", data=None) -> bytes:
	"""
	Uploads an image file to a server endpoint via HTTP POST request with the specified headers.

	Parameters:
	- image_path (str): The path to the image file to be uploaded.
	- url (str): The URL of the server endpoint to which the image file will be uploaded.
	- headers (dict): A dictionary of HTTP headers to be included in the request.

	Returns:
	- The binary content of the server response if the request is successful.

	Raises:
	- ValueError: If the HTTP request fails.

	Example usage:
	response_content = post_image('image.jpg', 'https://example.com/upload', {'Authorization': 'Bearer mytoken'})
	"""

	# Send the HTTP POST request with the specified headers and image file data
	try:
		# Send the HTTP POST request with the specified headers and image file data
		response = requests.post(url, files={key: open(image_path, 'rb')}, data=data, headers=headers)
		response.raise_for_status()  # Raise an error if the response contains an HTTP error status code
		return response.content
	except requests.exceptions.RequestException as err:
		raise requests.exceptions.RequestException(f"Error uploading image file: {err}") from None
	except Exception as e:
		message = f"Request failed. Reasons : {e}"
		raise ValueError(message)




def write_image_to_download(image_buffer, image_path):
	"""
	Writes an image from a binary buffer to a specified file path, while also creating a directory
	if it doesn't exist.

	Parameters:
	- image_buffer (bytes): A binary buffer containing the image data.
	- image_path (str): The file path and name where the image should be saved.

	Returns:
	- The file path where the processed image was saved.

	Example usage:
	processed_image_path = write_image_to_download(image_buffer, "/downloads/image.jpg")
	"""

	# Split the file path and name to get the image's name and extension
	filename = os.path.basename(image_path)
	name, extention  = os.path.splitext(filename)

	if not os.path.exists(DOWNLOAD_FOLDER):
		os.mkdir(DOWNLOAD_FOLDER)

	processed_image_path = f"{DOWNLOAD_FOLDER}/{name}-py-pro{extention}"
	with open(processed_image_path, "wb") as file:
		file.write(image_buffer)

	return processed_image_path


@decorators.log(message="REMOVING IMAGE BACKGROUND")
def remove_bg(path: str, data = {'size': 'auto'}) -> str:
	"""
	Removes the background of an image at the specified path using the remove.bg API.

	Parameters:
	- path (str): The path to the image file to process.

	Returns:
	- A string representing the path to the processed image file with the background removed.

	Raises:
	- ValueError: If the remove.bg API request fails.

	Example usage:
	processed_image_path = remove_bg('image.jpg')
	"""

	try:
		# Send the image file to the remove.bg API and receive the processed image data
		buffer = post_image(path, REMOVE_URL, REMOVE_HEADERS, data=data)
		return write_image_to_download(buffer, path)
	except:
		raise ValueError("Failed to remove background from image.") from None


@decorators.log(message="Enhance or increase your image quality")
def enhance_image(path: str) -> str:
	"""
	Removes the background of an image at the specified path using the cutout.pro API.

	Parameters:
	- path (str): The path to the image file to process.

	Returns:
	- A string representing the path to the processed image file with the background removed.


	Example usage:
	processed_image_path = enhance_image('image.jpg')
	"""

	try:
		# Send the image file to the remove.bg API and receive the processed image data
		buffer = post_image(path, CUTOUT_PRO_ENHANCE_URL, CUTOUT_PRO_HEADER, key="file")
		return write_image_to_download(buffer, path)
	except Exception as e:
		logging.warning(e)
		raise ValueError("Failed to enhance image .") from None



if __name__ == "__main__":
	path = "/home/christian/workspace/py-tools/shot.png"
	buffer = enhance_image(path)
	print(buffer)

	# write_image_to_download(buffer,path)
