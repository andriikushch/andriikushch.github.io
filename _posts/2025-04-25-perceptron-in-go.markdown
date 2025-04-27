---
layout: post
title:  "Perceptron in Go"
date:   2025-04-25 12:00:09 +0200
categories: posts
permalink: /:collection/:title
---

## What is it all about

Imagine we have two categories, like “yes” and “no,” “good” and “bad,” etc. We are also given a set of items and their affiliation to these classes.

![points_plot.png](/assets/images/7/points_plot.png)

We want to find a way to determine whether any new point belongs to one or another class. In other words, we want to classify it; therefore, we need a classifier.

What can be a classifier in that case? If we look at the image above, these two classes are linearly separable. We can imagine a straight line that separates these two sets, going from the top left corner to the bottom right.

If we have such a line, we can assume that all new points above the line belong to class 1 and below to class 0. This line can then be called a linear classifier.

This problem can be easily solved with a pen and ruler, of course, assuming that we are dealing with a two-dimensional space. But what if items in our set have more than two properties on which we base our decision?

For simplicity, in our example, we use items with only two features: their x and y coordinates. But let's use our imagination for a second and replace these abstract items with "houses". The features can then represent buying and maintenance prices, for example. In this case, two dimensions are enough. But what if we want to add size, age, number of parking lots, etc., to the list? We may need to add one more dimension to our plot for every new feature, and having more than three will be pretty hard to visualize. In that case, a pencil and ruler won't work well.

Nevertheless, until two classes are separable with a line, plane, or hyperplane, we can try using Perceptron to build the classifier for us.


## What is Perceptron

Perceptron is a model, which sounds pretty abstract. It can be a formula or computer program that, given an item represented as a set of numbers, answers the question: "Does the input belong to one or another class?"

But how does it know the answer?

Perceptron decides based on the configuration, which consists of `weights` and `bias`. 

Weights define how important a particular feature is for the final decision. Let's think about our example with houses. We can imagine a situation where the price is a deal-breaker for us, and it is far more important than having more parking lots. But how much is it more valuable? And how is its importance comparable with the number of bathrooms? We can answer this question by looking at the particular weight value. 

Bias shifts the decision boundary. We can explain bias graphically. For the line on the image above, weights are responsible for the angle, and a bias is for how high or low this line goes. The line will always go through the (0,0) point without it.

How can we find the proper configuration for the Perceptron? We can try to guess it or calculate manually, but it can be challenging and error-prone. Luckily, a perceptron algorithm allows us to derive it from the already labeled set.

## Training process

The concept behind the training process can be very straightforward:

1. We start with all weights set to 1 and bias to 0. We have already defined the model. Now we will try to improve it.
2. In the loop, we are doing the following:
   1. Checking how well our model matches the set. We can measure this by calculating the prediction error.
   2. We take a random item from our set and try to move our classification boundary (for 2D cases, it is a line) closer to that point.

## Hyperparameters

Before we start training, we need to provide two more parameters called hyperparameters. In our case, they are `epoch` and `learning rate`.

### Epoch 

This parameter defines how many iterations our loop will have before it stops. Theoretically, we could stop when the error that we calculate on each iteration is 0, but it won't work if classes are not perfectly separable. We can build a quite good model in that case, but some errors may always be present.

### Learning rate

The learning rate controls how aggressively we update our weights and how close we move our classification boundary to the item on each step. If it is too high, our model might not converge because it will try to match perfectly each individual item on every iteration, but it won't necessarily improve the overall model. Having it too small, will require more epochs and consequentially more time.

## Perceptron implementation in Go

Let's write a simple perceptron implementation in Go.

### Define the Perceptron type

First of all, let's define the Perceptron type and its constructor to set initial values.

Perceptron type can be implemented like the following.
```go
// Perceptron represents a simple linear classifier for numeric data
type Perceptron[T constraints.Float] struct {
	// weights are the adjustable coefficients for each input feature
	weights []T

	// bias is an extra adjustable value to shift the decision boundary
	bias T

	// features stores the training data (each inner slice is one data sample)
	features [][]T

	// labels stores the expected outputs (true classes) for the training data
	labels []T

	// mErr (mean error) tracks the average prediction error during training
	mErr T

	// trainingHistory keeps a record of weights, bias and error after each training step (optional, useful for analysis or visualization)
	trainingHistory [][]T
}
```

