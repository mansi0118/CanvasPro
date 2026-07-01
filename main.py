import cv2
import numpy as np
from hand_tracker import HandTracker
import math


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
success, frame = cap.read()
frame = cv2.flip(frame, 1)
h , w, c = frame.shape
tracker = HandTracker()

prev_x = 0
prev_y = 0
smooth_x = 0
smooth_y = 0
alpha = 0.2 # control smoothness

drawing = False

current_color = (255,0,255) # default color is magenta
cv2.namedWindow("Canvas Pro", cv2.WINDOW_NORMAL)
cv2.setWindowProperty(
    "Canvas Pro",
    cv2.WND_PROP_FULLSCREEN,
    cv2.WINDOW_FULLSCREEN
)

brush_size = 12
# STARTUP SCREEN
pulse = 0 # track animation progression
while True:
    pulse += 0.08 # control animation speed
    glow = int (150 + 105 * math.sin(pulse)) # calculate glow intensity(45->255)
    start_screen = np.zeros((h, w, 3), dtype=np.uint8)

    # Title
    cv2.putText(
        start_screen,
        "CANVAS PRO",
        (w//2 - 260, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        2.5,
        (255,0,255),
        5,
        cv2.LINE_AA
    )

    # Instructions
    instructions = [
        "INDEX FINGER  = DRAW",
        "TWO FINGERS   = ERASE",
        "OPEN HAND     = NAVIGATION",
        "S = SAVE    |    Z = UNDO |    Q/ESC = QUIT"
    ]

    y = 320

    for text in instructions:

        cv2.putText(
            start_screen,
            text,
            (w//2 - 320, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2,
            cv2.LINE_AA
        )

        y += 50

    # Start Message
    cv2.putText(
        start_screen,
        "PRESS SPACE TO START",
        (w//2 - 280, h - 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, glow//3, 0),
        8,
        cv2.LINE_AA
    )
    cv2.putText(
        start_screen,
        "PRESS SPACE TO START",
        (w//2 - 280, h - 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0,glow,0),
        3,
        cv2.LINE_AA
    )

    cv2.imshow("Canvas Pro", start_screen)

    key = cv2.waitKey(1)

    # Start App
    if key == 32:
        break

    # Quit App
    if key == ord('q') or key == 27:
        cap.release()
        cv2.destroyAllWindows()
        exit()

erasing = False

#saving file variables
save_count = 1
save_message = ""
save_message_timer = 0
save_pressed = False 

# for undo
canvas_history = []

# for dynamic background
theme = "black"
background_color = (0,0,0)
canvas = np.full(
    (h,w,c),
    background_color,
    dtype=np.uint8
)
while True:

    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame, landmarks = tracker.find_hands(frame)
    mode_text = "NO HAND DETECTED"
    mode_color = (0,0,255)
    if landmarks:
        index_finger = landmarks[8]
        middle_finger = landmarks[12]
        ring_finger = landmarks[16]
        pinky_finger = landmarks[20]

        index_joint = landmarks[6]
        middle_joint = landmarks[10]
        ring_joint = landmarks[14]
        pinky_joint = landmarks[18]
        
        index_up = index_finger[2] < index_joint[2]

        middle_up = middle_finger[2] < middle_joint[2]

        ring_up = ring_finger[2] < ring_joint[2]

        pinky_up = pinky_finger[2] < pinky_joint[2]
        index_pos = (index_finger[1], index_finger[2])
        smooth_x = int(alpha * index_pos[0] + (1 - alpha) * smooth_x)
        smooth_y = int(alpha * index_pos[1] + (1 - alpha) * smooth_y)
        index_pos = (smooth_x, smooth_y)
        
        # HSV COLOR BAR
        for i in range(360):

            hue = int(i / 2)

            hsv_color = np.uint8([[[hue, 255, 255]]])

            bgr_color = cv2.cvtColor(
                hsv_color,
                cv2.COLOR_HSV2BGR
            )[0][0]

            cv2.line(
                frame,
                (40, i + 100),
                (100, i + 100),
                (
                    int(bgr_color[0]),
                    int(bgr_color[1]),
                    int(bgr_color[2])
                ),
                2
            )
        # SELECT COLOR FROM BAR
        if 40 < index_pos[0] < 100 and not drawing:

            if 100 < index_pos[1] < 460:

                selected_y = index_pos[1] - 100

                hue = int(selected_y / 2)

                hsv_color = np.uint8([[[hue, 255, 255]]])

                bgr_color = cv2.cvtColor(
                    hsv_color,
                    cv2.COLOR_HSV2BGR
                )[0][0]

                current_color = (
                    int(bgr_color[0]),
                    int(bgr_color[1]),
                    int(bgr_color[2])
                )
        # CURRENT COLOR PREVIEW
        cv2.rectangle(
            frame,
            (30, 20),
            (110, 80),
            current_color,
            -1
        )

        cv2.rectangle(
            frame,
            (30, 20),
            (110, 80),
            (255,255,255),
            2
        )
        # clear canvas button   
        cv2.rectangle(frame, (500, 20), (650, 80), (50, 50, 50), -1)

        cv2.putText(
            frame,
            "CLEAR",
            (520, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            2
        )
        # Minus button
        cv2.rectangle(frame, (700, 20), (760, 80), (70,70,70), -1)

        cv2.putText(
            frame,
            "-",
            (722, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255,255,255),
            3
        )

        # Brush size text
        cv2.rectangle(frame, (770, 20), (930, 80), (40,40,40), -1)

        cv2.putText(
            frame,
            f"Brush: {brush_size}",
            (785, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )

        # Plus button
        cv2.rectangle(frame, (940, 20), (1000, 80), (70,70,70), -1)

        cv2.putText(
            frame,
            "+",
            (955, 65),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255,255,255),
            3
        )

        if 500 < index_pos[0] < 650 and index_pos[1] < 80 and not drawing:  # clean canvas button
            canvas[:] = background_color # set every pixel to black

        # Decrease brush size
        if 700 < index_pos[0] < 760 and 20 < index_pos[1] < 80 and not drawing:
            brush_size = max(2, brush_size - 1)


        # Increase brush size
        if 940 < index_pos[0] < 1000 and 20 < index_pos[1] < 80 and not drawing:
            brush_size = min(50, brush_size + 1)

         # Draw only when ONLY index finger is up
        if index_up and not middle_up and not ring_up and not pinky_up:

            drawing = True
            erasing = False
        elif index_up and middle_up and not ring_up and not pinky_up:

            drawing = False
            erasing = True
            
        else:

            drawing = False
            erasing = False
            prev_x, prev_y = 0, 0
        
        if drawing:   # drawing mode
            mode_text = "DRAW MODE"
            mode_color = (0,255,0)
            cv2.circle(frame, index_pos, 25, current_color, -1)

            if prev_x == 0 and prev_y == 0:
            
                # Save current canvas state
                canvas_history.append(canvas.copy())

                # Limit history size
                if len(canvas_history) > 20:

                    canvas_history.pop(0)

                prev_x, prev_y = index_pos

            cv2.line(
                canvas,
                (prev_x, prev_y),
                index_pos,
                current_color,
                brush_size*2,
                cv2.LINE_AA
            )
            cv2.line(
                canvas,
                (prev_x, prev_y),
                index_pos,
                current_color,
                brush_size,
                cv2.LINE_AA
            )
            prev_x, prev_y = index_pos

        elif erasing:
            mode_text = "ERASE MODE"
            mode_color = (255,255,255)
            cv2.circle(  # eraser outline cursor
                frame,
                index_pos,
                brush_size * 2,
                mode_color,
                3,
                cv2.LINE_AA
            )

            if prev_x == 0 and prev_y == 0:

                prev_x, prev_y = index_pos

            cv2.line(
                canvas,
                (prev_x, prev_y),
                index_pos,
                background_color,
                brush_size * 3,
                cv2.LINE_AA
            )

            prev_x, prev_y = index_pos

        else:
            mode_text = "NAVIGATION MODE"
            mode_color = (0, 165, 255)
            cv2.circle(frame, index_pos, 15, mode_color , -1)
    output = canvas.copy()
    # GRID THEME
    if theme == "grid":

        for x in range(0, w, 40):

            cv2.line(
                output,
                (x,0),
                (x,h),
                (50,50,50),
                1
            )

        for y in range(0, h, 40):

            cv2.line(
                output,
                (0,y),
                (w,y),
                (50,50,50),
                1
            )
    small_frame = cv2.resize(frame, (320, 180))
    output[20:200, w-340:w-20] = small_frame
    # Mode Panel Background
    cv2.rectangle(
        output,
        (w-340, 220),
        (w-20, 290),
        (25,25,25),
        -1
    )

    # Mode Panel Border
    cv2.rectangle(
        output,
        (w-340, 220),
        (w-20, 290),
        mode_color,
        5
    )

    # Mode Text
    cv2.putText(
        output,
        mode_text,
        (w-315, 268),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        mode_color,
        2,
        cv2.LINE_AA
    )
    # THEME SHORTCUT PANEL
    cv2.rectangle(
        output,
        (w-340, 310),
        (w-20, 455),
        (25,25,25),
        -1
    )

    cv2.rectangle(
        output,
        (w-340, 310),
        (w-20, 455),
        (120,120,120),
        2
    )

    themes = [
        "1 - BLACK",
        "2 - WHITEBOARD",
        "3 - GRID",
        "4 - BLUE"
    ]

    theme_y = 345

    for theme_text in themes:

        cv2.putText(
            output,
            theme_text,
            (w-315, theme_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2,
            cv2.LINE_AA
        )

        theme_y += 28
    # SAVE NOTIFICATION
    if save_message_timer > 0:

        cv2.rectangle(
            output,
            (w//2 - 180, 40),
            (w//2 + 180, 110),
            (40,40,40),
            -1
        )

        cv2.rectangle(
            output,
            (w//2 - 180, 40),
            (w//2 + 180, 110),
            (0,255,0),
            3
        )

        cv2.putText(
            output,
            save_message,
            (w//2 - 140, 87),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            3,
            cv2.LINE_AA
        )

        save_message_timer -= 1
    cv2.imshow("Canvas Pro", output)
    key = cv2.waitKey(1)
    # save canvas when 's' is pressed
    if key == ord('s') or key == ord('S') and not save_pressed:

        filename = f"screenshots/drawing_{save_count}.png"

        cv2.imwrite(filename, canvas)

        save_message = "IMAGE SAVED"

        save_message_timer = 60

        save_count += 1

        save_pressed = True

    if key != ord('s'):

        save_pressed = False

    # UNDO
    if key == ord('z'):

        if len(canvas_history) > 0:

            canvas = canvas_history.pop()

            save_message = "UNDO"

            save_message_timer = 40    
    # BLACK THEME
    if key == ord('1'):

        theme = "black"

        background_color = (0,0,0)

        canvas[:] = background_color


    # WHITEBOARD THEME
    if key == ord('2'):

        theme = "white"

        background_color = (255,255,255)

        canvas[:] = background_color


    # GRID THEME
    if key == ord('3'):

        theme = "grid"

        background_color = (30,30,30)

        canvas[:] = background_color


    # DARK BLUE THEME
    if key == ord('4'):

        theme = "blue"

        background_color = (40,20,0)

        canvas[:] = background_color
    if key == ord('q') or key == 27:  # 'q' or 'ESC' to quit
        break


cap.release()
cv2.destroyAllWindows()