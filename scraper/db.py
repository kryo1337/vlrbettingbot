from inserts import insert_upcoming_matches, insert_live_scores, insert_match_results
from scraper import vlr_upcoming_matches, vlr_live_score, vlr_match_results


if __name__ == "__main__":
    while True:
        print("1. upcoming matches")
        print("2. live scores")
        print("3. match results")
        print("0. exit")
        choice = input("select: ").strip()

        if choice == "1":
            upcoming_data = vlr_upcoming_matches()
            insert_upcoming_matches(upcoming_data)
            print("upcoming matches success")
        elif choice == "2":
            live_data = vlr_live_score()
            insert_live_scores(live_data)
            print("live scores success")
        elif choice == "3":
            results_data = vlr_match_results()
            insert_match_results(results_data)
            print("match results success")
        elif choice == "0":
            print("exiting")
            break
        else:
            print("select (1-3) or 0 to exit")