Now we can define `NewPerceptron` to create the Perceptron instance with initial weights equal to 1 and bias equal to 0.
```go
// NewPerceptron creates a new Perceptron instance with given features and labels.
// It initializes weights to 1 and bias to 0.
func NewPerceptron[T constraints.Float](features [][]T, labels []T) (*Perceptron[T], error) {
	// Check if there is at least one feature
	if len(features) < 1 {
		return nil, errors.New("cannot create perceptron: no features provided")
	}

	// Check if the number of labels matches the number of feature samples
	if len(features) != len(labels) {
		return nil, errors.New("cannot create perceptron: number of labels does not match number of feature samples")
	}

	// Initialize weights to 1 for each feature dimension
	var weights []T
	for range features[0] {
		weights = append(weights, T(1))
	}

	// Initialize bias to 0
	bias := T(0)

	// Return the initialized Perceptron
	return &Perceptron[T]{
		weights:  weights,
		bias:     bias,
		features: features,
		labels:   labels,
	}, nil
}

```

### Training function

The `Train` function represents the idea described above in the training process section. Additionally, it accepts the parameter `withHistory`, which defines whether we would like to store model parameters for each epoch during the training.
```go
// Train trains the Perceptron using the given learning rate and number of epochs.
// If withHistory is true, it saves weights, bias, and mean error after each update for later analysis.
func (p *Perceptron[T]) Train(learningRate T, epoch int, withHistory bool) ([]T, T, T, error) {
	var err error

	// Repeat the training process for the specified number of epochs
	for range epoch {
		// Calculate the mean error over the current dataset
		p.mErr, err = p.meanError()
		if err != nil {
			return nil, 0, 0, fmt.Errorf("failed to calculate mean error: %w", err)
		}

		// Pick a random training sample (feature and label)
		i := rand.IntN(len(p.features))
		randomFeature := p.features[i]
		featureLabel := p.labels[i]

		// Update the weights and bias based on the selected sample
		err = p.updateWeights(randomFeature, featureLabel, learningRate)
		if err != nil {
			return nil, 0, 0, fmt.Errorf("failed to update weights: %w", err)
		}

		// Optionally save the training history (weights, bias, error) after each update
		if withHistory {
			historyRecord := make([]T, len(p.weights)+2)
			copy(historyRecord, p.weights)
			historyRecord[len(p.weights)] = p.bias
			historyRecord[len(p.weights)+1] = p.mErr

			p.trainingHistory = append(p.trainingHistory, historyRecord)
		}
	}

	// Return final weights, bias, and mean error after training
	return p.weights, p.bias, p.mErr, nil
}

```


#### Error functions

Let's see how we can calculate the mean error function. In our case, we are iterating over the entire training set and calculating the error for each entry using `errorFunc`.

```go
// meanError calculates the mean (average) error over all training samples.
// It uses the Perceptron's error function (errorFunc) for each feature-label pair.
func (p *Perceptron[T]) meanError() (T, error) {
	var res T

	// Loop over all training samples
	for i := range p.features {
		// Calculate the error for a single sample
		e, err := p.errorFunc(p.features[i], p.labels[i])
		if err != nil {
			return 0, fmt.Errorf("error evaluating error function at sample %d: %w", i, err)
		}
		// Accumulate the error
		res += e
	}

	// Return the mean error (total error divided by number of samples)
	return res / T(len(p.features)), nil
}
```

We will implement the `errorFunc` like that.

```go
// errorFunc calculates the error for a single feature-label pair.
// It returns 0 if the prediction is correct; otherwise, it returns the absolute value of the prediction score.
// This error is used for updating weights during training.
func (p *Perceptron[T]) errorFunc(feature []T, label T) (T, error) {
	// Predict the label and get the raw score for the given feature
	prediction, score, err := p.predict(feature)
	if err != nil {
		return 0, fmt.Errorf("error during prediction in errorFunc: %w", err)
	}

	// If prediction matches the true label, there is no error
	if prediction == label {
		return 0, nil
	}

	// If prediction is incorrect, return the absolute score as the error
	return p.abs(score), nil
}
```

Additionally, we need to implement the `abs` method.

```go
// abs returns the absolute value of the given number n.
// If n is positive or zero, it returns n directly.
// If n is negative, it returns -n.
func (p *Perceptron[T]) abs(n T) T {
	if n >= 0 {
		return n
	}
	return -n
}
```

