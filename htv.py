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

        error(f"Please enter one of: {', '.join(sorted(valid_choices))}.")


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


def finite_factor_from_counts(counts):
    finite_counts = [count for count in counts if not math.isinf(count)]

    if not finite_counts:
        return 0

    factor = math.prod(finite_counts)
    return factor if factor > 1 else 0


def get_bounded_positive_int(prompt, maximum):
    while True:
        value = ask(prompt).strip()

        try:
            count = int(value)
        except ValueError:
            error(f"Please enter a whole number from 1 to {maximum}.")
            continue

        if 1 <= count <= maximum:
            return count

        error(f"Please enter a whole number from 1 to {maximum}.")


def get_parameterized_metrics(text):
    parameters = extract_parameters(text)

    if not parameters:
        return {
            "count": 1,
            "infinite_parameters": 0,
            "finite_parts": 1,
        }

    print()
    warning(
        "Parameters found: "
        + ", ".join(f"<{parameter}>" for parameter in parameters)
    )

    if len(parameters) == 1:
        count = get_parameter_value_count(parameters[0])

        if math.isinf(count):
            metrics = {
                "count": math.inf,
                "infinite_parameters": 1,
                "finite_parts": 0,
            }
        else:
            metrics = {
                "count": count,
                "infinite_parameters": 0,
                "finite_parts": count,
            }

        print()
        success(
            f"This represents {format_count(count)} working "
            f"{'variation' if count == 1 else 'variations'}"
        )

        return metrics

    independent = get_yes_no(
        "Do these parameters vary independently? [y/n]"
    )

    if independent:
        counts = [
            get_parameter_value_count(parameter)
            for parameter in parameters
        ]

        infinite_parameters = sum(
            1 for count in counts if math.isinf(count)
        )
        finite_parts = finite_factor_from_counts(counts)

        total = math.prod(counts)

        rendered_counts = " × ".join(
            format_count(count) for count in counts
        )

        print()
        success(
            f"{rendered_counts} = {format_count(total)} "
            "working variations"
        )

        return {
            "count": total,
            "infinite_parameters": infinite_parameters,
            "finite_parts": finite_parts if infinite_parameters else total,
        }

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

    if math.isinf(count):
        print()
        hint(
            "For infinite families, the program also tracks how many "
            "parameters are infinitely variable."
        )
        infinite_parameters = get_bounded_positive_int(
            f"How many of these {len(parameters)} parameters have "
            "infinitely many possible values?",
            len(parameters),
        )
        finite_parts = 0
    else:
        infinite_parameters = 0
        finite_parts = count

    print()
    success(
        f"This represents {format_count(count)} working "
        f"{'variation' if count == 1 else 'variations'}"
    )

    return {
        "count": count,
        "infinite_parameters": infinite_parameters,
        "finite_parts": finite_parts,
    }


# ------------------------------------------------------------
# Explanation / variation data helpers
# ------------------------------------------------------------


def recalculate_count(item):
    total = item["explanation_parameter_count"]
    infinite_parameters = item["explanation_infinite_parameters"]
    finite_parts = item["explanation_finite_parts"]

    for variation in item["variations"]:
        total += variation["count"]
        infinite_parameters += variation["infinite_parameters"]
        finite_parts += variation["finite_parts"]

    item["count"] = total
    item["infinite_parameters"] = infinite_parameters
    item["finite_parts"] = finite_parts


def make_variation(text):
    parameters = extract_parameters(text)

    if parameters:
        success("Parameterized variation recorded")
        metrics = get_parameterized_metrics(text)
    else:
        success("Variation recorded")
        metrics = {
            "count": 1,
            "infinite_parameters": 0,
            "finite_parts": 1,
        }

    return {
        "text": text,
        **metrics,
    }


def prompt_for_variation(number):
    text = input(
        f"{CYAN}{BOLD}Variation {number}:{RESET}\n> "
    ).strip()

    if not text:
        return None

    return make_variation(text)


def process_explanation_parameters(explanation):
    if not extract_parameters(explanation):
        return {
            "count": 0,
            "infinite_parameters": 0,
            "finite_parts": 0,
        }

    print()
    hint(
        "This explanation contains parameters. "
        "Let's count the working variations they represent."
    )

    metrics = get_parameterized_metrics(explanation)

    print()
    success(
        f"Explanation represents {format_count(metrics['count'])} "
        "working variations through its parameters"
    )

    return metrics


