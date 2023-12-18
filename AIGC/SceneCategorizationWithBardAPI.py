## LLM Bard API
from bardapi import Bard
import os
import threading

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
    
    return clean_categorization_list

def analyze_image(BARD_API_KEY, image_path):
    os.environ["_BARD_API_KEY"] = BARD_API_KEY

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
    Categorize each object class as Static (S), Dynamic (D), Non-mappable 非適合場景建圖的classes (N), or Irrelevant 不應該出現的classes (I) based on the scene context.
    
    Output Format:
    Return a 19-dimensional dictionary indicating the status of each category.
    
    Example 1:
    Input: An scene and a list of categories.
    Output:
    Scene: Urban Road
    Categories: {
        'road': S, 'sidewalk': S, 'building': S, 'wall': S, 'fence': S, 'pole': S,
        'traffic light': S, 'traffic sign': S, 'vegetation': N, 'terrain': S,
        'sky': N, 'person': D, 'rider': D, 'car': D, 'truck': D,
        'bus': D, 'train': D, 'motorcycle': D, 'bicycle': D
    }
    
    Example 2：
    Input: An scene 和 categories。
    Output:
    Scene: park
    Categories: {
    'road': N, 'sidewalk': S, 'building': N, 'wall': N, 'fence': S, 'pole': S,
    'traffic light': N, 'traffic sign': N, 'vegetation': S, 'terrain': S,
    'sky': S, 'person': D, 'rider': D, 'car': N, 'truck': N,
    'bus': N, 'train': I, 'motorcycle': N, 'bicycle': D
    }
    
    Example 3：
    Input: An scene 和 categories。
    Output:
    Scene: residential area
    Categories: {
    'road': S, 'sidewalk': S, 'building': S, 'wall': S, 'fence': S, 'pole': S,
    'traffic light': S, 'traffic sign': S, 'vegetation': S, 'terrain': S,
    'sky': N, 'person': D, 'rider': D, 'car': D, 'truck': D,
    'bus': D, 'train': N, 'motorcycle': D, 'bicycle': D
    }
    
    Example 4：
    Input: An scene 和 categories。
    Output:
    Scene: city ​​center night view
    Categories: {
    'road': S, 'sidewalk': S, 'building': S, 'wall': S, 'fence': N, 'pole': S,
    'traffic light': S, 'traffic sign': S, 'vegetation': N, 'terrain': N,
    'sky': N, 'person': D, 'rider': D, 'car': D, 'truck': D,
    'bus': D, 'train': N, 'motorcycle': D, 'bicycle': D
    }
    
    Example 5：
    Input: An scene 和 categories。
    Output:
    Scene: office
    Categories: {
    'road': S, 'sidewalk': I, 'building': S, 'wall': S, 'fence': S, 'pole': S,
    'traffic light': I, 'traffic sign': I, 'vegetation': I, 'terrain': S,
    'sky': I, 'person': D, 'rider': I, 'car': I, 'truck': I,
    'bus': I, 'train': I, 'motorcycle': I, 'bicycle': I
    }
    
    Now input: 
    scene: Please answer based on the scene of the previous round of dialogue.
    categories = ['road','sidewalk','building','wall','fence','pole','traffic light','traffic sign','vegetation','terrain','sky',
    'person','rider','car','truck','bus','train','motorcycle','bicycle']
    
    Please answer according to the following format:
    Based on the previous dialogue about a parking garage, here's the categorization breakdown for the provided scene and object categories:
    
    **Scene:** Parking Garage
    
    **Categories:**
    
    * **road:** N - Not suitable for mapping in a parking garage context.
    * **sidewalk:** N - Not present in most parking garages.
    * **building:** S - The concrete walls likely represent parts of a larger building structure.
    * **wall:** S - Concrete walls are prominent elements in parking garages.
    * **fence:** N - Not commonly found in typical parking garages.
    * **pole:** S - Pillars and support poles are frequently present.
    * **traffic light:** I - Irrelevant in a parking garage environment.
    * **traffic sign:** I - Irrelevant in a parking garage environment.
    * **vegetation:** N - Typically absent in parking garages.
    * **terrain:** S - The concrete floor serves as the ground-level terrain.
    * **sky:** N - Usually not visible within enclosed parking garages.
    * **person:** D - People can be present as parking or walking through the garage.
    * **rider:** I - Irrelevant within a parking garage context.
    * **car:** S/D - Depending on the scene, parked cars are static (S), while moving cars would be dynamic (D).
    * **truck:** S/D - Similar to cars, parked trucks are static (S), while moving ones are dynamic (D).
    * **bus:** N - Highly unlikely to be present in a parking garage.
    * **train:** I - Irrelevant in a parking garage context.
    * **motorcycle:** S/D - Similar to cars and trucks, parked motorcycles are static (S), while moving ones are dynamic (D).
    * **bicycle:** S/D - Similar to the above, parked bicycles are static (S), while moving ones are dynamic (D).
    '''
    bard = Bard()
    with open(image_path, 'rb') as img_file:
        image = img_file.read()
    bard_answer1 = bard.ask_about_image(prompt1, image)
    # print(bard_answer1['content'])
    bard_answer2 = bard.get_answer(prompt2)
    # print(bard_answer2['content'])
    llm_response = bard_answer2['content'].replace('*','')
    categorization_list = llm_response_process(llm_response)
    boolean_list = [cat == 'S' for cat in categorization_list]
    return boolean_list

# 'S'（靜態）、'D'（動態）、'N'（非適合場景建圖的類別）或'I'（不應該出現的類別）

if __name__ == '__main__':
    BARD_API_KEY = "eAjA29tVQl7ZdPqB7vbZYFE9mhDOTxC8s9QLEZYCxDCmByorzIISMYbcONNV67IDHdoDlQ."
    image_path = 'D:/Record/在職進修/修課/三維電腦視覺與深度學習應用/Final project/停車場.jpg'
    boolean_list = analyze_image(BARD_API_KEY, image_path)
