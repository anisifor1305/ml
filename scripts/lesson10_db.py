"""Инфраструктура занятия 10: отдельный PostgreSQL; учебных решений здесь нет."""

import argparse
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".lesson10_pg"
COMPOSE = ROOT / "infra/lesson_10/compose.yaml"
SEED = ROOT / "infra/lesson_10/seed.sql"


def binary(name):
    path = shutil.which(name)
    if path is None:
        raise RuntimeError("Не найден инструмент: " + name)
    return path


def psql_command(backend):
    if backend == "docker":
        return [
            binary("docker"),
            "compose",
            "-p",
            "ml-lesson10",
            "-f",
            str(COMPOSE),
            "exec",
            "-T",
            "db",
            "psql",
            "-U",
            "lesson10",
            "-d",
            "lesson10",
        ]
    return [
        binary("psql"),
        "-h",
        str(STATE / "socket"),
        "-p",
        "55410",
        "-U",
        "lesson10",
        "-d",
        "postgres",
    ]


def execute(backend, sql):
    result = subprocess.run(
        psql_command(backend) + ["-X", "-q", "-v", "ON_ERROR_STOP=1"],
        input=sql,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def start(backend):
    if backend == "docker":
        subprocess.run(
            [
                binary("docker"),
                "compose",
                "-p",
                "ml-lesson10",
                "-f",
                str(COMPOSE),
                "up",
                "-d",
                "--wait",
            ],
            check=True,
        )
    else:
        STATE.mkdir(mode=0o700, exist_ok=True)
        socket = STATE / "socket"
        socket.mkdir(mode=0o700, exist_ok=True)
        data = STATE / "data"
        if not (data / "PG_VERSION").exists():
            subprocess.run(
                [
                    binary("initdb"),
                    "-D",
                    str(data),
                    "-U",
                    "lesson10",
                    "--auth-local=trust",
                    "--auth-host=reject",
                    "--encoding=UTF8",
                    "--locale=C",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        status = subprocess.run([binary("pg_ctl"), "-D", str(data), "status"], capture_output=True)
        if status.returncode:
            options = "-k {} -p 55410 -c listen_addresses=''".format(socket)
            subprocess.run(
                [
                    binary("pg_ctl"),
                    "-D",
                    str(data),
                    "-l",
                    str(STATE / "server.log"),
                    "-o",
                    options,
                    "-w",
                    "start",
                ],
                check=True,
            )
    execute(backend, SEED.read_text())
    execute(backend, (ROOT / "infra/lesson_10/demo.sql").read_text())
    print("База готова. Backend: " + backend + "; схема: lesson10")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "stop", "shell"])
    parser.add_argument("--backend", choices=["local", "docker"], default="local")
    args = parser.parse_args()
    if args.action == "start":
        start(args.backend)
    elif args.action == "shell":
        if args.backend == "docker":
            command = [
                binary("docker"),
                "compose",
                "-p",
                "ml-lesson10",
                "-f",
                str(COMPOSE),
                "exec",
                "-e",
                "PGOPTIONS=-c search_path=lesson10",
                "db",
                "psql",
                "-X",
                "-U",
                "lesson10",
                "-d",
                "lesson10",
            ]
            subprocess.run(command, check=True)
        else:
            environment = dict(os.environ, PGOPTIONS="-c search_path=lesson10")
            subprocess.run(psql_command(args.backend) + ["-X"], env=environment, check=True)
    elif args.backend == "docker":
        subprocess.run(
            [binary("docker"), "compose", "-p", "ml-lesson10", "-f", str(COMPOSE), "stop"],
            check=True,
        )
    else:
        subprocess.run([binary("pg_ctl"), "-D", str(STATE / "data"), "-w", "stop"], check=True)


if __name__ == "__main__":
    main()