def create_explanation_item(explanation, collect_initial_variations=True):
    item = {
        "explanation": explanation,
        "variations": [],
        "explanation_parameter_count": 0,
        "explanation_infinite_parameters": 0,
        "explanation_finite_parts": 0,
        "count": 0,
        "infinite_parameters": 0,
        "finite_parts": 0,
    }

    divider()
    heading("Explanation")
    print(explanation)

    explanation_metrics = process_explanation_parameters(explanation)
    item["explanation_parameter_count"] = explanation_metrics["count"]
    item["explanation_infinite_parameters"] = explanation_metrics[
        "infinite_parameters"
    ]
    item["explanation_finite_parts"] = explanation_metrics["finite_parts"]

    if collect_initial_variations:
        if item["explanation_parameter_count"]:
            print()
            hint(
                "You can still enter other distinct ways this explanation "
                "can vary."
            )
            hint(
                "Don't separately enter cases already covered by the "
                "parameters above."
            )

        collect_additional_variations(item)

    recalculate_count(item)
    return item


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
# Variation collection and editing
# ------------------------------------------------------------


def collect_additional_variations(item):
    print()
    heading("Working variations")
    hint("Enter variations that would still work to explain the same thing.")
    hint("Use <X>, <Y>, etc. to describe families of variations.")
    hint("Press Enter when you're done.")
    print()

    while True:
        variation = prompt_for_variation(len(item["variations"]) + 1)

        if variation is None:
            break

        item["variations"].append(variation)
        recalculate_count(item)
        print()


def format_variation_metrics(data):
    if math.isinf(data["count"]):
        infinite_word = (
            "parameter"
            if data["infinite_parameters"] == 1
            else "parameters"
        )
        return (
            f"infinite, {data['infinite_parameters']} infinite "
            f"{infinite_word}, {data['finite_parts']} finite parts"
        )

    return str(data["count"])


def print_variations(item):
    if not item["variations"]:
        hint("No additional variations entered.")
        return

    for index, variation in enumerate(item["variations"], start=1):
        print(
            f"  [{index}] {variation['text']} "
            f"({format_variation_metrics(variation)})"
        )


def add_one_variation(item):
    print()
    variation = prompt_for_variation(len(item["variations"]) + 1)

    if variation is None:
        hint("No variation added.")
        return

    item["variations"].append(variation)
    recalculate_count(item)
    success("Variation added")


def choose_variation_index(item, action):
    if not item["variations"]:
        warning("There are no additional variations to edit or delete.")
        return None

    print()
    print_variations(item)
    valid = {str(i) for i in range(1, len(item["variations"]) + 1)} | {"0"}
    choice = get_choice(
        f"Which variation would you like to {action}? (0 to cancel)",
        valid,
    )

    if choice == "0":
        return None

    return int(choice) - 1


def edit_variation(item):
    index = choose_variation_index(item, "edit")

    if index is None:
        return

    current = item["variations"][index]
    print()
    hint(f"Current: {current['text']}")

    new_text = ask("Enter the corrected variation (blank to cancel):").strip()

    if not new_text:
        hint("Edit cancelled.")
        return

    # Re-run parameter handling because the edited text may have different
    # parameters or a different number of working values/combinations.
    item["variations"][index] = make_variation(new_text)
    recalculate_count(item)
    success("Variation updated")


def delete_variation(item):
    index = choose_variation_index(item, "delete")

    if index is None:
        return

    removed = item["variations"].pop(index)
    recalculate_count(item)
    success(f"Deleted variation: {removed['text']}")


def edit_explanation(item):
    print()
    hint(f"Current: {item['explanation']}")

    new_text = ask("Enter the corrected explanation (blank to cancel):").strip()

    if not new_text:
        hint("Edit cancelled.")
        return

    item["explanation"] = new_text

    # The explanation's own parameter count belongs to the explanation text,
    # so recalculate it whenever that text changes. Existing additional
    # variations are preserved.
    explanation_metrics = process_explanation_parameters(new_text)
    item["explanation_parameter_count"] = explanation_metrics["count"]
    item["explanation_infinite_parameters"] = explanation_metrics[
        "infinite_parameters"
    ]
    item["explanation_finite_parts"] = explanation_metrics["finite_parts"]
    recalculate_count(item)
    success("Explanation updated")


