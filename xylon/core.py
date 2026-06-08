"""备份与还原核心逻辑."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

from xylon.registry import AppConfig, get_app, list_apps


def _platform_name() -> str:
    return "macOS" if sys.platform == "darwin" else "Linux"


def _copy_file(src: Path, dst: Path) -> None:
    """复制单个文件，保留元数据."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _copy_dir(src: Path, dst: Path) -> None:
    """递归复制目录."""
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def _backup_app(app: AppConfig, store_dir: Path) -> list[str]:
    """备份单个应用，返回备份了哪些路径的日志信息."""
    logs: list[str] = []
    app_store = store_dir / app.name

    for src in app.get_paths():
        if not src.exists():
            continue

        if app.is_dir:
            # 目录：保持目录名复制到 store 下
            dst = app_store / src.name
            _copy_dir(src, dst)
            logs.append(f"  [DIR]  {src} -> {dst}")
        else:
            # 文件：扁平化存放在 app_store 下
            dst = app_store / src.name
            _copy_file(src, dst)
            logs.append(f"  [FILE] {src} -> {dst}")

    return logs


def backup(
    store_dir: Path,
    apps: list[str] | None = None,
    dry_run: bool = False,
) -> None:
    """备份指定应用（或全部）到 store_dir.

    Args:
        store_dir: 备份仓库根目录.
        apps: 要备份的应用列表；None 表示备份所有已注册且存在的应用.
        dry_run: 若为 True，仅打印将要执行的操作而不实际复制.
    """
    targets = apps if apps else list_apps()
    print(f"平台: {_platform_name()}")
    print(f"备份目录: {store_dir.resolve()}")
    print("-" * 50)

    backed_up = 0
    for name in targets:
        app = get_app(name)
        if app is None:
            print(f"[SKIP] 未知应用: {name}")
            continue

        if not app.exists():
            print(f"[SKIP] {app.name} ({app.description}) - 配置不存在")
            continue

        if dry_run:
            print(f"[DRY]  {app.name} ({app.description})")
            for src in app.get_paths():
                if src.exists():
                    print(f"  -> 将备份 {src}")
            backed_up += 1
            continue

        logs = _backup_app(app, store_dir)
        if logs:
            print(f"[OK]   {app.name} ({app.description})")
            for line in logs:
                print(line)
            backed_up += 1

    print("-" * 50)
    print(f"完成: {backed_up} 个应用已备份")


def _restore_app(app: AppConfig, store_dir: Path) -> list[str]:
    """还原单个应用，返回还原了哪些路径的日志信息."""
    logs: list[str] = []
    app_store = store_dir / app.name

    if not app_store.exists():
        return logs

    for src in app.get_paths():
        if app.is_dir:
            src_path = app_store / src.name
            if src_path.exists():
                if src.exists():
                    shutil.rmtree(src)
                _copy_dir(src_path, src)
                logs.append(f"  [DIR]  {src_path} -> {src}")
        else:
            src_path = app_store / src.name
            if src_path.exists():
                src.parent.mkdir(parents=True, exist_ok=True)
                _copy_file(src_path, src)
                logs.append(f"  [FILE] {src_path} -> {src}")

    return logs


def restore(
    store_dir: Path,
    apps: list[str] | None = None,
    dry_run: bool = False,
) -> None:
    """从 store_dir 还原指定应用（或全部）.

    Args:
        store_dir: 备份仓库根目录.
        apps: 要还原的应用列表；None 表示还原 store_dir 中所有存在的备份.
        dry_run: 若为 True，仅打印将要执行的操作而不实际复制.
    """
    targets = apps if apps else list_apps()
    print(f"平台: {_platform_name()}")
    print(f"备份目录: {store_dir.resolve()}")
    print("-" * 50)

    restored = 0
    for name in targets:
        app = get_app(name)
        if app is None:
            print(f"[SKIP] 未知应用: {name}")
            continue

        app_store = store_dir / app.name
        if not app_store.exists():
            print(f"[SKIP] {app.name} ({app.description}) - 备份不存在")
            continue

        if dry_run:
            print(f"[DRY]  {app.name} ({app.description})")
            for entry in app_store.iterdir():
                print(f"  -> 将还原到 {entry.name}")
            restored += 1
            continue

        logs = _restore_app(app, store_dir)
        if logs:
            print(f"[OK]   {app.name} ({app.description})")
            for line in logs:
                print(line)
            restored += 1

    print("-" * 50)
    print(f"完成: {restored} 个应用已还原")


def status(store_dir: Path) -> None:
    """显示当前系统和备份仓库的状态对比."""
    print(f"平台: {_platform_name()}")
    print(f"备份目录: {store_dir.resolve()}")
    print(f"{'应用':<12} {'描述':<20} {'系统':<8} {'仓库':<8}")
    print("-" * 52)

    for name in list_apps():
        app = get_app(name)
        if app is None:
            continue
        sys_exists = "✓" if app.exists() else "✗"
        store_exists = "✓" if (store_dir / app.name).exists() else "✗"
        print(f"{app.name:<12} {app.description:<20} {sys_exists:<8} {store_exists:<8}")
