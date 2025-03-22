from itertools import combinations, permutations
from collections import defaultdict, Counter
from flask import jsonify, request

# Список всех чемпионов и их трейтов
champions_traits = {
    "Alistar": ['Golden Ox', 'Bruiser'],
    "Annie": ['Golden Ox', 'A.M.P.'],
    "Aphelios": ['Golden Ox', 'Marksman'],
    "Aurora": ['Anima Squad', 'Dynamo'],
    "Brand": ['Street Demon', 'Techie'],
    "Braum": ['Syndicate', 'Vanguard'],
    "Cho'Gath": ['BoomBots', 'Bruiser'],
    "Darius": ['Syndicate', 'Bruiser'],
    "Draven": ['Cypher', 'Rapidfire'],
    "Dr.Mundo": ['Street Demon', 'Bruiser', 'Slayer'],
    "Ekko": ['Street Demon', 'Strategist'],
    "Elise": ['Nitro', 'Dynamo'],
    "Fiddlesticks": ['BoomBots', 'Techie'],
    "Galio": ['Cypher', 'Bastion'],
    "Garen": ['God of the Net'],
    "Gragas": ['Divinicorp', 'Bruiser'],
    "Graves": ['Golden Ox', 'Executioner'],
    "Illaoi": ['Anima Squad', 'Bastion'],
    "Jarvan IV": ['Golden Ox', 'Vanguard', 'Slayer'],
    "Jax": ['Exotech', 'Bastion'],
    "Jhin": ['Exotech', 'Marksman', 'Dynamo'],
    "Jinx": ['Street Demon', 'Marksman'],
    "Kindred": ['Nitro', 'Rapidfire', 'Marksman'],
    "Kobuko": ['Cyberboss', 'Bruiser'],
    "Kog'Maw": ['BoomBots', 'Rapidfire'],
    "LeBlanc": ['Cypher', 'Strategist'],
    "Leona": ['Anima Squad', 'Vanguard'],
    "Miss Fortune": ['Syndicate', 'Dynamo'],
    "Mordekaiser": ['Exotech', 'Bruiser', 'Techie'],
    "Morgana": ['Divinicorp', 'Dynamo'],
    "Naafiri": ['Exotech', 'A.M.P.'],
    "Neeko": ['Street Demon', 'Strategist'],
    "Nidalee": ['Nitro', 'A.M.P.'],
    "Poppy": ['Cyberboss', 'Bastion'],
    "Renekton": ['Overlord', 'Divinicorp', 'Bastion'],
    "Rengar": ['Street Demon', 'Executioner'],
    "Rhaast": ['Divinicorp', 'Vanguard'],
    "Samira": ['Street Demon', 'A.M.P.'],
    "Sejuani": ['Exotech', 'Bastion'],
    "Senna": ['Divinicorp', 'Slayer'],
    "Seraphine": ['Anima Squad', 'Techie'],
    "Shaco": ['Syndicate', 'Slayer'],
    "Shyvana": ['Nitro', 'Bastion', 'Techie'],
    "Skarner": ['BoomBots', 'Vanguard'],
    "Sylas": ['Anima Squad', 'Vanguard'],
    "Twisted Fate": ['Syndicate', 'Rapidfire'],
    "Urgot": ['BoomBots', 'Executioner'],
    "Varus": ['Exotech', 'Executioner'],
    "Vayne": ['Anima Squad', 'Slayer'],
    "Veigar": ['Cyberboss', 'Techie'],
    "Vex": ['Divinicorp', 'Executioner'],
    "Vi": ['Cypher', 'Vanguard'],
    "Viego": ['Soul Killer', 'Golden Ox', 'Techie'],
    "Xayah": ['Anima Squad', 'Marksman'],
    "Yuumi": ['Anima Squad', 'A.M.P.', 'Strategist'],
    "Zac": ['Virus'],
    "Zed": ['Cypher', 'Slayer'],
    "Zeri": ['Exotech', 'Rapidfire'],
    "Ziggs": ['Cyberboss', 'Strategist'],
    "Zyra": ['Street Demon', 'Techie']
}

