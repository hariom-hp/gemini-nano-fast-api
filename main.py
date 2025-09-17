from fastapi import FastAPI, UploadFile, Form, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from services import edit_image
import io
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Gemini Image Editor API")

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint to verify the API is running.
    """
    return JSONResponse(
        content={"status": "ok", "message": "API is running"},
        status_code=200
    )

@app.post("/edit-image")
async def edit_image_endpoint(
    file: UploadFile,
    prompt: str = Form(...)
):
    """
    Upload an image + text prompt → get back modified image.
    """
    try:
        image_bytes = await file.read()
        logger.info(f"Received image: {file.filename}, size: {len(image_bytes)} bytes")
        
        # Ensure image_bytes is of type bytes
        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode()
        if isinstance(image_bytes, str):
            image_bytes = image_bytes.encode()
        result = edit_image(image_bytes1=image_bytes, prompt=prompt)

        if result is None:
            logger.error("edit_image function returned None.")
            raise HTTPException(status_code=500, detail="AI did not return an image")

        logger.info("Returning streaming response with the edited image.")
        return StreamingResponse(
            io.BytesIO(result),
            media_type="image/png"
        )

    except Exception as e:
        logger.exception("Error in /edit-image endpoint:")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/design/generate")
async def design_generate_endpoint(request: Request):
    """
    Flexible endpoint that can handle various forms of input.
    Upload an image + text prompt → get back modified image.
    """
    try:
        logger.info("Received request to /design/generate endpoint")
        
        # Check content type
        content_type = request.headers.get("content-type", "")
        logger.info(f"Content-Type: {content_type}")
        
        # Handle multipart form data
        if "multipart/form-data" in content_type:
            try:
                form_data = await request.form()
                
                # Log form data keys
                logger.info(f"Form data keys: {list(form_data.keys())}")
                
                # Log available keys for debugging
                form_keys = list(form_data.keys())
                logger.info(f"Available form keys: {form_keys}")
                
                # Handle the different parameter names from the client
                image_file = None
                for key in ["file", "image", "upload"]:
                    if key in form_data:
                        image_file = form_data[key]
                        logger.info(f"Found image with key: {key}")
                        break
                
                prompt_text = None
                for key in ["prompt", "text", "description"]:
                    if key in form_data:
                        prompt_text = form_data[key]
                        logger.info(f"Found prompt with key: {key}")
                        break
                
                if not image_file:
                    logger.error(f"Missing image file in request. Available keys: {form_keys}")
                    raise HTTPException(status_code=400, detail="Missing image file")
                
                if not prompt_text:
                    logger.error(f"Missing prompt in request. Available keys: {form_keys}")
                    raise HTTPException(status_code=400, detail="Missing prompt")
                
                # Read the image file
                try:
                    # Don't use type checking, just try to read it
                    logger.info(f"Reading image file of type {type(image_file)}")
                    image_bytes = await image_file.read()
                    logger.info(f"Successfully read image, size: {len(image_bytes)} bytes")
                except Exception as e:
                    logger.error(f"Error reading file: {str(e)}")
                    raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
                
                # Ensure prompt is a string
                prompt = str(prompt_text)
                logger.info(f"Prompt: {prompt}")
                
                # Ensure image_bytes is bytes
                if isinstance(image_bytes, str):
                    image_bytes = image_bytes.encode()
                elif not isinstance(image_bytes, bytes):
                    raise HTTPException(status_code=400, detail="Uploaded image is not in bytes format")
                # Process the image
                result = edit_image(image_bytes1=image_bytes, prompt=prompt)
                
                if result is None:
                    logger.error("edit_image function returned None.")
                    raise HTTPException(status_code=500, detail="AI did not return an image")
                
                logger.info("Returning streaming response with the edited image.")
                return StreamingResponse(
                    io.BytesIO(result),
                    media_type="image/png"
                )
                
            except Exception as e:
                logger.exception(f"Error processing form data: {str(e)}")
                raise HTTPException(status_code=400, detail=f"Error processing form data: {str(e)}")
        else:
            logger.error(f"Unsupported content type: {content_type}")
            raise HTTPException(
                status_code=415, 
                detail="Unsupported content type. Please use multipart/form-data with 'file' and 'prompt' fields."
            )
            
    except HTTPException:
        # Re-raise HTTP exceptions to preserve status codes
        raise
        
    except Exception as e:
        logger.exception(f"Error in /design/generate endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/debug")
async def debug_endpoint(request: Request):
    """
    Debug endpoint to inspect incoming requests.
    """
    try:
        # Get headers
        headers = dict(request.headers)
        logger.info(f"Request headers: {headers}")
        
        # Get body
        body = await request.body()
        logger.info(f"Request body length: {len(body)} bytes")
        
        # Get content type
        content_type = headers.get("content-type", "")
        logger.info(f"Content-Type: {content_type}")
        
        return JSONResponse(
            content={"status": "ok", "message": "Debug info logged"},
            status_code=200
        )
    except Exception as e:
        logger.exception(f"Error in debug endpoint: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

@app.post("/test-json")
async def test_json_endpoint(request: Request):
    """
    Test endpoint that always returns a JSON response.
    """
    try:
        form_data = await request.form()
        
        # Log form data keys
        logger.info(f"Test endpoint received form data keys: {list(form_data.keys())}")
        
        # Return a simple JSON response
        return JSONResponse(
            content={
                "status": "ok",
                "message": "This is a test JSON response",
                "receivedKeys": list(form_data.keys())
            },
            status_code=200
        )
    except Exception as e:
        logger.exception(f"Error in test endpoint: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )
