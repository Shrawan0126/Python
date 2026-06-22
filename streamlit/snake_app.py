import streamlit as st
st.rerun()
import numpy as np
import plotly.graph_objects as go
import random

# Initialize session state
if "snake" not in st.session_state:
    st.session_state.snake = [(5, 5, 5)]
    st.session_state.direction = (1, 0, 0)
    st.session_state.food = (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
    st.session_state.score = 0
    st.session_state.game_over = False

def move_snake():
    x, y, z = st.session_state.snake[0]
    dx, dy, dz = st.session_state.direction
    new_head = (x + dx, y + dy, z + dz)

    # Collision check (bounds + self)
    if (
        new_head[0] < 0 or new_head[0] > 10 or
        new_head[1] < 0 or new_head[1] > 10 or
        new_head[2] < 0 or new_head[2] > 10 or
        new_head in st.session_state.snake
    ):
        st.session_state.game_over = True
        return

    st.session_state.snake.insert(0, new_head)

    # Food check
    if new_head == st.session_state.food:
        st.session_state.score += 1
        st.session_state.food = (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
    else:
        st.session_state.snake.pop()

def draw_snake():
    snake_x, snake_y, snake_z = zip(*st.session_state.snake)
    food_x, food_y, food_z = st.session_state.food

    fig = go.Figure()

    # Snake body
    fig.add_trace(go.Scatter3d(
        x=snake_x, y=snake_y, z=snake_z,
        mode="markers+lines",
        marker=dict(size=5, color="green"),
        line=dict(color="green", width=5)
    ))

    # Food
    fig.add_trace(go.Scatter3d(
        x=[food_x], y=[food_y], z=[food_z],
        mode="markers",
        marker=dict(size=6, color="red", symbol="diamond")
    ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(range=[0, 10]),
            yaxis=dict(range=[0, 10]),
            zaxis=dict(range=[0, 10])
        ),
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

st.title("🐍 3D Snake Game")

if st.session_state.game_over:
    st.write("### Game Over!")
    st.write(f"Final Score: {st.session_state.score}")
    if st.button("Restart"):
        st.session_state.snake = [(5, 5, 5)]
        st.session_state.direction = (1, 0, 0)
        st.session_state.food = (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
        st.session_state.score = 0
        st.session_state.game_over = False
else:
    st.plotly_chart(draw_snake(), use_container_width=True)
    st.write(f"Score: {st.session_state.score}")

    # Controls
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("⬅️ X-"):
            st.session_state.direction = (-1, 0, 0)
    with col2:
        if st.button("➡️ X+"):
            st.session_state.direction = (1, 0, 0)
    with col3:
        if st.button("⬆️ Y+"):
            st.session_state.direction = (0, 1, 0)
        if st.button("⬇️ Y-"):
            st.session_state.direction = (0, -1, 0)
    with col4:
        if st.button("⬆️ Z+"):
            st.session_state.direction = (0, 0, 1)
        if st.button("⬇️ Z-"):
            st.session_state.direction = (0, 0, -1)

    move_snake()
    st.experimental_rerun()
