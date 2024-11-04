import torch

# Check if PyTorch is using the GPU
if torch.cuda.is_available():
    print(f"PyTorch is using the GPU: {torch.cuda.get_device_name(0)}")
else:
    print("PyTorch is using the CPU.")



