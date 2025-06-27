# modules/rl_tool.py

from rl_selector import RLVersionSelector

def rl_cli():
    agent = RLVersionSelector()

    while True:
        print("\n🎛️ RL Feedback Tool")
        print("1. Add Feedback")
        print("2. Show Top Versions")
        print("3. Show All Scores")
        print("4. Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            version_id = input("🆔 Enter Version ID: ").strip()
            try:
                score = float(input("⭐ Enter rating (1-5): ").strip())
                assert 1 <= score <= 5
            except:
                print("❌ Invalid score.")
                continue
            agent.add_feedback(version_id, score)

        elif choice == "2":
            top = agent.get_top_versions()
            if not top:
                print("⚠️ No scores yet.")
                continue
            print("\n🏆 Top Ranked Versions:")
            for i, (vid, score) in enumerate(top, 1):
                print(f"{i}. 🆔 {vid} → Avg Score: {score:.2f}")

        elif choice == "3":
            agent.display_all_scores()

        elif choice == "4":
            print("👋 Exiting RL Tool.")
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    rl_cli()
