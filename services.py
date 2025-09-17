from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import os
import logging

# Load .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # pyright: ignore[reportPrivateImportUsage]

from typing import Optional

def edit_image(image_bytes1: bytes, image_bytes2: Optional[bytes] = None, prompt: str = ""):
    """
    Takes one or two image bytes and a prompt, and returns the modified image bytes.
    If only one image is provided, processes with a single image.
    If two images are provided, processes with both images.
    """
    try:
        # Check if API key is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("No GOOGLE_API_KEY found in environment variables")
            raise ValueError("Missing API key. Please configure GOOGLE_API_KEY in .env file.")
        
        # Improve the prompt by making it more specific
        enhanced_prompt = f"Edit these images: {prompt}. Return the modified image."
        logger.info(f"Processing image edit request with prompt: {enhanced_prompt[:100]}...")
        
        # Open and verify images
        try:
            image1 = Image.open(BytesIO(image_bytes1))
            logger.info(f"Successfully opened image1: {image1.format}, size: {image1.size}, mode: {image1.mode}")
            # Convert to RGB if needed (some formats like RGBA might cause issues)
            if image1.mode != "RGB":
                logger.info(f"Converting image1 from {image1.mode} to RGB")
                image1 = image1.convert("RGB")

            images = [enhanced_prompt, image1]

            if image_bytes2 is not None:
                image2 = Image.open(BytesIO(image_bytes2))
                logger.info(f"Successfully opened image2: {image2.format}, size: {image2.size}, mode: {image2.mode}")
                # Convert to RGB if needed (some formats like RGBA might cause issues)
                if image2.mode != "RGB":
                    logger.info(f"Converting image2 from {image2.mode} to RGB")
                    image2 = image2.convert("RGB")
                images.append(image2)

        except Exception as img_error:
            logger.error(f"Failed to process images: {str(img_error)}")
            raise ValueError(f"Invalid image format: {str(img_error)}")
        
        # Use only the specified model - gemini-2.5-flash-image-preview
        model_name = "gemini-2.5-flash-image-preview"
        logger.info(f"Using model: {model_name}")
        
        try:
            logger.info(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)  # pyright: ignore[reportPrivateImportUsage]
            
            # Set parameters for better results
            logger.info(f"Generating content with {model_name}...")
            
            # Create a generation config object if the API requires it
            try:
                # First, try without any special parameters
                response = model.generate_content(images)
            except Exception as config_error:
                logger.warning(f"Error with basic config: {str(config_error)}. Trying alternative approaches...")
                
                # Try different approaches based on the API version
                try:
                    # Try with generation_config as a named parameter
                    response = model.generate_content(
                        images,
                        generation_config={"temperature": 0.7}
                    )
                except:
                    # Last resort - just try with the content only
                    response = model.generate_content(images)
            
            if response.candidates and response.candidates[0].content:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, "inline_data") and part.inline_data and part.inline_data.data:
                        logger.info(f"AI returned modified image using model {model_name}.")
                        # Return the image bytes
                        return part.inline_data.data
            
            logger.warning(f"Model {model_name} did not return image data.")
            logger.error("AI did not return image data.")
            return None
            
        except Exception as model_error:
            logger.error(f"Error with model {model_name}: {str(model_error)}")
            return None

    except Exception as e:
        logger.exception("Error in edit_image:")
        return None
