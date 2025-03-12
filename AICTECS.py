import cv2
import numpy as np

def text_to_image(message, output_path, width=400, height=400):
    message += "###"  # Delimiter to identify the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    total_pixels = width * height * 3
    if len(binary_message) > total_pixels:
        raise ValueError("Message is too long to encode in the generated image.")
    
    image = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
    data_index = 0
    
    for row in image:
        for pixel in row:
            for channel in range(3):  # BGR channels
                if data_index < len(binary_message):
                    pixel[channel] = np.uint8((pixel[channel] & ~1) | int(binary_message[data_index]))
                    data_index += 1
                else:
                    break
    
    cv2.imwrite(output_path, image)
    print(f"Message encoded successfully in {output_path}")

def image_to_text(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to read.")
    
    binary_data = ""
    for row in image:
        for pixel in row:
            for channel in range(3):
                binary_data += str(pixel[channel] & 1)
    
    binary_chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message = ''.join(chr(int(char, 2)) for char in binary_chars)
    
    if "###" in message:
        message = message[:message.index("###")]
        print("Decoded message:", message)
        return message
    else:
        raise ValueError("No hidden message found.")

if __name__ == "__main__":
    choice = input("Do you want to (E)ncode or (D)ecode? ").strip().lower()
    if choice == 'e':
        msg = input("Enter the message to hide: ").strip()
        output_img = "encoded_image.png"
        text_to_image(msg, output_img)
    elif choice == 'd':
        img_path = input("Enter the image path: ").strip()
        decoded_msg = image_to_text(img_path)
        print("Extracted Message:", decoded_msg)
    else:
        print("Invalid choice. Please enter 'E' or 'D'.")