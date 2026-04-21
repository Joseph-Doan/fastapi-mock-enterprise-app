from __future__ import annotations

import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

IMAGE_NAME = "fastapi-mock-enterprise-app:local"
CONTAINER_NAME = "fastapi-container-validation"

HOST_PORT = "8080"
CONTAINER_PORT = "8080"

HEALTH_PATH = "/health"
HEALTH_URL = f"http://127.0.0.1:{HOST_PORT}{HEALTH_PATH}"

STARTUP_TIMEOUT_SECONDS = 30
POLL_INTERVAL_SECONDS = 2

APP_DIR = Path(__file__).resolve().parents[1]
DOCKERFILE = APP_DIR / "Dockerfile"


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def log(message: str) -> None:
    print(message, flush=True)


def run(
    cmd: list[str],
    *,
    check: bool = True,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """
    Run shell command and print stdout/stderr.
    """
    log(f"Running: {' '.join(cmd)}")

    result = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )

    if result.stdout.strip():
        log("\nSTDOUT:")
        log(result.stdout.strip())

    if result.stderr.strip():
        log("\nSTDERR:")
        log(result.stderr.strip())

    if check and result.returncode != 0:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {' '.join(cmd)}"
        )

    return result


def cleanup() -> None:
    """
    Remove validation container if present.
    """
    subprocess.run(
        ["docker", "rm", "-f", CONTAINER_NAME],
        text=True,
        capture_output=True,
    )


def ensure_docker_available() -> None:
    """
    Ensure Docker daemon is reachable before starting.
    """
    result = subprocess.run(
        ["docker", "info"],
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Docker is not available.\n"
            "Start Docker Desktop and ensure Linux containers are enabled.\n\n"
            f"{result.stderr.strip()}"
        )


def wait_for_external_health() -> None:
    """
    Poll host-mapped /health endpoint until healthy or timeout.
    """
    log(f"Waiting for FastAPI health endpoint: {HEALTH_URL}")

    deadline = time.time() + STARTUP_TIMEOUT_SECONDS

    while time.time() < deadline:
        try:
            with urllib.request.urlopen(HEALTH_URL, timeout=3) as response:
                if response.status == 200:
                    log(f"External health check passed: {HEALTH_URL}")
                    return

        except urllib.error.URLError:
            pass
        except Exception:
            pass

        time.sleep(POLL_INTERVAL_SECONDS)

    raise RuntimeError(
        f"FastAPI service did not become healthy within "
        f"{STARTUP_TIMEOUT_SECONDS} seconds."
    )


def verify_internal_health() -> None:
    """
    Confirm /health reachable from inside running container.
    """
    run([
        "docker",
        "exec",
        CONTAINER_NAME,
        "curl",
        "--fail",
        f"http://127.0.0.1:{CONTAINER_PORT}{HEALTH_PATH}",
    ])

    log("Internal container /health check passed.")


def verify_docker_health_status() -> None:
    """
    Optional: confirm Docker healthcheck reports healthy.
    """
    result = run(
        [
            "docker",
            "inspect",
            "--format={{.State.Health.Status}}",
            CONTAINER_NAME,
        ],
        check=False,
    )

    status = result.stdout.strip()

    if status:
        log(f"Docker container health status: {status}")


def print_container_logs() -> None:
    """
    Print logs for easier troubleshooting.
    """
    run(["docker", "logs", CONTAINER_NAME], check=False)


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main() -> int:
    cleanup()

    try:
        ensure_docker_available()

        # Build image
        run(
            [
                "docker",
                "build",
                "-t",
                IMAGE_NAME,
                "-f",
                str(DOCKERFILE),
                str(APP_DIR),
            ],
            cwd=APP_DIR,
        )

        # Start container
        run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                CONTAINER_NAME,
                "-p",
                f"{HOST_PORT}:{CONTAINER_PORT}",
                IMAGE_NAME,
            ]
        )

        # Validate host accessibility
        wait_for_external_health()

        # Validate internal accessibility
        verify_internal_health()

        # Optional Docker health state
        verify_docker_health_status()

        log("FCAPI validation passed.")
        return 0

    except Exception as exc:
        log(f"\nERROR: {exc}\n")
        print_container_logs()
        return 1

    finally:
        cleanup()


if __name__ == "__main__":
    sys.exit(main())