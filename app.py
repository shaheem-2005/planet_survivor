
import av
from streamlit_webrtc import VideoProcessorBase, webrtc_streamer
import streamlit as st

from gravity_detector import detect_gravity
from planet_matcher import match_planet, PLANETS
from survival_analyzer import analyze_survival

class CameraProcessor(VideoProcessorBase):
    def recv(self, frame):
        # Receive a frame from the browser webcam
        image = frame.to_ndarray(format="bgr24")

        # Return the frame to display it on the website
        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )


st.set_page_config(
    page_title="Planet Survivor",
    page_icon="🪐",
    layout="wide"
)

st.title("🪐 Planet Survivor")
st.subheader("Could humanity survive on another world?")

st.header("📷 Live Webcam")

st.write(
    "Allow camera access when your browser asks for permission."
)

webrtc_streamer(
    key="planet-survivor-camera",
    video_processor_factory=CameraProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)

st.write(
    "Measure gravity using your webcam, identify the closest "
    "planet by gravity, and explore its survival conditions."
)

st.warning(
    "This is an educational simulation. Webcam gravity estimates "
    "are experimental, and gravity alone cannot identify a planet."
)

if "gravity" not in st.session_state:
    st.session_state.gravity = None

if "planet" not in st.session_state:
    st.session_state.planet = None


st.header("Step 1: Measure Gravity")

st.write(
    "Keep your webcam stationary and follow the calibration "
    "instructions in the camera window."
)

if st.button("📷 Start Gravity Detection"):
    with st.spinner("Starting webcam gravity detection..."):
        measured_gravity = detect_gravity()

    if measured_gravity is not None and measured_gravity > 0:
        st.session_state.gravity = measured_gravity

        planet, difference = match_planet(measured_gravity)
        st.session_state.planet = planet

        st.success("Gravity measurement completed!")
    else:
        st.error(
            "Gravity measurement failed. Please try again "
            "and check the terminal for details."
        )


if st.session_state.gravity is not None:
    gravity = st.session_state.gravity

    st.metric(
        label="Measured Gravity",
        value=f"{gravity:.2f} m/s²"
    )

    st.header("Step 2: Find the Closest Planet")

    planet, difference = match_planet(gravity)

    if planet:
        st.success(f"Closest gravity match: {planet}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Reference Gravity",
                f"{PLANETS[planet]:.2f} m/s²"
            )

        with col2:
            st.metric(
                "Gravity Difference",
                f"{difference:.2f} m/s²"
            )

        st.caption(
            "This is the closest gravity match among the planets "
            "in the dataset, not a definitive planet identification."
        )

        st.header("Step 3: Survival Analysis")

        conditions = analyze_survival(planet)

        if conditions:
            st.subheader(f"🧑‍🚀 Survival Report: {planet}")

            for category, result in conditions.items():
                st.write(f"**{category.capitalize()}:** {result}")

            if planet == "Earth":
                st.info(
                    "Earth naturally supports human life under "
                    "normal surface conditions."
                )
            else:
                st.warning(
                    "Humans would need substantial life-support "
                    "systems or protected habitats on this world."
                )

st.divider()
st.caption("Planet Survivor | Educational Hackathon Project")
