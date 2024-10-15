import torch

def check_and_activate_gpu():
    # Check if CUDA (GPU) is available
    if torch.cuda.is_available():
        # Get the number of GPUs available
        num_gpus = torch.cuda.device_count()
        print(f"Number of GPUs available: {num_gpus}")
        
        # Print details for each available GPU
        for i in range(num_gpus):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        
        # Activate the first GPU (default)
        device = torch.device("cuda:0")
        print(f"Activated GPU: {torch.cuda.get_device_name(0)}")

        # Optionally, set the desired GPU
        torch.cuda.set_device(device)
        print(f"Current GPU: {torch.cuda.current_device()}")
        
    else:
        print("CUDA (GPU) is not available. Falling back to CPU.")
        device = torch.device("cpu")
    
    # Return the activated device (GPU or CPU)
    return device

if __name__ == "__main__":
    device = check_and_activate_gpu()

    # Example usage: Create a tensor and move it to the appropriate device
    example_tensor = torch.tensor([1.0, 2.0, 3.0])
    example_tensor = example_tensor.to(device)
    print(f"Tensor is on device: {example_tensor.device}")
