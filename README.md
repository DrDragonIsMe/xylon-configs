# Xylon

跨平台 CLI 配置备份与还原工具，支持 macOS 与 Ubuntu/Linux。

## 支持的应用

| 应用 | 描述 | 类型 |
|------|------|------|
| ghostty | Ghostty 终端模拟器 | 文件 |
| starship | Starship 提示符 | 文件 |
| tmux | Tmux 终端复用器 | 文件 |
| nvim | Neovim 编辑器 | 目录 |
| zsh | Zsh Shell | 文件 |
| bash | Bash Shell | 文件 |
| git | Git 版本控制 | 文件 |
| ssh | SSH 客户端配置 | 文件 |
| alacritty | Alacritty 终端模拟器 | 文件 |
| kitty | Kitty 终端模拟器 | 目录 |
| wezterm | WezTerm 终端模拟器 | 文件 |
| fzf | Fzf 模糊搜索 | 文件 |
| lazygit | Lazygit TUI | 文件 |
| helix | Helix 编辑器 | 目录 |
| fish | Fish Shell | 目录 |
| yazi | Yazi 文件管理器 | 目录 |

## 安装

```bash
pip install -e .
```

或直接运行：

```bash
python -m xylon --help
```

## 使用

### 查看支持的应用

```bash
xylon list
```

### 查看状态

```bash
xylon status
```

### 备份

备份所有检测到的配置：

```bash
xylon backup
```

备份指定应用：

```bash
xylon backup nvim tmux starship
```

### 还原

还原所有仓库中的配置：

```bash
xylon restore
```

还原指定应用：

```bash
xylon restore nvim tmux
```

### 干运行

加上 `-n` / `--dry-run` 可预览操作而不实际执行：

```bash
xylon backup -n
xylon restore -n nvim
```

### 指定备份目录

```bash
xylon -s /path/to/configs backup
```

## 项目结构

```
xylon-configs/
├── xylon/            # Python 包
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py        # 命令行接口
│   ├── core.py       # 备份/还原核心逻辑
│   └── registry.py   # 应用配置路径注册表
├── configs/          # 默认备份仓库（git 追踪）
├── pyproject.toml
└── README.md
```

## 添加新应用

在 `xylon/registry.py` 的 `REGISTRY` 字典中添加 `AppConfig` 即可。例如：

```python
"myapp": AppConfig(
    name="myapp",
    description="My App",
    paths={
        "macos": [Path.home() / ".myapp" / "config"],
        "linux": [Path.home() / ".config" / "myapp" / "config"],
    },
),
```
