import cv2
import numpy as np
import os



IMAGE_SIZE = (224, 224)

TEST_FOLDER = (
    "dataset_clean/test/Bacterial_spot"
)



def get_severity(infection_percentage):
    """
    Convert infection percentage into a
    project-defined severity category.
    """

    if infection_percentage < 10:
        return "Very Low"

    elif infection_percentage < 25:
        return "Mild"

    elif infection_percentage < 50:
        return "Moderate"

    elif infection_percentage < 75:
        return "Severe"

    else:
        return "Very Severe"



def detect_leaf(image):
    """
    Detect the approximate leaf region using HSV.

    Returns:
        Binary leaf mask
    """

    # Convert BGR → HSV
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    # Green vegetation range
    lower_green = np.array(
        [25, 30, 20]
    )

    upper_green = np.array(
        [100, 255, 255]
    )

    # Create mask
    leaf_mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    # Morphological operations
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    leaf_mask = cv2.morphologyEx(
        leaf_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    leaf_mask = cv2.morphologyEx(
        leaf_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    return leaf_mask



def detect_infected_region(
    image,
    leaf_mask
):
    """
    Detect possible diseased regions using
    brown, yellow and dark color regions.

    Returns:
        Binary infected-region mask
    """

    # Convert image to HSV
    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    lower_brown = np.array(
        [5, 40, 20]
    )

    upper_brown = np.array(
        [35, 255, 220]
    )

    brown_mask = cv2.inRange(
        hsv,
        lower_brown,
        upper_brown
    )

    lower_dark = np.array(
        [0, 0, 0]
    )

    upper_dark = np.array(
        [180, 255, 80]
    )

    dark_mask = cv2.inRange(
        hsv,
        lower_dark,
        upper_dark
    )


    infected_mask = cv2.bitwise_or(
        brown_mask,
        dark_mask
    )

    # Keep only pixels inside the leaf
    infected_mask = cv2.bitwise_and(
        infected_mask,
        leaf_mask
    )

    # -----------------------------------------------------
    # REMOVE SMALL NOISE
    # -----------------------------------------------------

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    infected_mask = cv2.morphologyEx(
        infected_mask,
        cv2.MORPH_OPEN,
        kernel
    )

    infected_mask = cv2.morphologyEx(
        infected_mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    return infected_mask



def calculate_infection_percentage(
    leaf_mask,
    infected_mask
):
    """
    Calculate infection percentage.

    Formula:

        Infection %
        =
        Infected Area / Leaf Area × 100
    """

    # Count leaf pixels
    leaf_area = cv2.countNonZero(
        leaf_mask
    )

    # Count infected pixels
    infected_area = cv2.countNonZero(
        infected_mask
    )

    # Avoid division by zero
    if leaf_area == 0:

        return (
            0.0,
            0,
            0
        )

    infection_percentage = (
        infected_area
        /
        leaf_area
    ) * 100

    return (
        infection_percentage,
        leaf_area,
        infected_area
    )



def create_infection_visualization(
    image,
    infected_mask
):
    """
    Highlight infected regions in red
    and draw their boundaries.
    """

    result = image.copy()


    red_overlay = np.zeros_like(
        image
    )

    red_overlay[:, :] = (
        0,
        0,
        255
    )

  
    infected_pixels = (
        infected_mask > 0
    )

    result[infected_pixels] = (
        0,
        0,
        255
    )

 
    contours, _ = cv2.findContours(
        infected_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # Draw boundaries
    cv2.drawContours(
        result,
        contours,
        -1,
        (0, 0, 255),
        2
    )

    return result



def analyze_infection(
    image_path
):
    """
    Perform complete infection analysis
    on a single tomato leaf image.
    """

    
    image = cv2.imread(
        image_path
    )

    if image is None:

        raise ValueError(
            f"Unable to read image: {image_path}"
        )

   
    image = cv2.resize(
        image,
        IMAGE_SIZE
    )

    leaf_mask = detect_leaf(
        image
    )

   
    infected_mask = (
        detect_infected_region(
            image,
            leaf_mask
        )
    )

    
    (
        infection_percentage,
        leaf_area,
        infected_area
    ) = calculate_infection_percentage(
        leaf_mask,
        infected_mask
    )

    severity = get_severity(
        infection_percentage
    )

    visualization = (
        create_infection_visualization(
            image,
            infected_mask
        )
    )

   
    return {

        "infection_percentage":
            infection_percentage,

        "leaf_area":
            leaf_area,

        "infected_area":
            infected_area,

        "severity":
            severity,

        "leaf_mask":
            leaf_mask,

        "infected_mask":
            infected_mask,

        "visualization":
            visualization
    }


def find_test_image():
    """
    Find the first image inside the
    Bacterial_spot test folder.
    """

    if not os.path.exists(
        TEST_FOLDER
    ):

        return None

    for filename in os.listdir(
        TEST_FOLDER
    ):

        if filename.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".bmp",
                ".webp"
            )
        ):

            return os.path.join(
                TEST_FOLDER,
                filename
            )

    return None


if __name__ == "__main__":

    
    print(" TOMATO LEAF INFECTION ANALYSIS")
    

    # Find test image
    test_image = find_test_image()

    if test_image is None:

        print(
            "\nERROR: No test image found."
        )

        print(
            f"Checked folder:\n{TEST_FOLDER}"
        )

    else:

        print(
            f"\nTest image:"
        )

        print(
            test_image
        )

        # Analyze image
        result = analyze_infection(
            test_image
        )

       
        print(" INFECTION ANALYSIS RESULT")
        

        print(
            f"\nLeaf area:"
        )

        print(
            result["leaf_area"]
        )

        print(
            f"\nInfected area:"
        )

        print(
            result["infected_area"]
        )

        print(
            f"\nInfection percentage:"
        )

        print(
            f"{result['infection_percentage']:.2f}%"
        )

        print(
            f"\nSeverity:"
        )

        print(
            result["severity"]
        )

        output_folder = "results/infection_analysis"

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        output_path = os.path.join(
            output_folder,
            "infection_result.jpg"
        )

        cv2.imwrite(
            output_path,
            result["visualization"]
        )

        print(
            f"\nVisualization saved to:"
        )

        print(
            output_path
        )

        print(" ANALYSIS COMPLETE")
        
