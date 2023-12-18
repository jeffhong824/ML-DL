## LLM Bard API
from bardapi import Bard
import os
import threading
from tqdm import tqdm

'''
Readme 
python env >= 3.9

Install
$ pip install bardapi
$ pip install git+https://github.com/dsdanielpark/Bard-API.git
$ pip install bardapi==0.1.38
'''

def llm_response_process(llm_response):
    # Extracting and categorizing the data from the response
    categories = ['road', 'sidewalk', 'building', 'wall', 'fence', 'pole', 'traffic light', 'traffic sign', 
                  'vegetation', 'terrain', 'sky', 'person', 'rider', 'car', 'truck', 'bus', 'train', 
                  'motorcycle', 'bicycle']
    
    # Re-processing the LLM response to create a clean 19-dimensional list of categories without any '*' characters
    
    # Extracting and categorizing the data from the response again
    clean_categorization_list = []

    start_index = llm_response.find("Scene:") + len("Scene:") # Find the start index of the scene description
    end_index = llm_response.find("\n", start_index) # Find the end index of the scene description (which is the start of 'Categories:')
    scene = llm_response[start_index:end_index].strip() # Extract the scene description
    
    for category in categories:
        if category + ":" in llm_response:
            # Find the categorization for each category
            start = llm_response.find(category + ":") + len(category) + 2
            end = llm_response.find("-", start)
            categorization = llm_response[start:end].strip()
    
            # If multiple categorizations, default to 'D'
            if '/' in categorization:
                categorization = 'D'
            
            # Remove any '*' characters
            categorization = categorization.replace('*', '').strip()
            
            clean_categorization_list.append(categorization)
        else:
            clean_categorization_list.append('N/A')  # Placeholder for missing category
    
    return scene, clean_categorization_list

