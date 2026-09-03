import math
import re


# ------------------------------------------------------------
# Terminal styling
# ------------------------------------------------------------

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"


def heading(text):
    print(f"{BOLD}{text}{RESET}")


def hint(text):
    print(f"{DIM}{text}{RESET}")


def success(text):
    print(f"{GREEN}✓ {text}{RESET}")


def warning(text):
    print(f"{YELLOW}{text}{RESET}")


def error(text):
    print(f"{RED}{text}{RESET}")


def styled_parameter(name):
    return f"{YELLOW}<{name}>{RESET}"


def divider():
    print(f"\n{DIM}{'-' * 60}{RESET}\n")


def ask(text):
    return input(f"{CYAN}{BOLD}{text}{RESET}\n> ")


# ------------------------------------------------------------
# Input helpers
# ------------------------------------------------------------

PARAMETER_PATTERN = re.compile(r"<([^<>]+)>")


def get_nonempty(prompt):
    while True:
        value = ask(prompt).strip()

        if value:
            return value

        error("Please enter something.")


def get_choice(prompt, valid_choices):
    while True:
        value = ask(prompt).strip()

        if value in valid_choices:
            return value

        error(f"Please enter one of: {', '.join(valid_choices)}.")


def get_yes_no(prompt):
    while True:
        value = ask(prompt).strip().lower()

        if value in ("y", "yes"):
            return True

        if value in ("n", "no"):
            return False

        error("Please enter y or n.")


def get_count(prompt):
    while True:
        value = ask(prompt).strip().lower()

        if value == "infinite":
            return math.inf

        try:
            count = int(value)
        except ValueError:
            error('Please enter a positive whole number or "infinite".')
            continue

        if count > 0:
            return count

        error('Please enter a positive whole number or "infinite".')


def format_count(count):
    if math.isinf(count):
        return "infinite"

    return str(count)


def extract_parameters(text):
    # Preserve the order in which parameters first appear.
    return list(dict.fromkeys(PARAMETER_PATTERN.findall(text)))


# ------------------------------------------------------------
# Parameter handling
# ------------------------------------------------------------

def enumerate_values(parameter):
    values = []

    print()
    heading(f"Values for <{parameter}>")
    hint("Enter one value per line. Press Enter when you're done.")
    print()

    while True:
        value = input(
            f"{CYAN}<{parameter}> value {len(values) + 1}:{RESET} "
        ).strip()

        if not value:
            if values:
                break

            error("Please enter at least one value.")
            continue

        values.append(value)

    success(f"<{parameter}> has {len(values)} possible values")

    return len(values)


def get_parameter_value_count(parameter):
    print()
    heading(f"For parameter <{parameter}>, would you like to:")
    print("  [1] Enter the number of possible values")
    print("  [2] List the possible values and let the program count")

    choice = get_choice("Choice:", {"1", "2"})

    if choice == "1":
        hint('Enter "infinite" if there is no finite limit.')

        count = get_count(
            f"How many values can <{parameter}> take?"
        )

        success(f"<{parameter}> = {format_count(count)}")

        return count

    return enumerate_values(parameter)


def enumerate_combinations(parameters):
    combinations = []
    parameter_list = ", ".join(f"<{p}>" for p in parameters)

    print()
    heading(f"Working combinations of {parameter_list}")
    hint("Enter one combination per line.")
    hint("Example: X=0.2, Y=0.8")
    hint("Press Enter when you're done.")
    print()

    while True:
        combination = input(
            f"{CYAN}Combination {len(combinations) + 1}:{RESET} "
        ).strip()

        if not combination:
            if combinations:
                break

            error("Please enter at least one combination.")
            continue

        combinations.append(combination)

    success(f"{len(combinations)} working combinations entered")

    return len(combinations)


def get_parameterized_count(text):
    parameters = extract_parameters(text)

    if not parameters:
        return 1

    print()
    warning(
        "Parameters found: "
        + ", ".join(f"<{parameter}>" for parameter in parameters)
    )

    # One parameter
    if len(parameters) == 1:
        count = get_parameter_value_count(parameters[0])

        print()
        success(
            f"This represents {format_count(count)} working "
            f"{'variation' if count == 1 else 'variations'}"
        )

        return count

    # Multiple parameters
    independent = get_yes_no(
        "Do these parameters vary independently? [y/n]"
    )

    if independent:
        counts = []

        for parameter in parameters:
            counts.append(get_parameter_value_count(parameter))

        total = math.prod(counts)

        rendered_counts = " × ".join(
            format_count(count) for count in counts
        )

        print()
        success(
            f"{rendered_counts} = {format_count(total)} "
            "working variations"
        )

        return total

    print()
    heading("Dependent parameters")
    print("  [1] Enter the number of working combinations")
    print("  [2] List the working combinations and let the program count")

    choice = get_choice("Choice:", {"1", "2"})

    if choice == "1":
        parameter_names = " and ".join(
            f"<{parameter}>" for parameter in parameters
        )

        hint('Enter "infinite" if there is no finite limit.')

        count = get_count(
            f"How many combinations of {parameter_names} work?"
        )
    else:
        count = enumerate_combinations(parameters)

    print()
    success(
        f"This represents {format_count(count)} working "
        f"{'variation' if count == 1 else 'variations'}"
    )

    return count


