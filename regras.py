import layout
import self
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout


class RulesWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Regras de Apostas")

        layout = QVBoxLayout()
        layout.addWidget(QLabel(
            "• Se um apostador acertar apenas o vencedor do jogo (time da casa ou time visitante), ele receberá 50% do valor da aposta como prêmio, somado ao valor apostado."))
        layout.addWidget(QLabel(
            "• Se um apostador acertar tanto o vencedor do jogo quanto o placar correto, ele receberá o valor apostado como prêmio, somado a 100% desse valor."))
        layout.addWidget(
            QLabel("\nO sistema exibirá o nome do apostador vencedor, o valor da aposta acertada e o prêmio recebido."))

        self.setLayout(layout)



# Implemente a função 'mostrar_regras'
def mostrar_regras(self):
    self.rules_window = RulesWindow()
    self.rules_window.show()
