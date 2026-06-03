# 出版商 PDF 适配器设计记录

> 本记录总结后续如需参考 `GAO-pooh/paper-scraper` 接入出版商 PDF 下载时的边界和设计原则。当前实现不启用这些适配器。

## 背景

当前文献阅读 Agent 已支持从 OpenAlex 元数据中识别开放 PDF URL，并通过 `scripts/download_pdfs.py` 下载开放获取 PDF。对于 ScienceDirect、INFORMS、Wiley、Springer、IEEE、ACM 等出版商平台，PDF 获取通常依赖机构订阅、浏览器登录态或出版商页面交互。

## 可参考的开源项目

- 项目：<https://github.com/GAO-pooh/paper-scraper>
- 可参考点：
  - ScienceDirect 使用浏览器环境和 Chrome DevTools Protocol 捕获 PDF 响应。
  - INFORMS 使用有效 session cookie 进行直接 HTTP 下载。
  - 保守限速、交互式登录、CSV/JSON/XLSX 元数据导出。

## 合规边界

- 不绕过 paywall。
- 不破解验证码、Cloudflare、防机器人机制或访问控制。
- 仅复用用户通过学校、机构或个人账号已经合法获得的访问权限。
- 默认关闭所有出版商适配器。
- 对无法合法自动获取的论文保留 `manual_required` 状态。

## 建议接口

```python
class PublisherAdapter:
    name: str

    def can_handle(self, record: dict) -> bool:
        return False

    def download(self, record: dict, output_path: Path) -> DownloadResult:
        raise NotImplementedError
```

## 建议启用条件

1. 用户明确确认具有对应出版商的合法访问权限。
2. `configs/sources.yaml` 中对应 adapter 的 `enabled` 改为 `true`。
3. adapter 保持限速，不批量高频请求。
4. 每次运行生成可审计日志。

## 暂不实现的内容

- 不实现 cookie 抽取。
- 不实现 Chrome DevTools Protocol 捕获。
- 不实现账号密码登录。
- 不实现任何规避检测或绕过访问控制的逻辑。
