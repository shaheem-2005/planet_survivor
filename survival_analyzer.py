
# survival_analyzer.py

PLANET_CONDITIONS = {
    "Earth": {
        "atmosphere": "Breathable",
        "water": "Abundant",
        "temperature": "Suitable",
        "radiation": "Relatively low at the surface",
        "food": "Suitable conditions for agriculture",
    },
    "Mars": {
        "atmosphere": "Mostly carbon dioxide; not breathable",
        "water": "Water ice available; liquid water is limited",
        "temperature": "Very cold",
        "radiation": "High compared with Earth's surface",
        "food": "Possible inside protected greenhouses",
    },
    "Moon": {
        "atmosphere": "No substantial breathable atmosphere",
        "water": "Ice exists in some permanently shadowed regions",
        "temperature": "Extreme temperature variations",
        "radiation": "High without shielding",
        "food": "Would require controlled growing systems",
    },
    "Mercury": {
        "atmosphere": "Almost no atmosphere",
        "water": "Ice may exist in permanently shadowed craters",
        "temperature": "Extreme temperature variations",
        "radiation": "High exposure risk",
        "food": "Would require sealed, controlled habitats",
    },
    "Venus": {
        "atmosphere": "Mostly carbon dioxide; extremely high pressure",
        "water": "No accessible surface liquid water",
        "temperature": "Extremely hot",
        "radiation": "Harsh surface environment",
        "food": "Surface agriculture is not feasible for humans",
    },
    "Jupiter": {
        "atmosphere": "Mostly hydrogen and helium",
        "water": "No known habitable solid surface",
        "temperature": "Extreme conditions",
        "radiation": "Extremely intense radiation environment",
        "food": "No known suitable solid surface for agriculture",
    },
    "Saturn": {
        "atmosphere": "Mostly hydrogen and helium",
        "water": "No known habitable solid surface",
        "temperature": "Extremely cold upper atmosphere",
        "radiation": "Hazardous radiation environment",
        "food": "No known suitable solid surface for agriculture",
    },
    "Uranus": {
        "atmosphere": "Hydrogen, helium, and methane",
        "water": "No known habitable solid surface",
        "temperature": "Extremely cold",
        "radiation": "Requires protection and further assessment",
        "food": "No known suitable solid surface for agriculture",
    },
    "Neptune": {
        "atmosphere": "Hydrogen, helium, and methane",
        "water": "No known habitable solid surface",
        "temperature": "Extremely cold",
        "radiation": "Requires protection and further assessment",
        "food": "No known suitable solid surface for agriculture",
    },
}


def analyze_survival(planet_name):
    """Return survival conditions for the selected planet."""

    conditions = PLANET_CONDITIONS.get(planet_name)

    if conditions is None:
        return None

    return conditions


def display_survival_report(planet_name):
    conditions = analyze_survival(planet_name)

    if conditions is None:
        print(f"No survival data available for {planet_name}.")
        return

    print(f"\n=== SURVIVAL REPORT: {planet_name.upper()} ===")

    for category, result in conditions.items():
        print(f"{category.capitalize()}: {result}")

    if planet_name == "Earth":
        print("\nAssessment: Naturally habitable for humans.")
    else:
        print(
            "\nAssessment: Humans would need substantial "
            "life-support systems or protected habitats."
        )


if __name__ == "__main__":
    planet = input("Enter planet name: ").strip().title()
    display_survival_report(planet)
