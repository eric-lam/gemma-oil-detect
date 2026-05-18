import torch
import timm

# 定义三个模型
models_to_download = {
    "mobilenetv3_large_100": "mobilenetv3_large_100_timm.pth"
}

for model_name, save_name in models_to_download.items():
    print(f"Downloading {model_name} ...")
    # 创建预训练模型（自动下载权重到缓存）
    model = timm.create_model(model_name, pretrained=True)
    # 保存 state_dict 到当前目录
    torch.save(model.state_dict(), save_name)
    print(f"Saved to {save_name}")