# Список всех чемпионов и их кодов
champions_codes = {
    "Alistar": "312",
    "Annie": "316",
    "Aphelios": "71a",
    "Aurora": "30d",
    "Brand": "2e1",
    "Braum": "2f8",
    "Cho'Gath": "30a",
    "Darius": "2e2",
    "Draven": "31c",
    "Dr.Mundo": "2e3",
    "Ekko": "31f",
    "Elise": "2e4",
    "Fiddlesticks": "2e5",
    "Galio": "2e6",
    "Garen": "2e7",
    "Gragas": "302",
    "Graves": "315",
    "Illaoi": "2fd",
    "Jarvan IV": "314",
    "Jax": "305",
    "Jhin": "300",
    "Jinx": "31e",
    "Kindred": "2fb",
    "Kobuko": "306",
    "Kog'Maw": "303",
    "LeBlanc": "2e8",
    "Leona": "30f",
    "Miss Fortune": "2e9",
    "Mordekaiser": "311",
    "Morgana": "2ea",
    "Naafiri": "301",
    "Neeko": "2eb",
    "Nidalee": "2f9",
    "Poppy": "308",
    "Renekton": "2ec",
    "Rengar": "2ed",
    "Rhaast": "317",
    "Samira": "2ee",
    "Sejuani": "307",
    "Senna": "2ef",
    "Seraphine": "2fe",
    "Shaco": "2f0",
    "Shyvana": "2fa",
    "Skarner": "304",
    "Sylas": "30c",
    "Twisted Fate": "2f1",
    "Urgot": "30b",
    "Varus": "2f2",
    "Vayne": "30e",
    "Veigar": "2f3",
    "Vex": "2f4",
    "Vi": "310",
    "Viego": "313",
    "Xayah": "2ff",
    "Yuumi": "2fc",
    "Zac": "31d",
    "Zed": "2f5",
    "Zeri": "2f6",
    "Ziggs": "309",
    "Zyra": "2f7"
}

# Список всех трейтов и их порогов
traits = {
    'Golden Ox': ['2', '4', '6'],
    'Bruiser': ['2', '4', '6'],
    'A.M.P.': ['2', '3', '4', '5'],
    'Marksman': ['2', '4'],
    'Anima Squad': ['3', '5', '7', '10'],
    'Dynamo': ['2', '3', '4'],
    'Street Demon': ['3', '5', '7', '10'],
    'Techie': ['2', '4', '6', '8'],
    'Syndicate': ['3', '5', '7'],
    'Vanguard': ['2', '4', '6'],
    'Cypher': ['3', '4', '5'],
    'Rapidfire': ['2', '4', '6'],
    'Strategist': ['2', '3', '4', '5'],
    'BoomBots': ['2', '4', '6'],
    'Bastion': ['2', '4', '6'],
    'Divinicorp': ['1', '2', '3', '4', '5', '6', '7'],
    'Executioner': ['2', '3', '4', '5'],
    'Slayer': ['2', '4', '6'],
    'Exotech': ['3', '5', '7', '10'],
    'Nitro': ['3', '4'],
    'Cyberboss': ['2', '3', '4'],
}

def find_best_team_prioritize_full_traits(emblems, champions_traits, traits, team_size=8):
    """
    Find the best team of a fixed size that prioritizes completing full traits.
    Run the algorithm for all permutations of emblems and return the best results.
    """
    best_teams = []
    max_activated_traits = 0

    # Iterate over all permutations of emblems
    for emblem_order in permutations(emblems):
        trait_counts = Counter(emblem_order)  # Start with emblems contributing to traits
        selected_champions = []

        while len(selected_champions) < team_size:
            best_champion = None
            best_completion_score = 0
            best_biggest_trait_contribution = 0

            # Determine the biggest trait (highest count in trait_counts)
            biggest_trait = max(trait_counts, key=lambda t: trait_counts[t], default=None)

            for champion, champion_traits in champions_traits.items():
                if champion in selected_champions:
                    continue

                # Simulate adding this champion
                new_trait_counts = trait_counts.copy()
                for trait in champion_traits:
                    new_trait_counts[trait] += 1

                # Calculate the completion score for this champion
                completion_score = 0
                for trait, count in new_trait_counts.items():
                    if trait in traits:
                        thresholds = list(map(int, traits[trait]))
                        if any(count == threshold for threshold in thresholds):
                            completion_score += 1

                # Check if the champion contributes to the biggest trait
                biggest_trait_contribution = 1 if biggest_trait in champion_traits else 0

                # Select the champion with the highest completion score or tie-break by biggest trait contribution
                if (completion_score > best_completion_score or
                    (completion_score == best_completion_score and biggest_trait_contribution > best_biggest_trait_contribution)):
                    best_completion_score = completion_score
                    best_biggest_trait_contribution = biggest_trait_contribution
                    best_champion = champion

            if best_champion is None:
                break  # No more champions can improve the team

            # Add the best champion to the team
            selected_champions.append(best_champion)
            for trait in champions_traits[best_champion]:
                trait_counts[trait] += 1

        # If the team is still not full, fill it with remaining champions
        if len(selected_champions) < team_size:
            remaining_champions = [champ for champ in champions_traits if champ not in selected_champions]
            selected_champions.extend(remaining_champions[:team_size - len(selected_champions)])

        # Prepare the list of activated traits and their counts
        activated_traits = {}
        for trait, count in trait_counts.items():
            if trait in traits:
                thresholds = list(map(int, traits[trait]))
                if any(count >= threshold for threshold in thresholds):
                    activated_traits[trait] = count

        # Compare the results and update the best teams
        num_activated_traits = len(activated_traits)
        if num_activated_traits > max_activated_traits:
            max_activated_traits = num_activated_traits
            best_teams = [(selected_champions, activated_traits, num_activated_traits)]
        elif num_activated_traits == max_activated_traits:
            # Avoid adding duplicate teams
            if (selected_champions, activated_traits, num_activated_traits) not in best_teams:
                best_teams.append((selected_champions, activated_traits, num_activated_traits))

    return best_teams

