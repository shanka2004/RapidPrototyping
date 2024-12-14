from PIL import Image
import numpy as np
import trimesh

def image_to_3d_model(image_path, output_path, height_scale=1.0):
    # Load the image
    img = Image.open(image_path).convert("L")  # Convert to grayscale
    img_array = np.array(img)

    # Normalize image array to range [0, 1]
    normalized_array = img_array / 255.0

    # Scale heights
    heights = normalized_array * height_scale

    # Create vertices
    rows, cols = heights.shape
    vertices = []
    for i in range(rows):
        for j in range(cols):
            if heights[i, j] > 100:
                heights[i, j] = 100
            vertices.append([j, i, heights[i, j]])
    
    # Create faces
    faces = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Vertices for two triangles forming a quad
            v0 = i * cols + j
            v1 = v0 + 1
            v2 = v0 + cols
            v3 = v2 + 1

            # Triangle 1
            faces.append([v0, v1, v2])
            # Triangle 2
            faces.append([v1, v3, v2])

    # Convert to trimesh object
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

    # Export as STL
    mesh.export(output_path)
    print(f"3D model saved to {output_path}")

# Example usage
image_to_3d_model("test.png", "output_model.stl", height_scale=100.0)
