import numpy as np
from scipy.special import zeta
from scipy.special import loggamma

def compute_hardy_z(t_array):
    """
    Evaluates Hardy's Z-function for an array of imaginary parts
    along the critical line Re(s) = 0.5.
    """
    z_values = []
    for t in t_array:
        s = 0.5 + 1j * t
        complex_zeta = zeta(s)
        
        # Calculate the Riemann-Siegel theta phase angle accurately
        log_gamma_phase = loggamma(0.25 + 0.5j * t)
        theta = log_gamma_phase.imag - (t / 2.0) * np.log(np.pi)
        
        # Rotational transformation to project complex values onto the real axis
        z = np.exp(1j * theta) * complex_zeta
        z_values.append(z.real)
        
    return np.array(z_values)

# Define evaluation domain
t_domain = np.linspace(0, 50, 1000)
hardy_data = compute_hardy_z(t_domain)
print(f"Hardy Z-function data computed successfully. Total points: {len(hardy_data)}")