from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
import torch
from PIL import Image

class ImageGenerator:
    def _init_(self, model_id="stabilityai/stable-diffusion-2", device="cuda"):
        self.model_id = model_id
        self.device = device
        self.scheduler = None
        self.pipe = None

    def setup_pipeline(self):
        try:
            self.scheduler = EulerDiscreteScheduler.from_pretrained(self.model_id, subfolder="scheduler")
            self.pipe = StableDiffusionPipeline.from_pretrained(self.model_id, scheduler=self.scheduler, torch_dtype=torch.float16)
            self.pipe = self.pipe.to(self.device)
        except Exception as e:
            print(f"An error occurred during pipeline setup: {e}")
    
    def generate_image(self, prompt, output_path="output_image.png"):
        if self.pipe is None:
            print("Pipeline is not set up. Please call setup_pipeline first.")
            return
        
        try:
            print(f"Generating image for prompt: '{prompt}'")
            with torch.autocast(self.device):
                image = self.pipe(prompt).images[0]
            image.save(output_path)
            print(f"Image saved to {output_path}")
        except Exception as e:
            print(f"An error occurred during image generation: {e}")

if __name__ == "__main__":
    generator = ImageGenerator()
    generator.setup_pipeline()
    generator.generate_image("cricket in the street", "cricket_in_the_street.png")

# from crewAI.linkedin import Linkedimage
# import torch
# from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
# from diffusers.utils import export_to_video

# class TextToVideoGenerator:
#     def _init_(self, model_name="damo-vilab/text-to-video-ms-1.7b", torch_dtype=torch.float16, variant="fp16"):
#         self.pipe = DiffusionPipeline.from_pretrained(model_name, torch_dtype=torch_dtype, variant=variant)
#         self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(self.pipe.scheduler.config)
#         self.pipe.enable_model_cpu_offload()
#         self.pipe.enable_vae_slicing()

#     def generate_video(self, prompt, num_inference_steps=25, num_frames=50):
#         video_frames = self.pipe(prompt, num_inference_steps=num_inference_steps, num_frames=num_frames).frames
#         flattened_frames = [frame for sublist in video_frames for frame in sublist]
#         try:
#             video_path = export_to_video(flattened_frames)
#             print(f"Video exported to {video_path}")
#         except ValueError as e:
#             print(f"Error exporting video: {e}")

# if __name__ == "__main__":
#     generator = TextToVideoGenerator()
#     prompt = "astronaut riding horse"
#     generator.generate_video(prompt)