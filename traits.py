from itertools import combinations, permutations
from collections import Counter
from flask import jsonify, request

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
champions_cost = {
    "Alistar": "1",
    "Annie": "4",
    "Aphelios": "4",
    "Aurora": "5",
    "Brand": "4",
    "Braum": "3",
    "Cho'Gath": "4",
    "Darius": "2",
    "Draven": "3",
    "Dr.Mundo": "1",
    "Ekko": "2",
    "Elise": "3",
    "Fiddlesticks": "3",
    "Galio": "3",
    "Garen": "5",
    "Gragas": "3",
    "Graves": "2",
    "Illaoi": "2",
    "Jarvan IV": "3",
    "Jax": "1",
    "Jhin": "2",
    "Jinx": "3",
    "Kindred": "1",
    "Kobuko": "5",
    "Kog'Maw": "1",
    "LeBlanc": "2",
    "Leona": "4",
    "Miss Fortune": "4",
    "Mordekaiser": "3",
    "Morgana": "1",
    "Naafiri": "2",
    "Neeko": "4",
    "Nidalee": "1",
    "Poppy": "1",
    "Renekton": "5",
    "Rengar": "3",
    "Rhaast": "2",
    "Samira": "5",
    "Sejuani": "4",
    "Senna": "3",
    "Seraphine": "1",
    "Shaco": "1",
    "Shyvana": "2",
    "Skarner": "2",
    "Sylas": "1",
    "Twisted Fate": "2",
    "Urgot": "5",
    "Varus": "3",
    "Vayne": "2",
    "Veigar": "2",
    "Vex": "4",
    "Vi": "1",
    "Viego": "5",
    "Xayah": "4",
    "Yuumi": "3",
    "Zac": "5",
    "Zed": "4",
    "Zeri": "4",
    "Ziggs": "4",
    "Zyra": "1"
}
traits = {
    'A.M.P.': ['2', '3', '4', '5'],
    'Anima Squad': ['3', '5', '7', '10'],
    'Bastion': ['2', '4', '6'],
    'BoomBots': ['2', '4', '6'],
    'Bruiser': ['2', '4', '6'],
    'Cyberboss': ['2', '3', '4'],
    'Cypher': ['3', '4', '5'],
    'Divinicorp': ['1', '2', '3', '4', '5', '6', '7'],
    'Dynamo': ['2', '3', '4'],
    'Executioner': ['2', '3', '4', '5'],
    'Exotech': ['3', '5', '7', '10'],
    'Golden Ox': ['2', '4', '6'],
    'Marksman': ['2', '4'],
    'Nitro': ['3', '4'],
    'Rapidfire': ['2', '4', '6'],
    'Slayer': ['2', '4', '6'],
    'Strategist': ['2', '3', '4', '5'],
    'Street Demon': ['3', '5', '7', '10'],
    'Syndicate': ['3', '5', '7'],
    'Techie': ['2', '4', '6', '8'],
    'Vanguard': ['2', '4', '6']
}
possible_emblems = ['Anima Squad','Bastion','BoomBots','Bruiser','Cypher','Divinicorp',
                    'Dynamo','Executioner','Exotech','Golden Ox','Marksman','Rapidfire',
                    'Slayer','Strategist','Street Demon','Syndicate','Techie','Vanguard']


