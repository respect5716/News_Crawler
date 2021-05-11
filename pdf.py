import os
from fpdf import FPDF

class PDF(FPDF):
    def __init__(self, key):
        super(PDF, self).__init__()
        self.key = key
        self.add_font('kor', '', os.path.join(os.environ['CONFIG_DIR'], 'NanumBarunGothic.ttf'), uni=True)
        self.add_font('kor', 'B', os.path.join(os.environ['CONFIG_DIR'], 'NanumBarunGothicBold.ttf'), uni=True)
    
    def header(self):
        self.set_font('kor', 'B', 11)
        self.cell(80)
        self.cell(30, 10, self.key, 0, 0, 'C')
        self.ln(30) # Line break

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def write_title(self, title):
        self.set_font('kor', 'B', 14)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(4)

    def write_text(self, text):
        self.set_font('kor', '', 13)
        self.multi_cell(0, 5, text)
        self.ln()

    def write_news(self, title, text):
        self.add_page()
        self.write_title(title)
        self.write_text(text)
        
    def write(self, data):
        for idx, row in data.iterrows():
            self.write_news(row.title, row.text)
        self.output(f'{self.key}.pdf', 'F')