def review_explanation(item):
    while True:
        divider()
        heading("Review explanation")
        print(item["explanation"])
        print()
        print(
            f"Working variations: "
            f"{format_variation_metrics(item)}"
        )

        if item["explanation_parameter_count"]:
            print(
                "  Explanation parameters: "
                f"{format_count(item['explanation_parameter_count'])}"
            )

        print_variations(item)

        print()
        print("  [1] Continue")
        print("  [2] Add variation")
        print("  [3] Edit variation")
        print("  [4] Delete variation")
        print("  [5] Edit explanation")

        choice = get_choice("What would you like to do?", {"1", "2", "3", "4", "5"})

        if choice == "1":
            return
        if choice == "2":
            add_one_variation(item)
        elif choice == "3":
            edit_variation(item)
        elif choice == "4":
            delete_variation(item)
        elif choice == "5":
            edit_explanation(item)


# ------------------------------------------------------------
# Final review / explanation-level CRUD
# ------------------------------------------------------------


def print_explanation_list(results):
    print()
    for index, item in enumerate(results, start=1):
        if math.isinf(item["count"]):
            infinite_word = (
                "parameter"
                if item["infinite_parameters"] == 1
                else "parameters"
            )
            print(
                f"  [{index}] {item['explanation']} "
                f"(infinite working variations, "
                f"{item['infinite_parameters']} infinite {infinite_word}, "
                f"{item['finite_parts']} finite parts)"
            )
        else:
            print(
                f"  [{index}] {item['explanation']} "
                f"({item['count']} working variations)"
            )


def choose_explanation_index(results, action, allow_cancel=True):
    print_explanation_list(results)

    valid = {str(i) for i in range(1, len(results) + 1)}
    if allow_cancel:
        valid.add("0")

    suffix = " (0 to cancel)" if allow_cancel else ""
    choice = get_choice(
        f"Which explanation would you like to {action}?{suffix}",
        valid,
    )

    if allow_cancel and choice == "0":
        return None

    return int(choice) - 1


def add_explanation(results):
    print()
    explanation = ask("Enter the new explanation:").strip()

    if not explanation:
        hint("No explanation added.")
        return

    item = create_explanation_item(explanation, collect_initial_variations=True)
    review_explanation(item)
    results.append(item)
    success("Explanation added")


def delete_explanation(results):
    if len(results) <= 2:
        warning("At least two explanations are required.")
        return

    index = choose_explanation_index(results, "delete")

    if index is None:
        return

    removed = results.pop(index)
    success(f"Deleted explanation: {removed['explanation']}")


def final_review(results):
    while True:
        divider()
        heading("Ready to rank")
        print_explanation_list(results)

        print()
        print("  [1] Show ranking")
        print("  [2] Review / edit an explanation")
        print("  [3] Add explanation")
        print("  [4] Delete explanation")

        choice = get_choice("What would you like to do?", {"1", "2", "3", "4"})

        if choice == "1":
            return

        if choice == "2":
            index = choose_explanation_index(results, "review")
            if index is not None:
                review_explanation(results[index])
        elif choice == "3":
            add_explanation(results)
        elif choice == "4":
            delete_explanation(results)


# ------------------------------------------------------------
# Ranking
# ------------------------------------------------------------


def ranking_key(item):
    return (
        item["count"],
        item["infinite_parameters"],
        item["finite_parts"],
    )


def show_ranking(results):
    ranked = sorted(results, key=ranking_key)

    divider()
    heading("HARDNESS-TO-VARY RANKING")

    previous_key = None
    rank = 0

    for index, item in enumerate(ranked, start=1):
        key = ranking_key(item)

        if key != previous_key:
            rank = index
            previous_key = key

        print()
        print(f"{BOLD}Rank {rank}{RESET}")
        print(item["explanation"])

        if math.isinf(item["count"]):
            warning("Working variations represented: infinite")
            print(
                "Infinitely variable parameters: "
                f"{item['infinite_parameters']}"
            )
            print(
                "Finite variation parts: "
                f"{item['finite_parts']}"
            )
        else:
            print(f"Working variations represented: {item['count']}")

    print()
    hint("Fewer working variations = harder to vary.")
    hint(
        "For infinite totals, fewer infinitely-variable parameters "
        "ranks higher; remaining ties are broken by fewer finite "
        "variation parts."
    )

    if len(ranked) == 2:
        first = ranked[0]
        second = ranked[1]

        print()
        heading("Result")

        if ranking_key(first) == ranking_key(second):
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
        item = create_explanation_item(
            explanation,
            collect_initial_variations=True,
        )
        review_explanation(item)
        results.append(item)

    final_review(results)

    divider()
    heading("Question")
    print(question)

    show_ranking(results)


if __name__ == "__main__":
    main()
