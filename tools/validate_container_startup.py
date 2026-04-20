from pathlib import Path
import subprocess
import time
import urllib.request
import sys

IMAGE_NAME = "fastapi-mock-enterprise-app:local"
CONTAINER_NAME = "fcapi45-fastapi-validation"
HOST_PORT = "8080"
CONTAINER_PORT = "8080"

APP_DIR = Path(__file__).resolve().parents[1]   # sut/FastAPIMockApp
DOCKERFILE = APP_DIR / "Dockerfile"


def run(cmd: list[str], check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess:
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        check=False,
        text=True,
        capture_output=True,
        cwd=str(cwd) if cwd else None,
    )

    if result.stdout:
        print("\nSTDOUT:")
        print(result.stdout)

    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {' '.join(cmd)}"
        )

    return result


def cleanup() -> None:
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        text=True,
        capture_output=True,
    )


def wait_for_health(url: str, timeout_seconds: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout_seconds:
        try:
            with urllib.request.urlopen(url, timeout=3) as response:
                if response.status == 200:
                    print(f"Health check passed: {url}")
                    return True
        except Exception:
            pass
        time.sleep(2)
    return False


def main() -> int:
    cleanup()

    try:
        run(
            ["docker", "build", "-t", IMAGE_NAME, "-f", str(DOCKERFILE), str(APP_DIR)],
            cwd=APP_DIR,
        )

        run([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", f"{HOST_PORT}:{CONTAINER_PORT}",
            IMAGE_NAME
        ])

        url = f"http://127.0.0.1:{HOST_PORT}/health"
        if not wait_for_health(url):
            print("FastAPI service did not become healthy in time.")
            logs = run(["docker", "logs", CONTAINER_NAME], check=False)
            print("\nContainer logs:\n")
            print(logs.stdout)
            print(logs.stderr)
            return 1

        print("FCAPI-45 validation passed.")
        return 0

    finally:
        cleanup()


if __name__ == "__main__":
    sys.exit(main())