#### Predictions

Let's write a function that can predict the class of the input and return its score. The sign of the score will define the class. Its absolute value is used for the error calculation.

Here is a visual representation of the score for the different points, given the weights equal to `[2, 3, -6]`.

![score.png](/assets/images/7/score.png){: .center-image}

```go
// predict calculates the prediction for a given feature vector.
// It first computes the raw score (linear combination of inputs and weights + bias).
// Then, it applies the step function to determine the final prediction (e.g., 0 or 1).
// Returns: prediction, score, and possible error.
func (p *Perceptron[T]) predict(feature []T) (T, T, error) {
	// Calculate the raw score (dot product + bias)
	s, err := p.score(feature)
	if err != nil {
		return 0, 0, fmt.Errorf("failed to calculate score in predict: %w", err)
	}

	// Apply step function to turn score into a discrete prediction
	prediction := p.stepFunc(s)

	return prediction, s, nil
}

```

This is the implementation of the `score` function.

```go
// score calculates the raw score (weighted sum + bias) for a given feature vector.
// It computes the dot product of weights and features, then adds the bias.
// Returns: the score and any potential error during dot product calculation.
func (p *Perceptron[T]) score(features []T) (T, error) {
	// Compute the dot product between weights and features
	res, err := p.dot(p.weights, features)
	if err != nil {
		return 0, fmt.Errorf("failed to calculate dot product in score: %w", err)
	}

	// Add the bias to the dot product result
	return res + p.bias, nil
}

```

The `dot` function can be implemented this way.

```go
// dot calculates the dot product of two vectors v1 and v2.
// The dot product is the sum of element-wise multiplications: (v1[0] * v2[0]) + (v1[1] * v2[1]) + ...
// Returns: the scalar result and any potential error if vector sizes do not match.
func (p *Perceptron[T]) dot(v1, v2 []T) (T, error) {
	// Ensure the vectors have the same length
	if len(v1) != len(v2) {
		return 0, fmt.Errorf("cannot calculate dot product: vectors must be of the same length (got %d and %d)", len(v1), len(v2))
	}

	var result T
	// Sum up the element-wise products
	for i := 0; i < len(v1); i++ {
		result += v1[i] * v2[i]
	}

	return result, nil
}

```

The last step here is the `stepFunc` implementation. Given a score, it returns the class to which this score corresponds.

```go
// stepFunc applies a step activation function to the given value.
// It returns 1 if the input value is greater than 0, and 0 otherwise.
// This is used to make a binary decision in the perceptron: class 1 or class 0.
func (p *Perceptron[T]) stepFunc(v T) T {
	// If the value is greater than 0, return 1 (indicating class 1)
	if v > 0 {
		return 1
	}

	// If the value is less than or equal to 0, return 0 (indicating class 0)
	return 0
}

```

### Updating the weights


The last part here is the `updateWeights` function.

```go
// updateWeights updates the perceptron's weights and bias based on the prediction error.
//
// It uses the perceptron learning rule:
//   weight = weight + learningRate * (label - prediction) * feature
//   bias   = bias + learningRate * (label - prediction)
//
// Parameters:
// - feature: the input feature vector
// - label: the true label (expected output)
// - learningRate: a value that controls how much the weights are adjusted
//
// Returns an error if prediction fails.
func (p *Perceptron[T]) updateWeights(feature []T, label T, learningRate T) error {
	// Predict the output for the given input features
	prediction, _, err := p.predict(feature)
	if err != nil {
		return fmt.Errorf("failed to predict: %w", err)
	}

	// Update each weight if needed based on the difference between label and prediction
	for i := range p.weights {
		p.weights[i] += (label - prediction) * feature[i] * learningRate
	}

	// Update the bias
	p.bias += (label - prediction) * learningRate

	return nil
}

```

## Result

Now, we have all the parts to run the algorithm.

