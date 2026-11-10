# -*- coding: utf-8 -*-
"""
turkiye-yapay-zeka-araclari core paketi
"""
from .ai_client import AIClient, generate_response
from .prompt_templates import PROMPT_TEMPLATES, get_tool_prompt
from .udf_parser import parse_udf, read_udf_or_text, extract_udf_signers


SUPPORTED_LOCAL_MODELS_2026 = ['deepseek-ai/DeepSeek-V3', 'meta-llama/Llama-3.3-70B-Instruct', 'qwen/Qwen2.5-Coder-32B']
