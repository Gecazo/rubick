"""
Rubik's Cube Random Configuration Generator
A Streamlit app that generates and displays random 3x3 Rubik's cube configurations
"""

import streamlit as st
import random
import json

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
    
    # Display cube in 2x3 grid layout
    st.subheader("Cube Visualization")
    st.write("Standard unfolded cube layout:")
    
    # Create 2 columns for the layout
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Row 1: Back, Up
        st.markdown(render_face(st.session_state.cube['B'], FACE_NAMES['B']), unsafe_allow_html=True)
        st.markdown(render_face(st.session_state.cube['U'], FACE_NAMES['U']), unsafe_allow_html=True)
        # Row 2: Left, Front
        st.markdown(render_face(st.session_state.cube['L'], FACE_NAMES['L']), unsafe_allow_html=True)
        st.markdown(render_face(st.session_state.cube['F'], FACE_NAMES['F']), unsafe_allow_html=True)
    
    with right_col:
        # Row 2: Right (aligned with Front)
        st.markdown("<div style='height: 130px;'></div>", unsafe_allow_html=True)  # Spacer
        st.markdown(render_face(st.session_state.cube['R'], FACE_NAMES['R']), unsafe_allow_html=True)
        # Row 3: Down
        st.markdown(render_face(st.session_state.cube['D'], FACE_NAMES['D']), unsafe_allow_html=True)
    
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