def find_best_team_prioritize_full_traits(emblems, champions_traits, traits, team_size=8):
    best_teams = []
    max_activated_traits = 0

    # Evaluate all subsets of emblems to ensure the best configuration is found
    for emblem_count in range(1, len(emblems) + 1):
        for emblem_subset in combinations(emblems, emblem_count):
            for emblem_order in permutations(emblem_subset):
                trait_counts = Counter(emblem_order)
                selected_champions = []

                while len(selected_champions) < team_size:
                    best_champion = None
                    best_completion_score = 0
                    best_total_traits = 0

                    for champion, champion_traits in champions_traits.items():
                        if champion in selected_champions:
                            continue

                        simulated_trait_counts = trait_counts.copy()
                        for trait in champion_traits:
                            simulated_trait_counts[trait] += 1

                        # Avoid creating incomplete thresholds
                        valid = True
                        for trait, count in simulated_trait_counts.items():
                            if trait in traits:
                                thresholds = list(map(int, traits[trait]))
                                if count > max(thresholds) and count - 1 not in thresholds:
                                    valid = False
                                    break
                        if not valid:
                            continue

                        # Calculate how many traits would be activated by adding this champion
                        completion_score = 0
                        for trait, count in simulated_trait_counts.items():
                            if trait in traits:
                                thresholds = list(map(int, traits[trait]))
                                if any(count == threshold for threshold in thresholds):
                                    completion_score += 1

                        total_traits = len(champion_traits)

                        # Select the champion that maximizes the number of activated traits
                        if (completion_score > best_completion_score or
                            (completion_score == best_completion_score and total_traits > best_total_traits)):
                            best_champion = champion
                            best_completion_score = completion_score
                            best_total_traits = total_traits

                    if best_champion is None:
                        break

                    selected_champions.append(best_champion)
                    for trait in champions_traits[best_champion]:
                        trait_counts[trait] += 1

                if len(selected_champions) < team_size:
                    remaining_champions = [champ for champ in champions_traits if champ not in selected_champions]
                    selected_champions.extend(remaining_champions[:team_size - len(selected_champions)])

                activated_traits = {}
                for trait, count in trait_counts.items():
                    if trait in traits:
                        thresholds = list(map(int, traits[trait]))
                        if any(count >= threshold for threshold in thresholds):
                            activated_traits[trait] = count

                num_activated_traits = len(activated_traits)
                if num_activated_traits > max_activated_traits:
                    max_activated_traits = num_activated_traits
                    best_teams = [(selected_champions, activated_traits, num_activated_traits)]
                elif num_activated_traits == max_activated_traits:
                    # Ensure all unique teams are added to the best_teams list
                    if not any(set(team[0]) == set(selected_champions) for team in best_teams):
                        best_teams.append((selected_champions, activated_traits, num_activated_traits))

    # Recount activated traits for the final best team
    final_teams = []
    if best_teams:
        for selected_champions, _, _ in best_teams:
            final_trait_counts = Counter(emblems)
            for champion in selected_champions:
                for trait in champions_traits[champion]:
                    final_trait_counts[trait] += 1

            # Recalculate activated traits
            final_activated_traits = {}
            all_traits_valid = True
            for trait, count in final_trait_counts.items():
                if trait in traits:
                    thresholds = list(map(int, traits[trait]))
                    if any(count == threshold for threshold in thresholds):  # Check if count matches any threshold
                        final_activated_traits[trait] = count
                    else:
                        all_traits_valid = False  # Mark as invalid if no threshold is met

            # Count the number of activated traits
            num_activated_traits = len(final_activated_traits)

            # Append the recalculated team with a flag for valid traits
            final_teams.append((selected_champions, final_activated_traits, num_activated_traits, all_traits_valid))

    # Filter teams to prioritize those with all valid traits
    teams_with_all_valid_traits = [team for team in final_teams if team[3]]  # Teams with all traits valid
    if teams_with_all_valid_traits:
        final_teams = teams_with_all_valid_traits
    else:
        # If no teams have all valid traits, filter by max traits
        max_traits = max(team[2] for team in final_teams)
        final_teams = [team for team in final_teams if team[2] == max_traits]

    # Remove the `all_traits_valid` flag before returning
    final_teams = [(team[0], team[1], team[2]) for team in final_teams]

    return final_teams

def fill_remaining_slots_by_traits(emblems, champions_traits, traits, trait_counts, selected_champions, team_size):
    remaining_slots = team_size - len(selected_champions)
    remaining_champions = [champ for champ in champions_traits if champ not in selected_champions]

    while remaining_slots > 0 and remaining_champions:
        best_champion = None
        best_completion_score = 0
        best_total_traits = 0

        for champion in remaining_champions:
            champion_traits = champions_traits[champion]

            completion_score = 0
            simulated_trait_counts = trait_counts.copy()
            for trait in champion_traits:
                simulated_trait_counts[trait] += 1
                if trait in traits:
                    thresholds = list(map(int, traits[trait]))
                    if any(simulated_trait_counts[trait] == threshold for threshold in thresholds):
                        completion_score += 1

            total_traits = len(champion_traits)

            if (completion_score > best_completion_score or
                (completion_score == best_completion_score and total_traits > best_total_traits)):
                best_champion = champion
                best_completion_score = completion_score
                best_total_traits = total_traits

        if best_champion is None:
            break

        selected_champions.append(best_champion)
        for trait in champions_traits[best_champion]:
            trait_counts[trait] += 1

        remaining_champions.remove(best_champion)
        remaining_slots -= 1

    return selected_champions, trait_counts

