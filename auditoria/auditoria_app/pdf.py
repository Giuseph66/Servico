from fpdf import FPDF
from datetime import datetime

class PDF(FPDF):
    def __init__(self, data_i, data_f, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_i = data_i
        self.data_f = data_f

    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'NORTE SISTEMA', 0, 0, 'L')
        self.set_font('Arial', '', 8)
        self.cell(0, 10, f'EMISSÃO: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}', 0, 1, 'R')
        self.cell(0, 10, f'EMITIDO: {self.data_i} a {self.data_f}', 0, 1, 'L')
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'RELATÓRIO DA AUDITORIA', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'www.nortesistema.com.br -  (66)3199-0330', 0, 0, 'C')
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'R')

    def clean_text(self, text):
        return str(text).encode('latin-1', 'ignore').decode('latin-1')  

    def add_table_row(self, row_data):
        header = ["CNPJ", "Nome Fantasia", "Empresa", "Data", "Hora", "Código Usuário", "Operação", "Tabela", "Máquina", "Executável"]
        cell_widths = []
        max_cell_width = 40  
        max_total_width = 210 

        for header_text, item in zip(header, row_data):
            item_str = self.clean_text(str(item))
            max_width = min(max(self.get_string_width(item_str), self.get_string_width(self.clean_text(header_text))) + 4, max_cell_width)
            cell_widths.append(max_width)
        scale=1
        total_table_width = sum(cell_widths)
        if total_table_width > max_total_width:
            scale = max_total_width / total_table_width
            cell_widths = [width * scale for width in cell_widths]
            font_size = max(int(8 * scale), 6)  
            page_width = self.w - 2 * self.l_margin  
            x_offset = (page_width - (sum(cell_widths)*scale)) / 2  
        else:
            page_width = self.w - 2 * self.l_margin  
            x_offset = (page_width - (sum(cell_widths))) / 2  
            font_size = 8  
            
        if x_offset<-10:
            print(page_width,x_offset)
        self.set_x(self.l_margin + x_offset)
        self.set_font('Arial', 'B', font_size)
        for header_text, width in zip(header, cell_widths):
            self.cell(width*scale, 8, self.clean_text(header_text), border=1, align='C')
        self.ln()

        self.set_x(self.l_margin + x_offset)
        self.set_font('Arial', '', font_size)
        for item, width in zip(row_data, cell_widths):
            item_str = self.clean_text(str(item))
            self.cell(width*scale, 8, item_str, border=1, align='C')
        self.ln()
        
    def add_log_table(self, log_data):
        header = ["Campo", "Antigo", "Novo"]
        cell_widths = [50, 50, 50]  
        for i, header_text in enumerate(header):
            max_width = min(max(self.get_string_width(header_text) + 4, cell_widths[i]), cell_widths[i])
            cell_widths[i] = max_width

        total_table_width = sum(cell_widths)
        page_width = self.w - 2 * self.l_margin  
        x_offset = (page_width - total_table_width) / 2  
        self.set_x(self.l_margin + x_offset)
        self.set_font('Arial', 'B', 8)
        self.cell(sum(cell_widths), 8, "Alterações no Registro", border=1, align='C')
        self.ln()
        self.set_x(self.l_margin + x_offset)
        for i, header_text in enumerate(header):
            self.cell(cell_widths[i], 8, self.clean_text(header_text), border=1, align='C')
        self.ln()

        self.set_font('Arial', '', 7)
        for log in log_data:
            self.set_x(self.l_margin + x_offset)
            for i, key in enumerate(["name", "old", "new"]):
                self.cell(cell_widths[i], 8, self.clean_text(log.get(key, "")), border=1, align='C')
            self.ln()
        self.ln(5)
        
    def add_table(self, dados):
        for index, row in dados.iterrows():
            main_row = [
                row['cpfCnpj'], row['fantasia'], row['empresa'],
                row['data'], row['hora'], row['usuCodigo'], row['operacao'],
                row['tabela'], row['maquina'], row['executavel']
            ]
            self.add_table_row(main_row)
            log_data = eval(row['log'])
            self.add_log_table(log_data)
            self.ln(5)
