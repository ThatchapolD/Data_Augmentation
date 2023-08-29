import torch
import torchvision.models as models
model = models.resnet18()
checkpoint = torch.load("C:/Users/ASUS/Desktop/Dataset_for_Faster_RCNN/model_final.pth")
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()
from PIL import Image
import torchvision.transforms as transforms
image_path = "C:/Users/ASUS/Downloads/MT3CF4.jpg"  # Replace with the path to your image
image = Image.open(image_path).convert('RGB')
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Apply transformations and add a batch dimension
input_tensor = preprocess(image)
input_batch = input_tensor.unsqueeze(0)
with torch.no_grad():
    output = model(input_batch)

# Assuming it's an image classification model, get the predicted class index
predicted_class_index = output.argmax().item()