def find_best_team_vertical_with_full_traits(emblems, champions_traits, traits, team_size=8, forced_trait=None):
    primary_trait = forced_trait or max(emblems, key=lambda e: max(map(int, traits[e])), default=None)
    if primary_trait is None:
        raise ValueError("No valid emblems provided.")

    trait_counts = Counter(emblems)
    selected_champions = []

    primary_trait_thresholds = list(map(int, traits[primary_trait]))
    primary_trait_thresholds.sort()

    champions_with_trait = [champ for champ, champ_traits in champions_traits.items() if primary_trait in champ_traits]
    max_possible_count = len(champions_with_trait) + trait_counts[primary_trait]
    max_achievable_threshold = next((t for t in reversed(primary_trait_thresholds) if t <= max_possible_count), None)

    while len(selected_champions) < team_size:
        current_primary_count = trait_counts[primary_trait]
        next_threshold = next((t for t in primary_trait_thresholds if t > current_primary_count), None)

        remaining_slots = team_size - len(selected_champions)
        if next_threshold is None or next_threshold > max_achievable_threshold or next_threshold - current_primary_count > remaining_slots:
            break

        best_champion = None
        best_primary_trait_contribution = 0
        best_total_traits = 0

        for champion, champion_traits in champions_traits.items():
            if champion in selected_champions:
                continue

            primary_trait_contribution = champion_traits.count(primary_trait)
            total_traits = len(champion_traits)

            # Prioritize champions with the primary_trait
            if primary_trait_contribution > 0 and (
                primary_trait_contribution > best_primary_trait_contribution or
                (primary_trait_contribution == best_primary_trait_contribution and total_traits > best_total_traits)
            ):
                best_champion = champion
                best_primary_trait_contribution = primary_trait_contribution
                best_total_traits = total_traits

        if best_champion is None:
            break

        selected_champions.append(best_champion)
        for trait in champions_traits[best_champion]:
            trait_counts[trait] += 1

    selected_champions, trait_counts = fill_remaining_slots_by_traits(
        emblems,
        champions_traits,
        traits,
        trait_counts,
        selected_champions,
        team_size
    )

    activated_traits = {}
    for trait, count in trait_counts.items():
        if trait in traits:
            thresholds = list(map(int, traits[trait]))
            if any(count >= threshold for threshold in thresholds):
                activated_traits[trait] = count

    return selected_champions, len(activated_traits), activated_traits, primary_trait

def generate_team_code(team, champions_codes):
    base_code = "02" + "0" * 30 + "TFTSet14"
    champion_positions = [champions_codes[champion] for champion in team]
    for i, code in enumerate(champion_positions):
        start_index = 2 + i * 3
        base_code = base_code[:start_index] + code + base_code[start_index + 3:]
    return base_code

def sort_champions_by_cost(champions, champions_cost):
    return sorted(champions, key=lambda champ: (int(champions_cost[champ]), champ.lower()))

def generate_team_api():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        emblems = data.get("emblems", [])
        team_size = data.get("team_size", 8)
        forced_trait = data.get("forced_trait", None)

        if not emblems or not isinstance(emblems, list) or not all(isinstance(e, str) for e in emblems):
            return jsonify({"error": "Invalid emblems input"}), 400

        best_team, max_traits, activated_traits, primary_trait = find_best_team_vertical_with_full_traits(
            emblems, champions_traits, traits, team_size, forced_trait
        )
        sorted_team = sort_champions_by_cost(best_team, champions_cost)
        return jsonify({
            "team": sorted_team,
            "activated_traits": activated_traits,
            "primary_trait": primary_trait,
            "team_code": generate_team_code(sorted_team, champions_codes)
        })
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

def generate_prioritize_full_traits_api():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        emblems = data.get("emblems", [])
        team_size = data.get("team_size", 8)

        if not emblems or not isinstance(emblems, list) or not all(isinstance(e, str) for e in emblems):
            return jsonify({"error": "Invalid emblems input"}), 400

        # Call the function to find the best teams
        final_teams = find_best_team_prioritize_full_traits(emblems, champions_traits, traits, team_size)

        # Ensure all activated traits are included in the response
        results = []
        for team, activated_traits, num_activated_traits in final_teams:
            sorted_team = sort_champions_by_cost(team, champions_cost)
            results.append({
                "team": sorted_team,
                "activated_traits": activated_traits,  # Use the recalculated activated traits
                "num_activated_traits": num_activated_traits,
                "team_code": generate_team_code(sorted_team, champions_codes)
            })

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500