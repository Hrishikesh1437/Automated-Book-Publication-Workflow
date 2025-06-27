from modules.rl_selector import RLVersionSelector

rl = RLVersionSelector()
print(rl.get_top_versions())  # Should print something like: [('version_id_1', 4.5), ...]
