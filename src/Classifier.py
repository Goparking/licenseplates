from svmutil import svm_train, svm_problem, svm_parameter, svm_predict, \
        svm_save_model, svm_load_model


class Classifier:
    def __init__(self, c=None, gamma=None, filename=None):
        if filename:
            # If a filename is given, load a model from the given filename
            self.model = svm_load_model(filename)
        elif c == None or gamma == None:
            raise Exception('Please specify both C and gamma.')
        else:
            self.param = svm_parameter()
            self.param.kernel_type = 2  # Radial kernel type
            self.param.C = c  # Soft margin
            self.param.gamma = gamma  # Parameter for radial kernel
            self.model = None

    def save(self, filename):
        """Save the SVM model in the given filename."""
        svm_save_model(filename, self.model)

    def train(self, learning_set):
        """Train the classifier with a list of character objects that have
        known values."""
        classes = []
        features = []
        l = len(learning_set)

        for i, char in enumerate(learning_set):
            print 'Training "%s"  --  %d of %d (%d%% done)' \
                  % (char.value, i + 1, l, int(100 * (i + 1) / l))
            classes.append(float(ord(char.value)))
            features.append(char.get_feature_vector())

        problem = svm_problem(classes, features)
        self.model = svm_train(problem, self.param)

    def test(self, test_set):
        """Test the classifier with the given test set and return the score."""
        matches = 0

        for char in test_set:
            prediction = self.classify(char)

            if char.value == prediction:
                matches += 1

        return float(matches) / len(test_set)

    def classify(self, character):
        """Classify a character object, return its value."""
        predict = lambda x: svm_predict([0], [x], self.model)[0][0]
        prediction_class = predict(character.get_feature_vector())

        return chr(int(prediction_class))
