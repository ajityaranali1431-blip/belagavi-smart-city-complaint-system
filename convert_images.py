import base64

images = [
    ("D:\\Projects\\smart city\\images\\Screenshot_8-5-2026_142829_www.shutterstock.com.jpeg", "image1_base64.txt"),
    ("D:\\Projects\\smart city\\images\\images.jpg", "image2_base64.txt")
]

for img_path, output_path in images:
    with open(img_path, "rb") as f:
        data = base64.b64encode(f.read()).decode('utf-8')
        full_base64 = f"data:image/jpeg;base64,{data}"
        with open(output_path, "w", encoding='utf-8') as out:
            out.write(full_base64)
        print(f"Successfully wrote base64 for {img_path} to {output_path}")
