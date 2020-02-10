import sys
import io
import pdfrw
from reportlab.pdfgen import canvas


def main(argv):
    canvas_data = get_overlay_canvas(argv[1], argv[2])
    form = merge(canvas_data, template_path='./template.pdf')
    print(argv[0])
    vouch_list = argv[0]

    final = every_other(vouch_list, form)
    save(final, filename='merged.pdf')


def every_other(vouch_list: str, sign: io.BytesIO) -> io.BytesIO:
    v = pdfrw.PdfReader(vouch_list)
    pages = v.pages
    sign_page = pdfrw.PdfReader(sign).pages[0]
    writer = pdfrw.PdfWriter()

    for page in range(len(pages)):
        writer.addpage(pages[page])
        writer.addpage(sign_page)

    form = io.BytesIO()
    writer.write(form)
    form.seek(0)
    return form


def get_overlay_canvas(kassor, ordf) -> io.BytesIO:
    data = io.BytesIO()
    pdf = canvas.Canvas(data)
    pdf.setFont('Helvetica', 12)
    pdf.drawString(x=170, y=359, text=kassor)
    pdf.drawString(x=408, y=359, text=ordf)
    pdf.save()
    data.seek(0)
    return data


def merge(overlay_canvas: io.BytesIO, template_path: str) -> io.BytesIO:
    template_pdf = pdfrw.PdfReader(template_path)
    overlay_pdf = pdfrw.PdfReader(overlay_canvas)
    for page, data in zip(template_pdf.pages, overlay_pdf.pages):
        overlay = pdfrw.PageMerge().add(data)[0]
        pdfrw.PageMerge(page).add(overlay).render()
    form = io.BytesIO()
    pdfrw.PdfWriter().write(form, template_pdf)
    form.seek(0)
    return form


def save(form: io.BytesIO, filename: str):
    with open(filename, 'wb') as f:
        f.write(form.read())


if __name__ == "__main__":
    main(sys.argv[1:])
