def get_nonempty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter something.")


def collect_explanations():
    explanations = []

    print("\nEnter explanations one at a time.")
    print("Press Enter on an empty line when you're done.\n")

    while True:
        explanation = input(f"Explanation {len(explanations) + 1}: ").strip()

        if not explanation:
            if len(explanations) >= 2:
                break

            print("Please provide at least two explanations.")
            continue

        explanations.append(explanation)

    return explanations


def collect_variations(explanation):
    variations = []

    print("\n" + "=" * 60)
    print("Explanation:")
    print(explanation)
    print()
    print(
        "Enter variations of this explanation that would still work "
        "to explain the same thing."
    )
    print("Press Enter on an empty line when you're done.\n")

    while True:
        variation = input(f"Variation {len(variations) + 1}: ").strip()

        if not variation:
            break

        variations.append(variation)

    return variations


def show_ranking(results):
    ranked = sorted(results, key=lambda item: len(item["variations"]))

    print("\n" + "=" * 60)
    print("HARDNESS-TO-VARY RANKING")
    print("=" * 60)

    previous_count = None
    rank = 0

    for index, item in enumerate(ranked, start=1):
        count = len(item["variations"])

        if count != previous_count:
            rank = index
            previous_count = count

        word = "variation" if count == 1 else "variations"

        print(f"\nRank {rank}")
        print(f"Explanation: {item['explanation']}")
        print(f"Working variations submitted: {count} {word}")

    print("\nFewer working variations = harder to vary.")

    if len(ranked) == 2:
        first = ranked[0]
        second = ranked[1]

        first_count = len(first["variations"])
        second_count = len(second["variations"])

        print("\nResult:")

        if first_count == second_count:
            print("The two explanations are equally hard to vary.")
        else:
            print(
                f'"{first["explanation"]}" is harder to vary than '
                f'"{second["explanation"]}".'
            )


def main():
    print("Hard-to-Vary Explanation Comparator")
    print("-----------------------------------")

    question = get_nonempty("\nWhat question are you trying to answer?\n> ")

    explanations = collect_explanations()

    results = []

    for explanation in explanations:
        variations = collect_variations(explanation)

        results.append(
            {
                "explanation": explanation,
                "variations": variations,
            }
        )

    print("\n" + "=" * 60)
    print("Question:")
    print(question)

    show_ranking(results)


if __name__ == "__main__":
    main()