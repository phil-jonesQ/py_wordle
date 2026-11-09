import pygame
import math
from pygame.math import Vector3

# Constants
WIDTH, HEIGHT = 800, 600
FOV = 300  # Field of View
ROTATE_SPEED = 0.02

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Rubik\'s Cube with Phong Shading')
clock = pygame.time.Clock()

# 3D cube vertices
vertices = [(-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
            (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)]

# 3D cube faces (connecting vertices)
faces = [(0, 1, 3, 2), (4, 5, 7, 6),
         (0, 1, 5, 4), (2, 3, 7, 6),
         (0, 2, 6, 4), (1, 3, 7, 5)]

angle_x, angle_y, angle_z = 0, 0, 0

light_source = Vector3(0, -1, -1).normalize()  # Direction of the light source

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a new surface for drawing
    back_buffer = pygame.Surface(window.get_size())

    # Apply rotation to the vertices
    rotated_vertices = []
    for vertex in vertices:
        x, y, z = vertex
        # Rotate around X-axis
        rotated_y = y * math.cos(angle_x) - z * math.sin(angle_x)
        rotated_z = y * math.sin(angle_x) + z * math.cos(angle_x)
        # Rotate around Y-axis
        rotated_x = x * math.cos(angle_y) + z * math.sin(angle_y)
        rotated_z = -x * math.sin(angle_y) + z * math.cos(angle_y)
        # Rotate around Z-axis
        rotated_x = rotated_x * math.cos(angle_z) - rotated_y * math.sin(angle_z)
        rotated_y = rotated_x * math.sin(angle_z) + rotated_y * math.cos(angle_z)
        # Perspective projection
        perspective = FOV / (rotated_z + 5)  # +5 is used to avoid division by zero
        screen_x = int(rotated_x * perspective + WIDTH / 2)
        screen_y = int(rotated_y * perspective + HEIGHT / 2)
        rotated_vertices.append(Vector3(screen_x, screen_y, rotated_z))  # Store as Vector3 instances

    # Calculate face normals and apply Phong shading
    for face in faces:
        # Calculate face normal using cross product of two edges
        edge1 = rotated_vertices[face[1]] - rotated_vertices[face[0]]
        edge2 = rotated_vertices[face[2]] - rotated_vertices[face[1]]
        normal = edge1.cross(edge2).normalize()

        # Calculate intensity based on the dot product of the face normal and light direction
        intensity = max(normal.dot(light_source), 0)
        
        # Calculate diffuse reflection using Phong shading model
        ambient_coefficient = 0.2  # Ambient reflection coefficient
        diffuse_coefficient = 0.8  # Diffuse reflection coefficient
        ambient_color = (255, 255, 255)  # Ambient light color (white)
        diffuse_color = (255, 255, 255)  # Diffuse light color (white)
        
        # Calculate final color using Phong shading model
        ambient = tuple(int(ambient_color[i] * ambient_coefficient) for i in range(3))
        diffuse = tuple(int(diffuse_color[i] * intensity * diffuse_coefficient) for i in range(3))
        color = tuple(min(ambient[i] + diffuse[i], 255) for i in range(3))

        # Fill face with lighting effect
        vertices_to_draw = [(rotated_vertices[face[i]].x, rotated_vertices[face[i]].y) for i in range(len(face))]
        pygame.draw.polygon(back_buffer, color, vertices_to_draw)

    # Blit the back buffer onto the window
    window.blit(back_buffer, (0, 0))

    pygame.display.flip()

    # Rotate the cube
    angle_x += ROTATE_SPEED  # X-axis rotation
    angle_y += ROTATE_SPEED  # Y-axis rotation
    #angle_z += ROTATE_SPEED  # Z-axis rotation

    clock.tick(60)

pygame.quit()
