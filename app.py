# -*- coding: utf-8 -*-
"""Unipus 复制内容解密 —— 桌面版启动器。

把网页版工具（web/index.html）装进一个原生窗口里，方便打包成 exe 分发。
"""

from __future__ import annotations

import ctypes
import pathlib
import sys

import webview

APP_NAME = "Unipus 复制内容解密"
PREFERRED_WIDTH = 980
PREFERRED_HEIGHT = 900
MIN_SIZE = (520, 400)


def resource_path(*parts: str) -> pathlib.Path:
    """返回资源路径；PyInstaller 单文件模式下从临时解压目录读取。"""
    base = getattr(sys, "_MEIPASS", None)
    if base:
        return pathlib.Path(base).joinpath(*parts)
    return pathlib.Path(__file__).resolve().parent.joinpath(*parts)


def window_geometry() -> tuple[int, int, int, int]:
    """按屏幕缩放比例计算窗口大小和居中位置（单位：逻辑像素）。

    pywebview 的 width/height 使用逻辑像素；高分屏上如果直接写 980x900，
    窗口可能比屏幕还大。这里取屏幕逻辑尺寸的 92%/88%，并限制在首选值以内。
    """
    try:
        screen = webview.screens[0]
        scale = float(getattr(screen, "scale", 1.0) or 1.0)
        logical_width = float(screen.width) / scale
        logical_height = float(screen.height) / scale
    except Exception:
        logical_width, logical_height = 1280.0, 800.0

    width = max(MIN_SIZE[0], min(PREFERRED_WIDTH, int(logical_width * 0.92)))
    height = max(MIN_SIZE[1], min(PREFERRED_HEIGHT, int(logical_height * 0.92)))
    x = max(0, int((logical_width - width) / 2))
    y = max(0, int((logical_height - height) / 2))
    return width, height, x, y


def main() -> None:
    index = resource_path("web", "index.html")
    if not index.exists():
        ctypes.windll.user32.MessageBoxW(
            0,
            f"缺少页面文件：\n{index}\n\n请重新解压或重新打包。",
            APP_NAME,
            0x10,
        )
        return

    width, height, x, y = window_geometry()
    webview.create_window(
        APP_NAME,
        url=index.as_uri(),
        width=width,
        height=height,
        x=x,
        y=y,
        min_size=MIN_SIZE,
        background_color="#f5f7fa",
        text_select=True,
        zoomable=True,
    )

    try:
        webview.start(gui="edgechromium")
    except Exception as exc:  # WebView2 运行时缺失等
        ctypes.windll.user32.MessageBoxW(
            0,
            "程序启动失败：\n"
            f"{exc}\n\n"
            "本程序依赖 Microsoft Edge WebView2 运行时。\n"
            "Windows 10/11 一般已自带；如缺失，请安装：\n"
            "https://developer.microsoft.com/microsoft-edge/webview2/",
            APP_NAME,
            0x10,
        )
        raise


if __name__ == "__main__":
    main()