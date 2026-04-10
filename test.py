import numpy as np
import plotly.graph_objects as go

# --- CONFIGURATION ---
LINK_LENGTH = 5
AXIS_LENGTH = 2
CANVAS_RANGE = [-6, 6]
WIDTH = 600
HEIGHT = 400  # 3:2 Aspect Ratio

def create_link_traces(theta_deg):
    """Generates the traces for a single frame of the revolute joint."""
    theta_rad = np.radians(theta_deg)
    x_e, y_e = LINK_LENGTH * np.cos(theta_rad), LINK_LENGTH * np.sin(theta_rad)
    
    # Axes - Text color changed to white for Dark Mode
    ax_x = go.Scatter(x=[0, AXIS_LENGTH], y=[0, 0], mode='lines+text', name="X-Axis",
                      line=dict(color='red', width=2), text=["", "X"], 
                      textposition="top right", textfont=dict(color="white"))
    ax_y = go.Scatter(x=[0, 0], y=[0, AXIS_LENGTH], mode='lines+text', name="Y-Axis",
                      line=dict(color='green', width=2), text=["", "Y"], 
                      textposition="top right", textfont=dict(color="white"))

    # Linkage
    link = go.Scatter(
        x=[0, x_e], y=[0, y_e], mode='lines+markers', name="Position",
        line=dict(width=16, color='#3498db'), 
        marker=dict(size=22, color=['#2c3e50', '#e74c3c'], line=dict(width=2, color='white'))
    )

    # Motion Arc
    t = np.linspace(0, theta_rad, 30)
    arc = go.Scatter(x=1.5 * np.cos(t), y=1.5 * np.sin(t), mode='lines', name="Joint angle",
                     line=dict(color='rgba(255, 165, 0, 0.6)', width=3, dash='dot'))

    return [ax_x, ax_y, arc, link]

def get_layout_settings(angles):
    """Defines the visual style and slider behavior."""
    sliders = [dict(
        active=0,
        # Slider font color changed to off-white
        currentvalue={"prefix": "θ: ", "suffix": "°", "font": {"size": 18, "color": "#ecf0f1"}},
        pad={"t": 50},
        steps=[dict(method="animate", label=str(a),
                    args=[[str(a)], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}]) 
               for a in angles]
    )]

    return dict(
        xaxis=dict(range=CANVAS_RANGE, visible=False, fixedrange=True),
        yaxis=dict(range=CANVAS_RANGE, visible=False, fixedrange=True, scaleanchor="x", scaleratio=1),
        sliders=sliders,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        width=WIDTH, height=HEIGHT,
        margin=dict(l=10, r=10, t=10, b=10),
        # Annotation color changed to a lighter blue for Dark Mode
        annotations=[dict(x=0.5, y=-0.7, text="Z (Rotation Axis)", showarrow=False, font=dict(color="#5dade2"))]
    )

def build_revolute_viz():
    """Main factory function to assemble the figure."""
    fig = go.Figure()
    angles = np.arange(0, 181, 2)
    
    # Initialize
    fig.add_traces(create_link_traces(angles[0]))
    
    # Build Frames
    fig.frames = [go.Frame(data=create_link_traces(a), name=str(a)) for a in angles]
    
    # Finalize Layout
    fig.update_layout(**get_layout_settings(angles))
    
    return fig

# Display for Quarto
fig = build_revolute_viz()
fig.show()