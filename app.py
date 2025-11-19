"""
Rubik's Cube Random Configuration Generator
A Streamlit app that generates and displays random 3x3 Rubik's cube configurations
"""

import streamlit as st
import random
import json
import plotly.graph_objects as go
import numpy as np

# Standard Rubik's cube colors
COLORS = {
    'W': '#FFFFFF',  # White (Up)
    'Y': '#FFFF00',  # Yellow (Down)
    'R': '#FF0000',  # Red (Front)
    'O': '#FF8800',  # Orange (Back)
    'B': '#0000FF',  # Blue (Right)
    'G': '#00FF00',  # Green (Left)
}

FACE_NAMES = {
    'U': 'Up (White)',
    'D': 'Down (Yellow)',
    'F': 'Front (Red)',
    'B': 'Back (Orange)',
    'R': 'Right (Blue)',
    'L': 'Left (Green)',
}

def create_solved_cube():
    """Create a solved cube state with each face having one color"""
    return {
        'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],
        'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],
        'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],
        'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],
        'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],
        'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],
    }

def generate_random_cube():
    """
    Generate a random but solvable Rubik's cube configuration.
    Uses a simple approach: start with solved cube and apply random moves.
    """
    cube = create_solved_cube()
    
    # Apply 20-30 random moves to scramble
    moves = ['U', 'D', 'F', 'B', 'R', 'L']
    num_scrambles = random.randint(20, 30)
    
    for _ in range(num_scrambles):
        move = random.choice(moves)
        apply_move(cube, move)
    
    return cube

def apply_move(cube, move):
    """
    Apply a 90-degree clockwise rotation to a face.
    This is a simplified version - enough to create valid scrambles.
    """
    if move == 'U':
        # Rotate Up face clockwise
        cube['U'] = rotate_face_cw(cube['U'])
        # Cycle edge pieces
        temp = cube['F'][0].copy()
        cube['F'][0] = cube['R'][0]
        cube['R'][0] = cube['B'][0]
        cube['B'][0] = cube['L'][0]
        cube['L'][0] = temp
    
    elif move == 'D':
        # Rotate Down face clockwise
        cube['D'] = rotate_face_cw(cube['D'])
        # Cycle edge pieces
        temp = cube['F'][2].copy()
        cube['F'][2] = cube['L'][2]
        cube['L'][2] = cube['B'][2]
        cube['B'][2] = cube['R'][2]
        cube['R'][2] = temp
    
    elif move == 'F':
        # Rotate Front face clockwise
        cube['F'] = rotate_face_cw(cube['F'])
        # Cycle edge pieces
        temp = [cube['U'][2][0], cube['U'][2][1], cube['U'][2][2]]
        cube['U'][2][0], cube['U'][2][1], cube['U'][2][2] = cube['L'][2][2], cube['L'][1][2], cube['L'][0][2]
        cube['L'][0][2], cube['L'][1][2], cube['L'][2][2] = cube['D'][0][0], cube['D'][0][1], cube['D'][0][2]
        cube['D'][0][0], cube['D'][0][1], cube['D'][0][2] = cube['R'][2][0], cube['R'][1][0], cube['R'][0][0]
        cube['R'][0][0], cube['R'][1][0], cube['R'][2][0] = temp[0], temp[1], temp[2]
    
    elif move == 'B':
        # Rotate Back face clockwise
        cube['B'] = rotate_face_cw(cube['B'])
        # Cycle edge pieces
        temp = [cube['U'][0][0], cube['U'][0][1], cube['U'][0][2]]
        cube['U'][0][0], cube['U'][0][1], cube['U'][0][2] = cube['R'][0][2], cube['R'][1][2], cube['R'][2][2]
        cube['R'][0][2], cube['R'][1][2], cube['R'][2][2] = cube['D'][2][2], cube['D'][2][1], cube['D'][2][0]
        cube['D'][2][0], cube['D'][2][1], cube['D'][2][2] = cube['L'][0][0], cube['L'][1][0], cube['L'][2][0]
        cube['L'][0][0], cube['L'][1][0], cube['L'][2][0] = temp[2], temp[1], temp[0]
    
    elif move == 'R':
        # Rotate Right face clockwise
        cube['R'] = rotate_face_cw(cube['R'])
        # Cycle edge pieces
        temp = [cube['F'][0][2], cube['F'][1][2], cube['F'][2][2]]
        cube['F'][0][2], cube['F'][1][2], cube['F'][2][2] = cube['D'][0][2], cube['D'][1][2], cube['D'][2][2]
        cube['D'][0][2], cube['D'][1][2], cube['D'][2][2] = cube['B'][2][0], cube['B'][1][0], cube['B'][0][0]
        cube['B'][0][0], cube['B'][1][0], cube['B'][2][0] = cube['U'][0][2], cube['U'][1][2], cube['U'][2][2]
        cube['U'][0][2], cube['U'][1][2], cube['U'][2][2] = temp[0], temp[1], temp[2]
    
    elif move == 'L':
        # Rotate Left face clockwise
        cube['L'] = rotate_face_cw(cube['L'])
        # Cycle edge pieces
        temp = [cube['F'][0][0], cube['F'][1][0], cube['F'][2][0]]
        cube['F'][0][0], cube['F'][1][0], cube['F'][2][0] = cube['U'][0][0], cube['U'][1][0], cube['U'][2][0]
        cube['U'][0][0], cube['U'][1][0], cube['U'][2][0] = cube['B'][2][2], cube['B'][1][2], cube['B'][0][2]
        cube['B'][0][2], cube['B'][1][2], cube['B'][2][2] = cube['D'][0][0], cube['D'][1][0], cube['D'][2][0]
        cube['D'][0][0], cube['D'][1][0], cube['D'][2][0] = temp[0], temp[1], temp[2]

