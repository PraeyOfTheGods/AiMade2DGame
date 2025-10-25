import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# Create a flowchart using plotly shapes and annotations
fig = go.Figure()

# Define positions for flowchart elements
positions = {
    'start': (5, 10),
    'decision': (5, 8.5),
    'left_rotate': (2, 7),
    'right_rotate': (8, 7),
    'reset': (5, 6.5),
    'tumble': (5, 5.5),
    'gravity': (5, 4),
    'collision': (5, 2.5),
    'on_platform': (2, 1),
    'in_air': (8, 1)
}

# Colors from the theme
colors = ['#1FB8CD', '#DB4545', '#2E8B57', '#5D878F', '#D2BA4C']

# Add rectangular boxes for processes
processes = [
    ('start', 'Start: Player on Platform'),
    ('left_rotate', 'Rotate 90° CCW\n+ Move Left'),
    ('right_rotate', 'Rotate 90° CW\n+ Move Right'),
    ('reset', 'Reset to Start Position'),
    ('tumble', 'Rectangle Tumbles\non Edge'),
    ('gravity', 'Gravity Applied:\nPlayer Falls'),
    ('on_platform', 'Can Rotate Again'),
    ('in_air', 'Continue Falling')
]

for i, (key, text) in enumerate(processes):
    x, y = positions[key]
    color = colors[i % len(colors)]
    
    # Add rectangle
    fig.add_shape(
        type="rect",
        x0=x-0.8, y0=y-0.3, x1=x+0.8, y1=y+0.3,
        fillcolor=color,
        opacity=0.7,
        line=dict(color="#13343B", width=2)
    )
    
    # Add text
    fig.add_annotation(
        x=x, y=y,
        text=text,
        showarrow=False,
        font=dict(size=10, color="#13343B"),
        align="center"
    )

# Add diamond shapes for decisions
decisions = [
    ('decision', 'Arrow Key\nPressed?'),
    ('collision', 'Collision Check\nwith Platforms')
]

for key, text in decisions:
    x, y = positions[key]
    
    # Create diamond shape using four points
    diamond_x = [x, x+0.8, x, x-0.8, x]
    diamond_y = [y+0.4, y, y-0.4, y, y+0.4]
    
    fig.add_shape(
        type="path",
        path=f"M {diamond_x[0]} {diamond_y[0]} L {diamond_x[1]} {diamond_y[1]} L {diamond_x[2]} {diamond_y[2]} L {diamond_x[3]} {diamond_y[3]} Z",
        fillcolor="#FFEB8A",
        opacity=0.7,
        line=dict(color="#13343B", width=2)
    )
    
    # Add text
    fig.add_annotation(
        x=x, y=y,
        text=text,
        showarrow=False,
        font=dict(size=10, color="#13343B"),
        align="center"
    )

# Add arrows to show flow
arrows = [
    # From start to decision
    (positions['start'], positions['decision']),
    # From decision to actions
    (positions['decision'], positions['left_rotate']),
    (positions['decision'], positions['right_rotate']),
    (positions['decision'], positions['reset']),
    # From rotations to tumble
    (positions['left_rotate'], positions['tumble']),
    (positions['right_rotate'], positions['tumble']),
    # From tumble to gravity
    (positions['tumble'], positions['gravity']),
    # From gravity to collision
    (positions['gravity'], positions['collision']),
    # From collision to outcomes
    (positions['collision'], positions['on_platform']),
    (positions['collision'], positions['in_air']),
    # Loop backs
    (positions['on_platform'], positions['decision']),
    (positions['in_air'], positions['gravity']),
    (positions['reset'], positions['start'])
]

for (start_pos, end_pos) in arrows:
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    
    # Adjust arrow positions to connect to box edges
    if start_y > end_y:  # Arrow going down
        start_y -= 0.3
        end_y += 0.3 if 'collision' not in str(end_pos) else 0.4
    elif start_y < end_y:  # Arrow going up
        start_y += 0.3
        end_y -= 0.3 if 'collision' not in str(start_pos) else 0.4
    
    if start_x != end_x:  # Horizontal adjustment
        if start_x > end_x:
            start_x -= 0.8
            end_x += 0.8
        else:
            start_x += 0.8
            end_x -= 0.8
    
    fig.add_annotation(
        x=end_x, y=end_y,
        ax=start_x, ay=start_y,
        xref="x", yref="y",
        axref="x", ayref="y",
        showarrow=True,
        arrowhead=2,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="#13343B"
    )

# Add labels for decision paths
fig.add_annotation(x=3.5, y=7.7, text="LEFT", showarrow=False, font=dict(size=9, color="#13343B"))
fig.add_annotation(x=6.5, y=7.7, text="RIGHT", showarrow=False, font=dict(size=9, color="#13343B"))
fig.add_annotation(x=5.3, y=7.5, text="R", showarrow=False, font=dict(size=9, color="#13343B"))
fig.add_annotation(x=3.5, y=1.7, text="On Platform", showarrow=False, font=dict(size=9, color="#13343B"))
fig.add_annotation(x=6.5, y=1.7, text="In Air", showarrow=False, font=dict(size=9, color="#13343B"))

# Set layout
fig.update_layout(
    title="Rotating Rectangle Platformer Mechanics",
    xaxis=dict(range=[0, 10], showgrid=False, showticklabels=False, zeroline=False),
    yaxis=dict(range=[0, 11], showgrid=False, showticklabels=False, zeroline=False),
    showlegend=False,
    plot_bgcolor='white'
)

# Save the chart
fig.write_image("platformer_flowchart.png")
fig.write_image("platformer_flowchart.svg", format="svg")
print("Flowchart saved as platformer_flowchart.png and platformer_flowchart.svg")