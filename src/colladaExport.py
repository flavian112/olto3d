import numpy as np
import collada

# -----------------------
# Helper Methods for Collada Export
# -----------------------

# Create 4x4 rotation matrix
def mat_rotate(x,y,z):

    xr = np.array([[1, 0, 0, 0],
                   [0, np.cos(x), -np.sin(x), 0],
                   [0, np.sin(x), np.cos(x), 0],
                   [0, 0, 0, 1]])

    yr = np.array([[np.cos(y), 0, np.sin(y), 0],
                   [0, 1, 0, 0],
                   [-np.sin(y), 0, np.cos(y), 0],
                   [0, 0, 0, 1]])

    zr = np.array([[np.cos(z), -np.sin(z), 0, 0],
                   [np.sin(z), np.cos(z), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

    return np.matmul(np.matmul(xr, yr), zr)

# Create 4x4 scalation matrix
def mat_scale(x,y,z):
    xyzs = np.array([[x, 0, 0, 0],
                     [0, y, 0, 0],
                     [0, 0, z, 0],
                     [0, 0, 0, 1]])

    return xyzs

# Create 4x4 translation matrix
def mat_translate(x, y, z):
    xyzt = np.array([[1, 0, 0, x],
                     [0, 1, 0, y],
                     [0, 0, 1, z],
                     [0, 0, 0, 1]])

    return xyzt

# Create terrain mesh from vertices
def createTerrain(verts, mesh):
    effect = collada.material.Effect("terrain-effect0", [], "phong", diffuse=(0,1,0), specular=(0,0,0))
    mat = collada.material.Material("terrain-material0", "terrainMaterial", effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    # reformat vertices array
    vert_arr = []
    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            y = verts[x][z]

            vert_arr += [x, y, z]


    vert_floats =  vert_arr


    # Calculate Normals between vertices
    normal_arr = []

    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            y = verts[x][z]

            # Each vertice has 3 normals connected to it
            # Normal is vector between surrounding vertices

            if (x < verts.shape[0] - 1 and z < verts.shape[1] - 1): # Case: Normals inside map
                xn1 = x + 1
                zn1 = z
                yn1 = verts[xn1][zn1]

                xn2 = -(x + 1)
                zn2 = -(z + 1)
                yn2 = -(verts[xn2][zn2])

                xn3 = x
                zn3 = z + 1
                yn3 = verts[xn3][zn3]

                normal_arr += [xn1, yn1, zn1, xn2, yn2, zn2, xn3, yn3, zn3]

            elif (x == verts.shape[0] - 1 and z < verts.shape[1] - 1): # Case: Normals at edge of map
                xn3 = x
                zn3 = z + 1
                yn3 = verts[xn3][zn3]

                normal_arr += [xn3, yn3, zn3]

            elif(z == verts.shape[1] - 1 and x < verts.shape[0] - 1): # Case: Normals at edge of map
                xn1 = x + 1
                zn1 = z
                yn1 = verts[xn1][zn1]

                normal_arr += [xn2, yn2, zn2]

    normal_floats = normal_arr

    vert_src = collada.source.FloatSource("terrain-verts-array", np.array(vert_floats), ('X', 'Y', 'Z'))
    normal_src = collada.source.FloatSource("terrain-normals-array", np.array(normal_floats), ('X', 'Y', 'Z'))
    geom = collada.geometry.Geometry(mesh, "geometry0", "terrain", [vert_src, normal_src])
    input_list = collada.source.InputList()
    input_list.addInput(0, 'VERTEX', "#terrain-verts-array")
    input_list.addInput(1, 'NORMAL', "#terrain-normals-array")


    # calculate indices that collada knows which vertices and normals correspond together
    # Normals and vertices of triangles must be saved as pairs. Each triangle consists of 3 vertices and 3 normals
    indices_arr = []
    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            if (x < verts.shape[0] - 2 and z < verts.shape[1] - 1): # Inside map case
                iv1 = x*verts.shape[1]+ z
                in1 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 2

                iv2 = x*verts.shape[1] + z + 1
                in2 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 3

                iv3 = (x + 1)*verts.shape[1] + z  + 1
                in3 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 1

                iv4 = iv1
                in6 = x*((verts.shape[1] - 1)*3 + 1) + z*(3)

                iv6 = (x + 1)*verts.shape[1] + z
                in5 = (x + 1)*((verts.shape[1] - 1)*3 + 1) + z*(3) + 2

                iv5 = iv3
                in4 = in3

                indices_arr += [iv1, in1, iv2, in2, iv3, in3, iv4, in4, iv5, in5, iv6, in6]

            elif (x < verts.shape[0] - 1 and z < verts.shape[1] - 1): # Edge case
                iv1 = x * verts.shape[1] + z
                in1 = x * ((verts.shape[1] - 1) * 3 + 1) + z*(3) + 2

                iv2 = x * verts.shape[1] + z + 1
                in2 = x * ((verts.shape[1] - 1) * 3 + 1) + z*(3) + 3

                iv3 = (x + 1) * verts.shape[1] + z + 1
                in3 = x * ((verts.shape[1] - 1) * 3 + 1) + z*(3) + 1

                iv4 = iv1
                in6 = x * ((verts.shape[1] - 1) * 3 + 1) + z

                iv6 = (x + 1) * verts.shape[1] + z
                in5 = (x + 1) * ((verts.shape[1] - 1) * 3 + 1) + z

                iv5 = iv3
                in4 = in3

                indices_arr += [iv1, in1, iv2, in2, iv3, in3, iv4, in4, iv5, in5, iv6, in6]


    indices = np.array(indices_arr)

    # Create triangles with data from above
    triset = geom.createTriangleSet(indices, input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    matnode = collada.scene.MaterialNode("materialref", mat, inputs=[])
    geomnode = collada.scene.GeometryNode(geom, [matnode])
    node = collada.scene.Node("terrainNode", children=[geomnode])

    mesh.scene.nodes.append(node)

    return mesh

def createMesh():
    # Create Colladamesh with empty root scene

    mesh = collada.Collada()
    rootscene = collada.scene.Scene("rootscene", [])
    mesh.scenes.append(rootscene)
    mesh.scene = rootscene
    return mesh





def loadMeshFromFile(path):
    mesh = collada.Collada(path)
    return mesh

def addNodeToMesh(mesh, nodes):
    mesh.scene.nodes += nodes
    return mesh

def addRessourcesToMesh(mesh, meshRessources):
    # Add ressources to mesh: Should only be run one per mesh Ressources
    mesh.scenes += meshRessources.scenes
    mesh.effects += meshRessources.effects
    mesh.materials += meshRessources.materials
    mesh.geometries += meshRessources.geometries
    mesh.images += meshRessources.images
    mesh.nodes += meshRessources.nodes

    return mesh


# Add object node to mesh
def addObjToMesh(mesh, obj, id, cords, scale=(1,1,1), rotation=(0,0,0)):
    xr, yr, zr, = rotation
    xs, ys, zs, = scale

    rot_scale = np.matmul(mat_rotate(xr, yr, zr), mat_scale(xs, ys, zs))

    objsnode = collada.scene.Node(id, children=[])

    for cord in cords:
        x, y, z = cord
        node_id = id + "-" + str(x) + "-" + str(y) + "-" + str(z)

        mat_transform = np.matmul(mat_translate(x,y,z), rot_scale)
        mat_transform = mat_transform.reshape((16,1))
        transform = collada.scene.MatrixTransform(mat_transform)

        objnode = collada.scene.Node(node_id, children=obj.scene.nodes, transforms=[transform])
        objsnode.children.append(objnode)

    mesh.scene.nodes.append(objsnode)
    return mesh

# Assets
tree = loadMeshFromFile('../ressources/assets/tree1.dae')
checkpoint = loadMeshFromFile('../ressources/assets/checkpoint.dae')
