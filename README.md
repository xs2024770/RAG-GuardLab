# RAG-GuardLab 🛡️

> 一个基于本地大模型的 RAG 间接提示注入（Indirect Prompt Injection）红队评测与防御验证平台。

## 📖 项目背景
随着 RAG（检索增强生成）架构的普及，**间接提示注入**成为了 OWASP LLM Top 10 中最危险的安全威胁之一。攻击者可以通过在知识库中投毒，从而劫持大模型的回答、泄露系统提示词，甚至执行越权操作。

本项目从零搭建了一套简易 RAG 系统，模拟 5 类真实攻击载荷，并验证了防御策略的有效性。

## 🏗️ 架构设计
`文档加载 -> BGE-M3 向量化 -> FAISS 检索 -> Ollama 生成 -> 防御过滤`

## 🧪 攻击与防御实验设计
- **攻击载荷**：构建了 5 类注入文档
  1. 越权读取 (`exfil`)
  2. 系统提示泄露 (`sysprompt`)
  3. 角色劫持 (`rolehijack`)
  4. 上下文污染 (`context_poison`)
  5. 编码隐藏 (`encoded`)
- **确定性判定**：每个攻击文档植入唯一 `CANARY-XXXX` 标识码，通过检测模型输出中是否包含该标识码来判定攻击是否成功。

## 📊 实验结果
| 测试阶段 | 模型 | ASR（攻击成功率） | 备注 |
| :--- | :--- | :--- | :--- |
| **基线测试** | Qwen2-7B | **20.0%** | 角色劫持攻击成功，模型输出了 CANARY 标识码 |
| **防御测试** | Qwen2-1.5B | **0.0%** | 启用指令隔离与输出过滤后，成功拦截注入 |
> **工程发现**：本地环境（8GB 显存）无法支持 7B 模型推理，实测中通过 `OLLAMA_NO_CUDA=1` 强制走 CPU 跑通全流程。模型规模越小，对复杂注入指令的“天然免疫力”越强，体现了模型能力与安全风险的博弈。
<table>
  <tr>
    <td width="50%"><img src="https://github.com/user-attachments/assets/0366cc52-2c99-42bb-afd3-357d51d3d587" alt="attack_result" width="100%"></td>
    <td width="50%"><img src="https://github.com/user-attachments/assets/f7374baf-f5e9-49cf-b538-b1069e63d8ca" alt="defense_result" width="100%"></td>
  </tr>
  <tr>
    <td align="center"><b>攻击测试 (ASR = 20%)</b></td>
    <td align="center"><b>防御测试 (ASR = 0%)</b></td>
  </tr>
</table>
## 🛡️ 防御策略
1. **指令隔离（Prompt Isolation）**：在 System Prompt 中明确标注检索材料为“不可信数据”，强制忽略材料中的指令。
2. **输出过滤（Output Filtering）**：对生成结果进行后处理，检测到 Canary 标识码或敏感词立即拦截。