```go
func main() {
	// Define the training features (input vectors)
	features := [][]float64{
		// Class 0 (label 0)
		{1, 0}, {0, 2}, {1, 1}, {1, 2}, {0, 0},
		{0, 1}, {2, 0}, {2, 1}, {3, 0}, {0, 3},
		{1.5, 1.5}, {0.5, 1}, {1, 0.5}, {0.2, 1.8}, {1.2, 1.3},
		{2.5, 0.5}, {0.3, 2.3}, {1.1, 0.9}, {1.8, 0.2}, {0.7, 1.1},

		// Class 1 (label 1)
		{1, 3}, {2, 2}, {2, 3}, {3, 2}, {2, 4},
		{3, 3}, {4, 2}, {4, 3}, {3, 4}, {5, 3},
		{3.5, 2.5}, {2.5, 3.5}, {4.2, 2.8}, {3.1, 3.9}, {2.2, 4.1},
		{3.3, 2.7}, {4.4, 3.6}, {2.6, 3.2}, {3.9, 2.1}, {3.7, 3.3},
	}

	// Define the corresponding labels for each feature vector
	labels := []float64{
		// Class 0
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,
		0, 0, 0, 0, 0,

		// Class 1
		1, 1, 1, 1, 1,
		1, 1, 1, 1, 1,
		1, 1, 1, 1, 1,
		1, 1, 1, 1, 1,
	}

	// Initialize a new perceptron with the training data
	p, err := NewPerceptron[float64](features, labels)
	if err != nil {
		log.Fatalf("failed to create perceptron: %v", err)
	}

	// Train the perceptron
	// Parameters:
	// - learning rate: 0.01
	// - epochs: 210
	// - record history is set to true
	weights, bias, meanError, err := p.Train(0.01, 210, true)
	if err != nil {
		log.Fatalf("failed to train perceptron: %v", err)
	}

	// Output the final trained weights, bias, and mean error
	fmt.Printf("Final model:\n")
	fmt.Printf("Weights: %v\n", weights)
	fmt.Printf("Bias: %.4f\n", bias)
	fmt.Printf("Mean error: %.6f\n", meanError)
}

```

If we visualize the training history, we can see something like the image below.

![animated_lines_with_errors.gif](/assets/images/7/animated_lines_with_errors.gif)

This animation demonstrates how we improve our model step by step. The decision boundary is getting closer and closer to where it should be, and at the same time, the error value is decreasing.

We can also try it with a 3D space. Let's change the input to contain three-dimensional data.

```go
// Define the training features (input vectors) in 3D space
features := [][]float64{
  // Class 0 (label 0)
  {1, 0, 0}, {0, 2, 0}, {1, 1, 0}, {1, 2, 0}, {0, 0, 0},
  {0, 1, 1}, {2, 0, 0}, {2, 1, 1}, {3, 0, 1}, {0, 3, 0},
  {1.5, 1.5, 0.5}, {0.5, 1, 0.5}, {1, 0.5, 0.2}, {0.2, 1.8, 0.3}, {1.2, 1.3, 0.4},
  {2.5, 0.5, 0.2}, {0.3, 2.3, 0.1}, {1.1, 0.9, 0.3}, {1.8, 0.2, 0.2}, {0.7, 1.1, 0.4},

  // Class 1 {label 1}
  {1, 3, 2}, {2, 2, 2}, {2, 3, 2}, {3, 2, 2}, {2, 4, 3},
  {3, 3, 2}, {4, 2, 3}, {4, 3, 3}, {3, 4, 3}, {5, 3, 3},
  {3.5, 2.5, 2.5}, {2.5, 3.5, 2.5}, {4.2, 2.8, 2.7}, {3.1, 3.9, 3.0}, {2.2, 4.1, 2.8},
  {3.3, 2.7, 2.6}, {4.4, 3.6, 3.2}, {2.6, 3.2, 2.4}, {3.9, 2.1, 2.3}, {3.7, 3.3, 2.9},
}

// Define the corresponding labels for each feature vector
labels := []float64{
  // Class 0
  0, 0, 0, 0, 0,
  0, 0, 0, 0, 0,
  0, 0, 0, 0, 0,
  0, 0, 0, 0, 0,

  // Class 1
  1, 1, 1, 1, 1,
  1, 1, 1, 1, 1,
  1, 1, 1, 1, 1,
  1, 1, 1, 1, 1,
}
```

Here is the result for 3D space.

![animated_planes_with_errors.gif](/assets/images/7/animated_planes_with_errors.gif)

The complete code can be found on the GitHub repo: [https://github.com/andriikushch/perceptron/blob/main/pkg/perceptron.go](https://github.com/andriikushch/perceptron/blob/main/pkg/perceptron.go).