# ------------------------------------------------------------
# Explanation collection
# ------------------------------------------------------------

def collect_explanations():
    explanations = []

    print()
    heading("Enter explanations one at a time.")
    hint("Tip: use <X>, <Y>, etc. to describe families of variations.")
    hint(
        "Example: <X> kg of grass mixed with <Y> kg of wheat "
        "cures the disease."
    )
    hint("Press Enter when you're done.")

    print()

    while True:
        explanation = input(
            f"{CYAN}{BOLD}Explanation {len(explanations) + 1}:{RESET}\n> "
        ).strip()

        if not explanation:
            if len(explanations) >= 2:
                break

            error("Please provide at least two explanations.")
            continue

        explanations.append(explanation)

        success(f"Explanation {len(explanations)} recorded")
        print()

    return explanations


# ------------------------------------------------------------
# Variation collection
# ------------------------------------------------------------

def collect_variations(explanation):
    variations = []
    explanation_parameter_count = 0

    divider()

    heading("Explanation")
    print(explanation)

    # Parameters directly in the explanation
    if extract_parameters(explanation):
        print()
        hint(
            "This explanation already contains parameters. "
            "Let's count the working variations they represent."
        )

        explanation_parameter_count = get_parameterized_count(
            explanation
        )

        print()
        success(
            f"Explanation already represents "
            f"{format_count(explanation_parameter_count)} "
            "working variations"
        )

        hint(
            "You can still enter other distinct ways this explanation "
            "can vary."
        )
        hint(
            "Don't separately enter cases already covered by the "
            "parameters above."
        )

    print()
    heading("Working variations")
    hint("Enter other variations of this explanation that would still work to explain the same thing.")
    hint("Tip: use <X>, <Y>, etc. to describe families of variations.")
    hint(
        "Example: <X> kg of grass mixed with <Y> kg of wheat "
        "cures the disease."
    )
    hint("Press Enter when you're done.")
    print()

    while True:
        variation = input(
            f"{CYAN}{BOLD}Variation {len(variations) + 1}:{RESET}\n> "
        ).strip()

        if not variation:
            break

        parameters = extract_parameters(variation)

        if parameters:
            success("Parameterized variation recorded")
            count = get_parameterized_count(variation)
        else:
            success("Variation recorded")
            count = 1

        variations.append(
            {
                "text": variation,
                "count": count,
            }
        )

        print()

    total_count = explanation_parameter_count

    for variation in variations:
        total_count += variation["count"]

    print()
    success(
        f"Total working variations represented: "
        f"{format_count(total_count)}"
    )

    return {
        "variations": variations,
        "explanation_parameter_count": explanation_parameter_count,
        "count": total_count,
    }


# ------------------------------------------------------------
# Ranking
# ------------------------------------------------------------

def show_ranking(results):
    ranked = sorted(
        results,
        key=lambda item: item["count"],
    )

    divider()

    heading("HARDNESS-TO-VARY RANKING")

    previous_count = None
    rank = 0

    for index, item in enumerate(ranked, start=1):
        count = item["count"]

        if count != previous_count:
            rank = index
            previous_count = count

        print()
        print(f"{BOLD}Rank {rank}{RESET}")
        print(item["explanation"])

        if math.isinf(count):
            warning("Working variations represented: infinite")
        else:
            print(f"Working variations represented: {count}")

    print()
    hint("Fewer working variations = harder to vary.")

    if len(ranked) == 2:
        first = ranked[0]
        second = ranked[1]

        print()
        heading("Result")

        if first["count"] == second["count"]:
            print(
                f"{YELLOW}The two explanations are equally "
                f"hard to vary.{RESET}"
            )
        else:
            print(
                f"{GREEN}{first['explanation']}{RESET}\n"
                f"is harder to vary than\n"
                f"{second['explanation']}"
            )


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    print()
    heading("Hard-to-Vary Explanation Comparator")
    hint("-----------------------------------")

    question = get_nonempty(
        "What question are you trying to answer?"
    )

    success("Question recorded")

    explanations = collect_explanations()

    results = []

    for explanation in explanations:
        collected = collect_variations(explanation)

        results.append(
            {
                "explanation": explanation,
                "variations": collected["variations"],
                "explanation_parameter_count": collected[
                    "explanation_parameter_count"
                ],
                "count": collected["count"],
            }
        )

    divider()

    heading("Question")
    print(question)

    show_ranking(results)


if __name__ == "__main__":
    main()
