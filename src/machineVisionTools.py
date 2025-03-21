import cv2

def zoomToCenter(image, zoom_factor):
    
    height, width = image.shape[:2]
    
    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)
    
    x1 = (width - new_width) // 2
    y1 = (height - new_height) // 2
    x2 = x1 + new_width
    y2 = y1 + new_height
    
    cropped = image[y1:y2, x1:x2]
    
    zoomed = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LINEAR)
    
    return zoomed