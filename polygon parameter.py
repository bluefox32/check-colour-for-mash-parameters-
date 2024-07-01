import trimesh
import numpy as np
import matplotlib.pyplot as plt

# 素材特性の判定関数
def material_properties(color):
    metal_colors = [(192, 192, 192), (169, 169, 169)]  # Silver, DarkGray
    non_metal_colors = [(255, 255, 255), (128, 128, 128)]  # White, Gray

    if color in metal_colors:
        hardness = 8.0
        reflectivity = 0.8
        transparency = 0.0
    elif color in non_metal_colors:
        hardness = 3.0
        reflectivity = 0.3
        transparency = 0.1
    else:
        hardness = 1.0
        reflectivity = 0.1
        transparency = 0.0

    return hardness, reflectivity, transparency

# メッシュデータを読み込む
mesh = trimesh.load_mesh('path_to_your_mesh.obj')

# 頂点の色情報を取得（実際のメッシュデータに色情報が含まれている場合）
if hasattr(mesh.visual, 'vertex_colors'):
    vertex_colors = mesh.visual.vertex_colors[:, :3]  # RGB値の取得
else:
    # 仮の頂点色データの生成
    vertex_colors = np.random.choice([(192, 192, 192), (169, 169, 169), (255, 255, 255), (128, 128, 128)], size=mesh.vertices.shape[0])

# 各頂点の素材特性を判定
vertex_materials = np.array([material_properties(tuple(color)) for color in vertex_colors])

# 法線ベクトルを計算
mesh.compute_vertex_normals()
normals = mesh.vertex_normals

# エッジを検出するための閾値
angle_threshold = np.radians(30)  # 30度

# エッジの検出
edges = []
for edge in mesh.edges_unique:
    normal1 = normals[edge[0]]
    normal2 = normals[edge[1]]
    angle = np.arccos(np.clip(np.dot(normal1, normal2), -1.0, 1.0))
    if angle > angle_threshold:
        edges.append(edge)

# 結果を表示
edges = np.array(edges)
edge_points = mesh.vertices[edges]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# メッシュをプロット
ax.plot_trisurf(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], triangles=mesh.faces, alpha=0.1)

# エッジをプロット
for edge in edge_points:
    ax.plot(edge[:, 0], edge[:, 1], edge[:, 2], color='r')

plt.show()

# 各頂点の素材特性の表示
for i, vertex in enumerate(mesh.vertices):
    hardness, reflectivity, transparency = vertex_materials[i]
    print(f"Vertex {i}: Hardness={hardness}, Reflectivity={reflectivity}, Transparency={transparency}")