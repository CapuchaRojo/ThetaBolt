from jsonargparse import ArgumentParser


def load_config(args=None):
    parser = ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--units", type=int, default=100)
    parser.add_argument("--sr", type=float, default=1.25)
    parser.add_argument("--lr", type=float, default=0.3)
    parser.add_argument("--ridge", type=float, default=1e-5)
    parser.add_argument("--num_agents", type=int, default=10)
    parser.add_argument("--use_quantum", type=bool, default=False)
    parser.add_argument("--quantum_threshold", type=int, default=100)
    parser.add_argument("--config", action="config", help="JSON config file")

    return parser.parse_args(args)
