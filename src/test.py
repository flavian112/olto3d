import numpy as np
import cv2

import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import collada



verts = np.array([[1,2,1,3],
                  [1,2,2,1],
                  [1,1,1,1],
                  [0,0,0,0]])

def toCollada(verts):
    mesh = collada.Collada()
    effect = collada.material.Effect("effect0", [], "phong", diffuse=(0,1,0), specular=(0,0,0))
    mat = collada.material.Material("material0", "mymaterial", effect)
    mesh.effects.append(effect)
    mesh.materials.append(mat)

    vert_arr = []
    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            y = verts[x][z]

            vert_arr += [x, y, z]


    vert_floats =  vert_arr

    # print(len(vert_arr)//3)
    # print(vert_arr)

    normal_arr = []



    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            y = verts[x][z]

            if (x < verts.shape[0] - 1 and z < verts.shape[1] - 1):
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

            elif (x == verts.shape[0] - 1 and z < verts.shape[1] - 1):
                xn3 = x
                zn3 = z + 1
                yn3 = verts[xn3][zn3]

                normal_arr += [xn3, yn3, zn3]

            elif(z == verts.shape[1] - 1 and x < verts.shape[0] - 1):
                xn1 = x + 1
                zn1 = z
                yn1 = verts[xn1][zn1]

                normal_arr += [xn2, yn2, zn2]

    # print(len(normal_arr)//3)
    # print(normal_arr)

    normal_floats = normal_arr

    vert_src = collada.source.FloatSource("cubeverts-array", np.array(vert_floats), ('X', 'Y', 'Z'))
    normal_src = collada.source.FloatSource("cubenormals-array", np.array(normal_floats), ('X', 'Y', 'Z'))
    geom = collada.geometry.Geometry(mesh, "geometry0", "mycube", [vert_src, normal_src])
    input_list = collada.source.InputList()
    input_list.addInput(0, 'VERTEX', "#cubeverts-array")
    input_list.addInput(1, 'NORMAL', "#cubenormals-array")

    indices_arr = []

    for x in range(verts.shape[0]):
        for z in range(verts.shape[1]):
            if (x < verts.shape[0] - 2 and z < verts.shape[1] - 1):
                iv1 = x*verts.shape[1]+ z
                in1 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 2

                iv2 = x*verts.shape[1] + z + 1
                in2 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 3

                iv3 = (x + 1)*verts.shape[1] + z  + 1
                in3 = x*((verts.shape[1] - 1)*3 + 1) + z*(3) + 1

                iv4 = iv1
                in4 = x*((verts.shape[1] - 1)*3 + 1) + z*(3)

                iv5 = (x + 1)*verts.shape[1] + z
                in5 = (x + 1)*((verts.shape[1] - 1)*3 + 1) + z*(3) + 2

                iv6 = iv3
                in6 = in3

                indices_arr += [iv1, in1, iv2, in2, iv3, in3, iv4, in4, iv5, in5, iv6, in6]

            elif (x < verts.shape[0] - 1 and z < verts.shape[1] - 1):
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
    in1 = []
    in2 = []

    # for i in range(indices.size):
    #     if (i % 2 == 0):
    #         in1.append(indices[i])
    #     else:
    #         in2.append(indices[i])
    #
    # print(len(indices_arr)//6)
    # print(in1)
    # print(max(in1))
    # print(in2)
    # print(max(in2))

    triset = geom.createTriangleSet(indices, input_list, "materialref")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)

    matnode = collada.scene.MaterialNode("materialref", mat, inputs=[])
    geomnode = collada.scene.GeometryNode(geom, [matnode])
    node = collada.scene.Node("node0", children=[geomnode])

    myscene = collada.scene.Scene("myscene", [node])
    mesh.scenes.append(myscene)
    mesh.scene = myscene

    mesh.write('test.dae')
    print("Done")






