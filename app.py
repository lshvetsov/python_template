from transformers import pipeline
import gradio as gr
import numpy as np

# Load the model
model = pipeline(
    "text-to-video-generation",
    model="stabilityai/stable-video-diffusion-img2vid-xt"
)

def predict(image, prompt):
    # Convert the image to the format expected by the model
    image = np.array(image)

    # Generate the video using the model
    video = model(image=image, prompt=prompt)

    # The output from the model is a dictionary with a 'video' key containing the video file path
    video_path = video['video'][0]

    return video_path

# Create the Gradio interface
with gr.Interface(
        fn=predict,
        inputs=[gr.inputs.Image(type="pil"), gr.inputs.Textbox(label="Text Prompt")],
        outputs=gr.outputs.Video(label="Generated Video"),
        title="Image and Text to Video Generation",
        description="Upload an image and enter a text prompt to generate a video."
) as interface:
    interface.launch()