'''
-----------------------------------------------------------------------
File: latex_ops.py
Creation Time: Nov 24th 2023 3:29 am
Author: Saurabh Zinjad
Developer Email: zinjadsaurabh1997@gmail.com
Copyright (c) 2023 Saurabh Zinjad. All rights reserved | GitHub: Ztrimus
-----------------------------------------------------------------------
'''

import os
import jinja2
import streamlit as st
from zlm.utils.utils import write_file, save_latex_as_pdf

def escape_for_latex(data):
    if isinstance(data, dict):
        new_data = {}
        for key in data.keys():
            new_data[key] = escape_for_latex(data[key])
        return new_data
    elif isinstance(data, list):
        return [escape_for_latex(item) for item in data]
    elif isinstance(data, str):
        # Adapted from https://stackoverflow.com/q/16259923
        latex_special_chars = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\^{}",
            "\\": r"\textbackslash{}",
            "\n": "\\newline%\n",
            "-": r"{-}",
            "\xA0": "~",  # Non-breaking space
            "[": r"{[}",
            "]": r"{]}",
        }
        return "".join([latex_special_chars.get(c, c) for c in data])

    return data

def latex_to_pdf(json_resume, dst_path):
    try:
        module_dir = os.path.dirname(__file__)
        templates_path = os.path.join(os.path.dirname(module_dir), 'templates')

        st.write(f"module_dir: {module_dir}")
        st.write(f"templates_path: {templates_path}")

        latex_jinja_env = jinja2.Environment(
            block_start_string="\BLOCK{",
            block_end_string="}",
            variable_start_string="\VAR{",
            variable_end_string="}",
            comment_start_string="\#{",
            comment_end_string="}",
            line_statement_prefix="%-",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            loader=jinja2.FileSystemLoader(templates_path),
        )

        escaped_json_resume = escape_for_latex(json_resume)
        st.write(f"escaped_json_resume: {escaped_json_resume}")

        resume_latex = use_template(latex_jinja_env, escaped_json_resume)
        st.write(f"resume_latex")
        st.markdown("---")
        st.write(resume_latex)
        st.markdown("---")

        tex_temp_path = os.path.join(os.path.realpath(templates_path), os.path.basename(dst_path).replace(".pdf", ".tex"))
        st.write(f"tex_temp_path: {tex_temp_path}")

        write_file(tex_temp_path, resume_latex)
        st.write("wrote latex on tex_temp_path...")
        return save_latex_as_pdf(tex_temp_path, dst_path), resume_latex
    except Exception as e:
        print(e)
        return None

def use_template(jinja_env, json_resume):
    try:
        resume_template = jinja_env.get_template(f"resume.tex.jinja")
        resume = resume_template.render(json_resume)

        return resume
    except Exception as e:
        print(e)
        return None