def analyze_image(bard, image_path):
    prompt1 = ''' Identify the scene depicted in the image.
    
    Input Format:
    An image file name or description.
    
    Your Role:
    Based on the description provided, identify and describe the scene depicted in the image.
    
    Example 1:
    Input: 'CityStreet.jpg'
    Output: Urban street scene. This image likely depicts a bustling urban street with cars, pedestrians, tall buildings, and traffic lights, signifying a busy city environment.
    
    Example 2:
    Input: 'ParkView.jpg'
    Output: Park scene. This image likely shows a tranquil park with green grass, trees, a small lake, and people sitting on benches, suggesting a peaceful, natural setting.
    
    Example 3:
    Input: 'SuburbanArea.jpg'
    Output: Residential neighborhood. The scene probably represents a residential area with houses, gardens, a few parked cars, and children playing on the sidewalk, indicating a family-friendly environment.
    
    Example 4:
    Input: 'BeachDay.jpg'
    Output: Beach scene. This image is likely to depict a crowded beach with people sunbathing, playing volleyball, and a clear blue ocean in the background, suggesting a popular seaside destination.
    
    Example 5:
    Input: 'IndustrialDistrict.jpg'
    Output: Industrial zone. This image probably shows an industrial area with large factories, warehouses, trucks loading goods, and few people, indicative of a commercial or industrial hub.
    
    '''
    
    prompt2 = ''' As an AI model, your task is to analyze images for ORB-SLAM enhanced with Segmentation. You will determine the scene and categorize detected objects as either static or dynamic for effective mapping in various environments.
    
    Input Format:
    1. An scene.
    2. A list of object categories.
    
    Your Role:
    Based on the description provided, Categorize each object class as Static (S), Dynamic (D), Non-mappable 非適合場景建圖的classes (N), or Irrelevant 不應該出現的classes (I) based on the scene context.
    
    Output Format:
    Return a 19-dimensional dictionary indicating the status of each category.
    
    Example 1:
    Output:
    Scene: Urban Road
    Categories:
    road: S
    sidewalk: S
    building: S
    wall: S
    fence: S
    pole: S
    traffic light: S
    traffic sign: S
    vegetation: S
    terrain: S
    sky: N
    person: D
    rider: D
    car: D
    truck: D
    bus: D
    train: D
    motorcycle: D
    bicycle: D
    
    Example 2：
    Output:
    Scene: park
    Categories:
    road: S
    sidewalk: S
    building: S
    wall: S
    fence: S
    pole:S
    traffic light: S
    traffic sign: I
    vegetation: S
    terrain: S
    sky: N
    person: D
    rider: D
    car: D
    truck: D
    bus: D
    train: I
    motorcycle: I
    bicycle: D
    
    Example 3：
    Output:
    Scene: residential area
    Categories:
    sidewalk: S
    building: S
    wall: S
    fence: S
    pole:S
    traffic light: S
    traffic sign: S
    vegetation: S
    terrain: S
    sky: N
    person: D
    rider: D
    car: D
    truck: D
    bus: D
    train: D
    motorcycle: D
    bicycle: D
    
    Example 4：
    Output:
    Scene: city ​​center night view
    Categories:
    sidewalk: S
    building: S
    wall: S
    fence: S
    pole: S
    traffic light: S
    traffic sign: S
    vegetation: S
    terrain: S
    sky: N
    person: D
    rider: D
    car: D
    truck: D
    bus: D
    train: D
    motorcycle: D
    bicycle: D
    
    Example 5：
    Input: An scene 和 categories。
    Output:
    Scene: office
    Categories:
    road: S 
    sidewalk: I 
    building: S
    wall: S 
    fence: S 
    pole: S 
    traffic light: I 
    traffic sign: I 
    vegetation: I 
    terrain: S 
    sky: I 
    person: D 
    rider: I 
    car: I
    truck: I 
    bus: I 
    train: I 
    motorcycle: I 
    bicycle: I 
    
    Now input: 
    categories = ['road','sidewalk','building','wall','fence','pole','traffic light','traffic sign','vegetation','terrain','sky',
    'person','rider','car','truck','bus','train','motorcycle','bicycle']

    scene: Please answer based on the scene of the previous round of dialogue.
    Parking Garages
    Office Spaces
    Schools and Universities
    Streets and Urban Roads
    Shopping Malls
    Residential Areas
    Industrial Warehouses
    Public Parks
    Airports and Train Stations
    Hospitals and Clinics
    Museums and Galleries
    Construction Sites
    Hotels and Resorts
    Sports Stadiums and Arenas
    Conference Centers
    Historical Sites and Monuments
    Forest Trails and Outdoor Hiking Paths
    Underground Tunnels and Subway Systems
    Ports and Dockyards
    Rural Countrysides
    ...etc
    '''

    with open(image_path, 'rb') as img_file:
        image = img_file.read()

    scene = None
    default_list = [True, True, True, True, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False]
    prompt1_result = ''
    try:
        bard_answer1 = bard.ask_about_image(prompt1, image)
        prompt1_result = bard_answer1['content']
    except:
        boolean_list = default_list
        
    # print(bard_answer1['content'])
    try:
        bard_answer2 = bard.get_answer(prompt2+prompt1_result)
        # print(bard_answer2['content'])
        llm_response = bard_answer2['content'].replace('*','')
        scene, categorization_list = llm_response_process(llm_response)
        boolean_list = [cat == 'S' for cat in categorization_list]
        if boolean_list == [False for each in range(19)]:
            boolean_list =  default_list
    except:
        boolean_list = default_list
    boolean_list[0:4] = [True for i in range(4)]
    return scene, boolean_list

# 'S'（靜態）、'D'（動態）、'N'（非適合場景建圖的類別）或'I'（不應該出現的類別）

if __name__ == '__main__':
    BARD_API_KEY = "eQjA2wU96wmfCJeVPuu71lcYaJL6W6usD2ZlPjSDNJO_0uYs4SbfwkGXBaYz5UDdX-MIZA."
    image_path = 'D:/Record/在職進修/修課/三維電腦視覺與深度學習應用/Final project/TUM.jpg'
    
    os.environ["_BARD_API_KEY"] = BARD_API_KEY
    bard = Bard()

    scene, boolean_list = analyze_image(bard, image_path)
