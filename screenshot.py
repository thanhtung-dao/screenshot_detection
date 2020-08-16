import os
import cv2


def get_continue_line(line, length, point_rate):
    output = 0
    max_points = int(length * point_rate)
    current = [-1, -1, -1]
    count = 0

    for point in line:
        point = point.tolist()
        if point != current:
            current = point
            if count >= max_points:
                output += count
            count = 1
        else:
            count += 1

    return output


def get_edge_info(image, edge, line_rate):
    assert edge in ['top', 'bottom', 'left', 'right'], "The edge must be 'top', 'bottom', 'left' or 'right'"
    height, width = image.shape[:2]
    if edge == 'top':
        length_range = int(line_rate * height)
        start_point = 0
        end_point = length_range
    elif edge == 'bottom':
        length_range = int(line_rate * height)
        start_point = height - length_range
        end_point = height
    elif edge == 'left':
        length_range = int(line_rate * width)
        start_point = 0
        end_point = length_range
    else:
        length_range = int(line_rate * width)
        start_point = width - length_range
        end_point = width

    return length_range, start_point, end_point


def check_screenshot(image, line_rate, edge):
    height, width = image.shape[:2]
    length_range, start_point, end_point = get_edge_info(image=image, edge=edge, line_rate=line_rate)
    count = 0
    for index in range(start_point, end_point):
        if edge == 'top' or edge == 'bottom':
            length_points = get_continue_line(line=image[index, :, :], length=width, point_rate=0.2)
            min_length = int(0.5 * width)
        else:
            length_points = get_continue_line(line=image[:, index, :], length=height, point_rate=0.2)
            min_length = int(0.5 * height)

        if length_points >= min_length:
            count += 1
    if (count / length_range) >= 0.5:
        return True
    
    return False


def check_image(image, line_rate):
    output = 'real image'
    height, width = image.shape[:2]
    if width > height:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    for edge in ['top', 'bottom', 'left', 'right']:
        result = check_screenshot(image=image, line_rate=line_rate, edge=edge)
        if result == True:
            output = 'screenshot image'

    return output


if __name__=='__main__':
    path = './Screenshot_20200816-065337.png'
    image = cv2.imread(path)
    result = check_image(image=image, line_rate=0.05)
    print(result)
