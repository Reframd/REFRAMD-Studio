import os
import streamlit as st
import trimesh
import plotly.graph_objects as go

# Define parameter ranges
lens_width_range = [40, 45, 50]
lens_height_range = [30, 35, 40]
bridge_width_range = [10, 15, 20]
bridge_types = ["Classic", "Keyhole"]
temple_length_range = [130, 140, 150]

# Path to your 3D files
file_directory = "/Users/ackeem/Dropbox/Work/Team Reframd/Designs/REFRAMD_Web_Files"

# Streamlit layout
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .css-1outpf7 {padding-top: 0rem;}  /* Remove padding at the top */
    .css-1d391kg {padding: 0rem;}      /* Remove padding around the app */
    iframe {height: 100vh !important;} /* Set iframe (Plotly charts) to full height */
    </style>
    """,
    unsafe_allow_html=True,
)

# Add sliders for parameter selection on the left column
col1, col2 = st.columns([2, 5], gap="small")

with col1:
    st.header("Adjust Parameters")
    selected_lens_width = st.slider("Lens Width (mm)", min_value=min(lens_width_range), max_value=max(lens_width_range), step=5)
    selected_lens_height = st.slider("Lens Height (mm)", min_value=min(lens_height_range), max_value=max(lens_height_range), step=5)
    selected_bridge_width = st.slider("Bridge Width (mm)", min_value=min(bridge_width_range), max_value=max(bridge_width_range), step=5)
    selected_bridge_type = st.selectbox("Bridge Type", bridge_types)
    selected_temple_length = st.slider("Temple Length (mm)", min_value=min(temple_length_range), max_value=max(temple_length_range), step=10)

# Construct the file name based on selected parameters
file_name = (
    f"lens_width_{selected_lens_width}_"
    f"lens_height_{selected_lens_height}_"
    f"bridge_width_{selected_bridge_width}_"
    f"bridge_type_{selected_bridge_type}_"
    f"temple_length_{selected_temple_length}.glb"
)
file_path = os.path.join(file_directory, file_name)

# Display visualization in the right column (full height)
with col2:
    st.header("3D Visualization")
    try:
        if os.path.exists(file_path):
            # Load the 3D model
            scene = trimesh.load(file_path)

            # Prepare the plotly Mesh3d data for all geometries in the scene
            fig = go.Figure()
            if isinstance(scene, trimesh.Scene):
                for name, mesh in scene.geometry.items():
                    vertices = mesh.vertices
                    faces = mesh.faces
                    fig.add_trace(
                        go.Mesh3d(
                            x=vertices[:, 0],
                            y=vertices[:, 1],
                            z=vertices[:, 2],
                            i=faces[:, 0],
                            j=faces[:, 1],
                            k=faces[:, 2],
                            color="#3b63e9",
                            opacity=1,
                            lighting=dict(
                                ambient=0.5,
                                diffuse=0.7,
                                specular=1.0,
                                roughness=0.2,
                                fresnel=0.3,
                            ),
                            lightposition=dict(x=50, y=50, z=100),
                            name=name,
                        )
                    )
            elif isinstance(scene, trimesh.Trimesh):
                vertices = scene.vertices
                faces = scene.faces
                fig.add_trace(
                    go.Mesh3d(
                        x=vertices[:, 0],
                        y=vertices[:, 1],
                        z=vertices[:, 2],
                        i=faces[:, 0],
                        j=faces[:, 1],
                        k=faces[:, 2],
                        color="#2a71ff",
                        opacity=1,
                        lighting=dict(
                            ambient=0.9,
                            diffuse=0.8,
                            specular=0.5,
                            roughness=0.2,
                            fresnel=0.3,
                        ),
                        lightposition=dict(x=50, y=50, z=100),
                    )
                )
            else:
                raise TypeError("Loaded object is neither a Scene nor a Trimesh.")

            # Define viewports: front, right, top, and perspective
            views = {
                "Perspective": dict(eye=dict(x=1.2, y=1.2, z=1.2)),
                "Front": dict(eye=dict(x=0, y=0, z=2), up=dict(x=0, y=1, z=0)),
                "Right": dict(eye=dict(x=2, y=0, z=0)),
                "Top": dict(eye=dict(x=0, y=3, z=0)),
            }

            # Create tabs for viewports
            tabs = st.tabs(views.keys())
            for tab, (view_name, camera_view) in zip(tabs, views.items()):
                with tab:
                    # Allow rotation only for the perspective view
                    dragmode = "orbit" if view_name == "Perspective" else False

                    fig.update_layout(
                        scene=dict(
                            bgcolor="rgb(242, 242, 242)",
                            xaxis=dict(title="X", showgrid=True, backgroundcolor="rgb(100,100,100)"),
                            yaxis=dict(title="Y", showgrid=True, backgroundcolor="rgb(100,100,100)"),
                            zaxis=dict(title="Z", showgrid=True, backgroundcolor="rgb(100,100,100)"),
                            camera=camera_view,
                        ),
                        dragmode=dragmode,
                        margin=dict(l=0, r=0, t=0, b=0),
                        height=800,  # Full-screen height for better display
                    )
                    st.plotly_chart(fig, use_container_width=True)

        else:
            st.error(f"File not found: {file_name}. Please check the parameters or file location.")

    except Exception as e:
        st.error(f"An error occurred while loading the 3D file: {e}")

# Instructions at the bottom
st.markdown("""
1. Use the sliders on the left to adjust parameters.
2. The configurator checks for the corresponding 3D file based on the selected values.
3. Ensure the files follow the correct naming convention and are in the specified directory.
""")