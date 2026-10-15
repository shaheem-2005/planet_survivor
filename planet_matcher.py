
# planet_matcher.py

# Gravity values in m/s^2
PLANETS = {
    "Earth": 9.81,
    "Mars": 3.71,
    "Moon": 1.62,
    "Mercury": 3.70,
    "Venus": 8.87,
    "Jupiter": 24.79,
    "Saturn": 10.44,
    "Uranus": 8.69,
    "Neptune": 11.15
}


def match_planet(measured_gravity):
    """
    Find the planet whose surface gravity is closest
    to the measured gravity.
    """

    if measured_gravity is None or measured_gravity <= 0:
        return None, None

    closest_planet = min(
        PLANETS,
        key=lambda planet: abs(
            PLANETS[planet] - measured_gravity
        )
    )

    difference = abs(
        PLANETS[closest_planet] - measured_gravity
    )

    return closest_planet, difference


if __name__ == "__main__":
    try:
        gravity = float(
            input("Enter measured gravity (m/s^2): ")
        )

        planet, difference = match_planet(gravity)

        if planet:
            print("\n=== PLANET MATCH ===")
            print(f"Closest match: {planet}")
            print(f"Planet gravity: {PLANETS[planet]} m/s^2")
            print(f"Difference: {difference:.2f} m/s^2")
        else:
            print("Please enter a positive gravity value.")

    except ValueError:
        print("Please enter a valid number.")
