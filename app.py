import time
import edgeiq
from package_monitor import PackageMonitor
"""
Monitor an area for packages and people and respond when packages have
been removed from the area.
"""


def main():
    # First make a detector to detect packages objects
    # !! You'll need to replace this with your own model. See README.md !!
    package_detector = edgeiq.ObjectDetection(
            "testuser/package_detector")
    package_detector.load(engine=edgeiq.Engine.DNN)

    # Then make a detector to detect people
    person_detector = edgeiq.ObjectDetection("alwaysai/mobilenet_ssd")
    person_detector.load(engine=edgeiq.Engine.DNN)

    # add a centroid tracker to see if a new package arrives
    centroid_tracker = edgeiq.CentroidTracker(
                                deregister_frames=10, max_distance=50)

    # Descriptions printed to console
    print("Engine: {}".format(package_detector.engine))
    print("Accelerator: {}\n".format(package_detector.accelerator))
    print("Model:\n{}\n".format(package_detector.model_id))
    print("Labels:\n{}\n".format(package_detector.labels))

    print("Engine: {}".format(person_detector.engine))
    print("Accelerator: {}\n".format(person_detector.accelerator))
    print("Model:\n{}\n".format(person_detector.model_id))
    print("Labels:\n{}\n".format(person_detector.labels))

    fps = edgeiq.FPS()

    # Variables to limit inference
    counter = 0
    DETECT_RATE = 10

    # Object to monitor the system
    pm = PackageMonitor()

    try:
        with edgeiq.WebcamVideoStream(cam=1) as video_stream, \
                edgeiq.Streamer() as streamer:

            # Allow Webcam to warm up
            time.sleep(2.0)
            fps.start()

            # Loop detection
            while True:
                counter += 1

                # Run this loop whenever there's a package detected or every DETECT_RATE frames
                if pm.package_is_detected() or counter % DETECT_RATE == 0:

                    # Read in the video stream
                    frame = video_stream.read()

                    # Check for packages in the new frame
                    package_results = package_detector.detect_objects(
                            frame, confidence_level=.90)

                    # update the package predictions
                    objects = centroid_tracker.update(package_results.predictions)
                    pm.set_packages(objects)

                    # Once a package is detected, check for people also
                    if pm.package_is_detected():
                        person_results = person_detector.detect_objects(
                                frame, confidence_level=0.5)

                        person_predictions = edgeiq.filter_predictions_by_label(
                                person_results.predictions, ['person'])

                        frame = edgeiq.markup_image(
                                frame, person_predictions, show_labels=True, line_thickness=3,
                                font_size=1, font_thickness=3, show_confidences=False,
                                colors=[(0, 0, 255)])

                        pm.set_person(person_predictions)

                        # remove packages that might actually be people
                        package_predictions = pm.remove_conflicting(
                                person_results, package_results)
                        package_results = edgeiq.ObjectDetectionResults(
                                package_predictions, package_results.duration, frame)

                    # Generate labels to display the face detections on the streamer
                    text = ["Model: {}".format("alwaysai/package_detector")]
                    text.append(
                            "Inference time: {:1.3f} s".format(package_results.duration))

                    predictions = []

                    # update labels for each identified package to print to the screen
                    for (object_id, prediction) in objects.items():
                        new_label = 'Package {}'.format(object_id)
                        prediction.label = new_label
                        text.append(new_label)
                        predictions.append(prediction)

                    # Alter the original frame mark up to show tracking labels
                    frame = edgeiq.markup_image(
                            frame, predictions,
                            show_labels=True, show_confidences=False,
                            line_thickness=3, font_size=1, font_thickness=3)

                    # Do some action based on state
                    text.append(pm.action())

                    # Send the image frame and the predictions to the output stream
                    streamer.send_data(frame, text)

                    fps.update()

                    if streamer.check_exit():
                        break

    finally:
        fps.stop()
        print("elapsed time: {:.2f}".format(fps.get_elapsed_seconds()))
        print("approx. FPS: {:.2f}".format(fps.compute_fps()))

        print("Program Ending")


if __name__ == "__main__":
    main()
