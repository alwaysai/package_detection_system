from copy import deepcopy
import time

class PackageMonitor:
    def __init__(self):
        """This class enables a state machine system for package detection.
        """
        self.previous_packages = {}
        self.current_packages = {}
        self.person_detected = False
        self.packages_added = []
        self.packages_removed = []
        self.pending = False
        self.timer = time.time()
        self.rois = {}

    def set_packages(self, objects):
        """Sets previous packages to the current packages and
        sets the current packages to the input objects.

        Args:
            objects (dictionary): the object ID is the key 
        and the ObjectDetectionPrediction as the value.
        """
        self.previous_packages = deepcopy(self.current_packages)
        if len(objects) > 0:
            self.rois = deepcopy(objects)
        self.current_packages = deepcopy(objects)
        self.check_for_updates()

    def set_person(self, predictions):
        """Sets the 'person_detected' state; sets to True
        if predictions is not empty.

        Args:
            predictions (ObjectDetectionPrediction): Person detected if not empty.
        """
        self.person_detected = True if len(predictions) > 0 else False

    def get_count(self):
        """Returns the number of current packages.

        Returns:
            int: Number of items in the current_packages dictionary.
        """
        return len(self.current_packages)

    def get_current_packages(self):
        """Returns current package dictionary.

        Returns:
            dictionary: the object ID is the key 
        and the ObjectDetectionPrediction as the value.
        """
        return self.current_packages

    def action(self):
        """Checks the state of the system. Replace returned
        string with desired action items for customized system.

        Returns:
            string: A string description of the state.
        """
        action = "{}: ".format(time.asctime())
        if self.person_detected:
            action += "PERSON DETECTED.\n"
        else:
            action += "No person detected.\n"
        if self.pending:
            if time.time() - self.timer >= 5:
                # check for old ROIs 
                if not self.check_overlap():
                    # if packages have been removed, send alert
                    action += "SEND ALERT: packages removed.\n"
                    print(action) #printing this for demo purposes
                else:
                    action += "False alarm, packages are there.\n"
                    print(action) #printing this for demo purposes
                self.pending = False   
            else:
                return action       
        if len(self.packages_removed) > 0:
            self.pending = True
            self.timer = time.time()
            action += "PACKAGES MAY HAVE BEEN REMOVED\n"
            print(action) #printing this for demo purposes
        if len(self.packages_added) > 0:
            action += "More packages have arrived!\n"
            print(action) #printing this for demo purposes
        
        if len(self.packages_removed) == 0 and len(self.packages_added) == 0:
            action += "Nothing new here, waiting for packages. Package count is {}".format(self.get_count())

        return action

    def check_overlap(self):
        """Checks if new predictions match the last non-empty
        bounding boxes sufficiently. Helps avoid false alerts.

        Returns:
            boolean: True if all previous boxes have sufficient current overlap.
        """
        rois = [prediction.box for prediction in self.rois.values()]
        predictions = [prediction.box for prediction in self.current_packages.values()]
        
        for roi in rois:
            match = False
            for pred in predictions:
                if pred.compute_overlap(roi) > 0.9:
                    match = True
            if not match:
                return False

        return True

    def check_for_updates(self):
        """Updates state for new and missing packages.
        """
        self.packages_added = list(self.current_packages.keys() 
                                    - self.previous_packages.keys())
        self.packages_removed = list(self.previous_packages.keys() 
                                    - self.current_packages.keys())
    
    def package_is_detected(self):
        """Gives current count of packages

        Returns:
            int: number of packages detected
        """
        return len(self.current_packages) > 0

    def person_is_detected(self):
        """Returns person_detected property value.

        Returns:
            boolean: True if person_detected is True
        """
        return self.person_detected

    def remove_conflicting(self, person_results, package_results):
        """Removes package_results that overlap with person_results 
        (or whatever predictions are passed in to the function).

        Args:
            person_results (ObjectDetectionResult): results to remove
            package_results (ObjectDetectionResult): results to check

        Returns:
            ObjectDetectionPrediction: Predictions to keep
        """
        remove_packages = []

        for person in person_results.predictions:
            for package in package_results.predictions:
                if person.box.compute_overlap(package.box) > 0.6:
                    remove_packages.append(package)

        new_predictions = [p for p in package_results.predictions if p not in remove_packages]
        return new_predictions
