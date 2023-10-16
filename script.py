import numpy as np

def index_to_state(index, size):
    x_size, y_size, z_size = size
    return (index // (y_size * z_size)) + 1, (index % (y_size * z_size)) // z_size + 1, (index % z_size) + 1

def state_to_index(x, y, z, size):
    x_size, y_size, z_size = size
    return (x - 1) * (y_size * z_size) + (y - 1) * z_size + (z - 1)

def build_transition_matrix(size):
    x_size, y_size, z_size = size
    total_states = x_size * y_size * z_size
    P = np.zeros((total_states, total_states))
    
    for i in range(total_states):
        x, y, z = index_to_state(i, size)
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
                j = state_to_index(nx, ny, nz, size)
                P[i, j] = prob
                
    return P

def expected_steps_to_boundary(P, size, boundary_condition):
    x_size, y_size, z_size = size
    total_states = x_size * y_size * z_size
    E = np.zeros(total_states)
    
    for i in range(total_states - 1, -1, -1):
        x, y, z = index_to_state(i, size)
        
        if boundary_condition(x, y, z):
            continue
        
        E[i] = 1 + np.sum(P[i, :] * E)
        
    return E[state_to_index(1, 1, 1, size)]

# Example usage
size = (1, 5, 1)
boundary_condition = lambda x, y, z: y == 5
P = build_transition_matrix(size)
result = expected_steps_to_boundary(P, size, boundary_condition)
print(f"The expected number of steps to reach the boundary condition is approximately {result}")