def rotate_face_cw(face):
    """Rotate a 3x3 face 90 degrees clockwise"""
    return [
        [face[2][0], face[1][0], face[0][0]],
        [face[2][1], face[1][1], face[0][1]],
        [face[2][2], face[1][2], face[0][2]],
    ]

def render_face(face_data, face_name):
    """Render a single face as a 3x3 grid using HTML/CSS"""
    html = f"<div style='text-align: center; margin: 2px;'>"
    html += f"<h4 style='margin-bottom: 3px; font-size: 14px;'>{face_name}</h4>"
    html += "<div style='display: inline-block; border: 3px solid black;'>"
    
    for row in face_data:
        html += "<div style='display: flex;'>"
        for color in row:
            bg_color = COLORS[color]
            # Add border to make individual stickers visible
            html += f"<div style='width: 30px; height: 30px; background-color: {bg_color}; border: 2px solid #000;'></div>"
        html += "</div>"
    
    html += "</div></div>"
    return html

def create_3d_cube(cube_state):
    """Create a 3D visualization of the Rubik's cube using Plotly"""
    fig = go.Figure()
    
    # Define the 6 faces and their positions/orientations
    # Each face is a 3x3 grid of small cubes (stickers)
    sticker_size = 0.95  # Size of each sticker relative to cube unit
    gap = 0.05  # Gap between stickers
    
    faces_config = {
        'F': {'normal': [0, 0, 1], 'offset': [0, 0, 1.5], 'right': [1, 0, 0], 'up': [0, 1, 0]},  # Front (Red)
        'B': {'normal': [0, 0, -1], 'offset': [0, 0, -1.5], 'right': [-1, 0, 0], 'up': [0, 1, 0]},  # Back (Orange)
        'U': {'normal': [0, 1, 0], 'offset': [0, 1.5, 0], 'right': [1, 0, 0], 'up': [0, 0, -1]},  # Up (White)
        'D': {'normal': [0, -1, 0], 'offset': [0, -1.5, 0], 'right': [1, 0, 0], 'up': [0, 0, 1]},  # Down (Yellow)
        'R': {'normal': [1, 0, 0], 'offset': [1.5, 0, 0], 'right': [0, 0, -1], 'up': [0, 1, 0]},  # Right (Blue)
        'L': {'normal': [-1, 0, 0], 'offset': [-1.5, 0, 0], 'right': [0, 0, 1], 'up': [0, 1, 0]},  # Left (Green)
    }
    
    for face_name, config in faces_config.items():
        face_data = cube_state[face_name]
        normal = np.array(config['normal'])
        offset = np.array(config['offset'])
        right = np.array(config['right'])
        up = np.array(config['up'])
        
        # Draw each sticker on this face
        for row in range(3):
            for col in range(3):
                color_code = face_data[row][col]
                color = COLORS[color_code]
                
                # Calculate center position of this sticker
                center = offset + right * (col - 1) + up * (1 - row)
                
                # Create a small square for this sticker
                half_size = sticker_size / 2
                corners = [
                    center + right * half_size + up * half_size,
                    center - right * half_size + up * half_size,
                    center - right * half_size - up * half_size,
                    center + right * half_size - up * half_size,
                ]
                
                # Create mesh for this sticker
                x = [c[0] for c in corners] + [corners[0][0]]
                y = [c[1] for c in corners] + [corners[0][1]]
                z = [c[2] for c in corners] + [corners[0][2]]
                
                fig.add_trace(go.Scatter3d(
                    x=x, y=y, z=z,
                    mode='lines',
                    line=dict(color='black', width=3),
                    showlegend=False,
                    hoverinfo='skip'
                ))
                
                # Fill the sticker with color using Mesh3d
                fig.add_trace(go.Mesh3d(
                    x=[c[0] for c in corners],
                    y=[c[1] for c in corners],
                    z=[c[2] for c in corners],
                    i=[0, 0],
                    j=[1, 2],
                    k=[2, 3],
                    color=color,
                    opacity=1.0,
                    showlegend=False,
                    hoverinfo='skip',
                    flatshading=True
                ))
    
    # Update layout for better 3D view
    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False, range=[-2, 2]),
            yaxis=dict(visible=False, range=[-2, 2]),
            zaxis=dict(visible=False, range=[-2, 2]),
            aspectmode='cube',
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.5),
                center=dict(x=0, y=0, z=0)
            ),
            bgcolor='rgba(240,240,240,0.9)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        height=500,
        showlegend=False
    )
    
    return fig

