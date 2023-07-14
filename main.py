import sqlite3
import random
from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox, QWidget, QApplication, QPushButton, QLineEdit, QLabel
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt

# Criação da base de dados em memória
conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute("""CREATE TABLE apostas (
            nome TEXT,
            time_casa TEXT,
            time_visitante TEXT,
            valor_aposta INTEGER,
            gols_casa INTEGER,
            gols_visitante INTEGER
            )""")


class App(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cadastro de Apostas")
        self.setGeometry(100, 100, 800, 400)

        self.create_form()
        self.show()

    def create_form(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Formulário de aposta
        self.nome = self.create_line_edit(layout, 'Nome do apostador')
        self.time_casa = self.create_line_edit(layout, 'Time da casa')
        self.time_visitante = self.create_line_edit(layout, 'Time visitante')
        self.valor_aposta = self.create_line_edit(layout, 'Valor da aposta', True)
        self.gols_casa = self.create_line_edit(layout, 'Gols do time da casa', True)
        self.gols_visitante = self.create_line_edit(layout, 'Gols do time visitante', True)


        # Botões
        self.create_button(layout, 'Cadastrar Aposta', self.cadastrar_aposta)
        self.create_button(layout, 'Verificar Apostas', self.verificar_apostas)


        # Tabela de apostas
        self.table = QTableWidget(0, 7) # Alterei para 7 para adicionar uma nova coluna
        self.table.setHorizontalHeaderLabels(['Nome', 'Time da Casa', 'Time Visitante', 'Valor da Aposta', 'Gols da Casa', 'Gols Visitante', 'Ganhos']) # Adicionei 'Ganhos'
        layout.addWidget(self.table)

        central_widget.setLayout(layout)

    def create_line_edit(self, layout, label, is_number=False):
        layout.addWidget(QLabel(label))
        line_edit = QLineEdit()
        if is_number:
            line_edit.setValidator(QIntValidator(0, 99999999))
        layout.addWidget(line_edit)
        return line_edit

    def create_button(self, layout, label, callback):
        button = QPushButton(label)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def cadastrar_aposta(self):
        nome = self.nome.text()
        time_casa = self.time_casa.text()
        time_visitante = self.time_visitante.text()
        valor_aposta = self.valor_aposta.text()
        gols_casa = self.gols_casa.text()
        gols_visitante = self.gols_visitante.text()

        # Verifica se todos os campos estão preenchidos
        if not all([nome, time_casa, time_visitante, valor_aposta, gols_casa, gols_visitante]):
            QMessageBox.warning(self, 'Aviso', 'Todos os campos são obrigatórios.')
            return

        # Adiciona a aposta à tabela
        self.table.insertRow(self.table.rowCount())
        self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(nome))
        self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(time_casa))
        self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(time_visitante))
        self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(valor_aposta))
        self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem(gols_casa))
        self.table.setItem(self.table.rowCount() - 1, 5, QTableWidgetItem(gols_visitante))

        c.execute("INSERT INTO apostas VALUES (:nome, :time_casa, :time_visitante, :valor_aposta, :gols_casa, :gols_visitante)",
                  {'nome': nome, 'time_casa': time_casa, 'time_visitante': time_visitante, 'valor_aposta': valor_aposta, 'gols_casa': gols_casa, 'gols_visitante': gols_visitante})

        conn.commit()

    def gerar_placar(self):
        gols_casa = random.randint(0, 5)
        gols_visitante = random.randint(0, 5)

        placar = {
            "time_casa": gols_casa,
            "time_visitante": gols_visitante
        }

        return placar

    def validar_vencedor(self, placar):
        if placar['time_casa'] > placar['time_visitante']:
            return "time_casa"
        elif placar['time_visitante'] > placar['time_casa']:
            return "time_visitante"
        else:
            return "empate"

    def validar_vencedor(self, placar):
        if placar['time_casa'] > placar['time_visitante']:
            return "time_casa"
        elif placar['time_visitante'] > placar['time_casa']:
            return "time_visitante"
        else:
            return "empate"

    def verificar_apostas(self):
        placar = self.gerar_placar()
        vencedor = self.validar_vencedor(placar)

        QMessageBox.information(self, 'Resultado',
                                f"Placar final: Casa {placar['time_casa']} x {placar['time_visitante']} Visitante")

        c.execute("SELECT * FROM apostas")
        apostas = c.fetchall()

        for index, aposta in enumerate(apostas):
            premio = 0
            aposta_vencedor = None
            if aposta[4] > aposta[5]:
                aposta_vencedor = "time_casa"
            elif aposta[5] > aposta[4]:
                aposta_vencedor = "time_visitante"

            acertou_vencedor = aposta_vencedor == vencedor
            acertou_placar = aposta[4] == placar['time_casa'] and aposta[5] == placar['time_visitante']

            if acertou_vencedor and acertou_placar:
                premio = aposta[3] * 2
                QMessageBox.information(self, 'Resultado',
                                        f"Aposta vencedora: {aposta[0]} acertou o vencedor e o placar! Prêmio: {premio}")
            elif acertou_vencedor:
                premio = aposta[3] * 1.5
                QMessageBox.information(self, 'Resultado',
                                        f"Aposta vencedora: {aposta[0]} acertou apenas o vencedor! Prêmio: {premio}")

            self.table.setItem(index, 6, QTableWidgetItem(str(premio)))  # Adiciona o valor de ganhos na tabela


app = QApplication([])
window = App()
app.exec_()
conn.close()
