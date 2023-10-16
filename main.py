import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout

# 计算函数
def calculate_expected_steps(x_size, y_size, z_size, boundary_y):
    total_states = x_size * y_size * z_size
    P = np.zeros((total_states, total_states))

    def index_to_state(index):
        return (index // (y_size * z_size)) + 1, (index % (y_size * z_size)) // z_size + 1, (index % z_size) + 1

    def state_to_index(x, y, z):
        return (x - 1) * (y_size * z_size) + (y - 1) * z_size + (z - 1)

    for i in range(total_states):
        x, y, z = index_to_state(i)
        next_states = []

        if x < x_size:
            next_states.append((x + 1, y, z))
        if y < y_size:
            next_states.append((x, y + 1, z))
        if z < z_size:
            next_states.append((x, y, z + 1))
        
        if len(next_states) > 0:
            prob = 1 / len(next_states)
            for nx, ny, nz in next_states:
                j = state_to_index(nx, ny, nz)
                P[i, j] = prob

    E = np.zeros(total_states)
    for i in range(total_states - 1, -1, -1):
        x, y, z = index_to_state(i)
        if y == boundary_y:
            continue
        E[i] = 1 + np.sum(P[i, :] * E)

    return E[state_to_index(1, 1, 1)]

# GUI
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Expected Steps Calculator')

layout = QVBoxLayout()

x_label = QLabel('Enter X size:')
layout.addWidget(x_label)
x_input = QLineEdit()
layout.addWidget(x_input)

y_label = QLabel('Enter Y size:')
layout.addWidget(y_label)
y_input = QLineEdit()
layout.addWidget(y_input)

z_label = QLabel('Enter Z size:')
layout.addWidget(z_label)
z_input = QLineEdit()
layout.addWidget(z_input)

boundary_label = QLabel('Enter boundary Y:')
layout.addWidget(boundary_label)
boundary_input = QLineEdit()
layout.addWidget(boundary_input)

result_label = QLabel('Result:')
layout.addWidget(result_label)

def on_calculate():
    x_size = int(x_input.text())
    y_size = int(y_input.text())
    z_size = int(z_input.text())
    boundary_y = int(boundary_input.text())
    result = calculate_expected_steps(x_size, y_size, z_size, boundary_y)
    result_label.setText(f'Result: {result}')

calculate_button = QPushButton('Calculate')
calculate_button.clicked.connect(on_calculate)
layout.addWidget(calculate_button)

window.setLayout(layout)
window.show()
sys.exit(app.exec_())
