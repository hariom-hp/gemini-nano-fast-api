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

def edit_image(image_bytes: bytes, prompt: str):
    """
    Takes image bytes and a prompt, and returns the modified image bytes.
    """
    try:
        # Check if API key is configured
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("No GOOGLE_API_KEY found in environment variables")
            raise ValueError("Missing API key. Please configure GOOGLE_API_KEY in .env file.")
        
        # Improve the prompt by making it more specific
        enhanced_prompt = f"Edit this image to {prompt}. Return the modified image."
        logger.info(f"Processing image edit request with prompt: {enhanced_prompt[:100]}...")
        
        # Open and verify the image
        try:
            image = Image.open(BytesIO(image_bytes))
            logger.info(f"Successfully opened image: {image.format}, size: {image.size}, mode: {image.mode}")
            
            # Convert to RGB if needed (some formats like RGBA might cause issues)
            if image.mode != "RGB":
                logger.info(f"Converting image from {image.mode} to RGB")
                image = image.convert("RGB")
                
        except Exception as img_error:
            logger.error(f"Failed to process image: {str(img_error)}")
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
                response = model.generate_content([enhanced_prompt, image])
            except Exception as config_error:
                logger.warning(f"Error with basic config: {str(config_error)}. Trying alternative approaches...")
                
                # Try different approaches based on the API version
                try:
                    # Try with generation_config as a named parameter
                    response = model.generate_content(
                        [enhanced_prompt, image],
                        generation_config={"temperature": 0.7}
                    )
                except:
                    # Last resort - just try with the content only
                    response = model.generate_content([enhanced_prompt, image])
            
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
