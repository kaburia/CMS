# Generate QR code to redirect to UI for conreols
from qrcode import QRCode, constants
import matplotlib.pyplot as plt

qr = QRCode(version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=20,
            border=2)

# Data to display
qr.add_data("SCAN TO ACCESS CONTROL")
qr.make(fit=True)

img = qr.make_image(fill_color='black', back_color='white')
img.save('qr.jpg')
plt.imshow(img)
plt.show()
