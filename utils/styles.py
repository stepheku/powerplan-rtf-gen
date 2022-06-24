from docx import Document
from docx.shared import Pt


def add_styles_to_doc(doc_obj: Document) -> Document:
    doc_obj.styles["Normal"].font.name = "Arial"
    doc_obj.styles["Normal"].font.size = Pt(10)
    doc_obj.styles["Normal"].paragraph_format.space_before = Pt(0)
    doc_obj.styles["Normal"].paragraph_format.space_after = Pt(0)
    return doc_obj


def add_bold_para_run_to_doc(doc_obj: Document, s: str) -> Document:
    """
    Adds a paragraph with a run that is bold, containing the string given to
    the Document object
    """
    p = doc_obj.add_paragraph("")
    p.add_run(s).bold = True
    return doc_obj