"""应用配置注册表：定义各 CLI 工具在不同平台下的配置路径."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    """单个应用的配置定义."""

    name: str
    description: str
    paths: dict[str, list[Path]]
    is_dir: bool = False

    def get_paths(self) -> list[Path]:
        """返回当前平台下的配置路径列表."""
        platform = "macos" if sys.platform == "darwin" else "linux"
        return self.paths.get(platform, [])

    def exists(self) -> bool:
        """检查当前平台下是否有任何配置存在."""
        return any(p.exists() for p in self.get_paths())

    def __repr__(self) -> str:
        return f"AppConfig({self.name})"


_HOME = Path.home()

# ---------------------------------------------------------------------------
# 注册表
# ---------------------------------------------------------------------------
REGISTRY: dict[str, AppConfig] = {
    "ghostty": AppConfig(
        name="ghostty",
        description="Ghostty 终端模拟器",
        paths={
            "macos": [_HOME / "Library" / "Application Support" / "com.mitchellh.ghostty" / "config"],
            "linux": [_HOME / ".config" / "ghostty" / "config"],
        },
    ),
    "starship": AppConfig(
        name="starship",
        description="Starship 提示符",
        paths={
            "macos": [_HOME / ".config" / "starship.toml"],
            "linux": [_HOME / ".config" / "starship.toml"],
        },
    ),
    "tmux": AppConfig(
        name="tmux",
        description="Tmux 终端复用器",
        paths={
            "macos": [
                _HOME / ".tmux.conf",
                _HOME / ".config" / "tmux" / "tmux.conf",
            ],
            "linux": [
                _HOME / ".tmux.conf",
                _HOME / ".config" / "tmux" / "tmux.conf",
            ],
        },
    ),
    "nvim": AppConfig(
        name="nvim",
        description="Neovim 编辑器",
        paths={
            "macos": [_HOME / ".config" / "nvim"],
            "linux": [_HOME / ".config" / "nvim"],
        },
        is_dir=True,
    ),
    "zsh": AppConfig(
        name="zsh",
        description="Zsh Shell",
        paths={
            "macos": [
                _HOME / ".zshrc",
                _HOME / ".zprofile",
                _HOME / ".zshenv",
                _HOME / ".zlogin",
                _HOME / ".zlogout",
            ],
            "linux": [
                _HOME / ".zshrc",
                _HOME / ".zprofile",
                _HOME / ".zshenv",
                _HOME / ".zlogin",
                _HOME / ".zlogout",
            ],
        },
    ),
    "bash": AppConfig(
        name="bash",
        description="Bash Shell",
        paths={
            "macos": [
                _HOME / ".bashrc",
                _HOME / ".bash_profile",
                _HOME / ".bash_logout",
                _HOME / ".profile",
            ],
            "linux": [
                _HOME / ".bashrc",
                _HOME / ".bash_profile",
                _HOME / ".bash_logout",
                _HOME / ".profile",
            ],
        },
    ),
    "git": AppConfig(
        name="git",
        description="Git 版本控制",
        paths={
            "macos": [_HOME / ".gitconfig"],
            "linux": [_HOME / ".gitconfig"],
        },
    ),
    "ssh": AppConfig(
        name="ssh",
        description="SSH 客户端配置（仅 config 文件）",
        paths={
            "macos": [_HOME / ".ssh" / "config"],
            "linux": [_HOME / ".ssh" / "config"],
        },
    ),
    "alacritty": AppConfig(
        name="alacritty",
        description="Alacritty 终端模拟器",
        paths={
            "macos": [
                _HOME / ".config" / "alacritty" / "alacritty.toml",
                _HOME / ".config" / "alacritty" / "alacritty.yml",
            ],
            "linux": [
                _HOME / ".config" / "alacritty" / "alacritty.toml",
                _HOME / ".config" / "alacritty" / "alacritty.yml",
            ],
        },
    ),
    "kitty": AppConfig(
        name="kitty",
        description="Kitty 终端模拟器",
        paths={
            "macos": [_HOME / ".config" / "kitty"],
            "linux": [_HOME / ".config" / "kitty"],
        },
        is_dir=True,
    ),
    "wezterm": AppConfig(
        name="wezterm",
        description="WezTerm 终端模拟器",
        paths={
            "macos": [_HOME / ".config" / "wezterm" / "wezterm.lua"],
            "linux": [_HOME / ".config" / "wezterm" / "wezterm.lua"],
        },
    ),
    "fzf": AppConfig(
        name="fzf",
        description="Fzf 模糊搜索",
        paths={
            "macos": [
                _HOME / ".fzf.bash",
                _HOME / ".fzf.zsh",
            ],
            "linux": [
                _HOME / ".fzf.bash",
                _HOME / ".fzf.zsh",
            ],
        },
    ),
    "lazygit": AppConfig(
        name="lazygit",
        description="Lazygit TUI",
        paths={
            "macos": [_HOME / ".config" / "lazygit" / "config.yml"],
            "linux": [_HOME / ".config" / "lazygit" / "config.yml"],
        },
    ),
    "helix": AppConfig(
        name="helix",
        description="Helix 编辑器",
        paths={
            "macos": [_HOME / ".config" / "helix"],
            "linux": [_HOME / ".config" / "helix"],
        },
        is_dir=True,
    ),
    "fish": AppConfig(
        name="fish",
        description="Fish Shell",
        paths={
            "macos": [_HOME / ".config" / "fish"],
            "linux": [_HOME / ".config" / "fish"],
        },
        is_dir=True,
    ),
    "yazi": AppConfig(
        name="yazi",
        description="Yazi 文件管理器",
        paths={
            "macos": [_HOME / ".config" / "yazi"],
            "linux": [_HOME / ".config" / "yazi"],
        },
        is_dir=True,
    ),
}


def list_apps() -> list[str]:
    """返回所有已注册的应用名称（按字母序）."""
    return sorted(REGISTRY.keys())


def get_app(name: str) -> AppConfig | None:
    """根据名称获取应用配置定义."""
    return REGISTRY.get(name)
