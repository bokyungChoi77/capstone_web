import qrcode

# QR 코드에 포함될 URL
url = "https://d2fa-223-195-58-115.ngrok-free.app"

# QR 코드 생성
qr = qrcode.make(url)

# 현재 디렉토리에 QR 코드 이미지 저장
qr.save("webpage_qr.png")
