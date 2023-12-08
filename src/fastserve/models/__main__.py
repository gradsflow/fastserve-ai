import argparse

from fastserve.utils import get_default_device

from . import ServeSDXLTurbo
from .llama_cpp import ServeLlamaCpp
from .ssd import ServeSSD1B

parser = argparse.ArgumentParser(description="Serve models with FastServe")
parser.add_argument("--model", type=str, required=True, help="Name of the model")
parser.add_argument("--device", type=str, required=False, help="Device")
parser.add_argument(
    "--batch_size",
    type=int,
    default=1,
    required=False,
    help="Maximum batch size for the ML endpoint",
)
parser.add_argument(
    "--timeout",
    type=float,
    default=0.0,
    required=False,
    help="Timeout to aggregate maximum batch size",
)

parser.add_argument(
    "--model_path",
    type=str,
    required=False,
    help="Model checkpoint path",
)

args = parser.parse_args()

app = None
device = args.device or get_default_device()

if args.model == "ssd-1b":
    app = ServeSSD1B(device=device, timeout=args.timeout, batch_size=args.batch_size)
elif args.model == "sdxl-turbo":
    app = ServeSDXLTurbo(
        device=device, timeout=args.timeout, batch_size=args.batch_size
    )

elif args.model == "llama-cpp":
    app = ServeLlamaCpp(
        model_path=args.model_path,
        device=device,
        timeout=args.timeout,
        batch_size=args.batch_size,
    )
else:
    raise Exception(f"FastServe.models doesn't implement model={args.model}")

app.run_server()