def main():
    """Main Streamlit app"""
    st.set_page_config(page_title="Rubik's Cube Generator", layout="wide")
    
    st.title("🎲 Random Rubik's Cube Generator")
    st.write("Generate random 3x3 Rubik's cube configurations and export them as JSON")
    
    # Initialize session state for cube
    if 'cube' not in st.session_state:
        st.session_state.cube = create_solved_cube()
    
    # Button to generate random cube
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Generate Random Cube", type="primary"):
            st.session_state.cube = generate_random_cube()
            st.rerun()
    
    # Display cube in 2 columns: 2D unfolded view and 3D view
    st.subheader("Cube Visualization")
    
    # Create 2 columns for the layout
    left_col, right_col = st.columns([1, 1])
    
    with left_col:
        st.write("**2D Unfolded Layout:**")
        # Row 1: Back, Up
        st.markdown(render_face(st.session_state.cube['B'], FACE_NAMES['B']), unsafe_allow_html=True)
        st.markdown(render_face(st.session_state.cube['U'], FACE_NAMES['U']), unsafe_allow_html=True)
        # Row 2: Left, Front
        st.markdown(render_face(st.session_state.cube['L'], FACE_NAMES['L']), unsafe_allow_html=True)
        st.markdown(render_face(st.session_state.cube['F'], FACE_NAMES['F']), unsafe_allow_html=True)
        # Row 3: Right, Down
        st.markdown(render_face(st.session_state.cube['R'], FACE_NAMES['R']), unsafe_allow_html=True)
        st.markdown(render_face(st.session_state.cube['D'], FACE_NAMES['D']), unsafe_allow_html=True)
    
    with right_col:
        st.write("**3D Interactive View:**")
        fig = create_3d_cube(st.session_state.cube)
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Display cube state as JSON
    st.subheader("Cube State (JSON)")
    st.json(st.session_state.cube)
    
    # Export to JSON button
    cube_json = json.dumps(st.session_state.cube, indent=2)
    st.download_button(
        label="📥 Export to JSON",
        data=cube_json,
        file_name="rubiks_cube_state.json",
        mime="application/json",
    )

if __name__ == "__main__":
    main()
