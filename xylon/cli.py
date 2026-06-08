"""命令行接口."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from xylon import __version__
from xylon.core import backup, restore, status
from xylon.registry import list_apps


def _default_store_dir() -> Path:
    """默认备份仓库目录：脚本所在仓库的 configs/ 目录."""
    # 当作为包运行时，取包的上级目录
    try:
        import xylon

        pkg_dir = Path(xylon.__file__).resolve().parent
        return pkg_dir.parent / "configs"
    except Exception:
        return Path.cwd() / "configs"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xylon",
        description="Xylon - 跨平台 CLI 配置备份与还原工具",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "-s",
        "--store",
        type=Path,
        default=_default_store_dir(),
        help=f"备份仓库根目录 (默认: {_default_store_dir()})",
    )
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="仅打印将要执行的操作，不实际复制文件",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # backup
    backup_parser = sub.add_parser("backup", help="备份配置到仓库")
    backup_parser.add_argument(
        "apps",
        nargs="*",
        help="要备份的应用名称（空格分隔）；省略则备份所有已注册且存在的应用",
    )

    # restore
    restore_parser = sub.add_parser("restore", help="从仓库还原配置")
    restore_parser.add_argument(
        "apps",
        nargs="*",
        help="要还原的应用名称（空格分隔）；省略则还原仓库中所有存在的备份",
    )

    # status
    sub.add_parser("status", help="查看系统配置与备份仓库的状态对比")

    # list
    list_parser = sub.add_parser("list", help="列出所有支持的应用")
    list_parser.add_argument(
        "-a", "--all", action="store_true", help="列出全部应用；否则仅列出当前系统检测到的"
    )

    return parser


def _cmd_list(args: argparse.Namespace) -> int:
    from xylon.registry import get_app

    print(f"{'应用':<12} {'描述':<20} {'状态'}")
    print("-" * 40)
    for name in list_apps():
        app = get_app(name)
        if app is None:
            continue
        if args.all or app.exists():
            status_str = "已检测" if app.exists() else "未检测"
            print(f"{app.name:<12} {app.description:<20} {status_str}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    store_dir: Path = args.store
    store_dir.mkdir(parents=True, exist_ok=True)

    if args.command == "backup":
        apps = args.apps if args.apps else None
        backup(store_dir, apps=apps, dry_run=args.dry_run)
        return 0

    if args.command == "restore":
        apps = args.apps if args.apps else None
        restore(store_dir, apps=apps, dry_run=args.dry_run)
        return 0

    if args.command == "status":
        status(store_dir)
        return 0

    if args.command == "list":
        return _cmd_list(args)

    return 1


if __name__ == "__main__":
    sys.exit(main())
