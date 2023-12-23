env
python env >= 3.9

Install
$ pip install bardapi
$ pip install git+https://github.com/dsdanielpark/Bard-API.git
$ pip install bardapi==0.1.38

1. **Set Your Bard API Key as an Environment Variable**: 
   Configure your Bard API key as an environment variable named `_BARD_API_KEY`. This is crucial for the script to authenticate and access the Bard API services.

2. **Adjust the `image_path` Variable**: 
   Modify the `image_path` variable in the script to point to the path of the image you wish to analyze. Ensure that the path correctly leads to your image file.

3. **Execute the Script**: 
   Run the script in your Python environment. The script will open the image file, utilize the Bard API to analyze the image, and return a scene description along with a categorized list of objects found in the image.

### Important Notes

- **Correct Image Path**: 
  Ensure that the image path specified in the `image_path` variable is accurate and points to a valid image file.

- **API Key Confidentiality and Accuracy**: 
  Make sure that your Bard API key is correctly set up in the environment variable and kept confidential. This key is essential for accessing the Bard API services.

- **Python Environment Compatibility**: 
  Verify that your Python environment meets the version requirements of the script. The script is intended to be run in Python 3.9 or higher.

---

These instructions and notes are designed to guide you through setting up and running the script effectively, making sure that all necessary configurations are in place.