def fill_remaining_slots_by_traits(emblems, champions_traits, traits, trait_counts, selected_champions, team_size):
    """
    Fill the remaining slots by maximizing other traits.
    """
    remaining_slots = team_size - len(selected_champions)
    remaining_champions = [champ for champ in champions_traits if champ not in selected_champions]

    while remaining_slots > 0 and remaining_champions:
        best_champion = None
        best_completion_score = 0
        best_total_traits = 0

        for champion in remaining_champions:
            champion_traits = champions_traits[champion]

            # Calculate the completion score (number of traits completed by adding this champion)
            completion_score = 0
            simulated_trait_counts = trait_counts.copy()
            for trait in champion_traits:
                simulated_trait_counts[trait] += 1
                if trait in traits:
                    thresholds = list(map(int, traits[trait]))
                    if any(simulated_trait_counts[trait] == threshold for threshold in thresholds):
                        completion_score += 1

            # Calculate the total number of traits the champion provides
            total_traits = len(champion_traits)

            # Prioritize champions that complete traits and provide the most traits
            if (completion_score > best_completion_score or
                (completion_score == best_completion_score and total_traits > best_total_traits)):
                best_champion = champion
                best_completion_score = completion_score
                best_total_traits = total_traits

        if best_champion is None:
            break  # No more champions can improve the team

        # Add the best champion to the team
        selected_champions.append(best_champion)
        for trait in champions_traits[best_champion]:
            trait_counts[trait] += 1

        # Remove the selected champion from the remaining pool
        remaining_champions.remove(best_champion)
        remaining_slots -= 1

    return selected_champions, trait_counts

def find_best_team_vertical_with_full_traits(emblems, champions_traits, traits, team_size=8):
    """
    Find the best team of a fixed size that prioritizes maximizing the primary vertical trait,
    and switches to completing other traits after reaching the maximum threshold.
    """
    # Identify the primary emblem's trait (the one with the largest thresholds)
    primary_trait = max(emblems, key=lambda e: max(map(int, traits[e])), default=None)
    if primary_trait is None:
        raise ValueError("No valid emblems provided.")

    trait_counts = Counter(emblems)  # Start with emblems contributing to traits
    selected_champions = []

    # Determine the thresholds for the primary trait
    primary_trait_thresholds = list(map(int, traits[primary_trait]))
    primary_trait_thresholds.sort()

    # Calculate the maximum achievable threshold for the primary trait
    champions_with_trait = [champ for champ, champ_traits in champions_traits.items() if primary_trait in champ_traits]
    max_possible_count = len(champions_with_trait) + trait_counts[primary_trait]  # Include emblems
    max_achievable_threshold = next((t for t in reversed(primary_trait_thresholds) if t <= max_possible_count), None)

    # Phase 1: Focus on maximizing the primary vertical trait
    while len(selected_champions) < team_size:
        current_primary_count = trait_counts[primary_trait]
        next_threshold = next((t for t in primary_trait_thresholds if t > current_primary_count), None)

        # If no further thresholds are achievable, break out of Phase 1
        remaining_slots = team_size - len(selected_champions)
        if next_threshold is None or next_threshold > max_achievable_threshold or next_threshold - current_primary_count > remaining_slots:
            break

        # Find the best champion to reach the next threshold
        best_champion = None
        best_primary_trait_contribution = 0
        best_total_traits = 0

        for champion, champion_traits in champions_traits.items():
            if champion in selected_champions:
                continue

            # Calculate the contribution to the primary trait
            primary_trait_contribution = champion_traits.count(primary_trait)

            # Calculate the total number of traits the champion provides
            total_traits = len(champion_traits)

            # Prioritize champions that contribute to the primary trait and provide the most traits
            if (primary_trait_contribution > best_primary_trait_contribution or
                (primary_trait_contribution == best_primary_trait_contribution and total_traits > best_total_traits)):
                best_champion = champion
                best_primary_trait_contribution = primary_trait_contribution
                best_total_traits = total_traits

        if best_champion is None:
            break  # No champion can help reach the next threshold

        # Add the best champion to the team
        selected_champions.append(best_champion)
        for trait in champions_traits[best_champion]:
            trait_counts[trait] += 1

    # Phase 2: Fill remaining slots by completing other traits
    selected_champions, trait_counts = fill_remaining_slots_by_traits(
        emblems,
        champions_traits,
        traits,
        trait_counts,
        selected_champions,
        team_size
    )

    # Calculate activated traits
    activated_traits = {}
    for trait, count in trait_counts.items():
        if trait in traits:
            thresholds = list(map(int, traits[trait]))
            if any(count >= threshold for threshold in thresholds):
                activated_traits[trait] = count

    return selected_champions, len(activated_traits), activated_traits, primary_trait

