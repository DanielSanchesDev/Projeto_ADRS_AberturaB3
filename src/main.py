import os
import sys

# Adiciona o diretório 'src' ao PATH do Python para habilitar os imports
sys.path.insert(
    0, os.path.abspath(os.path.dirname(__file__))
)

from gui.app import CarteiraApp

if __name__ == "__main__":
    app = CarteiraApp()
    app.mainloop()