
import cv2
import numpy as np
import time

calibration_points = []


def mouse_callback(event, x, y, flags, param):
    """Select two points on a ruler."""
    if event == cv2.EVENT_LBUTTONDOWN and len(calibration_points) < 2:
        calibration_points.append((x, y))
        print(
            f"Calibration point {len(calibration_points)}: ({x}, {y})"
        )


def detect_gravity():
    global calibration_points

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Error: Could not open webcam.")
        return None

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    subtractor = cv2.createBackgroundSubtractorMOG2(
        history=300,
        varThreshold=35,
        detectShadows=False
    )

    print("\n=== PLANET SURVIVOR ===")
    print("Keep the camera stationary.")
    print("Keep the drop area clear while the background learns.")

    # Learn the empty background.
    for _ in range(60):
        ret, frame = camera.read()
        if not ret:
            camera.release()
            return None

        subtractor.apply(frame)

    # ---------------- CALIBRATION ----------------
    calibration_points = []
    window = "Planet Survivor - Calibration"

    cv2.namedWindow(window)
    cv2.setMouseCallback(window, mouse_callback)

    print("\n=== CALIBRATION ===")
    print("1. Place a ruler vertically in the drop area.")
    print("2. Click two marks on the ruler.")
    print("3. Press C to calculate their pixel distance.")
    print("4. Enter the known distance between the marks in cm.")
    print("Press Q to quit.")

    meters_per_pixel = None

    while True:
        ret, frame = camera.read()

        if not ret:
            camera.release()
            cv2.destroyAllWindows()
            return None

        display = frame.copy()

        # Draw the selected points.
        for point in calibration_points:
            cv2.circle(display, point, 6, (0, 255, 0), -1)

        if len(calibration_points) == 2:
            p1, p2 = calibration_points

            cv2.line(display, p1, p2, (0, 255, 0), 2)

            pixel_distance = abs(p2[1] - p1[1])

            cv2.putText(
                display,
                f"Vertical distance: {pixel_distance} pixels",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        cv2.putText(
            display,
            "Click 2 ruler marks, then press C",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 255),
            2
        )

        cv2.imshow(window, display)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            camera.release()
            cv2.destroyAllWindows()
            return None

        elif key == ord("c"):
            if len(calibration_points) != 2:
                print("Please click two ruler marks first.")
                continue

            p1, p2 = calibration_points

            # Automatically calculate vertical pixel distance.
            pixel_distance = abs(p2[1] - p1[1])

            if pixel_distance < 10:
                print("Choose two points farther apart vertically.")
                continue

            print(f"\nPixel distance: {pixel_distance} pixels")

            try:
                distance_cm = float(
                    input(
                        "Enter the actual distance between marks (cm): "
                    )
                )

                if distance_cm <= 0:
                    raise ValueError

            except ValueError:
                print("Enter a valid positive distance in centimeters.")
                continue

            # Convert centimeters to meters and calculate scale.
            meters_per_pixel = (
                (distance_cm / 100.0) / pixel_distance
            )

            print("\nCalibration successful!")
            print(f"Pixel distance: {pixel_distance} pixels")
            print(f"Actual distance: {distance_cm:.2f} cm")
            print(
                f"Scale: {meters_per_pixel:.6f} meters/pixel"
            )
            break

    cv2.destroyWindow(window)

    # ---------------- OBJECT TRACKING ----------------
    points = []
    tracking = False
    start_time = None
    duration = 1.5

    print("\n=== MEASUREMENT ===")
    print("Remove the ruler from the drop path.")
    print("Keep the camera in the same position.")
    print("Press SPACE, then release your object.")
    print("Press R to retry or Q to quit.")

    kernel = np.ones((5, 5), np.uint8)

    while True:
        ret, frame = camera.read()

        if not ret:
            break

        # Freeze background learning during tracking so the
        # falling object is less likely to disappear from the mask.
        if tracking:
            mask = subtractor.apply(frame, learningRate=0)
        else:
            mask = subtractor.apply(frame)

        mask = cv2.morphologyEx(
            mask, cv2.MORPH_OPEN, kernel
        )
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        candidates = [
            contour for contour in contours
            if cv2.contourArea(contour) > 40
        ]

        center = None

        if candidates:
            contour = max(candidates, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(contour)
            center = (x + w // 2, y + h // 2)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.circle(frame, center, 4, (0, 0, 255), -1)

        if tracking:
            elapsed = time.perf_counter() - start_time

            if center is not None:
                points.append((elapsed, center[1]))

            cv2.putText(
                frame,
                f"Time: {elapsed:.3f} s",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2
            )

            if elapsed >= duration:
                tracking = False
                print(f"Tracking finished: {len(points)} points captured.")

        cv2.putText(
            frame,
            "SPACE: Start | R: Reset | Q: Quit",
            (10, frame.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

        cv2.imshow("Planet Survivor - Object Tracker", frame)
        cv2.imshow("Motion Mask", mask)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        elif key == ord("r"):
            points = []
            tracking = False
            start_time = None
            print("Reset. Press SPACE to try again.")

        elif key == ord(" ") and not tracking:
            points = []
            tracking = True
            start_time = time.perf_counter()
            print("Release the object now!")

    camera.release()
    cv2.destroyAllWindows()

    # ---------------- GRAVITY CALCULATION ----------------
    if len(points) < 10:
        print("Not enough tracking points. Try again.")
        return None

    data = np.array(points, dtype=float)
    t = data[:, 0]
    y_pixels = data[:, 1]

    # Fit y = a*t^2 + b*t + c.
    a, b, c = np.polyfit(t, y_pixels, 2)

    # Image y increases downward, so positive acceleration
    # corresponds to downward motion.
    acceleration_pixels = 2 * a
    gravity = acceleration_pixels * meters_per_pixel

    fitted_y = np.polyval([a, b, c], t)
    residual = np.sqrt(np.mean((y_pixels - fitted_y) ** 2))

    print("\n=== GRAVITY RESULTS ===")
    print(f"Tracked points: {len(points)}")
    print(f"Estimated gravity: {gravity:.2f} m/s^2")
    print(f"Trajectory fit error: {residual:.2f} pixels")

    if gravity <= 0:
        print("Invalid result: tracking may not represent a falling object.")
    elif residual > 15:
        print("Warning: tracking was noisy. Repeat the experiment.")
    else:
        print("Gravity estimate obtained. Repeat to check consistency.")

    return gravity


if __name__ == "__main__":
    detect_gravity()