def generate_team_code(team, champions_codes):
    """
    Generate a team code for the given team of champions.
    The code follows the pattern: 02000000000000000000000000000000TFTSet14
    """
    base_code = "02" + "0" * 30 + "TFTSet14"
    champion_positions = [champions_codes[champion] for champion in team]
    for i, code in enumerate(champion_positions):
        start_index = 2 + i * 3
        base_code = base_code[:start_index] + code + base_code[start_index + 3:]
    return base_code

def generate_team_api():
    """
    API endpoint to generate a team based on selected emblems.
    """
    print("Generating team based on selected emblems...")
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug: Log the incoming data

        if not data:
            print("No JSON data received")  # Debug: Log missing data
            return jsonify({"error": "No JSON data received"}), 400

        emblems = data.get("emblems", [])
        team_size = data.get("team_size", 8)

        if not emblems or not isinstance(emblems, list) or not all(isinstance(e, str) for e in emblems):
            print("Invalid emblems input")  # Debug: Log invalid input
            return jsonify({"error": "Invalid emblems input"}), 400

        best_team, max_traits, activated_traits, primary_trait = find_best_team_vertical_with_full_traits(
            emblems, champions_traits, traits, team_size
        )
        return jsonify({
            "team": best_team,
            "activated_traits": activated_traits,
            "primary_trait": primary_trait,
            "team_code": generate_team_code(best_team, champions_codes)
        })
    except Exception as e:
        print(f"Error in generate_team_api: {e}")  # Debug: Log unexpected errors
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    # Example usage
    emblems = ['Marksman', 'Anima Squad', 'A.M.P.']  # Input your emblems here
    team_size = 10

    # Example usage for prioritizing full traits
    best_teams = find_best_team_prioritize_full_traits(emblems, champions_traits, traits, team_size)
    print(f"Best teams of size {team_size} (bronze for life):")
    for team, activated_traits, num_activated_traits in best_teams:
        print(f"Team: {team}")
        print(f"Number of activated non-unique traits: {num_activated_traits}")
        print("Activated traits and their counts:")
        for trait, count in activated_traits.items():
            print(f"{trait}: {count}")
        print(f'Team code: {generate_team_code(team, champions_codes)}\n')

    # Example usage for vertical approach with full traits
    best_team, max_traits, activated_traits, primary_trait = find_best_team_vertical_with_full_traits(emblems, champions_traits, traits, team_size)
    print(f"Best team of size {team_size} prioritizing vertical for '{primary_trait}': {best_team}")
    print(f"Number of activated non-unique traits: {max_traits}")
    print("Activated traits and their counts:")
    for trait, count in activated_traits.items():
        print(f"{trait}: {count}")

    # Example usage for generating team code
    team_code = generate_team_code(best_team, champions_codes)
    print(f"Team code: {team_code}")


    # # Example usage for finding the best combination of emblems and team
    # best_combination = find_best_emblems_and_team(champions_traits, traits, team_size=11, max_emblems=3)
    # if best_combination:
    #     emblems, team, activated_traits = best_combination
    #     print(f"Best combination of up to 3 emblems and team of size {team_size}:")
    #     print(f"Emblems: {emblems}")
    #     print(f"Team: {team}")
    #     print("Activated traits and their counts:")
    #     for trait, count in activated_traits.items():
    #         print(f"{trait}: {count}")
    #     print(f'Team code: {generate_team_code(team, champions_codes)}\n')
